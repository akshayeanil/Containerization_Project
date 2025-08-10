import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_fontawesome import FontAwesome

# Configure logging (helps in debugging inside containers)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
fa = FontAwesome(app)

# Use environment variables for security and flexibility
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'db')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'python_crud')

mysql = MySQL(app)


@app.route('/')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students")
        data = cur.fetchall()
        cur.close()
        return render_template('index.html', students=data)
    except Exception as e:
        logging.error(f"Error fetching students: {e}")
        flash("Error loading data")
        return render_template('index.html', students=[])


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO students(name, email, phone) VALUES(%s, %s, %s)",
                (name, email, phone)
            )
            mysql.connection.commit()
            flash("Data Inserted Successfully!")
        except Exception as e:
            logging.error(f"Error inserting student: {e}")
            flash("Error inserting data")
        return redirect(url_for('index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == "POST":
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE students
                SET name=%s, email=%s, phone=%s
                WHERE id=%s
            """, (name, email, phone, id_data))
            mysql.connection.commit()
            flash("Data Updated Successfully")
        except Exception as e:
            logging.error(f"Error updating student: {e}")
            flash("Error updating data")
        return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods=['POST', 'GET'])
def delete(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
        mysql.connection.commit()
        flash("Data Deleted Successfully")
    except Exception as e:
        logging.error(f"Error deleting student: {e}")
        flash("Error deleting data")
    return redirect(url_for('index'))


if __name__ == "__main__":
    # Bind to 0.0.0.0 so it works inside Docker
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)), debug=True)
