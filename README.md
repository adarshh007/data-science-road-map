# DS Journey - 150-Day Data Science Learning Tracker

A modern, responsive web application to track your data science learning journey across 11 modules, 75 topics, and 150 days of structured learning.

## 🎯 Features

- **Complete Syllabus Tracking**: 150-day curriculum with 11 modules and 75 topics
- **Progress Monitoring**: Track topic progress, confidence levels, and study time
- **Study Session Logging**: Record detailed study sessions with learning outcomes
- **Smart Recommendations**: Get personalized topic recommendations based on prerequisites and confidence
- **Revision System**: Intelligent revision scheduling based on spaced repetition
- **Analytics Dashboard**: Visualize your learning patterns with charts and statistics
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark/Light Mode**: Comfortable viewing in any environment
- **User Authentication**: Secure JWT-based authentication

## 🏗️ Project Structure

```
ds-journey/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Configuration and security
│   │   ├── models.py    # Database models
│   │   ├── schemas.py   # Pydantic schemas
│   │   └── database.py  # Database configuration
│   ├── main.py          # Application entry point
│   ├── seed.py          # Database seeding script
│   ├── requirements.txt # Python dependencies
│   └── .env             # Environment variables
│
└── frontend/            # React + TypeScript frontend
    ├── src/
    │   ├── components/  # Reusable UI components
    │   ├── contexts/    # React contexts (Auth, etc.)
    │   ├── pages/       # Page components
    │   ├── services/    # API client services
    │   ├── store/       # Zustand state management
    │   ├── App.tsx      # Main app component
    │   └── main.tsx     # Entry point
    ├── package.json     # Node dependencies
    ├── vite.config.ts   # Vite configuration
    └── tailwind.config.js # Tailwind CSS config
```

## 📋 Syllabus Structure

### 11 Modules:
1. **M1: Foundations for Data Science** (Days 1-22)
   - Data acquisition, cleaning, statistics, probability

2. **M2: Python Programming** (Days 23-42)
   - Variables, loops, functions, Pandas, Matplotlib

3. **M3: Data Preparation & Statistical Testing** (Days 43-60)
   - Clustering, text mining, distributions, regression

4. **M4: Machine Learning** (Days 59-78)
   - Classification, clustering, ensemble methods, association rules

5. **M5: R Programming** (Days 79-94)
   - R basics, data structures, dplyr, ggplot2, ML

6. **M6: AI & Deep Learning** (Days 95-108)
   - Neural networks, CNN, RNN, LSTM, autoencoders

7. **M7: Generative AI** (Days 109-116)
   - LLMs, transformers, prompt engineering

8. **M8: Tableau** (Days 117-124)
   - Visualizations, dashboards, interactive reports

9. **M9: SQL & Databases** (Days 125-134)
   - DDL, DML, joins, subqueries, window functions

10. **M10: Excel** (Days 135-146)
    - Formulas, pivot tables, dashboards, power query

11. **M11: Capstone Project** (Days 147-150)
    - Project implementation, presentation

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file** (already provided, but verify settings)
```bash
cat .env
```

5. **Initialize database and seed data**
```bash
python seed.py
```

6. **Run the backend server**
```bash
python main.py
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory** (from project root)
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create .env file** (if needed)
```bash
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

4. **Run development server**
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Demo Credentials

After seeding the database, use these credentials to login:
- **Email**: demo@example.com
- **Password**: password123

(You can also create a new account via the registration page)

## 📚 Database Schema

### Key Tables:
- **users** - User accounts and settings
- **modules** - 11 learning modules
- **topics** - 75 learning topics (2 days each)
- **subtopics** - Detailed breakdowns of topics
- **study_sessions** - Individual study session records
- **topic_progress** - User progress on each topic
- **revisions** - Revision scheduling and tracking
- **notes** - User notes for topics
- **resources** - Learning resources (videos, articles, etc.)
- **projects** - Project tracking
- **achievements** - User achievements/badges

## 🔐 Authentication

- JWT token-based authentication
- Password hashing with bcrypt
- Secure token expiration (30 minutes access token)
- Refresh token support

## 🎨 UI/UX Features

- Modern, minimal design
- Responsive grid layouts
- Dark/light theme support
- Progress visualizations (bars, circles, charts)
- Smooth transitions and animations
- Accessible form inputs
- Toast notifications (ready to implement)
- Loading and error states

## 📊 Key Pages

- **Dashboard** - Overview of progress, current learning, recommendations
- **Syllabus** - Complete 150-day curriculum explorer
- **Topic Details** - In-depth topic tracking with checklist
- **Study Log** - All study sessions with filtering
- **Analytics** - Charts and statistics on learning patterns
- **Revision** - Upcoming and overdue revisions
- **Settings** - User preferences and goals

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/token` - Get access token

### Modules & Topics
- `GET /api/modules` - Get all modules
- `GET /api/modules/{id}` - Get module details
- `GET /api/topics` - Get all topics
- `GET /api/topics/{id}` - Get topic details
- `PUT /api/topics/{id}` - Update topic

### Study Sessions
- `POST /api/study-sessions` - Create study session
- `GET /api/study-sessions` - Get all sessions
- `GET /api/study-sessions/stats/today` - Today's stats
- `GET /api/study-sessions/stats/streak` - Streak info

### Analytics
- `GET /api/analytics/overview` - Overview statistics
- `GET /api/analytics/study-hours-over-time` - Chart data
- `GET /api/analytics/study-hours-by-module` - Module breakdown

### Recommendations
- `GET /api/recommendations` - Get topic recommendations

### Revisions
- `GET /api/revisions/due` - Get due revisions
- `POST /api/revisions` - Create revision
- `PUT /api/revisions/{id}` - Update revision

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database
- **SQLite** - Development database (PostgreSQL ready)
- **Pydantic** - Data validation
- **Python-Jose** - JWT handling
- **Passlib** - Password hashing

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS
- **Zustand** - State management
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **Lucide React** - Icons

## 📦 Build & Deployment

### Backend Build
```bash
cd backend
pip install -r requirements.txt
# For production, use uvicorn with gunicorn:
# gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Frontend Build
```bash
cd frontend
npm run build
# Output in dist/ directory
```

### Environment Variables

**Backend (.env)**
```
DATABASE_URL=sqlite:///./ds_journey.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False  # Set to False in production
```

**Frontend (.env)**
```
VITE_API_URL=http://your-api-url/api
```

## 🧪 Testing

Backend tests can be added using pytest:
```bash
pip install pytest pytest-asyncio
pytest
```

Frontend tests can be added using Vitest:
```bash
npm install vitest @testing-library/react
npm run test
```

## 📈 Future Enhancements

- [ ] Social features (leaderboards, sharing)
- [ ] Mobile app (React Native)
- [ ] Video integration
- [ ] AI-powered learning path suggestions
- [ ] Timed quizzes and assessments
- [ ] Collaboration features
- [ ] Email notifications
- [ ] Export to PDF
- [ ] Calendar integration
- [ ] Community forum

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Support

For issues or questions, please check the documentation or create an issue in the repository.

---

**Built with ❤️ for data science learners everywhere**
