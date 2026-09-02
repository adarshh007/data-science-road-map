# DS Journey - Project Structure & File Guide

## 📁 Complete Directory Structure

```
ds-journey/
├── README.md                          # Main project documentation
├── QUICK_START.md                     # 5-minute quick start guide
├── SETUP.md                           # Detailed setup instructions
├── COMPLETION_CHECKLIST.md            # Phase 1 completion summary
├── PROJECT_STRUCTURE.md               # This file
│
├── backend/                           # FastAPI backend application
│   ├── main.py                        # Application entry point
│   ├── requirements.txt               # Python dependencies
│   ├── .env                           # Environment variables
│   ├── seed.py                        # Database initialization & seeding
│   │
│   └── app/                           # Application package
│       ├── __init__.py               # Package marker
│       ├── database.py               # SQLAlchemy database setup
│       ├── models.py                 # ORM models (15 models)
│       ├── schemas.py                # Pydantic validation schemas
│       │
│       ├── core/                     # Core utilities
│       │   ├── __init__.py
│       │   ├── config.py             # Environment configuration
│       │   └── security.py           # Password & JWT handling
│       │
│       └── api/                      # API routes (8 modules)
│           ├── __init__.py
│           ├── auth.py               # Authentication endpoints
│           ├── users.py              # User profile endpoints
│           ├── modules.py            # Module listing & progress
│           ├── topics.py             # Topic CRUD & progress
│           ├── study_sessions.py     # Study session tracking
│           ├── analytics.py          # Analytics & statistics
│           ├── recommendations.py    # Smart recommendations
│           └── revisions.py          # Revision scheduling
│
└── frontend/                          # React + TypeScript frontend
    ├── package.json                   # Node.js dependencies
    ├── tsconfig.json                  # TypeScript configuration
    ├── tsconfig.node.json            # TypeScript for build tools
    ├── vite.config.ts                # Vite build configuration
    ├── tailwind.config.js            # Tailwind CSS configuration
    ├── postcss.config.js             # PostCSS configuration
    ├── index.html                    # HTML entry point
    │
    └── src/                          # Source code
        ├── main.tsx                  # React entry point
        ├── App.tsx                   # Main app component & router
        ├── App.css                   # Global app styles
        ├── index.css                 # Tailwind directives
        │
        ├── contexts/                 # React contexts
        │   └── AuthContext.tsx       # Authentication context
        │
        ├── services/                 # API service layer
        │   └── api.ts                # Axios client & endpoints
        │
        ├── store/                    # State management
        │   └── appStore.ts           # Zustand global store
        │
        ├── components/               # Reusable UI components
        │   ├── Navbar.tsx            # Top navigation bar
        │   ├── Sidebar.tsx           # Side navigation menu
        │   ├── ProgressCard.tsx      # Metric card component
        │   └── TopicCard.tsx         # Topic preview component
        │
        └── pages/                    # Page components (9 pages)
            ├── LoginPage.tsx         # Login page
            ├── RegisterPage.tsx      # User registration
            ├── DashboardPage.tsx     # Main dashboard
            ├── SyllabusPage.tsx      # Course curriculum
            ├── TopicDetailsPage.tsx  # Topic detail view
            ├── StudyLogPage.tsx      # Study session history
            ├── AnalyticsPage.tsx     # Analytics & charts
            ├── RevisionPage.tsx      # Revision manager
            └── SettingsPage.tsx      # User settings
```

---

## 📚 Backend Files Detailed

### Core Files

#### `main.py` (Entry Point)
```python
# Initializes FastAPI app
# Sets up CORS
# Includes all API routes
# Runs Uvicorn server
```
**Key Functions:**
- FastAPI app creation
- CORS middleware configuration
- Route inclusion
- Startup/shutdown events

#### `requirements.txt` (Dependencies)
```
fastapi==0.104.1
sqlalchemy==2.0.23
python-jose==3.3.0
passlib==1.7.4.1
bcrypt==4.1.1
python-dotenv==1.0.0
uvicorn==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
```

#### `seed.py` (Database Initialization)
**Purpose**: Creates database and seeds it with 150-day curriculum
**Data Structure**: 11 modules, 75 topics across 150 days
**Execution**: `python seed.py`
**Idempotency**: Safe to run multiple times (checks for existing data)

---

### Database & Configuration

#### `app/database.py`
**Contains:**
- SQLAlchemy engine configuration
- Session factory setup
- Database URL from environment

