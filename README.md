# Flask React Assessment - VarshithGaddam

This repository contains the completed assessment with both Task 1 (Comment CRUD APIs) and Task 2 (Frontend Task Management Interface).

## 🎯 Assessment Tasks Completed

### ✅ Task 1: Comment CRUD APIs
- **Complete comment management system** for tasks
- **5 REST API endpoints** with full CRUD operations
- **Comprehensive test suite** (18 service tests + 30+ API tests)
- **Authentication & authorization** with JWT middleware
- **Error handling & validation** with proper HTTP status codes
- **MongoDB integration** with proper indexing and soft deletion

### ✅ Task 2: Frontend Task Management Interface
- **Complete React-based UI** for task management
- **Responsive design** with mobile-first approach
- **Full CRUD operations** using existing task APIs
- **Custom hooks** for state management (useTasks)
- **Modal forms** for create/edit operations
- **Toast notifications** for user feedback
- **Pagination support** for large task lists

## 🚀 Quick Start

### Prerequisites
- **Node.js**: 22.x (you have v22.21.0 ✅)
- **Python**: 3.11+
- **MongoDB**: 8.x (running locally or connection string)
- **pipenv**: For Python dependency management

### Installation & Setup

```bash
# 1. Navigate to project directory
cd flask-react-assessment-VarshithGaddam-main

# 2. Install JavaScript dependencies (ignore engine warnings)
npm install --legacy-peer-deps

# 3. Install Python dependencies
pip install pipenv
pipenv install --dev

# 4. Set up environment variables (create .env file)
echo "MONGODB_URI=mongodb://localhost:27017/flask_react_dev" > .env

# 5. Start MongoDB (if running locally)
# Windows: net start MongoDB
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod
```

### Running the Application

```bash
# Option 1: Start full stack (recommended)
npm run serve

# Option 2: Start without Temporal (simpler)
npm run serve -- --no-temporal

# Option 3: Start backend only
pipenv run python src/apps/backend/server.py
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080

## 🧪 Running Tests

### Task 1 - Comment API Tests
```bash
# Run all comment tests
pipenv run python -m pytest tests/modules/comment/ -v

# Run specific test files
pipenv run python -m pytest tests/modules/comment/test_comment_service.py -v
pipenv run python -m pytest tests/modules/comment/test_comment_api.py -v

# Run with coverage
pipenv run python -m pytest tests/modules/comment/ --cov=src/apps/backend/modules/comment -v
```

### Task 2 - Frontend (Manual Testing)
1. Navigate to http://localhost:3000
2. Login with test credentials
3. Click "Tasks" in the sidebar
4. Test CRUD operations:
   - Create new tasks
   - Edit existing tasks
   - Delete tasks with confirmation
   - Navigate through pages

## 📁 Project Structure

```
flask-react-assessment-VarshithGaddam-main/
├── src/apps/backend/
│   ├── modules/comment/          # Task 1: Comment CRUD APIs
│   │   ├── rest_api/            # REST endpoints
│   │   ├── internal/            # Business logic & data access
│   │   ├── types.py             # Type definitions
│   │   ├── errors.py            # Custom exceptions
│   │   └── comment_service.py   # Service layer
│   └── server.py                # Flask application (updated)
├── src/apps/frontend/
│   ├── components/task/         # Task 2: React components
│   │   ├── task-list/          # Task list display
│   │   ├── task-form/          # Create/edit forms
│   │   ├── task-modal/         # Modal dialogs
│   │   └── pagination/         # Pagination controls
│   ├── hooks/use-tasks.hook.ts  # Custom React hook
│   ├── pages/tasks/            # Tasks page
│   ├── services/task.service.ts # API integration
│   └── types/task.ts           # TypeScript definitions
└── tests/modules/comment/       # Comprehensive test suite
    ├── test_comment_service.py  # Service layer tests
    ├── test_comment_api.py      # API integration tests
    └── base_test_comment.py     # Test utilities
