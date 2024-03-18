import sqlite3
conn = sqlite3.connect('school_management.db')

cur = conn.execute('SELECT * FROM users')
row = cur.fetchall()


list = [(1,'ad'), (2, 'bc')]
list_comprehension = [x for x in list]
print(list_comprehension)