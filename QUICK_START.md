# 🚀 Quick Start Guide - Personal Budget Tracker

## ⚡ Fast Commands (Copy & Paste)

### 1. Start the Application
```powershell
cd "E:\Personal Budget Tracker_1\personal_budget_tracker"
.\venv\Scripts\Activate.ps1
python run.py
```

### 2. Access the App
Open browser: **http://127.0.0.1:5000**

### 3. Make Yourself Admin
```powershell
python make_admin.py
```

### 4. Reset Database (if needed)
```powershell
python init_db.py
```

## 🔑 Important Information

- **Project Location:** `E:\Personal Budget Tracker_1\personal_budget_tracker\`
- **Database:** `budget.db` (in main directory)
- **Admin Username:** RAM
- **Admin Email:** ram@gmail.com

## 🛠️ Admin Panel Access
1. Login with your account
2. Click "🔧 Admin Panel" in navigation
3. Available pages:
   - Dashboard
   - Users
   - All Transactions
   - User Details

## 🆘 If Something Breaks
1. Delete `budget.db`
2. Run `python init_db.py`
3. Register new account
4. Run `python make_admin.py`
5. Start with `python run.py`

---
**Save this file to your pendrive for quick reference!** 