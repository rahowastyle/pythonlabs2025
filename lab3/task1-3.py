import sqlite3
import hashlib

DB_NAME = "users.db"

def create_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Connection failed: {e}")
        return None

def create_table():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        sql_create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            login TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL
        );
        """
        cursor.execute(sql_create_users_table)
        conn.commit()
        conn.close()
        print("Таблиця 'users' перевірена/створена.")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(login, password, full_name):
    conn = create_connection()
    if conn:
        hashed_pw = hash_password(password)
        sql = "INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)"
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (login, hashed_pw, full_name))
            conn.commit()
            print(f"User '{login}' added.")
        except sqlite3.IntegrityError:
            print(f"User '{login}' already exists.")
        finally:
            conn.close()

def update_password(login, new_password):
    conn = create_connection()
    if conn:
        hashed_pw = hash_password(new_password)
        sql = "UPDATE users SET password = ? WHERE login = ?"
        cursor = conn.cursor()
        cursor.execute(sql, (hashed_pw, login))
        conn.commit()
        
        if cursor.rowcount > 0:
            print("Password updated.")
        else:
            print(f"User '{login}' wasnt found.")
        conn.close()

def authenticate_user(login, password):
    conn = create_connection()
    if conn:
        sql = "SELECT password FROM users WHERE login = ?"
        cursor = conn.cursor()
        cursor.execute(sql, (login,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_hash = result[0]
            input_hash = hash_password(password)
            
            if stored_hash == input_hash:
                print(f"Welcome, {login}.")
                return True
            else:
                print("Wrong password.")
                return False
        else:
            print("No user with this login was found")
            return False
          
if __name__ == "__main__":
    create_table()

    while True:
        print("--- menu ---")
        print("1. add user")
        print("2. change pswd")
        print("3. login")
        print("4. exit")
        
        choice = input("Choose option (1-4): ")

        if choice == '1':
            l = input("Type login: ")
            p = input("Type password: ")
            n = input("Type full name: ")
            add_user(l, p, n)
        
        elif choice == '2':
            l = input("Type login: ")
            p = input("Type new password: ")
            update_password(l, p)

        elif choice == '3':
            l = input("Login: ")
            p = input("Password: ")
            authenticate_user(l, p)

        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Wrong choice, try again.")
