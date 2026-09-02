# Deployment Guide - DS Journey

Complete guide to deploy DS Journey to production environments.

## 🌍 Deployment Options

### Option 1: Cloud Platforms (Easiest)

#### A. Heroku (Simplified, Paid)
1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   heroku login
   ```

2. **Create Procfile in root directory**
   ```bash
   # backend/Procfile
   web: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

3. **Create requirements.txt**
   ```bash
   pip freeze > requirements.txt
   ```

4. **Deploy Backend**
   ```bash
   cd backend
   heroku create your-app-name-backend
   heroku addons:create heroku-postgresql:hobby-dev
   git push heroku main
   ```

5. **Deploy Frontend to Netlify**
   ```bash
   cd frontend
   npm run build
   # Drag dist/ folder to Netlify
   # Set environment variable: VITE_API_URL=https://your-backend.herokuapp.com/api
   ```

#### B. Vercel (Recommended for Frontend)
1. **Push code to GitHub**
2. **Connect GitHub to Vercel**
3. **Deploy frontend**
   ```bash
   cd frontend
   npm run build
   ```
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

#### C. Railway (Easy, Affordable)
1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Deploy Backend**
   ```bash
   cd backend
   railway init
   railway up
   ```

3. **Add Environment Variables**
   ```bash
   railway variables set DATABASE_URL=postgresql://...
   railway variables set SECRET_KEY=your-key
   ```

#### D. Render (Free tier available)
1. **Connect GitHub repository**
2. **Create Web Service**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker`
3. **Add Environment Variables**
   - DATABASE_URL
   - SECRET_KEY

---

### Option 2: Self-Hosted (AWS, DigitalOcean, etc.)

#### A. DigitalOcean Droplet (Cost: $5-12/month)

**1. Create Ubuntu Droplet**
- Size: 2GB RAM minimum
- Region: Closest to users
- Auth: SSH keys

**2. SSH into Droplet**
```bash
ssh root@your_server_ip
```

**3. Install Dependencies**
```bash
apt update && apt upgrade -y
apt install -y python3-pip python3-venv node npm postgresql
```

**4. Setup Database (PostgreSQL)**
```bash
sudo -u postgres psql
CREATE DATABASE ds_journey;
CREATE USER ds_user WITH PASSWORD 'secure_password';
ALTER ROLE ds_user SET client_encoding TO 'utf8';
ALTER ROLE ds_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ds_user SET default_transaction_deferrable TO on;
ALTER ROLE ds_user SET default_transaction_read_committed TO on;
GRANT ALL PRIVILEGES ON DATABASE ds_journey TO ds_user;
\q
```

**5. Setup Backend**
```bash
git clone your-repo
cd ds-journey/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env
cat > .env << EOF
DATABASE_URL=postgresql://ds_user:secure_password@localhost/ds_journey
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
EOF

# Run migrations (if using Alembic - add later)
# alembic upgrade head
```

**6. Create Systemd Service for Backend**
```bash
sudo cat > /etc/systemd/system/ds-journey-backend.service << EOF
[Unit]
Description=DS Journey Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/ds-journey/backend
Environment="PATH=/var/www/ds-journey/backend/venv/bin"
ExecStart=/var/www/ds-journey/backend/venv/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind unix:/var/run/ds-journey.sock

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start ds-journey-backend
sudo systemctl enable ds-journey-backend
```

**7. Setup Frontend**
```bash
cd /var/www/ds-journey/frontend
npm install
npm run build

# Output is in dist/ directory
```

**8. Setup Nginx Reverse Proxy**
```bash
sudo cat > /etc/nginx/sites-available/ds-journey << 'EOF'
upstream ds_journey_backend {
    server unix:/var/run/ds-journey.sock;
}

