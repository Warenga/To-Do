# Contains forms used in main

from flask.ext.wtf import Form 
from ..models import User
from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators
from wtforms.validators import Required, Email, Length, EqualTo
from wtforms import ValidationError

class CardForm(Form):
	card = StringField('New Card')
	submit = SubmitField('Save')

class TaskForm(Form):
	task = StringField('')
	submit = SubmitField('Submit')

class UserForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	username = StringField('Username', validators=[Required(), Length(1, 64)])
	password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Register')
