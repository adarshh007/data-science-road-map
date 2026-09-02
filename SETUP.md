# Setup Guide - DS Journey

Complete step-by-step guide to get DS Journey running on your machine.

## ✅ Prerequisites Check

Verify you have the following installed:

```bash
# Python (3.8 or higher)
python --version

# Node.js and npm (16 or higher)
node --version
npm --version

# Git (optional but recommended)
git --version
```

If any are missing, install them:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- Git: https://git-scm.com/

## 🔧 Step 1: Backend Setup (Python)

### 1.1 Navigate to Backend Directory

```bash
cd backend
```

### 1.2 Create Python Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat
```

You should see `(venv)` in your terminal prompt.

### 1.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- SQLAlchemy (database ORM)
- python-jose (JWT handling)
- passlib (password hashing)
- python-multipart (form data)
- uvicorn (ASGI server)
- python-dotenv (environment variables)
- pydantic (data validation)

### 1.4 Verify .env File

The `.env` file should exist in the backend directory with:

```
DATABASE_URL=sqlite:///./ds_journey.db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

If it doesn't exist, create it:

```bash
echo "DATABASE_URL=sqlite:///./ds_journey.db" > .env
echo "SECRET_KEY=dev-key-change-in-production" >> .env
echo "ALGORITHM=HS256" >> .env
echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env
echo "DEBUG=True" >> .env
```

### 1.5 Initialize Database and Seed Data

This creates the SQLite database and populates it with the 150-day curriculum:

```bash
python seed.py
```

Expected output:
```
Database initialized successfully!
Created users table
Created modules table
Created topics table
...
Database seeding completed successfully!
```

If you see `Database already seeded with topics` - that's fine, it means the database was already initialized.

### 1.6 Start the Backend Server

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 1.7 Verify Backend is Running

Open in your browser:
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

You should see the interactive API documentation.

**Important**: Keep this terminal open. The backend must be running for the frontend to work.

---

## 📱 Step 2: Frontend Setup (Node.js/React)

### 2.1 Open New Terminal

Keep the backend terminal open and open a **new terminal window/tab**.

### 2.2 Navigate to Frontend Directory

```bash
cd frontend
```

### 2.3 Install Node Dependencies

```bash
npm install
```

This installs all React, TypeScript, and Tailwind CSS dependencies (~500MB).

### 2.4 Verify .env (if needed)

The frontend should have a proxy configured in `vite.config.ts` that points to `http://localhost:8000/api`.

### 2.5 Start Development Server

```bash
npm run dev
```

You should see:
```
  VITE v5.0.0  ready in 456 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### 2.6 Open in Browser

Navigate to: http://localhost:5173

You should see the **DS Journey Login Page**.

---

## 🔐 Step 3: Login & Test

### 3.1 Create Demo Account

1. Click "Don't have an account? Register here"
2. Fill in the form:
   - **Full Name**: Your Name
   - **Username**: yourname
   - **Email**: your@example.com
   - **Password**: AnyPassword123! (min 8 characters)
   - **Confirm Password**: AnyPassword123!
3. Click "Register"

### 3.2 Or Use Demo Account

If seeding created a demo account:
- **Email**: demo@example.com
- **Password**: password123

### 3.3 Login

1. Enter your email and password
2. Click "Login"
3. You should be redirected to the **Dashboard**

### 3.4 Verify Everything Works

On the Dashboard, you should see:
- ✅ Overall Progress (should be 0%)
- ✅ Study Hours (should be 0)
- ✅ Current Streak (should be 0)
- ✅ Module Count (should be 11)
- ✅ 30-day chart
- ✅ Recommended topics

---

## 🧭 Navigation Guide

Once logged in, you can access:

1. **Dashboard** (home icon)
   - Overview of your learning progress
   - Recommended topics to study next

2. **Syllabus** (book icon)
   - View all 150 days of curriculum
   - See all 11 modules and 75 topics
   - Expand modules to see topics

3. **Study Log** (clipboard icon)
   - Record study sessions
   - View all previous sessions
   - Filter by time period

4. **Analytics** (chart icon)
   - Visualize your learning patterns
   - Study hours trends
   - Progress by module

5. **Revision** (repeat icon)
   - View revision due dates
   - Snooze or mark revisions complete

6. **Settings** (gear icon)
   - Update profile
   - Set daily/weekly goals
   - Choose dark/light theme
   - Logout

---

## 🔧 Troubleshooting

### "Cannot connect to backend"

**Problem**: Frontend shows "Failed to load analytics"

**Solution**:
1. Verify backend terminal shows `Application startup complete`
2. Check http://localhost:8000/docs is accessible
3. Check that backend is on port 8000 (not 8001, 8002, etc.)
4. Restart backend: Press Ctrl+C, then run `python main.py` again

### "ModuleNotFoundError" when running seed.py

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Make sure virtual environment is activated (you should see (venv) in terminal)
pip install -r requirements.txt
# Then try again
python seed.py
```

### "Port already in use"

**Problem**: `Address already in use` for port 8000 or 5173

**Solution**:
```bash
# Find process using the port (macOS/Linux)
lsof -i :8000
# Kill the process
kill -9 <PID>

# On Windows, use PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

Then restart the server.

### "npm: command not found"

**Problem**: Node.js not installed

**Solution**: Install Node.js from https://nodejs.org/

### Database Errors

**Problem**: SQLite database locked or corrupt

**Solution**:
```bash
# Delete the database file
rm backend/ds_journey.db

# Reseed the database
cd backend
python seed.py
```

---

## 📝 Common Tasks

### Create Your First Study Session

1. Go to **Study Log**
2. Click "Add Session" (or similar button once implemented)
3. Enter:
   - Topic
   - Date
   - Duration
   - Notes about what you learned
4. Click "Save"

### Track Topic Progress

1. Go to **Syllabus**
2. Click on a topic to expand it
3. Mark it as: Learning → Practicing → Completed → Mastered
4. Update confidence level (stars)
5. Add notes

### View Your Progress

1. Go to **Analytics**
2. See charts showing:
   - Study hours over time
   - Progress by module
   - Topic status distribution

---

## 🚀 Next Steps

### To stop the servers:
- **Backend**: Press Ctrl+C in the backend terminal
- **Frontend**: Press Ctrl+C in the frontend terminal

### To restart:
- Backend: `python main.py`
- Frontend: `npm run dev`

### To build for production:

**Backend**:
```bash
# Backend is ready as-is, use Gunicorn for production
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

**Frontend**:
```bash
npm run build
# Output will be in dist/ folder
# Deploy dist/ to your web server
```

---

## 💡 Tips

1. **Keep both terminals open** during development
2. **Use browser DevTools** (F12) to debug frontend issues
3. **Check API responses** in Network tab for backend issues
4. **Read error messages carefully** - they usually tell you what's wrong
5. **Clear browser cache** if you see old data: Ctrl+Shift+Delete

---

## 📚 Learning Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **SQLAlchemy**: https://sqlalchemy.org/

---

**You're all set! 🎉 Happy learning!**
