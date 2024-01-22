import os
from Controller.roleController import *
from Controller.loginController import *
from Controller.userController import *
from functools import wraps
app = Flask(__name__)
app.secret_key='abcda1234'
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session and 'username' in session and 'login_status' in session:
            return func(*args, **kwargs)
        return redirect(url_for('admin_login'))
    return wrapper

@app.route('/')
def home():
    # all_user = user.fetchone()
    # student = conn.execute('SELECT ')
    return render_template('blog/index.html')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    user_count = count_user()
    teacher_count = count_user_by_role("teacher")
    student_count = count_user_by_role("student")
    count_list = [user_count, teacher_count, student_count]
    return render_template('management/pages/dashboard.html', count_list=count_list)
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():  # put application's code here
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('admin_dashboard'))
        return render_template('management/pages/login.html')
    if request.method == 'POST':
        check = log_in(request.form['username'], request.form['password'])
        print(check)
        if check:
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Your username/ password is not correct. PLease try again')
            return redirect(url_for('admin_login'))
@app.route('/admin/user_list')
@login_required
def user_list():
    all_user = get_all_user()
    return render_template('management/pages/user_list.html', user_data = all_user)
@app.route('/admin/user_edit/<user_id>', methods = ['GET', 'POST'])
@login_required
def user_edit(user_id):
    if request.method == 'GET':
        roles = get_all_role()
        user_info = get_user_by_id(user_id)
        if not user_info:
            flash("This user doesn't exist")
        return render_template('management/pages/edit_user.html', roles = roles, user_info = user_info, user_id = user_id)
    if request.method == 'POST':
        username = request.form['username']
        role_id = request.form.get('role_id')
        status = request.form['status']
        print(role_id)
        print(username)
        check = check_username(username)
        print(check)
        if not check:
            flash('Your username has existed. Please try another one')
            return redirect(url_for('user_edit', user_id))
        else:
            save = update_user(user_id, username, role_id, status)
            flash('Update information successfully')
            return redirect(url_for('user_edit', user_id))



@app.route('/admin/user/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if request.method == 'GET':
        roles = get_all_role()
        if len(roles) == 0:
            flash('Can not load role lists. Please contact to administrator')
        return render_template('management/pages/roles/create_user.html', title='Register', roles=roles)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role_id']
        check = check_username(username)
        print(check)
        if not check:
            flash('Your username has existed. Please use another one')
            return redirect(url_for('create_user'))
        else:
            user = insert_user(username,password, role_id)
            if not user:
                flash('Insert failed')
                return redirect(url_for('admin_login'))
            else:
                flash('Insert successfully')
                return redirect(url_for('user_list'))







@app.route('/admin/roles/create', methods=['GET','POST'])
@login_required
def create_role():
    if request.method == 'GET':
        return render_template('management/pages/roles/create.html')
    if request.method == 'POST':
        role_name = request.form['role_name']
        result = save_role(role_name)
        if not result:
            flash('Insert category' + role_name + 'failed')
        else:
            flash('Insert category' + role_name + 'successfully')
            return redirect(url_for('admin_dashboard'))

@app.route('/admin/role_list')
@login_required
def role_list():
    all_role = get_all_role()
    return render_template('management/pages/role_list.html', role_data = all_role)



@app.route('/logout')
def logout():
    delete_session_login()
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run()
#
#