```

## 🔧 API Endpoints (Task 1)

### Comment CRUD Operations
```
POST   /api/accounts/{account_id}/tasks/{task_id}/comments
GET    /api/accounts/{account_id}/tasks/{task_id}/comments
GET    /api/accounts/{account_id}/tasks/{task_id}/comments/{comment_id}
PATCH  /api/accounts/{account_id}/tasks/{task_id}/comments/{comment_id}
DELETE /api/accounts/{account_id}/tasks/{task_id}/comments/{comment_id}
```

### Task Operations (Existing - Used by Task 2)
```
POST   /api/accounts/{account_id}/tasks
GET    /api/accounts/{account_id}/tasks
GET    /api/accounts/{account_id}/tasks/{task_id}
PATCH  /api/accounts/{account_id}/tasks/{task_id}
DELETE /api/accounts/{account_id}/tasks/{task_id}
```

## 🎨 Frontend Features (Task 2)

### Task Management Interface
- **Responsive grid layout** for task display
- **Create tasks** with modal form and validation
- **Edit tasks** with pre-populated forms
- **Delete tasks** with confirmation dialog
- **Pagination** for large task lists
- **Loading states** and error handling
- **Toast notifications** for user feedback
- **Mobile-optimized** touch interactions

### Navigation
- **Sidebar integration** with existing menu
- **Active page indicators**
- **Keyboard accessibility**

## 🔒 Security Features

- **JWT Authentication** on all API endpoints
- **Account-level data isolation**
- **Input validation** and sanitization
- **CORS protection**
- **Soft deletion** (data marked inactive, not physically deleted)

## 🚨 Troubleshooting

### Engine Version Warnings
```bash
# If you see engine warnings, use:
npm install --legacy-peer-deps
# or
npm install --force
```

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
mongo --eval "db.adminCommand('ismaster')"

# Update connection string in .env file
MONGODB_URI=mongodb://localhost:27017/flask_react_dev
```

### Python Dependencies
```bash
# If pipenv issues, try:
pip install --upgrade pipenv
pipenv install --dev --skip-lock
```

### Port Conflicts
```bash
# If ports are in use, kill processes:
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:3000 | xargs kill -9
```

## 📊 Test Coverage

### Task 1 - Comment APIs
- **18 Service Tests**: Complete business logic coverage
- **30+ API Tests**: All endpoints with various scenarios
- **Edge Cases**: Authentication, validation, cross-account access
- **Error Handling**: Proper HTTP status codes and messages

### Task 2 - Frontend
- **Manual Testing**: Complete user workflow testing
- **Responsive Design**: Mobile and desktop compatibility
- **Error States**: Network failures and API errors
- **User Experience**: Loading states and feedback

## 🎬 Video Walkthrough

The video walkthrough demonstrates:
1. **Code architecture** and design decisions
2. **Live application demo** with all features
3. **Test execution** showing comprehensive coverage
4. **Technical trade-offs** and implementation choices

## 📝 Implementation Highlights

### Task 1 - Technical Decisions
- **Modular architecture** following existing patterns
- **Service layer separation** for business logic
- **Repository pattern** for data access
- **Comprehensive error handling** with custom exceptions
- **Soft deletion** for data integrity

### Task 2 - Technical Decisions
- **Custom hooks** for state management
- **Component composition** for reusability
- **TypeScript** for type safety
- **Responsive design** with Tailwind CSS
- **Optimistic updates** for better UX

## 🏆 Assessment Completion

Both tasks have been successfully implemented with:
- ✅ **Complete functionality** as per requirements
- ✅ **Professional code quality** following best practices
- ✅ **Comprehensive testing** (Task 1)
- ✅ **Great user experience** (Task 2)
- ✅ **Proper documentation** and README
- ✅ **Video walkthrough** explaining implementation

---

**Developed by VarshithGaddam** | **Assessment for Better Software**