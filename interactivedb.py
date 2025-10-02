import mysql.connector
from getpass import getpass

# input for logging in
user = input("Enter MySQL username: ")
password = getpass("Enter MySQL password: ")  # hides input

try:
    db = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database="ao3_library"
    )
    cursor = db.cursor()
    print("Connected to ao3_library")
except mysql.connector.Error as err:
    print(f"Connection error: {err}")
    exit()