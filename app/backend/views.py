import os
from flask import render_template, redirect, request, url_for, flash
from . import backend
from .forms import LoginForm
from flask_login import login_user,login_required,logout_user
from ..models import User, Category, Label,Post, Link, Setting, PostLabel
from .. import db
from .helper import json_data, json_lists
from datetime import datetime
from werkzeug.utils import secure_filename
import json


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


@backend.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('backend.login'))

#首页控制台
@backend.route('/index')
@login_required
def index():
    return render_template('backend/console/index.html')

#管理员列表
@backend.route('/user/index')
@login_required
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
@login_required
def user_create():
    method = request.method
    if method == 'POST':
        user = User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            mobile=request.form.get('mobile'),
            password=request.form.get('password'),
            enabled= '1' == request.form.get('enabled',False),
            created_at=datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        return json_data(url_for('backend.users'),'创建成功')
    return render_template('backend/user/create.html')

#管理员编辑
@backend.route('/user/edit',methods=['GET','POST'])
@login_required
def user_edit():
    method = request.method
    if method == 'POST':
        user = User.query.get(request.form.get('id'))
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.mobile = request.form.get('mobile')
        if request.form.get('password') != '':
            user.password = request.form.get('password')
        
        user.enabled = '1' == request.form.get('enabled',False)
        db.session.commit()
        return json_data(url_for('backend.users'),'修改成功')
    else:
        id = request.args.get('id',0, type=int)
        user = User.query.filter_by(id=id).first_or_404()
    return render_template('backend/user/edit.html',user=user)


#管理员删除
@backend.route('/user/del')
@login_required
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
@login_required
def posts():
    page = request.args.get('page',0, type=int)
    if page > 0:
        lists = Post.query.order_by(Post.created_at.desc()).paginate(page,per_page=15,error_out=False)
        data = {
            'list':lists.items,
            'total':lists.total
        }
        return json_lists(data)
    return render_template('backend/post/index.html')


