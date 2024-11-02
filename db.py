import sqlite3

# function to initialize the database
def db_init():
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, sport TEXT)")
        connection.commit()
        cursor.close()
        print("<db init>")



def users(query, params=(), fetch=False):
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        result = cursor.execute(query, params)
        if not fetch:
            connection.commit()  # Ensure changes are saved for INSERT, UPDATE, DELETE queries
            cursor.close()
            return None
        else:
            data = result.fetchall()
            cursor.close()
            return data
        
        

def add_user(name, password, sport):
    query = "INSERT INTO users (name, password, sport) VALUES (?, ?, ?)"
    params = (name, password, sport)
    users(query, params, fetch=False)
    print(f"User '{name}' added.")

def get_users():
    query = "SELECT * FROM users;"
    return users(query, fetch=True)

def delete_user(id):
    query = "DELETE FROM users WHERE id = ?"
    users(query, params=(id), fetch=False)
    print(f"User with id <{id}> is deleted")