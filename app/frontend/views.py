from flask import render_template, redirect, request, url_for, flash
from . import frontend
from ..models import Category, Label, Post, Link,Setting

@frontend.route('/')
def index():
    nav = Category.query.filter_by(enabled=True).all()
    page = request.args.get('page',1, type=int)
    pagination = Post.query.filter_by(enabled=True).order_by(Post.created_at.desc()).paginate(page,per_page=15,error_out=False)
    posts = pagination.items
    for post in posts:
        post.body = post.body[0:250]

    sets = Setting.query.all()
    site = {}
    for s in sets:
        site[s.name] = s.value
    return render_template('index.html',nav=nav,posts=posts,site=site,pagination=pagination)


@frontend.route('/category/<int:id>')
def category(id):
    return render_template('category.html')

@frontend.route('/article/<int:id>')
def post(id):
    return render_template('post.html')

@frontend.route('/search')
def search():
    return render_template('search.html')
