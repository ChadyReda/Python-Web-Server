import sqlite3

# function to initialize the database
def db_init():
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, sport TEXT)")
        connection.commit()
        cursor.close()
        print("<db init>")


# function to add a user
def add_user(query, params):
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        result = cursor.execute(query, params)
        cursor.close()
        return result 
