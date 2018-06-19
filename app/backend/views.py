from flask import render_template, redirect, request, url_for, flash
from . import backend
from .forms import LoginForm
from flask_login import login_user,login_required,logout_user
from ..models import User
from .. import db
from .helper import json_data, json_lists
from pprint import pprint

@backend.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data,enabled=True).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, False)
            return json_data(url_for('.index'),'登录成功')
        return json_data('','登录失败',0)
    return render_template('backend/login/index.html',form=form)

#首页控制台
@backend.route('/index')
@login_required
def index():
    return render_template('backend/console/index.html')

#管理员列表
@backend.route('/user/index')
def users():
    page = request.args.get('page',0, type=int)
    if page > 0:
        lists = User.query.order_by(User.created_at.desc()).paginate(page,per_page=15,error_out=False)
        data = {
            'list':lists.items,
            'total':lists.total
        }
        return json_lists(data)
    return render_template('backend/user/index.html')

#管理员编辑
@backend.route('/user/edit')
def user_edit():
    return render_template('backend/user/edit.html')

#文章列表
@backend.route('/post/index')
def posts():
    return render_template('backend/post/index.html')

@backend.route('/category/index')
def category():
    return render_template('backend/category/index.html')

@backend.route('/label/index')
def labels():
    return render_template('backend/label/index.html')

@backend.route('/statis')
def statis():
    return render_template('backend/statis/index.html')

@backend.route('/log/index')
def logs():
    return render_template('backend/log/index.html')

#系统设置
@backend.route('/setting/index')
def setting():
    return render_template('backend/setting/index.html')


