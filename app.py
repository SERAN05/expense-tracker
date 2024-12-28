from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Route to display the home page and show all expenses
@app.route('/')
def index():
    # Connect to the database
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    
    # Fetch all expenses
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html', expenses=expenses)

# Route to handle adding a new expense
@app.route('/add', methods=['POST'])
def add_expense():
    item = request.form['item']
    amount = request.form['amount']
    
    # Insert the new expense into the database
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (item, amount) VALUES (?, ?)", (item, amount))
    conn.commit()
    conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
