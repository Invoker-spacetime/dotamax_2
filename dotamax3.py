#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hero_rate import hero ,list_dict
import time
from multiprocessing import Pool
import os
from sql_hero import hero_sql
import json
import re
class hero_data_after(object):
	def __init__(self, hero_name,hero_rate,rate_team,rate_opps,com_rate):
		self.rate_team = rate_team
		self.rate_opps = rate_opps
		self.com_rate = com_rate
		self.hero_name = hero_name
		self.hero_rate = hero_rate
		

	def __repr__(self):
		return '''This hero is: %s\r\nHero rate: %s\r\nHero rate up in this team: %s\r\nHero rate up face this opps: %s\r\nHero mult rate up: %s'''%(self.hero_name,self.hero_rate,self.rate_team,self.rate_opps,self.com_rate)
	
	__str__ = __repr__

	def __dict__(self):
		return {'This hero is' : self.hero_name , 'Hero rate' : self.hero_rate, 
		'Hero rate up in this team' :  self.rate_team ,'Hero rate up face this opps' : self.rate_opps, 
		'Hero mult rate up':self.com_rate}

	def __redict__(H_Dict):
		self.rate_team = H_Dict['Hero rate up in this team']
		self.rate_opps = H_Dict['Hero rate up face this opps']
		self.com_rate = H_Dict['Hero rate up in this team']
		self.hero_name = H_Dict['This hero is']
		self.hero_rate = H_Dict['Hero rate']
		return self

	def get_rate_team(self):
		return self.rate_team
	def get_rate_opps(self):
		return self.rate_opps
	def get_com_rate(self):
		return self.com_rate
	def get_hero_name(self):
		return self.hero_name
	def get_hero_rate(self):
		return self.hero_rate

	operate = {'team' : get_rate_team, 'opps' : get_rate_opps,'com': get_com_rate,'only_hero':get_hero_rate}

def hero_sorted(data_list , mod = 'com' , num = 5):
	
	new_list = sorted(data_list, key= hero_data_after.operate[mod],reverse=True)
	return new_list[0:num]


def pickle_search(hero_name_p,rate_all):
	return hero(hero_name_p,rate_all).search_hero_rate()

def Nice_Best_Hero(teammate_list_ch,opponent_list_ch,model = 'com'):

	print 'ch_list:',teammate_list_ch,opponent_list_ch

	teammate_list , error_team_name = ch_list_eng_list(teammate_list_ch)
	opponent_list , error_opps_name = ch_list_eng_list(opponent_list_ch)

	print 'eng_list',teammate_list,opponent_list

	error_name = error_team_name + error_opps_name
	print error_name
	
	hero_list ,hero_rate_dict , hero_url_dict = Get_Database(0)
	#rate_point = 0
	#rate_max = -100
	#best_hero = 'Nobody'
	Hero_Result = []

	len_team = len(teammate_list)
	print "len_team",len_team
	len_opps = len(opponent_list)
	print "len_opps",len_opps
	
	if  (len_team + len_opps) == 0:
		return [],error_name

	for hero_iter in hero_list:  
		rate_team  =   rate_opps = com_rate = 0.0
		#len_team = 0
		#len_opps = 0
		if ((hero_iter in teammate_list)|(hero_iter in opponent_list)) == False:
			for team_iter in teammate_list: 
				if (team_iter in hero_list) :   #right hero name   
					rate_team_p = hero_sql().search_hero_sql(hero_iter,team_iter,'Nobody') 
					rate_team = rate_team_p + rate_team
					#len_team = len_team + 1					
					print 'team_rate',hero_iter,team_iter,rate_team_p
			
				#else:
				#	raise
			for opps_iter in opponent_list:
				if (opps_iter in hero_list) :   #currect hero name   
					rate_opps_p = hero_sql().search_hero_sql(hero_iter,'Nobody',opps_iter) 
					rate_opps = rate_opps_p + rate_opps
					#len_opps = len_opps + 1	
					print 'opp_rate',hero_iter,opps_iter,rate_opps_p

			
				#else:
				#	raise
			

			if len_team == 0:
				com_rate_up = (rate_opps/len_opps) - float(hero_rate_dict[hero_iter])
				rate_team_up = -100
				rate_opps_up = rate_opps/len_opps - float(hero_rate_dict[hero_iter])
				only_rate = rate_opps/len_opps
			elif len_opps == 0:
				com_rate_up = (rate_team/len_team) - float(hero_rate_dict[hero_iter])
				rate_team_up = rate_team/len_team - float(hero_rate_dict[hero_iter])
				rate_opps_up = -100
				only_rate = rate_team/len_team
			else:
				com_rate_up = (rate_team/len_team + rate_opps/len_opps) - 2*float(hero_rate_dict[hero_iter])			
				rate_team_up = rate_team/len_team - float(hero_rate_dict[hero_iter])
				rate_opps_up = rate_opps/len_opps - float(hero_rate_dict[hero_iter])
				only_rate = (rate_team/len_team + rate_opps/len_opps)/2
			
			hero_iter_ch = eng_list_ch_list((hero_iter,))

			this_hero = hero_data_after(hero_iter_ch[0] , only_rate ,
				rate_team_up ,rate_opps_up , com_rate_up)

			#print this_hero
			#print hero_rate_dict[hero_iter]
			#print '\r\n'
			Hero_Result.append(this_hero)
			#if (com_rate) > rate_max:
			#	rate_max = com_rate 
			#	best_hero = hero_iter

			#print '%.2f\t%.2f\t%s\r\n'%(com_rate,float(hero_rate_dict[hero_iter]),hero_iter)
	print_txt = ''
	Best_Hero_List = hero_sorted(Hero_Result , model)
	#print  model
	#for li in Best_Hero_List:
	#	pass
		#print_txt = print_txt   + li.__str__ + '\r\n'
		#print li
	#	print '\r\n'

	#Hero_Dict_List = list(map(lambda obj:obj.__dict__ , Best_Hero_List))
	#print Hero_Dict_List
	#a = json.dumps(Best_Hero_List[0], default = lambda obj: obj.__dict__)
	#a = json.dumps(Best_Hero_List[0].__dict__())
	#print a
	#return a
	
	print 'error_name',error_name

	return Best_Hero_List,error_name


