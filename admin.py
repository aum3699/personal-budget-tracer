# app/admin.py - Admin panel routes
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from .models import User, Transaction
from . import db
from datetime import datetime
import sqlalchemy as sa

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to check if user is admin"""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics
    total_users = User.query.count()
    total_transactions = Transaction.query.count()
    total_income = db.session.query(sa.func.sum(Transaction.amount)).filter(Transaction.type == 'Income').scalar() or 0
    total_expense = db.session.query(sa.func.sum(Transaction.amount)).filter(Transaction.type == 'Expense').scalar() or 0
    
    # Get recent transactions
    recent_transactions = Transaction.query.order_by(Transaction.date.desc()).limit(10).all()
    
    # Get users with transaction counts
    users = User.query.all()
    user_stats = []
    for user in users:
        user_transactions = Transaction.query.filter_by(user_id=user.id).count()
        user_income = db.session.query(sa.func.sum(Transaction.amount)).filter(
            Transaction.user_id == user.id, Transaction.type == 'Income'
        ).scalar() or 0
        user_expense = db.session.query(sa.func.sum(Transaction.amount)).filter(
            Transaction.user_id == user.id, Transaction.type == 'Expense'
        ).scalar() or 0
        user_stats.append({
            'user': user,
            'transaction_count': user_transactions,
            'total_income': user_income,
            'total_expense': user_expense,
            'balance': user_income - user_expense
        })
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_transactions=total_transactions,
                         total_income=total_income,
                         total_expense=total_expense,
                         recent_transactions=recent_transactions,
                         user_stats=user_stats,
                         currency_symbol=current_app.config['CURRENCY_SYMBOL'])

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/transactions')
@login_required
@admin_required
def transactions():
    page = request.args.get('page', 1, type=int)
    transactions = Transaction.query.order_by(Transaction.date.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    # Calculate totals for all transactions
    total_income = db.session.query(sa.func.sum(Transaction.amount)).filter(Transaction.type == 'Income').scalar() or 0
    total_expense = db.session.query(sa.func.sum(Transaction.amount)).filter(Transaction.type == 'Expense').scalar() or 0
    
    return render_template('admin/transactions.html', 
                         transactions=transactions,
                         total_income=total_income,
                         total_expense=total_expense,
                         currency_symbol=current_app.config['CURRENCY_SYMBOL'])

@admin.route('/user/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).all()
    total_income = sum(t.amount for t in transactions if t.type == 'Income')
    total_expense = sum(t.amount for t in transactions if t.type == 'Expense')
    balance = total_income - total_expense
    
    return render_template('admin/user_detail.html', 
                         user=user,
                         transactions=transactions,
                         total_income=total_income,
                         total_expense=total_expense,
                         balance=balance,
                         currency_symbol=current_app.config['CURRENCY_SYMBOL'])

@admin.route('/make_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def make_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash(f'{user.username} is now an admin!', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/remove_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def remove_admin(user_id):
    if user_id == current_user.id:
        flash('You cannot remove admin privileges from yourself!', 'danger')
        return redirect(url_for('admin.users'))
    
    user = User.query.get_or_404(user_id)
    user.is_admin = False
    db.session.commit()
    flash(f'{user.username} is no longer an admin.', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin.users'))
    
    user = User.query.get_or_404(user_id)
    # Delete all user's transactions first
    Transaction.query.filter_by(user_id=user_id).delete()
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} and all their transactions have been deleted.', 'success')
    return redirect(url_for('admin.users')) 