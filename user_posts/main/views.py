from flask import Blueprint, render_template, flash, redirect, session, request, url_for

from user_posts.data.models import Post, Author, db
from user_posts.main.forms import PostForm

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template("index.html")


@main.route('posts')
def display_posts():
    posts = [post for post in Post.query.all()]
    return render_template("posts.html", posts=posts)

@main.route('add_post', methods=['GET','POST'])
def add_post():
	try:
		form = PostForm(request.form)
		if request.method == 'POST' and form.validate():
			title = form.title.data
			rating = form.rating.data
			description = form.description.data
			author = Author.query.filter(Author.username == session['username']).first()
			post = Post(title=title,rating=rating,description=description,author=author)
			db.session.add(post)
			db.session.commit()
			flash('New post was added successfully')
			return redirect(url_for('main.display_posts'))
	except Exception as e:
		flash(e)
	return render_template('add_post.html', form=form)

@main.route('delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
	post = Post.query.filter(Post.id == post_id).first()
	db.session.delete(post)
	db.session.commit()
	flash('Your post was successfully removed')
	return redirect(url_for('main.display_posts'))