# from flask import Flask
# import redis

# app = Flask(__name__)

# r = redis.Redis(host="redis", port=6379)


# @app.route("/")
# def home():
#     count = r.incr("hits")
#     return f"This page has been visited {count} times."


# if __name__ == "__main__":
#     app.run(host="0.0.0.0")

from flask import Flask
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'root',         # Your MySQL username
    'password': '', # Your MySQL password
    'host': 'localhost',          # MySQL service name in Docker
    'database': 'visits'  # Your MySQL database name
}

# Function to increment the visit count
def increment_count():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create the visits table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                count INT NOT NULL
            )
        """)

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
    app.run(host="0.0.0.0")
