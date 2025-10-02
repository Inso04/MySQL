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

# helper function for showing all existing tables
def show_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("\nTables in ao3_library:")
    for table in tables:
        print("-", table[0])
    print()

def insert_work():
    # Get work details
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    summary = input("Summary: ").strip()
    notes = input("Notes (optional): ").strip()
    word_count = input("Word count: ").strip()
    word_count = int(word_count) if word_count.isdigit() else None
    chapters = input("Chapters (default 1): ").strip()
    chapters = int(chapters) if chapters.isdigit() else 1
    complete = input("Complete? (y/n, default n): ").lower() == 'y'
    published_at = input("Published date (YYYY-MM-DD HH:MM:SS, optional): ").strip() or None
    rating = input("Rating (General Audiences, Teen, Mature, Explicit, default General Audiences): ").strip() or "General Audiences"

    # Insert work
    try:
        cursor.execute("""
            INSERT INTO works (title, author, summary, notes, word_count, chapters, complete, published_at, rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, author, summary, notes, word_count, chapters, complete, published_at, rating))
        db.commit()
        work_id = cursor.lastrowid
        print(f"Work inserted with ID {work_id}")
    except mysql.connector.Error as err:
        print(f"Error inserting work: {err}")
        return

    # Insert tags
    tags_input = input("Enter tags separated by commas: ").strip()
    tags_list = [t.strip() for t in tags_input.split(",") if t.strip()]
    for tag in tags_list:
        # Check if tag exists
        cursor.execute("SELECT id FROM tags WHERE tag_name=%s", (tag,))
        result = cursor.fetchone()
        if result:
            tag_id = result[0]
        else:
            # Insert new tag
            cursor.execute("INSERT INTO tags (tag_name) VALUES (%s)", (tag,))
            db.commit()
            tag_id = cursor.lastrowid
        # Link work and tag
        try:
            cursor.execute("INSERT INTO work_tags (work_id, tag_id) VALUES (%s, %s)", (work_id, tag_id))
            db.commit()
        except mysql.connector.Error:
            # Skip if already linked
            pass
    print("Tags added/linked successfully.\n")

def browse_works():
    keyword = input("Enter keyword to search in title/summary (leave empty to see all): ").strip()
    query = "SELECT id, title, author, rating FROM works"
    params = ()
    if keyword:
        query += " WHERE title LIKE %s OR summary LIKE %s"
        params = (f"%{keyword}%", f"%{keyword}%")
    cursor.execute(query, params)
    results = cursor.fetchall()
    if results:
        print("\nFound works:")
        for row in results:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Rating: {row[3]}")
        print()
    else:
        print("No works found.\n")

# --- Step 3: Main loop ---
while True:
    print("Choose an action:")
    print("1 - Show all tables")
    print("2 - Insert a new work")
    print("3 - Browse works")
    print("0 - Exit")
    choice = input("Your choice: ").strip()

    if choice == "0":
        print("Exiting...")
        break
    elif choice == "1":
        show_tables()
    elif choice == "2":
        insert_work()
    elif choice == "3":
        browse_works()
    else:
        print("Invalid choice. Try again.\n")

# Close connection
cursor.close()
db.close()
print("Connection closed")
