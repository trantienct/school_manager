from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

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

def count_user_by_role(role_name):
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('SELECT COUNT(*) FROM user_role JOIN roles ON user_role.role_id = roles.id WHERE roles.role_name = ?',(role_name, ))
    row = cur.fetchone()
    return row[0]

def get_user_by_id(user_id):
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('SELECT users.username, users.is_active, user_role.role_id FROM users JOIN user_role ON users.id = user_role.user_id WHERE users.id = ?',(user_id))
    user_info = cur.fetchone()
    if user_info:
        return user_info
    return False
