# app.py

from flask import Flask, render_template, redirect
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "project"
}


def connect_to_database():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def close_database_connection(conn, cursor):
    try:
        # Close the MySQL connection
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")


@app.route('/')
def display_data():
    # Connect to MySQL
    conn = connect_to_database()

    if conn is not None:
        cursor = conn.cursor()

        try:
            # Retrieve data from the MySQL table
            query = "SELECT * FROM students"
            cursor.execute(query)
            data = cursor.fetchall()

            # Render the HTML template with the data
            return render_template('index.html', data=data)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the MySQL connection
            close_database_connection(conn, cursor)

    return "Error connecting to the database"


@app.route('/delete/<int:uid>')
def delete_record(uid):
    # Connect to MySQL
    conn = connect_to_database()

    if conn is not None:
        cursor = conn.cursor()

        try:
            # Delete the record from the MySQL table
            query = "DELETE FROM students WHERE UID = %s"
            cursor.execute(query, (uid,))

            # Commit the changes
            conn.commit()

            # Redirect back to the main page after deletion
            return redirect('/')

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the MySQL connection
            close_database_connection(conn, cursor)

    return "Error connecting to the database"


if __name__ == '__main__':
    app.run(debug=True)
