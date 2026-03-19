# Personal Budget Tracker - Project Notes

## 📁 Project Location
```
E:\Personal Budget Tracker_1\personal_budget_tracker\
```

## 🚀 How to Run the Application

### Step 1: Navigate to the correct directory
```powershell
cd "E:\Personal Budget Tracker_1\personal_budget_tracker"
```

### Step 2: Activate the virtual environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Run the application
```powershell
python run.py
```

### Step 4: Access the application
Open your browser and go to: **http://127.0.0.1:5000**

## 🔧 Important Files and Their Purposes

### Core Application Files
- `run.py` - Main application entry point
- `app/__init__.py` - Flask app configuration and database setup
- `app/models.py` - Database models (User, Transaction)
- `app/routes.py` - Main application routes
- `app/auth.py` - Authentication routes (login, register, logout)
- `app/admin.py` - Admin panel routes
- `app/forms.py` - Form definitions

### Database Files
- `budget.db` - SQLite database (created in main directory)
- `init_db.py` - Database initialization script
- `make_admin.py` - Script to make a user an admin

### Template Files
- `app/templates/index.html` - Main dashboard
- `app/templates/login.html` - Login page
- `app/templates/register.html` - Registration page
- `app/templates/edit_transaction.html` - Edit transaction form
- `app/templates/admin/dashboard.html` - Admin dashboard
- `app/templates/admin/users.html` - User management
- `app/templates/admin/transactions.html` - All transactions view
- `app/templates/admin/user_detail.html` - Individual user details

## 🛠️ Admin Panel Setup

### Making Yourself an Admin
1. Register your first account at http://127.0.0.1:5000/register
2. Run the admin setup script:
   ```powershell
   python make_admin.py
   ```
3. You'll see: "✅ [YourUsername] is now an admin!"

### Accessing Admin Panel
1. Log in to your account
2. Click "🔧 Admin Panel" in the navigation (only visible to admins)
3. Available admin features:
   - Dashboard: Overview of all users and transactions
   - Users: Manage all users (make/remove admins, delete users)
   - All Transactions: View all transactions across all users
   - User Details: Individual user transaction views

## 🔒 Database Configuration

### Database Location
- **File:** `budget.db` (in main project directory)
- **Type:** SQLite database
- **Configuration:** Updated to use absolute path to avoid permission issues

### Database Schema
- **User Table:** username, email, password_hash, is_admin
- **Transaction Table:** user_id, type, category, amount, date, note

## 🐛 Common Issues and Solutions

### 1. Permission Denied Error
**Error:** `[Errno 13] Permission denied: 'venv\Scripts\python.exe'`
**Solution:** 
- Delete the problematic `venv` folder
- Recreate virtual environment: `python -m venv venv`
- Activate: `.\venv\Scripts\Activate.ps1`

### 2. Database Read-Only Error
**Error:** `sqlite3.OperationalError: attempt to write a readonly database`
**Solution:**
- Database moved to main directory (not instance folder)
- Updated `app/__init__.py` to use absolute path
- Run `python init_db.py` to recreate database

### 3. UnicodeDecodeError
**Error:** `'utf-8' codec can't decode byte 0xff in position 0`
**Solution:**
- Template files recreated with proper UTF-8 encoding
- Added `<meta charset="UTF-8">` to HTML templates

### 4. Wrong Directory Error
**Error:** `can't open file 'run.py': [Errno 2] No such file or directory`
**Solution:**
- Make sure you're in: `E:\Personal Budget Tracker_1\personal_budget_tracker`
- NOT in: `E:\Personal Budget Tracker_1`

## 📦 Dependencies

### Required Packages (installed in venv)
```
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.2
WTForms==3.2.1
email-validator==2.2.0
```

### Install Dependencies
```powershell
pip install -r requirements.txt
```

## 🎯 Key Features

### User Features
- ✅ User registration and login
- ✅ Add income and expenses
- ✅ Edit and delete transactions
- ✅ Filter transactions by month
- ✅ Export transactions to CSV
- ✅ View personal budget summary

### Admin Features
- ✅ View all users and transactions
- ✅ Make/remove admin privileges
- ✅ Delete user accounts
- ✅ View detailed statistics
- ✅ Access user transaction details

## 🔐 Security Features
- Password hashing with Werkzeug
- User session management
- Data isolation between users
- CSRF protection
- Admin-only access to admin panel

## 📱 Application URLs

### Main Application
- **Home:** http://127.0.0.1:5000/
- **Login:** http://127.0.0.1:5000/login
- **Register:** http://127.0.0.1:5000/register

### Admin Panel
- **Dashboard:** http://127.0.0.1:5000/admin/dashboard
- **Users:** http://127.0.0.1:5000/admin/users
- **All Transactions:** http://127.0.0.1:5000/admin/transactions
- **User Detail:** http://127.0.0.1:5000/admin/user/{user_id}

## 💾 Backup and Restore

### Backup Database
```powershell
Copy-Item budget.db "backup_budget_$(Get-Date -Format 'yyyy-MM-dd').db"
```

### Restore Database
```powershell
Copy-Item "backup_budget_2024-01-01.db" budget.db
```

## 🔄 Development Commands

### Reset Database
```powershell
python init_db.py
```

### Make User Admin
```powershell
python make_admin.py
```

### Check Dependencies
```powershell
pip list
```

## 📝 Notes for Future Development

### Potential Enhancements
- Transaction categories management
- Budget goals and alerts
- Data visualization (charts/graphs)
- Multi-currency support
- Mobile app integration
- Email notifications
- Data import/export features

### File Structure
```
personal_budget_tracker/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── auth.py
│   ├── admin.py
│   ├── models.py
│   ├── forms.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── edit_transaction.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       ├── users.html
│   │       ├── transactions.html
│   │       └── user_detail.html
│   └── static/
├── venv/
├── budget.db
├── run.py
├── init_db.py
├── make_admin.py
├── requirements.txt
└── README.md
```

## 🆘 Emergency Recovery

### If Everything Breaks
1. Delete `budget.db`
2. Run `python init_db.py`
3. Register a new account
4. Run `python make_admin.py`
5. Start fresh with `python run.py`

### Contact Information
- **Project:** Personal Budget Tracker
- **Version:** 1.0
- **Last Updated:** [Current Date]
- **Status:** Fully Functional

---
**Remember:** Always activate the virtual environment before running the application!
**Command:** `.\venv\Scripts\Activate.ps1` 