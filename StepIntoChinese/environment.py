#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
import os,sys,string
import wx

DEBUG=0

class Environment:
	def __init__(self,appname):

		OS=None
		SITEPKGDIR=None
		HOMEDIR=None
		
		OS=string.lower(sys.platform)

		if string.find(OS,'mac')>-1:OS='mac'
		elif string.find(OS,'arwin')>-1:OS='mac'
		elif string.find(OS,'win')>-1:OS='win'
		elif string.find(OS,'lin')>-1:OS='lin'
		else:OS=None
		if(OS==None):sys.exit()
		
		sp=wx.StandardPaths.Get()
		
		if OS=='lin':
			for dname in sys.path:
				if os.path.basename(dname)=='site-packages':
					SITEPKGDIR=dname
					break
			HOMEDIR=wx.StandardPaths.GetUserConfigDir(sp)
			
		elif OS=='win':
			import thread
			for dname in sys.path:
				if os.path.basename(dname)=='site-packages':
					SITEPKGDIR=dname
					break
			HOMEDIR=wx.StandardPaths.GetUserConfigDir(sp)
			
		else:#Mac uses this to run from install directory
			SITEPKGDIR='.'
			HOMEDIR=os.getenv('HOME')
			if HOMEDIR=='':HOMEDIR=os.getenv('HOMEPATH')
		
		#If application hasn't been installed (via setup.py) then try to run from tgz directory:
		if os.path.exists(appname) and os.path.exists('stepintochinese.py'):#if yes, then probably want to be running w/o installing.
			SITEPKGDIR='.'
			HOMEDIR=os.getenv('HOME')
			if not HOMEDIR:HOMEDIR=os.getenv('HOMEPATH')
			if not HOMEDIR:HOMEDIR=os.getenv('USERPROFILE')
			
		elif os.path.exists(os.path.join(SITEPKGDIR,appname,'stepintochinese.py')):pass
		elif os.path.exists(os.path.join(SITEPKGDIR,appname,'stepintochinese.py')) and OS=='win':pass
		else:
			SITEPKGDIR='.'
			HOMEDIR=os.getenv('HOME')
			if not HOMEDIR:HOMEDIR=os.getenv('HOMEPATH')
			if not HOMEDIR:HOMEDIR=os.getenv('USERPROFILE')
		
		self.OS=OS
		self.SITEPKGDIR=os.path.abspath(SITEPKGDIR)
		self.HOMEDIR=os.path.abspath(HOMEDIR)
		self.appname=appname

		if DEBUG:
			print 'SITEPKGDIR  =%s'%self.SITEPKGDIR
			print 'appname     =%s'%self.appname
			print 'HOMEDIR     =%s'%self.HOMEDIR
