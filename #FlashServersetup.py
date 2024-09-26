#FlashServersetup
from gettext import install


zip install Flask
from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route for the main page
@app.route('/')
def index():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Dynamic time
    return render_template('index.html', current_time=current_time)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    # Save to the database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO submissions (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

    return f'Form submitted successfully! Name: {name}, Email: {email}'

# Route to display submissions
@app.route('/submissions')
def submissions():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM submissions')
    data = cursor.fetchall()
    conn.close()
    return render_template('submissions.html', data=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
