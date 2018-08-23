from flask import render_template, redirect, request, url_for, flash, session
from . import frontend
from ..models import Category, Label, Post, Link,Setting
from datetime import datetime

@frontend.route('/')
def index():
    page = request.args.get('page',1, type=int)
    pagination = Post.query.filter_by(enabled=True).order_by(Post.created_at.desc()).paginate(page,per_page=15,error_out=False)
    posts = pagination.items

    essence = Post.query.filter_by(enabled=True).order_by(Post.views.desc()).limit(6);

    return render_template('index.html',posts=posts,pagination=pagination,current_time=datetime.utcnow(),essence=essence)


@frontend.route('/category/<int:id>')
def category(id):
    page = request.args.get('page',1, type=int)
    pagination = Post.query.filter_by(enabled=True,cat_id=id).order_by(Post.created_at.desc()).paginate(page,per_page=15,error_out=False)
    posts = pagination.items
    category = Category.query.filter_by(id=id).first()

    return render_template('category.html',posts=posts,pagination=pagination,id=id,category=category)

@frontend.route('/article/<int:id>')
def post(id):
    post = Post.query.filter_by(id=id).first()
    post.views = post.views+1
    return render_template('post.html',post=post)

@frontend.route('/search',methods=['GET','POST'])
def search():
    keyword = request.form.get('keyword','')  
    if not keyword.strip():
        keyword = session.get('keyword')
    session['keyword'] = keyword    
    page = request.args.get('page',1, type=int)
    pagination = Post.query.filter(Post.title.like('%'+keyword+'%')).order_by(Post.created_at.desc()).paginate(page,per_page=15,error_out=False)
    posts = pagination.items
    return render_template('search.html',posts=posts,pagination=pagination,keyword=keyword)

@frontend.context_processor
def common():
    nav = Category.query.filter_by(enabled=True).all()    
    sets = Setting.query.all()
    site = {}
    for s in sets:
        site[s.name] = s.value
    links = Link.query.filter_by(enabled=True).order_by(Link.sort.asc()).all()
    return dict(site=site,nav=nav,links=links)
