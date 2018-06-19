from flask import render_template, redirect, request, url_for, flash
from . import backend
from .forms import LoginForm
from flask_login import login_user,login_required,logout_user
from ..models import User
from .. import db
from .helper import json_data, json_lists
from datetime import datetime

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

#管理员新增
@backend.route('/user/create',methods=['GET','POST'])
def user_create():
    method = request.method
    if method == 'POST':
        enabled = request.form.get('enabled',False)
        enabled = 1 == enabled
        user = User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            mobile=request.form.get('mobile'),
            password=request.form.get('password'),
            enabled=enabled,
            created_at=datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        return json_data(url_for('backend.users'),'创建成功')
    return render_template('backend/user/create.html')

#管理员编辑
@backend.route('/user/edit',methods=['GET','POST'])
def user_edit():
    method = request.method
    if method == 'POST':
        user = User.query.get(request.form.get('id'))
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.mobile = request.form.get('mobile')
        if request.form.get('password') != '':
            user.password = request.form.get('password')
        
        user.enabled = request.form.get('enabled',False)
        db.session.commit()
        return json_data(url_for('backend.users'),'修改成功')
    else:
        id = request.args.get('id',0, type=int)
        user = User.query.filter_by(id=id).first_or_404()
    return render_template('backend/user/edit.html',user=user)


#管理员删除
@backend.route('/user/del')
def user_del():
    id = request.args.get('id',0, type=int)
    if id > 0:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return json_data(url_for('backend.users'),'删除成功')
    return json_data('','数据不存在',0)

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


