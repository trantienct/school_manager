from flask import Flask, render_template,request
import sqlite3, os

app = Flask(__name__)
app.secret_key='abcda1234'
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('blog/index.html')
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('management/pages/index.html')
@app.route('/admin/login')
def admin_login():  # put application's code here
    return render_template('management/pages/login.html')


if __name__ == '__main__':
    app.run()
