from flask import jsonify, render_template, session, redirect, request, url_for, flash
from . import main
from .forms import TaskForm, CardForm, UserForm, CheckForm
from ..import db
from ..models import User, Cards, Tasks
from flask.ext.login import login_required, current_user
import json
from datetime import datetime

@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	"""
		Contains the url and form for adding a new card
	"""
	form1 = CardForm()
	if form1.validate_on_submit():
		card = Cards(card=form1.card.data, author=current_user._get_current_object())
		db.session.add(card)
		db.session.commit()
		flash('You have made a new List')
		return redirect(url_for('.index'))
	user = current_user._get_current_object()
	cards = user.cards.order_by(Cards.card).all()
	return render_template('index.html', form1=form1, task_form=TaskForm(), user=user, check_form=CheckForm(),
	 cards=cards)

@main.route('/tasks/<int:id>/', methods=['GET', 'POST'])
def task(id):
	"""
		Contains the url and form for adding a new task in a card
	"""
	card = Cards.query.get_or_404(id)
	task_form = TaskForm()
	if request.method == 'POST' and task_form.validate_on_submit():
		task = Tasks(task=task_form.task.data, card=card)
		db.session.add(task)
		db.session.commit()
		flash('You have made a new Task')
		return redirect(url_for('.index'))
	tasks = Tasks.query.order_by(Tasks.task).all()
	return render_template('index.html', task_form=task_form, form1=CardForm(), check_form=CheckForm(),
	 cards=[card], tasks=tasks)

# @main.route('/check/<int:id>', methods=['GET', 'POST'])
# def tick(id):
# 	"""
# 		Checks checked box and saves in database
# 	"""
# 	task = Tasks.query.get_or_404(id)
# 	check_form = CheckForm()
# 	if request.method == 'POST' and check_form.validate():
# 		check = Tasks(done=check_form.done.data, task=task)
# 		db.session.add(check)
# 		db.session.commit()
# 		check_form.done.data = True
# 		flash('Task %r done' % check.done)
# 		return redirect(url_for('.index'))
# 	checks = Tasks.query.order_by(Tasks.done).all()
# 	return render_template('index.html', check_form=check_form, form1=CardForm(),
# 	 task_form=task_form, tasks=[task], checks=tasks)

# @main.route('/check/<int:id>', methods=['POST'])
# def tick(id):
# 	task = Tasks.query.get_or_404(id)
# 	if request.method == 'POST':
# 		task = Tasks.query.get(request.form.get('id'))
# 		task.done = True
# 		db.session.add(post)
# 		db.session.commit()
# 		return True
# 	return False

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_card(id):
	"""
		Contains the url and id for deleting a card in the database
	"""
	card = Cards.query.get_or_404(id)
	if request.method == 'POST':
		db.session.delete(card)
		db.session.commit()
		flash('Card deleted')
		return redirect(url_for('.index', cards=[card]))


@main.route('/delete/task/<int:id>', methods=['GET', 'POST'])
def delete_task(id):
	"""
		Contains the url and id for deleting a tasks in the database
	"""
	task = Tasks.query.get_or_404(id)
	if request.method == 'POST':
		db.session.delete(task)
		db.session.commit()
		flash('Task deleted')
		return redirect(url_for('.index', tasks=[task]))

@main.route('/settings', methods=['GET','POST'])
@login_required
def settings():
	form = UserForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.password = form.password.data
		user = current_user
		db.session.delete(user)
		db.session.add(user)
		db.session.commit()
		flash('Your settings have been changed')
		return redirect('/index')
	form.username.data = current_user.username
	form.email.data = current_user.email
	return render_template('settings.html', form=form)




