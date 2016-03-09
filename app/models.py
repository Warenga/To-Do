from . import db, login_manager
from flask import current_app, session, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from datetime import datetime
import json

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	cards = db.relationship('Cards', backref='author', lazy='dynamic')

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __str__(self):
		return str(self.username)

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	__repr__ = __str__



				
class Cards(db.Model):
	__tablename__ = 'cards'
	id = db.Column(db.Integer, primary_key=True)
	card = db.Column(db.String(64), unique=True)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	tasks = db.relationship('Tasks', backref='card', lazy='immediate')
	
class Tasks(db.Model):
	__tablename__ = 'tasks'
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.Text(64))
	# created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	# finshed_time = db.Column(db.DateTime, index=True, default=None)
	done = db.Column(db.Boolean, default=False)
	card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))

	def __repr__(self):
		return '%r' % self.task

	# def is_done(self):
	# 	if self.task.exists():
	# 		return not self.tasks.where(Tasks.done == False).exists()

