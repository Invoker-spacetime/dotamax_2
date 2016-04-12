#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import Required
from dotamax3 import Nice_Best_Hero,hero_data_after
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(Form):
	Teammate_1 = StringField('1')
	Teammate_2 = StringField('2')
	Teammate_3 = StringField('3')
	Teammate_4 = StringField('4')
	Opponent_1 = StringField('1')
	Opponent_2 = StringField('2')
	Opponent_3 = StringField('3')
	Opponent_4 = StringField('4')
	Opponent_5 = StringField('5')
	Select_Mode = SelectField(u'模式：', choices=[('com',u'均衡'), ('team',u'配合'),('opps',u'针对'),('only_hero',u'胜率')])
	submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	
	if form.validate_on_submit():
		
		teammate_list = [form.Teammate_1.data,form.Teammate_2.data,form.Teammate_3.data,form.Teammate_4.data]
		print teammate_list

		print type(form.Teammate_1.data)

		opponent_list = [form.Opponent_1.data,form.Opponent_2.data,form.Opponent_3.data,
			form.Opponent_4.data,form.Opponent_5.data]
		print opponent_list

		#print '1'
		if ((teammate_list == [u'',u'',u'',u''])&(opponent_list == [u'',u'',u'',u'',u''])): #when no input use pld
 			teammate_list = session['T_List']
			opponent_list = session['O_List']
			print 'no input'
		#print '2'

		mod = form.Select_Mode.data
		nice_best_hero ,error_list= Nice_Best_Hero(teammate_list,opponent_list,mod)	

		if nice_best_hero:
		#old_name = session.get('name')
		#if old_name is not None and old_name != form.name.data:
			#flash('Looks like you have changed your name!')
		#session['name'] = form.name.data
		#flash(nice_best_hero)
		#print nice_best_hero
			session['hero_info_1'] = nice_best_hero[0].__dict__()
			session['hero_info_2'] = nice_best_hero[1].__dict__()
			session['hero_info_3'] = nice_best_hero[2].__dict__()
			#print type(nice_best_hero[0].__dict__()['This hero is'])
		#if error_list:
		session['error_list'] = error_list

		
		session['T_List'] = teammate_list
		session['O_List'] = opponent_list
		print teammate_list,opponent_list

		return redirect(url_for('index'))

	return render_template('index.html', form=form, hero_best_list_1 = session.get('hero_info_1'),
		hero_best_list_2 = session.get('hero_info_2'),hero_best_list_3 = session.get('hero_info_3'),
		Teammates_List = session.get('T_List'),Opponents_List = session.get('O_List'),error_info = session.get('error_list'))


if __name__ == '__main__':
	manager.run()

