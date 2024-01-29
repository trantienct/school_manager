from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

def save_role(role_name):
    conn = sqlite3.connect('school_management.db')
    insert_query = 'INSERT INTO roles(role_name) VALUES(?)'
    cur = conn.execute(insert_query, (role_name,))
    conn.commit()
    conn.close()
    if cur.lastrowid == 0:
        return False
    return True
def get_all_role():
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('SELECT * FROM roles')
    result = cur.fetchall()
    return result

def get_role_id_by_name(role_name):
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('SELECT id FROM roles WHERE role_name = ?', (role_name,))
    result = cur.fetchall()
    print(result)
    if len(result) == 0 or len(result) > 1:
        return False
    return result[0][0]

