"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2011 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import os,string,shutil,sys
from dict_formatter import *

class CfgMgr:
	def __init__(self,parent_class):

		self.parent_class=parent_class

		self.master=os.path.join(parent_class.SITEPKGDIR,'.stepintochinese_config_master')
		self.infname=os.path.join(parent_class.HOMEDIR,'.stepintochinese_config')

		self.config=self.load_config()
		
	def get_config(self):
		return self.config
			
	def load_config(self):

		parent_class=self.parent_class

		if not os.path.exists(self.infname):
			if os.path.exists(self.master):
				shutil.copy(self.master,self.infname)
			else:
				print 'could not find: %s'%(self.master)
				sys.exit()
		
		inf=open(self.infname)
		config=eval(inf.read())
		inf.close()
		return config

	def get_value(self,key):
		if self.config.has_key(key):
			return self.config[key]
		else:
			return None
			
	def update_config(self,d):
		#print 'CfgMgr: update_config\n',d
		for key in d.keys():
			self.config[key]=d[key]
		self.save_config()
		self.config=self.load_config()
	
	def set_config(self,d):
		#print 'CfgMgr: set_config\n',d
		self.config=d
		self.save_config()
		self.config=self.load_config()

	def save_config(self):
		#print 'CfgMgr: save_config'
		ouf=open(self.infname,'w')
		rval=format_dict(self.config,0)
		ouf.write(rval)
		ouf.close()
	






