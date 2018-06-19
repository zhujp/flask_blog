from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, default='')
    body = db.Column(db.Text, nullable=False, default='')
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    author = db.Column(db.String(30), nullable=False, default='')
    views = db.Column(db.SmallInteger, nullable=False, default=0)
    keywords = db.Column(db.String(255), nullable=False, default='')
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    enabled = db.Column(db.Boolean, nullable=False, default=False)

    category = db.relationship('Category',
        backref=db.backref('posts', lazy=True))
    def __repr__(self):
        return '<Posts %r>' % self.title


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40), nullable=False, default='')
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    sort = db.Column(db.SmallInteger, nullable=False, default=0)
    def __repr__(self):
        return '<Category %r>' % self.name    

class Label(db.Model):
    __tablename__ = 'labels'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40), nullable=False, default='')
    enabled = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Label %r>' % self.name


class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40), nullable=False, default='')
    url = db.Column(db.String(100), nullable=False, default='')
    sort = db.Column(db.SmallInteger, nullable=False, default=0)
    enabled = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Label %r>' % self.name


class PostLabel(db.Model):
    __tablename__ = 'post_labels'
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer, nullable=False, default=0)
    label_id = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<PostLabel %r>' % self.article_id


class User(UserMixin, db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False,default='')
    email = db.Column(db.String(40), unique=True, nullable=False,default='')
    mobile = db.Column(db.String(20), unique=True, nullable=False, default='')
    password_hash = db.Column(db.String(255), nullable=False, default='')
    created_at = db.Column(db.DateTime)
    enabled = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Setting(db.Model):

    __tablename__='setting'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(60),nullable=False,default='')
    value = db.Column(db.String(255), nullable=False,default='')

    def __repr_(self):
        return '<Setting %r>' % self.name

