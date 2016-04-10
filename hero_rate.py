#hero_rate.py
import urllib2
import re
import os
from sql_hero import hero_sql

re_hero = re.compile(r'''class="hero-name-list">([a-zA-Z\s\-\_]+)''') #
re_rate_inteam = re.compile(r'''<div class="segment segment-gold" style="width:([0-9]+.[0-9]+)%''')
re_rate = re.compile(r'''<div class="segment segment-green" style="width:([0-9]+.[0-9]+)%''')
re_html_hero = re.compile('''\<tr onclick\=\"DoNav\(\'\/hero\/detail\/([a-z\_]+)''')#keeper_of_the_night

class hero(object):

	#global vars
	qurllist_hero_c = []
	hero_rate_dict_c = ()
	hero_html_dict_c = ()

	request_headers = {'User-Agent':r'''Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0
		Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8''',
		'Accept-Language':r'''en-US,en;q=0.5'''}

	def __init__(self , hero_name='default' , rate_all=0 , match_up_anti = dict() , team_mate = dict()):
		self.hero_name = hero_name
		self.rate_all = rate_all
		self.rate_comb_dict = ()
		self.rate_anti_dict = ()

	def search_hero_rate(self):
		#print  'Run task %s(%s)' %(self.hero_name,os.getpid())
		url_hero = 'http://dotamax.com/hero/detail/' + 'match_up_anti/' + hero.hero_html_dict_c[self.hero_name]+'/'
		print url_hero
		#get html
		request_hero = urllib2.Request(url = url_hero,
				headers = hero.request_headers)
		hero_content = urllib2.urlopen(request_hero).read() 
		#with open('dotamax.html','wb') as f:
		#	f.write(hero_content)
		assert hero_content != '', 'content is zero!'
		qurlist_anti_name = re.findall(re_hero,hero_content)
		#assert qurlist_anti_name != [], 'qurlist_anti_name is empty!'
		qurlist_anti_rate = re.findall(re_rate_inteam,hero_content)
		#assert qurlist_anti_rate != [], 'qurlist_anti_rate is empty!'
		self.rate_anti_dict = list_dict(qurlist_anti_name,qurlist_anti_rate)####
		#print self.rate_anti_dict
	       #get comb hero rate
		url_hero = 'http://dotamax.com/hero/detail/' + 'match_up_comb/' + hero.hero_html_dict_c[self.hero_name]+'/'
		print url_hero
		#get html
		request_hero = urllib2.Request(url = url_hero,
				headers = hero.request_headers)
		hero_content = urllib2.urlopen(request_hero).read() 
		#with open('dotamax.html','wb') as f:
		#	f.write(hero_content)
		assert hero_content != '', 'content is zero!'
		qurlist_comb_name = re.findall(re_hero,hero_content)
		#assert qurlist_comb_name != [], 'qurlist_anti_name is empty!'
		qurlist_comb_rate = re.findall(re_rate_inteam,hero_content)
		#assert qurlist_comb_rate != [], 'qurlist_anti_rate is empty!'
		self.rate_comb_dict = list_dict(qurlist_comb_name,qurlist_comb_rate)####
		#print self.rate_comb_dict
		hero_sql(self.hero_name , self.rate_all , self.rate_comb_dict , self.rate_anti_dict).save_hero_sql()
		return self

	#def __getattr__(self ,attr):
	#	pass	 

	def  get_main_hero(self):
		
		request_dotamax = urllib2.Request(url = 'http://dotamax.com/hero/rate/',
				headers = hero.request_headers)

		content = urllib2.urlopen(request_dotamax).read() 
		#get hero list
		#with open('dotamax.html','wb') as f:
		#	f.write(content)

		qurllist_hero = re.findall(re_hero,content)	
		qurllist_rate = re.findall(re_rate,content)	
		qurllist_url = re.findall(re_html_hero,content)

		#<tr onclick="DoNav('/hero/detail/omniknight')" style="cursor: pointer;">
		hero_rate_dict = list_dict(qurllist_hero,qurllist_rate)
		hero_html_dict = list_dict(qurllist_hero,qurllist_url)#dict url hero name
		hero.hero_rate_dict_c = hero_rate_dict
		hero.hero_html_dict_c = hero_html_dict
		return qurllist_hero,hero_rate_dict,hero_html_dict 


def list_dict(name,value):
	return dict(zip(name,value))



