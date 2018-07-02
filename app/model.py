import sys
from mongoengine import *
from flask.ext.login import UserMixin
from wtforms import Form, BooleanField, StringField, PasswordField, validators


reload(sys)
sys.setdefaultencoding('utf-8')
register_connection("blog-db","blog")


class User(UserMixin):

    def __init__(self,username):
        self.username = username
    def is_authenticated(self):
        return True
    def get_id(self):
        return self.username

class Admin(DynamicDocument):
    meta = {
        'db_alias':'blog-db',
        'collection': 'Admin' ,
        'strict': False,
    }
    username = StringField(required=True , max_length=64)
    password = StringField(required=True , max_length=64)

class Post(DynamicDocument):
    meta = {
        'db_alias':'blog-db',
        'collection':'post',
        'strict':False,
    }
    postid      = StringField(required=True, max_length = 10)
    title       = StringField(required=True, max_length = 64   )
    content     = StringField(required=True, max_length = 960000)
    tag         = StringField(required=True, max_length = 20   )
    time        = StringField(required=True, max_length = 20   )
    status      = StringField(required=True, max_length = 20   )


class Comment(Document):
    meta = {
        'db_alias':'blog-db',
        'collection':'comment',
        'strict':False,
    }
    author    = StringField(required=True, max_length = 20 )
    comment   = StringField(required=True, max_langth = 100)
    time      = StringField(required=True, max_length = 20 )
    passageid = StringField(required=True, max_length = 10 )






class CommentForm(Form):
    username = StringField('username',[validators.Length(min=3,max=7  )])
    comment  = StringField('comment' ,[validators.Length(min=3,max=400)])
    id       = StringField('id'      ,[validators.Length(min=1,max=10 )])



