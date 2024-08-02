import sqlite3
import hashlib

# Connect to the database (create if it doesn't exist)
connection = sqlite3.connect("users.db")
c = connection.cursor()

# Create the users table with an additional balance column
c.execute('''CREATE TABLE IF NOT EXISTS users (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           email TEXT NOT NULL,
           username TEXT NOT NULL UNIQUE,
           password TEXT NOT NULL,
           balance REAL DEFAULT 0.0
           )''')

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add a user to the database
def add_user(email, username, password):
    try:
        with connection:
            hashed_password = hash_password(password)
            c.execute("INSERT INTO users (email, username, password, balance) VALUES (?, ?, ?, ?)", (email, username, hashed_password, 0.0))
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    hashed_password = hash_password(password)
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    return c.fetchone()

def sign_up():
    email = input("Enter your email: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if add_user(email, username, password):
        print("User signed up successfully!")
    else:
        print("This user already exists")

def log_in():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user_data = authenticate_user(username, password)
    if user_data:
        print("Logged in successfully!")
        print(f"Your email is {user_data[1]}")
        print(f"Your balance is {user_data[4]:.2f}")
    else:
        print("Invalid username or password, please try again")

def main():
    while True:
        action = input("Type 'S' to sign up, type 'L' to log in, type 'Q' to quit: ")
        if action == 'S':
            sign_up()
        elif action == 'L':
            log_in()
        elif action == 'Q':
            break

if __name__ == "__main__":
    main()

# Close the database connection
connection.close()