from user_posts import app
from user_posts.data.models import Post, Author, db

with app.app_context():
	db.drop_all()
	db.create_all()

	db.session.commit()