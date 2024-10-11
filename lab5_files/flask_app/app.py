from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'root',         # Your MySQL username
    'password': '',         # Your MySQL password
    'host': 'localhost',    # MySQL service name in Docker
    'database': 'visits'    # Your MySQL database name
}

# Function to create the visits database if it doesn't exist
def create_database():
    try:
        conn = mysql.connector.connect(user='root', password='', host='localhost')
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS visits")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        conn.close()

# Function to execute SQL from a file
def execute_sql_file(filename):
    cursor = None
    try:
        with open(filename, 'r') as file:
            sql_script = file.read()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Execute each statement in the SQL script
        for statement in sql_script.split(';'):
            if statement.strip():  # Avoid executing empty statements
                cursor.execute(statement)
        
        conn.commit()  # Commit all changes after execution
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        conn.close()

# Print the current working directory
print("Current working directory:", os.getcwd())

# Function to increment the visit count
def increment_count():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if there's already a count in the database
        cursor.execute("SELECT count FROM visits WHERE id = 1")
        result = cursor.fetchone()
        print("Current count from database:", result)  # Debugging line

        if result:
            new_count = result[0] + 1
            cursor.execute("UPDATE visits SET count = %s WHERE id = 1", (new_count,))
            print("Incremented count to:", new_count)  # Debugging line
        else:
            cursor.execute("INSERT INTO visits (count) VALUES (1)")
            print("Initialized count to 1.")  # Debugging line

        conn.commit()

        cursor.execute("SELECT count FROM visits WHERE id = 1")
        current_count = cursor.fetchone()[0]
        print("Retrieved current count:", current_count)  # Debugging line

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        current_count = 0  # Default value in case of error

    finally:
        if cursor:
            cursor.close()
        conn.close()

    return current_count

@app.route("/")
def home():
    count = increment_count()
    return f"This page has been visited {count} times."

if __name__ == "__main__":
    # Create the database if it doesn't exist
    create_database()
    
    # Execute the SQL file to create the table
    execute_sql_file(r'C:\xampp\htdocs\Cloud-Computing-Lab-5\lab5_files\flask_app\visits.sql')
    
    app.run(host="0.0.0.0")
