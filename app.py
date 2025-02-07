from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Sample data to simulate a user and transaction list
users = {"user": "password"}  # A simple demo user for login
transactions = []

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    flash('Invalid username or password!', 'error')
    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    if username in users:
        flash('Username already exists!', 'error')
        return redirect(url_for('register'))
    users[username] = password
    flash('Account created successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', transactions=transactions)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if 'username' not in session:
        return redirect(url_for('index'))
    amount = float(request.form['amount'])
    category = request.form['category']
    date = request.form['date']
    transaction_type = request.form['transaction_type']
    transactions.append({'amount': amount, 'category': category, 'date': date, 'type': transaction_type})
    return redirect(url_for('dashboard'))

@app.route('/view_balance')
def view_balance():
    if 'username' not in session:
        return redirect(url_for('index'))
    balance = sum(t['amount'] if t['type'] == 'Income' else -t['amount'] for t in transactions)
    return render_template('balance.html', balance=balance)

@app.route('/monthly_summary')
def monthly_summary():
    if 'username' not in session:
        return redirect(url_for('index'))
    # Get the current month
    current_month = datetime.now().month
    monthly_income = sum(t['amount'] for t in transactions if t['type'] == 'Income' and datetime.strptime(t['date'], '%Y-%m-%d').month == current_month)
    monthly_expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense' and datetime.strptime(t['date'], '%Y-%m-%d').month == current_month)
    return render_template('summary.html', income=monthly_income, expense=monthly_expense, period="Month")

@app.route('/weekly_summary')
def weekly_summary():
    if 'username' not in session:
        return redirect(url_for('index'))
    # Get the start and end of the current week
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    weekly_income = sum(t['amount'] for t in transactions if t['type'] == 'Income' and start_of_week <= datetime.strptime(t['date'], '%Y-%m-%d') <= end_of_week)
    weekly_expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense' and start_of_week <= datetime.strptime(t['date'], '%Y-%m-%d') <= end_of_week)
    return render_template('summary.html', income=weekly_income, expense=weekly_expense, period="Week")

@app.route('/view_all_transactions')
def view_all_transactions():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('all_transactions.html', transactions=transactions)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
