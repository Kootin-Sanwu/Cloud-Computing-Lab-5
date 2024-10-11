from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'root',         # Your MySQL username
    'password': '',         # Your MySQL password
    'host': '13.60.47.185',    # MySQL service name in Docker
    'database': 'visits'    # Your MySQL database name
}

# Function to create the visits database if it doesn't exist
def create_database():
    try:
        conn = mysql.connector.connect(user='root', password='', host='13.60.47.185')
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

        conn = mysql.connector.connect(user='root', password='', host='13.60.47.185')
        cursor = conn.cursor()

        # Execute each statement in the SQL script
        for statement in sql_script.split(';'):
            if statement.strip():  # Avoid executing empty statements
                cursor.execute(statement)
                print(f"Executed: {statement.strip()}")  # Debugging line
        
        conn.commit()  # Commit all changes after execution
        print("SQL file executed successfully.")

    except mysql.connector.Error as err:
        print(f"Error executing SQL file: {err}")
    finally:
        if cursor:
            cursor.close()
        conn.close()

# Print the current working directory
print("Current working directory:", os.getcwd())

# Function to increment the visit count
def increment_count():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if there's already a count in the database
        cursor.execute("SELECT count FROM visits WHERE id = 1")
        result = cursor.fetchone()
        print("Current count from database:", result)  # Debugging output

        if result:
            new_count = result[0] + 1
            cursor.execute("UPDATE visits SET count = %s WHERE id = 1", (new_count,))
            print("Updated count to:", new_count)  # Debugging output
        else:
            cursor.execute("INSERT INTO visits (count) VALUES (1)")
            print("Initialized count to 1.")  # Debugging output

        conn.commit()  # Commit the changes
        cursor.execute("SELECT count FROM visits WHERE id = 1")
        current_count = cursor.fetchone()[0]
        print("Retrieved current count:", current_count)  # Debugging output

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
    
    home()
    
    # Execute the SQL file to create the table
    execute_sql_file(r'C:\xampp\htdocs\Cloud-Computing-Lab-5\lab5_files\flask_app\visits.sql')
    
    app.run(host="0.0.0.0")
