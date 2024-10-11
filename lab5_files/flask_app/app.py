from flask import Flask
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'root',         # Your MySQL username
    'password': '',         # Your MySQL password
    'host': 'localhost',    # MySQL service name in Docker
    'database': 'visits'    # Your MySQL database name
}

# Function to execute SQL from a file
def execute_sql_file(filename):
    with open(filename, 'r') as file:
        sql_script = file.read()

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql_script, multi=True)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to increment the visit count
def increment_count():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if there's already a count in the database
        cursor.execute("SELECT count FROM visits WHERE id = 1")
        result = cursor.fetchone()

        if result:
            # Increment the count
            new_count = result[0] + 1
            cursor.execute("UPDATE visits SET count = %s WHERE id = 1", (new_count,))
        else:
            # Initialize the count if it doesn't exist
            cursor.execute("INSERT INTO visits (count) VALUES (1)")

        # Commit changes
        conn.commit()

        # Return the current count
        cursor.execute("SELECT count FROM visits WHERE id = 1")
        current_count = cursor.fetchone()[0]

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        current_count = 0  # Default value in case of error

    finally:
        cursor.close()
        conn.close()

    return current_count

@app.route("/")
def home():
    count = increment_count()
    return f"This page has been visited {count} times."

if __name__ == "__main__":
    # Execute the SQL file to create the table
    execute_sql_file('visits.sql')
    app.run(host="0.0.0.0")
