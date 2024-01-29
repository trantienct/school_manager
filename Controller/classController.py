from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

def check_teacher_existed(teacher_id):
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('SELECT * FROM classes WHERE teacher_id = ?',(teacher_id,))
    result = cur.fetchall()
    if len(result) > 0:
        return False
    return True
def save_class(class_name):
    conn = sqlite3.connect('school_management.db')
    insert_query = 'INSERT INTO classes(class_name) VALUES(?)'
    cur = conn.execute(insert_query, (class_name,))
    conn.commit()
    conn.close()
    if cur.lastrowid == 0:
        return False
    return True
def get_all_class():
    conn = sqlite3.connect('school_management.db')
    cur = conn.execute('SELECT * FROM classes')
    result = cur.fetchall()
    return result