@backend.route('/post/create',methods=['GET','POST'])
@login_required
def post_create():
    method = request.method
    if method == 'POST':
        post = Post(
            title=request.form.get('title'),
            author=request.form.get('author'),
            body=request.form.get('body'),
            keywords=request.form.get('keywords'),
            cat_id=request.form.get('cat_id',0),
            enabled= '1' == request.form.get('enabled',False),
            created_at=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        
        #文章标签
        # for v in request.form.getlist('label'):
        #     post_label = PostLabel(
        #         post_id = post.id,
        #         label_id = v
        #         )
        #     db.session.add(post_label)
        #     db.session.commit()
        # return json_data('',json.dumps(request.form.getlist('label')),0)
        return json_data(url_for('backend.posts'),'创建成功')
    category = Category.query.filter_by(enabled=True).all()
    labels = Label.query.filter_by(enabled=True).all()
    return render_template('backend/post/create.html',category=category,labels=labels)

@backend.route('/post/edit',methods=['GET','POST'])
@login_required
def post_edit():
    method = request.method
    if method == 'POST':
        post = Post.query.get(request.form.get('id'))
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        post.author = request.form.get('author')
        post.keywords = request.form.get('keywords')
        post.cat_id = request.form.get('cat_id',0)
        post.enabled = '1' == request.form.get('enabled',False)
        db.session.commit()
        return json_data(url_for('backend.posts'),'修改成功')
    else:
        id = request.args.get('id',0, type=int)
        post = Post.query.filter_by(id=id).first_or_404()
        category = Category.query.filter_by(enabled=True).all()
        labels = Label.query.filter_by(enabled=True).all()
        return render_template('backend/post/edit.html',post=post,category=category,labels=labels)


@backend.route('/post/del')
@login_required
def post_del():
    id = request.args.get('id',0, type=int)
    if id > 0:
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        return json_data(url_for('backend.posts'),'删除成功')
    return json_data('','数据不存在',0)

@backend.route('/category/index')
@login_required
def category():
    page = request.args.get('page',0, type=int)
    if page > 0:
        lists = Category.query.order_by(Category.id.desc()).paginate(page,per_page=15,error_out=False)
        data = {
            'list':lists.items,
            'total':lists.total
        }
        return json_lists(data)
    return render_template('backend/category/index.html')


@backend.route('/category/create',methods=['GET','POST'])
@login_required
def category_create():
    method = request.method
    if method == 'POST':
        enabled = '1' == request.form.get('enabled',False)
        category = Category(
            name=request.form.get('name'),
            sort=request.form.get('sort',0),
            enabled=enabled)
        db.session.add(category)
        db.session.commit()
        return json_data(url_for('backend.category'),'创建成功')
    return render_template('backend/category/create.html')

@backend.route('/category/edit',methods=['GET','POST'])
@login_required
def category_edit():
    method = request.method
    if method == 'POST':
        category = Category.query.get(request.form.get('id'))
        category.name = request.form.get('name')
        category.sort = request.form.get('sort',0)
        category.enabled = '1' == request.form.get('enabled',False)
        db.session.commit()
        return json_data(url_for('backend.category'),'修改成功')
    else:
        id = request.args.get('id',0, type=int)
        category = Category.query.filter_by(id=id).first_or_404()
    return render_template('backend/category/edit.html',category=category)


@backend.route('/category/del')
@login_required
def category_del():
    id = request.args.get('id',0, type=int)
    if id > 0:
        category = Category.query.filter_by(id=id).first()
        db.session.delete(category)
        db.session.commit()
        return json_data(url_for('backend.category'),'删除成功')
    return json_data('','数据不存在',0)

@backend.route('/label/index')
@login_required
def labels():
    page = request.args.get('page',0, type=int)
    if page > 0:
        lists = Label.query.order_by(Label.id.desc()).paginate(page,per_page=15,error_out=False)
        data = {
            'list':lists.items,
            'total':lists.total
        }
        return json_lists(data)
    return render_template('backend/label/index.html')

@backend.route('/label/create',methods=['GET','POST'])
@login_required
def label_create():
    method = request.method
    if method == 'POST':
        label = Label(
            name=request.form.get('name'),
            enabled= '1' == request.form.get('enabled',False)
            )
        db.session.add(label)
        db.session.commit()
        return json_data(url_for('backend.labels'),'创建成功')
    return render_template('backend/label/create.html')

@backend.route('/label/edit',methods=['GET','POST'])
@login_required
def label_edit():
    method = request.method
    if method == 'POST':
        label = Label.query.get(request.form.get('id'))
        label.name = request.form.get('name')
        label.enabled = '1' == request.form.get('enabled',False)
        db.session.commit()
        return json_data(url_for('backend.labels'),'修改成功')
    else:
        id = request.args.get('id',0, type=int)
        label = Label.query.filter_by(id=id).first_or_404()
    return render_template('backend/label/edit.html',label=label)


@backend.route('/label/del')
@login_required
def label_del():
    id = request.args.get('id',0, type=int)
    if id > 0:
        label = Label.query.filter_by(id=id).first()
        db.session.delete(label)
        db.session.commit()
        return json_data(url_for('backend.labels'),'删除成功')
    return json_data('','数据不存在',0)


@backend.route('/statis')
@login_required
def statis():
    return render_template('backend/statis/index.html')

@backend.route('/log/index')
@login_required
def logs():
    return render_template('backend/log/index.html')

#系统设置
@backend.route('/setting/index',methods=['GET','POST'])
@login_required
def setting():
    method = request.method
    if method == 'POST':
        post = request.form
        for k,v in post.items():
            if k == 'csrf_token':
                continue

            item = Setting.query.filter_by(name=k).first()
            if item is not None:
                item.value = v
            else:
                item = Setting(name=k,value=v)
            db.session.add(item)
            db.session.commit()
        return json_data(url_for('backend.setting'),'修改成功')

    else:
        sets = Setting.query.all()
        set_data = {}
        for s in sets:
            set_data[s.name] = s.value

    return render_template('backend/setting/index.html',set_data=set_data)


@backend.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return json_data('','没有需要上传到文件')

        file = request.files['file']
        if file.filename == '':
            return json_data('','没有选择要上传到文件')

        # if file and allowed_file(file.filename): #验证允许上传到文件类型
        filename = secure_filename(file.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(basedir,'..','static/uploads/')
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        url_path = '/static/uploads/'+filename
        return json_data(url_path,'图片上传成功',0)

    return json_data('','图片上传失败',1)

# 友情连接
@backend.route('/link/index')
@login_required
def links():
    page = request.args.get('page',0, type=int)
    if page > 0:
        lists = Link.query.order_by(Link.id.desc()).paginate(page,per_page=15,error_out=False)
        data = {
            'list':lists.items,
            'total':lists.total
        }
        return json_lists(data)
    return render_template('backend/link/index.html')


@backend.route('/link/create',methods=['GET','POST'])
@login_required
def link_create():
    method = request.method
    if method == 'POST':
        link = Link(
            name=request.form.get('name'),
            url=request.form.get('url'),
            sort=request.form.get('sort',0),
            enabled= '1' == request.form.get('enabled',False)
            )
        db.session.add(link)
        db.session.commit()
        return json_data(url_for('backend.links'),'创建成功')
    return render_template('backend/link/create.html')

@backend.route('/link/edit',methods=['GET','POST'])
@login_required
def link_edit():
    method = request.method
    if method == 'POST':
        link = Link.query.get(request.form.get('id'))
        link.name = request.form.get('name')
        link.sort = request.form.get('sort',0)
        link.enabled = '1' == request.form.get('enabled',False)
        db.session.commit()
        return json_data(url_for('backend.links'),'修改成功')
    else:
        id = request.args.get('id',0, type=int)
        link = Link.query.filter_by(id=id).first_or_404()
    return render_template('backend/link/edit.html',link=link)


@backend.route('/link/del')
@login_required
def link_del():
    id = request.args.get('id',0, type=int)
    if id > 0:
        link = Link.query.filter_by(id=id).first()
        db.session.delete(link)
        db.session.commit()
        return json_data(url_for('backend.links'),'删除成功')
    return json_data('','数据不存在',0)

