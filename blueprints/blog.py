from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import datetime

from repos.post.post_repo import repo_posts as posts
from models.post import Post
from .methods.preview import preview
from .methods import post_misc_generator as generator


bp = Blueprint('blog', __name__)

@bp.route('/')
def home():
    return render_template('blog/home.html', posts=posts.get_all(), preview=preview, generator=generator)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']        
        error = None

        if not title:
            error = "Title is required"
        if not text:
            error = "Text is required"
        if error is not None:
            flash(error)
        else:
            id = posts.next_id()
            time_now = datetime.datetime.now().strftime("%H:%M  %d.%m.%Y")
                
            posts.add(Post(id, title, text, "Owner", time_now, time_now))

            return redirect(url_for('blog.home'))
    
    return render_template('blog/create_post.html')

@bp.route('/<int:id>/', methods=['GET'])
def show(id):
    return render_template('blog/show_post.html', post=posts.get(id))

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    post = posts.get(id)
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        if not title:
            title = post.title
        if not text:
            text = post.text
        else:
            date_modified = datetime.datetime.now().strftime("Last edited at: %H:%M            %d.%m.%Y       ")
            posts.update(id, title, text, date_modified) 

            return redirect(url_for('blog.home'))
    return render_template('blog/update_post.html', post=post)

@bp.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    posts.delete(id)
    return redirect(url_for('blog.home'))