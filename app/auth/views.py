from flask import render_template, redirect, session, url_for, flash, request, current_app
from . import auth, facebook, twitter
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User
from flask.ext.login import login_user, logout_user, login_required, current_user

@auth.route('/')
def welcome():
	""" Contains Url to the welcomepage """
	return render_template('auth/welcomepage.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		flash('Welcome %s' % user.username)
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	session.pop('twitter_oauth', None)
	return redirect(url_for('auth.welcome'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		flash('You can now login')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)


@auth.route('/facebook-login')
def facebook_login():
	callback = url_for(
		'auth.facebook_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True
		)
	return facebook.authorize(callback=callback)

@auth.route('/facebook-login')
def facebook_authorized():
	resp = facebook.authorized_response()
	if resp in None:
		return 'Access denied: reason=%s error=%s' % (
			request.args['error_reason'],
			request.args['error_description']
			)
	if isinstance(resp, OAuthException):
		return 'Access denied: %s' % resp.message

	session['oauth_token'] = (resp['access_token'], '')
	me = facebook.get('/me')
	return 'Logged in as name=%s redirect=%s' %(me.data['name'], 
		request.args.get('next') or url_for('main.index')) 

@facebook.tokengetter
def get_facebook_oauth_token():
	return session.get('oauth_token')

@twitter.tokengetter
def get_twitter_token():
	if 'twitter oauth' in session:
		resp = session['twitter_oauth']
		return resp['oauth_token'], resp['oauth_token_secret']

@auth.route('/twitter-login')
def twitter_login():
	callback_url = url_for(
		'auth.twitter_oauthorized',
		next= request.args.get('next'))
	return twitter.authorize(callback=callback_url or request.referrer or None)

@auth.route('/oauthorized')
def twitter_oauthorized():
	resp = twitter.authorized_response()
	if resp is None:
		flash('You denied the request to sign in')
		redirect(url_for('main.login'))
	else:
		session['twitter_oauth']= resp
	this_user = User.query.filter_by(username=resp['screen_name']).first()
	if this_user is None:
		new_user = User(username=resp['screen_name'],
			password=resp['oauth_token_secret'])
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user)
	else:
		login_user(this_user)
	return redirect(url_for('main.index'))