import sqlite3
conn = sqlite3.connect('school_management.db')

cur = conn.execute('SELECT * FROM users')
row = cur.fetchall()
print(row)