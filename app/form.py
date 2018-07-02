from flask_wtf import Form
from wtforms import TextField,BooleanField,PasswordField
from wtforms.validators import Required


class LoginForm(Form):
    name = TextField('Name', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember_Me', default=False)


class PostForm(Form):
    title  = TextField('Title', validators=[Required()])
    content= TextField('Content',validators=[Required()])
    tag    = TextField('Tag', validators=[Required()])
