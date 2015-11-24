from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(30), unique=True) 
    rating = db.Column(db.Integer) 
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('posts', lazy='joined'))

    def __init__(self,title,description,author,rating=0):
    	self.title = title
    	self.rating = rating
    	self.description = description
    	self.author = author

    def __repr__(self):
    	return '<Title: %r>'%(self.title)


class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, unique=True)
    # confirm = db.Column(db.String(100), nullable=False)
    # accept = db.Column(db.Boolean(), nullable=False)

    def __init__(self, username,email,password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Author: %r>'% (self.username)