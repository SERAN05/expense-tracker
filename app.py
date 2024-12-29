import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    # Fetch all expenses from the database
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT name, amount, date FROM expenses')
    expenses = c.fetchall()
    
    # Calculate total amount spent
    c.execute('SELECT SUM(amount) FROM expenses')
    total = c.fetchone()[0] or 0  # Default to 0 if no expenses
    conn.close()

    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    name = request.form['name']
    amount = request.form['amount']
    date = request.form['date']
    
    # Insert into the database
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (name, amount, date) VALUES (?, ?, ?)', (name, amount, date))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/delete_expense/<string:name>', methods=['POST'])
def delete_expense(name):
    # Delete expense from the database by name
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE name = ?', (name,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
