import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('school_management.db')
users_sql = '''
    CREATE TABLE IF NOT EXISTS users
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    is_active INTEGER,
    created_at DATE,
    created_by INTEGER,
    updated_at DATE NULL,
    updated_by INTEGER NULL,
    deleted_at DATE NULL,
    deleted_by INTEGER NULL
    );
'''

roles_sql = '''
 CREATE TABLE IF NOT EXISTS roles
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT
    );
    
'''

user_role_sql = '''
 CREATE TABLE IF NOT EXISTS user_role
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER,
    user_id INTEGER,
    create_at DATE,
    created_by INTEGER,
    updated_at DATE NULL,
    updated_by INTEGER NULL,
    deleted_at DATE NULL,
    deleted_by INTEGER NULL
    );
'''
user_info_sql = '''
 CREATE TABLE IF NOT EXISTS user_info
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name TEXT,
    class_name TEXT,
    gender BOOLEAN,
    birthday DATE,
    address TEXT NULL,
    phone_number TEXT,
    father_name TEXT NULL,
    mother_name TEXT NULL,
    image TEXT NULL,
    create_at DATE,
    created_by INTEGER,
    updated_at DATE NULL,
    updated_by INTEGER NULL,
    deleted_at DATE NULL,
    deleted_by INTEGER NULL
    );
'''

classes_sql = '''
 CREATE TABLE IF NOT EXISTS classes
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT,
    teacher_id INTEGER,
    semester INTEGER,
    create_at DATE,
    created_by INTEGER,
    updated_at DATE NULL,
    updated_by INTEGER NULL,
    deleted_at DATE NULL,
    deleted_by INTEGER NULL
    );
'''

class_member_sql = '''
 CREATE TABLE IF NOT EXISTS class_member
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER,
    student_id INTEGER,
    create_at DATE,
    created_by INTEGER,
    updated_at DATE NULL,
    updated_by INTEGER NULL,
    deleted_at DATE NULL,
    deleted_by INTEGER NULL
    );
'''

lessons_sql = '''
 CREATE TABLE IF NOT EXISTS lessons
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_name TEXT,
    create_at DATE,
    created_by INTEGER,
    updated_at DATE NULL,
    updated_by INTEGER NULL,
    deleted_at DATE NULL,
    deleted_by INTEGER NULL
    );
'''

student_grade_sql = '''
 CREATE TABLE IF NOT EXISTS lessons
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    lesson_id INTEGER,
    student_grade INTEGER,
    create_at DATE,
    created_by INTEGER,
    updated_at DATE NULL,
    updated_by INTEGER NULL,
    deleted_at DATE NULL,
    deleted_by INTEGER NULL
    );
'''
def insert_user():
    conn = sqlite3.connect('school_management.db')
    admin_password = generate_password_hash("123456789")
    conn.execute('INSERT INTO users(username, password, is_active, created_at, created_by) VALUES(?,?,?,?,?)',('administrator', admin_password, 1, '2023-12-18', 0,))
    conn.execute('INSERT INTO roles(role_name) VALUES(?)', ('Admin',))
    conn.execute('INSERT INTO user_role(role_id, user_id,create_at,created_by) VALUES (?,?,?,?)',(1, 1, '2023-12-18', '0'))
    conn.commit()





conn.execute(users_sql)
conn.execute(roles_sql)
conn.execute(user_role_sql)
conn.execute(user_info_sql)
conn.execute(classes_sql)
conn.execute(class_member_sql)
conn.execute(lessons_sql)
conn.execute(student_grade_sql)
insert_user()
conn.commit()