**Key Objects:**
```python
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

#### `app/models.py` (15 ORM Models)
**User & Auth:**
- `User` - User accounts, authentication, preferences

**Curriculum Structure:**
- `Module` - 11 learning modules
- `Day` - 150 days mapped to modules
- `Topic` - 75 learning topics
- `Subtopic` - Detailed topic breakdowns

**Progress Tracking:**
- `TopicProgress` - User progress per topic (status, confidence, progress%)
- `StudySession` - Individual study records
- `SessionNote` - Notes within sessions

**Learning Features:**
- `Revision` - Spaced repetition tracking
- `Note` - Topic notes
- `Resource` - Learning materials (videos, articles)
- `Project` - Project tracking

**Gamification:**
- `Achievement` - User achievements/badges

**Enums:**
- `StatusEnum` - (NOT_STARTED, LEARNING, PRACTICING, COMPLETED, MASTERED, NEEDS_REVISION)
- `ConfidenceEnum` - (NO_CONFIDENCE, LOW, MEDIUM, HIGH, VERY_HIGH, EXPERT)

---

#### `app/schemas.py` (Pydantic Models)
**Purpose:** Validate request/response data
**Contains:** 20+ schema classes matching ORM models
**Example:**
```python
class TopicUpdate(BaseModel):
    status: StatusEnum
    confidence: ConfidenceEnum
    progress: int  # 0-100
    notes: str
```

---

### Security & Configuration

#### `app/core/config.py`
**Settings:**
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT signing key
- `ALGORITHM` - JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration
- `CORS_ORIGINS` - Allowed origins
- `DEBUG` - Debug mode flag

#### `app/core/security.py`
**Functions:**
- `get_password_hash(password)` - Bcrypt hashing
- `verify_password(plain, hashed)` - Password verification
- `create_access_token(data, expires_delta)` - JWT creation
- `decode_token(token)` - JWT verification

---

### API Routes (8 modules)

#### `app/api/auth.py` - Authentication
**Endpoints:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login (returns JWT token)
- `POST /api/auth/token` - OAuth2-compatible token endpoint

**Validation:**
- Email uniqueness check
- Username uniqueness check
- Password requirements (8+ chars recommended)

#### `app/api/users.py` - User Profile
**Endpoints:**
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update profile
- `GET /api/users/{user_id}` - Get public user info

**Dependencies:**
- `get_current_user()` - Extracts JWT token from Authorization header

#### `app/api/modules.py` - Modules
**Endpoints:**
- `GET /api/modules` - List all modules
- `GET /api/modules/{module_id}` - Get module details
- `GET /api/modules/{module_id}/progress` - Calculate module progress

#### `app/api/topics.py` - Topics (Largest Module)
**Endpoints:**
- `GET /api/topics` - List topics (filters: module_id, status)
- `GET /api/topics/{topic_id}` - Full topic with subtopics
- `PUT /api/topics/{topic_id}` - Update progress/status/confidence
- `POST /api/topics/{topic_id}/subtopics` - Create subtopic
- `GET /api/topics/{topic_id}/subtopics` - List subtopics
- `PUT /topics/subtopics/{subtopic_id}` - Update subtopic
- `GET /api/topics/{topic_id}/study-sessions` - Get topic sessions

**Smart Logic:**
- Auto-progresses status to COMPLETED when progress reaches 100%
- Validates confidence level changes

#### `app/api/study_sessions.py` - Study Sessions
**Endpoints:**
- `POST /api/study-sessions` - Create session
- `GET /api/study-sessions` - List (filters: topic_id, module_id, date_range)
- `PUT /api/study-sessions/{session_id}` - Update session
- `DELETE /api/study-sessions/{session_id}` - Remove session
- `GET /api/study-sessions/stats/today` - Today's stats
- `GET /api/study-sessions/stats/streak` - Streak calculation

**Automatic Calculations:**
- Duration: Calculated in minutes from start_time to end_time
- Confidence improvement: Tracked from before/after values

#### `app/api/analytics.py` - Analytics & Statistics
**Endpoints:**
- `GET /api/analytics/overview` - Aggregate statistics
- `GET /api/analytics/study-hours-over-time` - 30-day trend
- `GET /api/analytics/study-hours-by-module` - Module breakdown
- `GET /api/analytics/study-hours-by-topic` - Top N topics
- `GET /api/analytics/weekly-stats` - 12-week rolling summary

**Helper Functions:**
- `get_streak_data()` - Calculate current and longest streaks

#### `app/api/recommendations.py` - Smart Recommendations
**Endpoint:**
- `GET /api/recommendations` - Get topic recommendations (up to N topics)

**Scoring Algorithm:**
```
score = (status_weight * 0.4 + 
         importance_weight * 0.2 + 
         confidence_gap_weight * 0.2 + 
         progress_encouragement * 0.2)
