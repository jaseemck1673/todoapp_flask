from flask import Flask,render_template,request,redirect,url_for
import mysql.connector

app = Flask(__name__)

# MySQL Database Configuration
db_config = {
    'host': 'localhost',  # Replace with your MySQL server hostname
    'user': 'root',       # Replace with your MySQL username
    'password': 'root',       # Replace with your MySQL password
    'database': 'todo_db_flask' # Replace with your database name
}


# Dispalyin tasks
@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Adding task 
@app.route('/add', methods=['POST'])
def add_task():
    task_title = request.form.get('task')
    if task_title:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (task_title,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

# Delete task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Mark completed
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)







