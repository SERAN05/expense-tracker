from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']

        conn = get_db_connection()
        conn.execute('INSERT INTO expenses (description, amount) VALUES (?, ?)',
                     (description, amount))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add.html')

if __name__ == '__main__':
    app.run()
