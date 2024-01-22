from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
def log_in(username,password):
    conn = sqlite3.connect('school_management.db')
    select_user = 'SELECT * FROM users WHERE username=?'
    cur = conn.execute(select_user,(username,))
    row = cur.fetchone()
    if row and check_password_hash(row[2], password):
        conn.close()
        session['login_status'] = 1
        session['user_id'] = row[0]
        session['username'] = row[1]
        return True
    else:
        conn.close()
        return False

def get_all_user():
    conn = sqlite3.connect('school_management.db')
    sql = 'SELECT id, username FROM users'
    cur = conn.execute(sql)
    result = cur.fetchall()
    return result


def delete_session_login():
    session.pop('login_status')
    session.pop('user_id')
    session.pop('username')