import mysql.connector

# Connect to MySQL server
try:
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'Inso',
        password = 'AO3iSQL!',
    )

    cursor = db.cursor()
    print("Connected to MySQL server\n")
except mysql.connector.Error as err:
    print(f"Connection error: {err}\n")
    exit()

# try:
#     cursor.execute("DROP DATABASE IF EXISTS ao3_library")
#     print("Dropped existing database 'ao3_library' (all tables removed)")
# except mysql.connector.Error as err:
#     print(f"Error dropping database: {err}")
#     exit() 

# creating database
cursor.execute("CREATE DATABASE IF NOT EXISTS ao3_library")
# sets as active schema
cursor.execute("USE ao3_library")


# table for works
cursor.execute("""
    CREATE TABLE IF NOT EXISTS works (
        id INT AUTO_INCREMENT PRIMARY KEY,                                                          -- unique ID for each work
        title VARCHAR (255) NOT NULL,                                                               -- fic title (required)
        author VARCHAR(100) NOT NULL,                                                               -- author name (required)
        fandom VARCHAR(255),                                                                        -- main fandom for fic
        summary TEXT,                                                                               -- fic summary
        notes TEXT,                                                                                 -- my notes
        word_count INT,                                                                             -- total words
        chapters INT DEFAULT 1,                                                                     -- number of chapters
        complete BOOLEAN DEFAULT FALSE NOT NULL,                                                    -- finished or ongoing
        published_at DATETIME,                                                                      -- when it was first published
        rating ENUM('General Audiences', 'Teen', 'Mature', 'Explicit') DEFAULT 'General Audiences', -- Content rating of the work
        UNIQUE (title, author)                                                                      -- Prevent author from having duplicate titles
    )
""")

# table for tags
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INT AUTO_INCREMENT PRIMARY KEY,  -- unique ID for each tag
        tag_name VARCHAR(100) UNIQUE        -- name of tag (relationship, character or general tags)
    )
""")

# create work_tags table (m-to-m relation)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS work_tags (
        work_id INT, -- reference to work.id
        tag_id INT,  -- reference to tags.id
        PRIMARY KEY (work_id, tag_id),
        FOREIGN KEY (work_id) REFERENCES works(id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
    )
""")

cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print("tables: ")
for table in tables:
    print(table[0])

cursor.execute("DESCRIBE works")
columns = cursor.fetchall()
print("\nColumns in 'works': ")
for col in columns:
    print(col)

db.commit()
cursor.close()
db.close()
print("\nAll done, connection closed\n")