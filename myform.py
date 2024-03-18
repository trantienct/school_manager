from flask_wtf import *
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SelectField, DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length
class UserInfo(Form):
    user_id = StringField('User ID')
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=5, max=20)])
    birthday = DateField('Birthday')
    address = StringField('Address')
    gender = SelectField('Gender', choices=[(0, 'Male'), (1, 'Female')])
    phone_number = IntegerField('Phone Number')
    father_name = StringField('Father Name')
    mother_name = StringField('Mother name')
    image = FileField('User Image', validators=[FileRequired(),FileAllowed(['JPG', 'PNG'], 'Only JPG and PNG are allowed')])
    submit = SubmitField('Save')