# app/routes.py - Blueprint and route definitions
from flask import Blueprint, render_template, redirect, url_for, flash, send_file, request, current_app
from flask_login import login_required, current_user
from .models import Transaction
from .forms import TransactionForm, MonthFilterForm
from . import db
import csv
from io import StringIO
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = TransactionForm()
    filter_form = MonthFilterForm()
    
    # Handle transaction form submission
    if form.validate_on_submit():
        txn = Transaction(
            type=form.type.data,
            category=form.category.data,
            amount=form.amount.data,
            note=form.note.data,
            user_id=current_user.id
        )
        db.session.add(txn)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('main.index'))
    
    # Handle month filter
    month = request.args.get('month', datetime.now().strftime('%m'))
    year = request.args.get('year', str(datetime.now().year))
    
    # Filter transactions by month and year for current user
    start_date = datetime(int(year), int(month), 1)
    if int(month) == 12:
        end_date = datetime(int(year) + 1, 1, 1)
    else:
        end_date = datetime(int(year), int(month) + 1, 1)
    
    transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).order_by(Transaction.date.desc()).all()
    
    income = sum(t.amount for t in transactions if t.type == 'Income')
    expense = sum(t.amount for t in transactions if t.type == 'Expense')
    balance = income - expense

    return render_template('index.html', form=form, filter_form=filter_form, 
                         transactions=transactions, income=income, expense=expense, 
                         balance=balance, current_month=month, current_year=year,
                         currency_symbol=current_app.config['CURRENCY_SYMBOL'])

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    txn = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = TransactionForm(obj=txn)
    if form.validate_on_submit():
        txn.type = form.type.data
        txn.category = form.category.data
        txn.amount = form.amount.data
        txn.note = form.note.data
        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('edit_transaction.html', form=form, transaction_id=id)

@main.route('/delete/<int:id>')
@login_required
def delete_transaction(id):
    txn = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(txn)
    db.session.commit()
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('main.index'))

@main.route('/export/csv')
@login_required
def export_csv():
    # Create CSV data
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date', 'Type', 'Category', 'Amount', 'Note'])
    
    # Get month/year from query parameters
    month = request.args.get('month', datetime.now().strftime('%m'))
    year = request.args.get('year', str(datetime.now().year))
    
    # Filter transactions by month and year for current user
    start_date = datetime(int(year), int(month), 1)
    if int(month) == 12:
        end_date = datetime(int(year) + 1, 1, 1)
    else:
        end_date = datetime(int(year), int(month) + 1, 1)
    
    transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).order_by(Transaction.date.desc()).all()
    
    for txn in transactions:
        cw.writerow([
            txn.date.strftime('%Y-%m-%d'),
            txn.type,
            txn.category,
            txn.amount,
            txn.note
        ])
    
    output = si.getvalue()
    si.close()
    
    # Create response
    from flask import Response
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=budget_export_{year}_{month}.csv'}
    ) 