server {
    listen 80;
    server_name your_domain.com;

    # Frontend
    location / {
        root /var/www/ds-journey/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://ds_journey_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/ds-journey /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**9. Setup SSL with Let's Encrypt**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

**10. Setup Auto-renewal**
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

#### B. AWS EC2

**1. Launch EC2 Instance**
- AMI: Ubuntu 22.04 LTS
- Instance Type: t3.medium or larger
- Security Group: Allow ports 22, 80, 443

**2. Connect via SSH**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

**3. Follow same steps as DigitalOcean above**

---

#### C. Docker Deployment (Any Cloud)

**1. Create Dockerfile for Backend**
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

**2. Create Dockerfile for Frontend**
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**3. Create docker-compose.yml**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ds_journey
      POSTGRES_USER: ds_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://ds_user:${DB_PASSWORD}@db:5432/ds_journey
      SECRET_KEY: ${SECRET_KEY}
      DEBUG: "False"
    depends_on:
      - db
    command: sh -c "python seed.py && gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      VITE_API_URL: http://localhost/api
    depends_on:
      - backend

volumes:
  postgres_data:
```

**4. Deploy with Docker**
```bash
# Set environment variables
export DB_PASSWORD=secure_password
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

---

### Option 3: Serverless (AWS Lambda, Google Cloud Functions)

**Not recommended for this application** due to:
- Always-on requirement for study tracking
- Database connections overhead
- Better suited for traditional servers or containers

---

## 📋 Pre-Deployment Checklist

### Backend
- [ ] Change `SECRET_KEY` to a long random string
  ```bash
  python -c 'import secrets; print(secrets.token_urlsafe(32))'
  ```
- [ ] Set `DEBUG=False` in .env
- [ ] Use PostgreSQL (not SQLite) for production
- [ ] Configure proper CORS origins
- [ ] Setup database backups
- [ ] Configure logging to files/external service
- [ ] Add error monitoring (Sentry)
- [ ] Setup health check endpoint

### Frontend
- [ ] Run `npm run build` and test dist/
- [ ] Verify `VITE_API_URL` points to production backend
- [ ] Enable gzip compression
- [ ] Setup CDN for static assets
- [ ] Add Google Analytics (optional)
- [ ] Configure error tracking
- [ ] Add robots.txt and sitemap.xml

### Infrastructure
- [ ] Setup monitoring (Uptime Robot, Datadog)
- [ ] Configure SSL/TLS certificates
- [ ] Setup automated backups
- [ ] Configure email notifications
- [ ] Document rollback procedures
- [ ] Setup CI/CD pipeline
- [ ] Configure security headers

---

## 🔒 Security Hardening

### Backend Security
```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Only production domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "www.yourdomain.com"]
)
```

### Frontend Security
- Implement Content Security Policy (CSP)
- Use HTTPS only
- Implement rate limiting on login
- Add CSRF protection if needed
- Sanitize user inputs

### Database Security
- Use strong passwords
- Restrict database access to backend only
- Enable SSL for database connections
- Regular backups to secure storage
- Implement row-level security if needed

---

## 📊 Performance Optimization

### Backend
```python
# Add caching
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

# Add rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

### Frontend
- Enable gzip compression in web server
- Minify CSS/JavaScript (Vite does this)
- Lazy load page components
- Implement image optimization
- Add service worker for offline support

### Database
- Add indexes on frequently queried columns
- Implement query caching
- Archive old study sessions
- Monitor slow queries

---

## 🚨 Monitoring & Logging

### Backend Monitoring
```python
# Add logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add Sentry for error tracking
import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

### Frontend Monitoring
```javascript
// Add error tracking
import * as Sentry from "@sentry/react";
Sentry.init({
  dsn: "your-sentry-dsn",
  environment: "production"
});
```

### Server Monitoring
- CPU & Memory usage
- Disk space
- Network bandwidth
- Application error rates
- Response times
- Database connections

---

## 🔄 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy DS Journey

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test Backend
        run: |
          cd backend
          pip install -r requirements.txt pytest
          pytest
      - name: Test Frontend
        run: |
          cd frontend
          npm install
          npm run test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Production
        run: |
          # Your deployment commands here
          echo "Deploying to production..."
```

---

## 📝 Environment Variables for Production

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host:5432/db_name
SECRET_KEY=your-long-random-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]
ALLOWED_HOSTS=["yourdomain.com", "www.yourdomain.com"]
LOG_LEVEL=INFO
SENTRY_DSN=your-sentry-dsn
```

### Frontend (.env)
```
VITE_API_URL=https://yourdomain.com/api
VITE_APP_NAME=DS Journey
```

---

## 🚀 Deployment Commands Quick Reference

### Heroku
```bash
git push heroku main
heroku logs --tail
heroku restart
```

### Railway
```bash
railway up
railway logs
```

### Docker
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Manual SSH
```bash
ssh user@server
cd /var/www/ds-journey
git pull origin main
source backend/venv/bin/activate
pip install -r requirements.txt
systemctl restart ds-journey-backend
```

---

## 🆘 Troubleshooting Deployment

### Backend Issues
- Check logs: `docker-compose logs backend`
- Verify database connection: Test with psql
- Check environment variables: `echo $DATABASE_URL`
- Verify API endpoints: `curl http://localhost:8000/docs`

### Frontend Issues
- Check build output: `npm run build`
- Verify dist/ folder exists and has files
- Check API URL configuration
- Clear browser cache: Ctrl+Shift+Delete

### Database Issues
- Check connection string format
- Verify user permissions: `psql -U user -d db_name`
- Check disk space: `df -h`
- Monitor connections: `SELECT count(*) FROM pg_stat_activity;`

---

## 📚 Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [React Deployment](https://create-react-app.dev/deployment/)
- [PostgreSQL Backups](https://www.postgresql.org/docs/current/backup.html)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

**Ready to take your app to production!** 🚀
