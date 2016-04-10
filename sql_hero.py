# -*- coding: utf-8 -*-
#sql_hero.py

#from hero_rate import hero
from sqlalchemy import Column, String, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Integer, MetaData

# 创建对象的基类:
Base = declarative_base()

	
# 定义User对象:
class  Dota_Hero(Base):
# 表的名字:
	__tablename__ = 'dota_hero'		
	# 表的结构:
	id = Column(Integer, primary_key=True)
	hero_name = Column(String(20))
	hero_rate = Column(Float)
	#hero_anti_rate = relationship('Hero_Anti_Rate')
		#order_by = 'Hero_Anti_Rate.hero_anti_name',
		#back_populates = 'dota_hero')
	#hero_comb_rate = relationship('Hero_Comb_Rate')
		#order_by = 'Hero_Comb_Rate.hero_comb_name',
		#back_populates = 'dota_hero')


class  Hero_Anti_Rate(Base):

	__tablename__ = 'hero_anti_rate'		
	# 表的结构:
	id = Column(Integer, primary_key=True)
	hero_anti_name = Column(String(20))
	hero_name = Column(String(20))
	beat_rate = Column(Float)
	#dota_hero = relationship('Dota_Hero', back_populates = 'hero_anti_rate')


class  Hero_Comb_Rate(Base):

	__tablename__ = 'hero_comb_rate'

	id = Column(Integer, primary_key=True)
	hero_comb_name = Column(String(20))
	hero_name = Column(String(20))
	team_rate = Column(Float)
	#dota_hero = relationship('Dota_Hero', back_populates = 'hero_comb_rate')
class hero_sql(object):
	
	#class.var
	DBSession_My_Hero = object

	def __init__(self ,  hero_name='', rate_all=0, rate_comb_dict=() ,rate_anti_dict=()): #init by hero obj 
		self.hero_name = hero_name
		self.hero_rate = rate_all
		self.rate_comb_dict = rate_comb_dict
		self.rate_anti_dict = rate_anti_dict
		

	def  init_sql(self):
		#engine = create_engine('mysql+mysqlconnector://root:root@localhost/my_hero')
		engine = create_engine('sqlite:///database/my_hero.db')
		metadata = MetaData()
		#metadata.clear()
		#creat 3 tables
		mytable_hero = Table('dota_hero', metadata,
                	Column('id', Integer, primary_key=True),
                	Column('hero_name', String(20)),
               	Column('hero_rate', Float)
           		)
		mytable_anti = Table('hero_anti_rate', metadata,
		Column('id', Integer, primary_key=True),
                	Column('hero_anti_name', String(20)),
               	Column('beat_rate', Float),
               	Column('hero_name', String(20))
           		)
		mytable_comb = Table('hero_comb_rate', metadata,
		Column('id', Integer, primary_key=True),
                	Column('hero_comb_name', String(20)),
               	Column('team_rate', Float),
               	Column('hero_name', String(20))
           		)

		metadata.create_all(engine)
		DBSession = sessionmaker(bind=engine)
		hero_sql.DBSession_My_Hero = DBSession


	def save_hero_sql(self):
		print self.hero_name		
		#hero_anti_s = Hero_Anti_Rate(hero_anti_name = self.hero_anti_name,)
		session = hero_sql.DBSession_My_Hero()
		hero_s = Dota_Hero(hero_name=self.hero_name,hero_rate=self.hero_rate)
		session.add(hero_s)#save dotahero table
		session.commit()
		#print self.rate_comb_dict
		#assert self.rate_comb_dict != ()
		for k in self.rate_comb_dict:
			hero_comb_s = Hero_Comb_Rate(hero_comb_name = k,
				hero_name = self.hero_name,team_rate = self.rate_comb_dict[k])
			print 'hero_comb_name : %s'%(k),self.rate_comb_dict[k]
			session.add(hero_comb_s)
		session.commit()
		for k in self.rate_anti_dict:
			hero_anti_s = Hero_Anti_Rate(hero_anti_name = k,
				hero_name = self.hero_name,beat_rate = self.rate_anti_dict[k])
			print 'hero_anti_name : %s'%(k),self.rate_anti_dict[k]
			session.add(hero_anti_s)
		session.commit()
		#session.commit()
		session.close()
		#pass

	def search_hero_sql(self,hero_name_search,hero_comb = 'default',hero_anti = 'default'):
		# 创建Session:
		session = hero_sql.DBSession_My_Hero() 
		# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
		dota_hero_find = session.query(Dota_Hero).filter(Dota_Hero.hero_name==hero_name_search).one()
		
		dota_comb_find = session.query(Hero_Comb_Rate).filter(Hero_Comb_Rate.hero_name==hero_name_search , 
				Hero_Comb_Rate.hero_comb_name == hero_comb).all()
		
		dota_anti_find = session.query(Hero_Anti_Rate).filter(Hero_Anti_Rate.hero_name==hero_name_search , 
				Hero_Anti_Rate.hero_anti_name == hero_anti).all()		
	
		#dota_anti_find = session.query(Hero_Anti_Rate).all()
		# 关闭Session:
		session.close()
		#pass
		
		if dota_comb_find != []:
			return dota_comb_find[0].team_rate
		elif dota_anti_find != []:
			return dota_anti_find[0].beat_rate
		else:
			return dota_hero_find.hero_rate


	