```

**Factors:**
- Status (NEEDS_REVISION highest, COMPLETED lowest)
- Importance (1-5 scale)
- Confidence gaps (lower = higher priority)
- Partial progress (encourage continuation)

#### `app/api/revisions.py` - Revision Scheduling
**Endpoints:**
- `POST /api/revisions` - Create revision
- `GET /api/revisions/due` - Get due/overdue/completed revisions
- `PUT /api/revisions/{id}` - Mark completed
- `POST /api/revisions/{id}/snooze` - Postpone (1-30 days)
- `POST /api/revisions/schedule/{topic_id}` - Auto-schedule/update

---

## 🎨 Frontend Files Detailed

### Configuration Files

#### `vite.config.ts`
```typescript
// React plugin enabled
// Port: 5173
// Proxy: /api → localhost:8000/api
// Hot module replacement enabled
```

#### `tailwind.config.js`
```javascript
// Dark mode: class strategy
// Custom color variables (HSL-based)
// Typography, spacing, rounded presets
// Extended theme configuration
```

#### `tsconfig.json`
```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2020",
    "jsx": "react-jsx",
    "moduleResolution": "bundler"
  }
}
```

---

### Application Core

#### `App.tsx` (Main Router)
**Structure:**
- AuthProvider wraps entire app
- AppContent component handles routing logic
- Conditional routing based on authentication
- Protected routes redirect unauthenticated users
- Sidebar & Navbar only shown when authenticated

**Routes:**
```
Public:
  /login - LoginPage
  /register - RegisterPage

Protected:
  / - DashboardPage
  /syllabus - SyllabusPage
  /topics/:topicId - TopicDetailsPage
  /study-log - StudyLogPage
  /analytics - AnalyticsPage
  /revision - RevisionPage
  /settings - SettingsPage
```

#### `contexts/AuthContext.tsx`
**Functions:**
- `login(email, password)` - Authenticate user
- `register(email, username, password, fullName)` - Create account
- `logout()` - Clear session

**State:**
- `user` - Current user object
- `token` - JWT token
- `isAuthenticated` - Boolean flag
- `isLoading` - Loading state

**Persistence:**
- Stores token in localStorage
- Automatically retrieves on app load
- Injects token into all API requests

---

### Services & State

#### `services/api.ts` (API Client)
**Structure:**
```typescript
// Base axios instance with API_BASE_URL
// Request interceptor adds Bearer token
// Organized by resource:
  modulesApi.getAll()
  topicsApi.getById(id)
  studySessionsApi.create(data)
  analyticsApi.getOverview()
  revisionsApi.getDue(status)
  recommendationsApi.getAll()
  usersApi.updateProfile(data)
  authApi.login(credentials)