def  Get_Database(update):
	if update: #get databass,sometimes dont use
		#hero_list_dir = os.path.join
		try:
			os.remove('database/hero_list.txt')
			os.remove('database/hero_rate_dict.txt')
			os.remove('database/hero_url_dict.txt')
			os.remove('database/my_hero.db')		
		except Exception, e:
			raise e
		finally:
			pass

		hero_sql().init_sql()
		hero_list , hero_rate_dict , hero_url_dict= hero('all').get_main_hero() #get hero list
		with open ('database/hero_list.txt','wb') as f:
			f.write(json.dumps(hero_list))
		with open ('database/hero_rate_dict.txt','wb') as f:
			f.write(json.dumps(hero_rate_dict))
		with open ('database/hero_url_dict.txt','wb') as f:
			f.write(json.dumps(hero_url_dict))

		p = Pool(1)
		for i in hero_list:
			#p.apply_async(pickle_search , args = (i,hero_rate_dict[i]))
			pickle_search(i,hero_rate_dict[i])
		p.close()
		p.join()
		
	else:
		hero_sql().init_sql()
		with open ('database/hero_list.txt','rb') as f:
			context = f.read()
		#print context
		hero_list = json.loads(context)
		with open ('database/hero_rate_dict.txt','rb') as f:
			context = f.read()
		hero_rate_dict= json.loads(context)
		with open ('database/hero_url_dict.txt','rb') as f:
			context = f.read()
		hero_url_dict = json.loads(context)


	return hero_list ,hero_rate_dict , hero_url_dict



def get_chinese_list():
	re_ch = re.compile(u"[\u4e00-\u9fa5]+") 
	re_hero = re.compile(r"([a-zA-Z\s\-\_']+),")
	with open ('database/hero_chinese.txt','rb') as f:
		context = f.read().decode('utf-8')

	#print context

	ch_list = re.findall(re_ch , context)
	#print 'ch_list:',ch_list
	eng_list = re.findall(re_hero , context)
	#print 'eng_list:',eng_list

	ch_eng_dict = list_dict(ch_list,eng_list)
	eng_ch_dict = list_dict(eng_list,ch_list)

	with open ('database/ch_eng_dict.txt','w') as f:
		f.write(json.dumps(ch_eng_dict))
	#print ch_eng_dict

	with open ('database/eng_ch_dict.txt','w') as f:
		f.write(json.dumps(eng_ch_dict ))
	#print eng_ch_dict 

	with open ('database/ch_name.txt','w') as f:
		f.write(json.dumps(ch_list))
	return ch_eng_dict


def eng_list_ch_list(eng_list):

	with open ('database/eng_ch_dict.txt','rb') as f:
			context = f.read()
	eng_ch_dict = json.loads(context)

	with open ('database/hero_list.txt','rb') as f:
			context = f.read()
	eng_name = json.loads(context)

	ch_list = []
	error_name = []
		
	for i in eng_list:
		if i in eng_name:
			ch_list.append(eng_ch_dict[i])
			print eng_ch_dict[i]
			print type(eng_ch_dict[i])
		elif i != '':
			error_name.append(i)	

	return ch_list#,error_name

def ch_list_eng_list(ch_list):

	with open ('database/ch_eng_dict.txt','rb') as f:
			context = f.read()
	ch_eng_dict = json.loads(context)

	with open ('database/ch_name.txt','rb') as f:
			context = f.read()
	ch_name = json.loads(context)

	eng_list = []
	error_name = []
		
	for i in ch_list:
		if i in ch_name:
			eng_list.append(ch_eng_dict[i])
		elif i != '':
			error_name.append(i)	
	return eng_list,error_name


if __name__ == '__main__':
	#get_chinese_list()
	
	#Get_Database(0)
	
	tm = [u'剃刀']
	ap = []
	Nice_Best_Hero(tm,ap)
	
	



