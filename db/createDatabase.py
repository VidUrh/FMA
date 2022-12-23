import sqlite3

# Connect to the database
conn = sqlite3.connect("./test_fma.db")

# Open the SQL file
with open("fma.sql", "r") as f:
    # Execute the SQL commands in the file
    conn.executescript(f.read())

# Commit the changes and close the connection
conn.commit()
conn.close()