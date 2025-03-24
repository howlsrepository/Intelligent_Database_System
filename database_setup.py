import sqlite3

# Connect to Sakila database
db_path = "sakila_master.db"  # Ensure the database file is in the same directory
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in cursor.fetchall()]

print("✅ Connected to Sakila Database.")
print("📌 Tables and Columns in the database:\n")

# Loop through tables and fetch column names
for table in tables:
    cursor.execute(f"PRAGMA table_info({table});")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]  # Extract column names
    
    print(f"📂 Table: {table}")
    print(f"   ➡ Columns: {', '.join(column_names)}\n")

# Close connection
conn.close()