```

**Features:**
- Automatic token injection from localStorage
- Error handling with logging
- Query parameter support for filtering
- Resource-specific methods

#### `store/appStore.ts` (Zustand Store)
**State Sections:**
- `modules` - Array of modules
- `topics` - Array of all topics
- `studySessions` - User study sessions
- `currentTopic` - Currently viewed topic
- `sidebarOpen` - Sidebar visibility
- `theme` - Light/dark/system
- `isLoading` - Loading state
- `error` - Error messages

**Setters:** `setModules()`, `setTopics()`, `addTopic()`, `updateTopic()`, etc.

---

### Layout Components

#### `components/Navbar.tsx`
**Features:**
- User full name and email display
- Settings link
- Logout button
- Mobile menu toggle
- Responsive design

#### `components/Sidebar.tsx`
**Navigation Items:**
1. Dashboard (/)
2. Syllabus (/syllabus)
3. Study Log (/study-log)
4. Analytics (/analytics)
5. Revision (/revision)
6. Settings (/settings)

**Features:**
- Active route highlighting
- Responsive (collapses on mobile)
- Auto-closes on navigation
- Icon + label display

---

### UI Components

#### `components/ProgressCard.tsx`
```typescript
interface Props {
  title: string
  value: string | number
  unit?: string
  icon?: React.ReactNode
  subtext?: string
}
```
**Usage:** Display key metrics (hours, progress %, streaks)

#### `components/TopicCard.tsx`
```typescript
interface Props {
  topic: Topic
  onClick?: () => void
  showStudyTime?: boolean
}
```
**Features:**
- Status badge (color-coded)
- Progress bar
- Confidence stars (0-5)
- Study time (actual/estimated)
- Day range display

---

### Page Components

#### `pages/LoginPage.tsx`
- Email & password inputs
- Demo credentials reference
- Error messages
- Link to registration
- Form validation

#### `pages/RegisterPage.tsx`
- Full name, username, email, password fields
- Password confirmation validation
- Error handling
- Auto-focuses email field

#### `pages/DashboardPage.tsx`
**Sections:**
1. Welcome header with syllabus info
2. 4 metric cards (Progress, Hours, Streak, Modules)
3. 30-day study chart (Recharts)
4. Currently Learning card
5. Recommended Next section (top 3)
6. Module Progress grid

**API Calls:**
- `analyticsApi.getOverview()`
- `analyticsApi.getStudyHoursOverTime(30)`
- `recommendationsApi.getAll()`

#### `pages/SyllabusPage.tsx`
- Summary statistics
- Expandable modules
- Nested topic cards
- Module progress bars
- Topic filtering options

#### `pages/TopicDetailsPage.tsx`
**Sections:**
1. Header: Status, Progress %, Confidence, Study time
2. Learning Checklist (9 items)
3. Subtopics (collapsible)
4. Study Sessions (list)

**Interactions:**
- Update progress on checklist
- View subtopic details
- Access session history

#### `pages/StudyLogPage.tsx`
- Time filter tabs (All, Week, Month)
- Session cards with:
  - Date & duration
  - What learned
  - Confidence change
  - Difficulty level
- Loading & empty states

#### `pages/AnalyticsPage.tsx`
**Charts:**
1. Key metrics cards (Hours, Avg Duration, Streaks)
2. Line chart: Study hours over 30 days
3. Pie chart: Topic status distribution
4. Bar chart: Hours by module
5. Module progress cards

**Libraries:** Recharts for visualizations

#### `pages/RevisionPage.tsx`
**Sections:**
- Filter tabs (All, Pending, Overdue, Completed)
- Revision cards with:
  - Due dates
  - Status indicators
  - Notes/topics
- Actions: Mark Done, Snooze (7 days)

#### `pages/SettingsPage.tsx`
**Sections:**
1. Profile (email, full name)
2. Learning Goals (daily/weekly hours)
3. Appearance (Light/Dark/System)
4. Account (logout)
5. Save & About

---

## 🔄 Data Flow Diagram

```
User Action
    ↓
React Component
    ↓
API Service (api.ts)
    ↓
Axios HTTP Request
    ↓
FastAPI Endpoint
    ↓
SQLAlchemy ORM
    ↓
SQLite Database
    ↓
[Response]
    ↓
Zustand Store (appStore.ts)
    ↓
React Component Re-render
    ↓
UI Update
```

---

## 🔐 Authentication Flow

```
1. User enters credentials
2. LoginPage → authApi.login()
3. Backend: Verify password, create JWT
4. Response: { access_token, token_type, user }
5. Frontend: Store token in localStorage
6. AuthContext: Set user & token in state
7. App: Redirect to Dashboard
8. All subsequent requests: Add Authorization header
9. Backend: Verify JWT on protected endpoints
```

---

## 📊 Database Schema Relationships

```
User (1) ──────── (many) TopicProgress
  │                           │
  │                       Topic
  │                           │
  ├──────────── (many) StudySession
  │                      │
  ├──────────── (many) Revision
  │
  └──────────── (many) Note

Module (1) ──────── (many) Topic
             ├──────── (many) Day
             
Topic (1) ──────---- (many) Subtopic
     │
     └──────────── (many) StudySession

StudySession (1) ─── (many) SessionNote
```

---

## 🚀 Deployment Considerations

### Backend (Production)
```bash
# Use Gunicorn + Uvicorn
pip install gunicorn
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

# Environment variables
export DATABASE_URL=postgresql://user:pass@host/db
export SECRET_KEY=your-production-secret-key
```

### Frontend (Production)
```bash
npm run build
# Output: dist/
# Deploy dist/ to web server (Nginx, Vercel, etc.)

# Environment variables
VITE_API_URL=https://your-api.com/api
```

---

## 📝 Key Files Quick Reference

| Purpose | File | Key Function |
|---------|------|--------------|
| Start backend | `main.py` | FastAPI app |
| Initialize DB | `seed.py` | Database seeding |
| User auth | `auth.py` | Login/Register |
| App routing | `App.tsx` | Route definition |
| API calls | `api.ts` | HTTP requests |
| Global state | `appStore.ts` | Zustand store |
| Dashboard | `DashboardPage.tsx` | Main overview |
| Settings | `SettingsPage.tsx` | User preferences |

---

**This project is fully structured for easy navigation and maintenance!** 🎉
