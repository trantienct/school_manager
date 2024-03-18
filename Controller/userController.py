from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from Controller.roleController import *
from Config.constant import *
from datetime import datetime
import os

def check_username(username):
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('SELECT COUNT(*) FROM users WHERE username = ?',(username,))
    row = cur.fetchone()
    if row:
        if row[0] == 0:
            return True
    return False
def insert_user(username, password, role_id):
    create_at = datetime.now()
    new_password = generate_password_hash(password)
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('INSERT INTO users(username, password, is_active, created_at, created_by) VALUES (?,?,?,?,?)',(username,new_password,1, create_at,session.get('user_id')))
    conn.commit()
    user_id = cur.lastrowid
    cur2 = conn.execute('INSERT INTO user_role(role_id, user_id, create_at, created_by) VALUES (?,?,?,?)', (role_id, user_id, create_at, session.get('user_id')))
    conn.commit()
    conn.close()
    return True

def update_user(user_id, username,role_id, status):
    conn = sqlite3.connect('school_management.db')
    conn.execute('UPDATE users SET username = ?, is_active = ? WHERE id = ?', (username, status, user_id))
    conn.commit()
    conn.execute('UPDATE user_role SET role_id = ? WHERE user_id = ?', (role_id, user_id))
    conn.commit()
    conn.close()
    return True

def count_user():
    conn = sqlite3.connect('school_management.db')
    user = conn.execute('SELECT COUNT(*) FROM users')
    row = user.fetchone()
    return row[0]

def get_user_info_by_id(user_id):
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('SELECT * FROM user_info WHERE user_id = ?',(user_id))
    user_info = cur.fetchone()
    if user_info:
        return user_info
    return False
def count_user_by_role(role_name):
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('SELECT COUNT(*) FROM user_role JOIN roles ON user_role.role_id = roles.id WHERE roles.role_name = ?',(role_name, ))
    row = cur.fetchone()
    return row[0]

def get_user_by_id(user_id):
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('SELECT users.username, users.is_active, user_role.role_id FROM users JOIN user_role ON users.id = user_role.user_id WHERE users.id = ?',(user_id))
    user = cur.fetchone()
    if user:
        return user
    return False

def get_user_by_role(role_name):
    role_id = get_role_id_by_name(role_name)
    print(role_id)
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('''SELECT users.id, users.username 
                          FROM users 
                          JOIN user_role ON users.id = user_role.user_id
                          WHERE user_role.role_id = ?  ''', (role_id,))
    result = cur.fetchall()
    if len(result) == 0:
        return False
    return result

def search_user(username, is_active, role_id):
    conn = sqlite3.connect('school_management.db')
    query = '''
            SELECT users.id, users.username, users.is_active, roles.role_name
            FROM users JOIN user_role ON users.id = user_role.user_id
            JOIN roles ON user_role.role_id = roles.id'''
    condition = []
    value = []
    if username:
        condition.append('username LIKE ?')
        value.append('%' + username + '%')
    if is_active:
        condition.append('is_active LIKE ?')
        value.append('%' + is_active + '%')
    if role_id:
        condition.append('role_id LIKE ?')
        value.append('%' + role_id + '%')
    if len(condition) > 0:
        condition2 = " AND ".join(condition)
        query = query + ' WHERE ' + condition2
    cur = conn.execute(query, value)
    row = cur.fetchall()
    row2 = [list(x) for x in row]
    result = []
    for user in row2:
        user_id = user[0]
        check = conn.execute('SELECT * FROM user_info WHERE user_id = ?',(user_id,))
        row3 = check.fetchall()
        if len(row3) > 0:
            user.append(1)
        else:
            user.append(0)
        result.append(user)
    print(result)
    return result

def insert_user_info(user_id, fullname, gender, birthday, address, phone_number, father_name, mother_name):
    create_at = datetime.now()
    # filepath = os.path.join('../uploads', image.filename)
    # image.save(filepath)
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('INSERT INTO user_info(user_id, fullname, gender, birthday, address, phone_number, father_name, mother_name,  create_at, create_by) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                       (user_id, fullname, gender, birthday, address, phone_number, father_name, mother_name, create_at, session.get('user_id')))
    conn.commit()
    conn.close()
    return True


