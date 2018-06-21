from flask import render_template, redirect, request, url_for, flash
from . import frontend
from ..models import Category, Label, Post, Link

@frontend.route('/')
def index():
    return render_template('index.html');


@frontend.route('/category/<int:id>')
def category(id):
    return render_template('category.html')

@frontend.route('/article/<int:id>')
def post(id):
    return render_template('post.html')

@frontend.route('/search')
def search():
    return render_template('search.html')
