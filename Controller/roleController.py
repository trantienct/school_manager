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
