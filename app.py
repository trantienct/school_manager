import os
from Controller.roleController import *
from Controller.loginController import *
from Controller.userController import *
from Controller.classController import *
from functools import wraps
from myform import UserInfo
app = Flask(__name__)
app.secret_key='abcda1234'
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def access_allow(allowed_role):
    user_role = get_role_name_by_user_id(session.get('user_id'))
    if user_role in allowed_role:
        return True
    return False


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

@app.route('/admin/user/info/<user_id>', methods = ['GET', 'POST'])
def user_info(user_id):
    message = ''
    check_user = get_user_by_id(user_id)
    if not check_user:
        message = 'This user does not exists'
    user_info = get_user_info_by_id(user_id)
    if not user_info:
        message = 'This user does not have any user info'
    return render_template('management/pages/user/info.html', message=message, user = user_info)

@app.route('/admin/user/list')
@login_required
def user_list():
    check_access = access_allow((ADMIN_ROLE,))
    print(check_access)
    if not check_access:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'GET':
        username = request.args.get('username')
        actived = request.args.get('is_actived')
        role_id = request.args.get('role_id')
        list_user = search_user(username, actived, role_id)
        roles = get_all_role()
    return render_template('management/pages/user/list.html', user_data = list_user,roles = roles, student_role = STUDENT_ROLE )

@app.route('/student/<student_id>', methods=['GET', 'POST'])
@login_required
def show_user_info(student_id):
    pass

@app.route('/student/<student_id>/add_user_info', methods=['GET', 'POST'])
@login_required
def add_user_info(student_id):
    user_info_form = UserInfo()
    user_info_form.user_id.data = student_id
    user_info_form.user_id.render_kw = {'disabled': True}
    if request.method == 'GET':
        return render_template('management/pages/user_info/add_info.html', form=user_info_form, student_id = student_id )
    if request.method == 'POST':
        user_id = request.form['user_id']
        fullname = request.form['fullname']
        birthday = request.form['birthday']
        address = request.form['address']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        mother_name = request.form['mother_name']
        father_name = request.form['father_name']
        # image_file = request.files['image']
        print(user_id)
        check_user_id = get_user_by_id(user_id)
        if not check_user_id:
            flash('We can not find your user')
            return redirect(url_for('add_user_info'))
        check_role_name = get_role_name_by_user_id(user_id)
        if check_role_name != STUDENT_ROLE:
            flash('Your role is not student')
            return redirect(url_for('add_user_info'))
        save_user_info = insert_user_info(user_id,fullname,gender,birthday,address,phone_number,father_name,mother_name)
        return redirect(url_for('user_list'))

@app.route('/admin/user/edit/<user_id>', methods = ['GET', 'POST'])
@login_required
def user_edit(user_id):
    if request.method == 'GET':
        roles = get_all_role()
        user_info = get_user_by_id(user_id)
        if not user_info:
            flash("This user doesn't exist")
        return render_template('management/pages/user/edit.html', roles = roles, user_info = user_info, user_id = user_id)
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
            return redirect(url_for('user_edit', user_id=user_id))
        else:
            save = update_user(user_id, username, role_id, status)
            flash('Update information successfully')
            return redirect(url_for('user_edit', user_id=user_id))

@app.route('/admin/user/create', methods=['GET', 'POST'])
@login_required
def create_user():
    check_access = access_allow((ADMIN_ROLE,))
    if not check_access:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'GET':
        roles = get_all_role()
        if len(roles) == 0:
            flash('Can not load role lists. Please contact to administrator')
        return render_template('management/pages/user/create.html', title='Register', roles=roles)
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
    check_access = access_allow((ADMIN_ROLE,))
    if not check_access:
        return redirect(url_for('admin_dashboard'))
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
    check_access = access_allow((ADMIN_ROLE,))
    if not check_access:
        return redirect(url_for('admin_dashboard'))
    all_role = get_all_role()
    return render_template('management/pages/role_list.html', role_data = all_role)

@app.route('/admin/class/create', methods=['GET', 'POST'])
@login_required
def create_class():
    check_access = access_allow((ADMIN_ROLE,))
    if not check_access:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'GET':
        all_teacher = get_user_by_role(TEACHER_ROLE)
        return render_template('management/pages/class/create.html', teacher_data = all_teacher)
    if request.method == 'POST':
        class_name = request.form['class_name']
        teacher_id = request.form['teacher_id']
        session['class_name'] = class_name
        session['teacher_id'] = teacher_id
        check_teacher = check_teacher_existed(teacher_id)
        print(check_teacher)
        if check_teacher:
            result = save_class(class_name, teacher_id)
            if not result:
                flash('Insert class' + class_name + 'failed')
            else:
                flash('Insert category' + class_name + 'successfully')
                return redirect(url_for('admin_dashboard'))
        else:
            flash('This teacher has already taught other class')
            return redirect(url_for('create_class'))

@app.route('/admin/class/list')
@login_required
def class_list():
    check_access = access_allow((ADMIN_ROLE,))
    if not check_access:
        return redirect(url_for('admin_dashboard'))
    all_class = get_all_class()
    return render_template('management/pages/class/list.html', class_data = all_class)



@app.route('/logout')
def logout():
    delete_session_login()
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run()
#
#
