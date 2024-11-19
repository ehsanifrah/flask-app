from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route for home page
@app.route('/')
def index():
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM entries').fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

# Route to add an entry
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if title and content:
            conn = get_db_connection()
            conn.execute('INSERT INTO entries (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect('/')
    return render_template('add.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
