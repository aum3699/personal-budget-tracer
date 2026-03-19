# app/forms.py - WTForms definitions
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, DateField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from datetime import datetime

class TransactionForm(FlaskForm):
    type = SelectField('Type', choices=[('Income', 'Income'), ('Expense', 'Expense')])
    category = StringField('Category', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    note = StringField('Note')
    submit = SubmitField('Add Transaction')

class MonthFilterForm(FlaskForm):
    month = SelectField('Month', choices=[
        ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
        ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
        ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], default=datetime.now().strftime('%m'))
    year = SelectField('Year', choices=[
        (str(year), str(year)) for year in range(datetime.now().year - 5, datetime.now().year + 1)
    ], default=str(datetime.now().year))
    submit = SubmitField('Filter')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register') 