"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Support         :www.asymptopia.org/forum

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2015 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import os,sys,string

DEBUG=False

class Environment:
	def __init__(self,appname):
		self.OS=None
		OS=sys.platform.lower()

		if DEBUG:print(OS)

		if OS.find('mac')>-1:OS='mac'
		elif OS.find('arwin')>-1:OS='mac'
		elif OS.find('win')>-1:OS='win'
		elif OS.find('lin')>-1:OS='lin'
		else:OS=None
		if(OS==None):sys.exit()

		if OS=='lin':
			import pygame
			for sitepkgdir in sys.path:
				if sitepkgdir[-13:]=='site-packages':break
			configdir=os.path.join('/','var','games',appname)#,os.path.basename(appname)
			fontdir=os.path.join('/','var','games',appname)#,os.path.basename(appname)

			if os.path.exists("/usr/share/games/stepintochinese"):
				sitepkgdir=os.path.join('/','usr','share','games','stepintochinese', 'lib')
				configdir=os.path.join('/','usr','share','games','stepintochinese')#,os.path.basename(appname)
				fontdir=os.path.join('/','usr','share','games','stepintochinese')#,os.path.basename(appname)

			homedir=os.getenv('HOME')

		elif OS=='win':
			import thread
			pf=os.getenv("PROGRAMFILES")
			sitepkgdir=os.path.join(pf,appname)
			configdir=os.path.join(sitepkgdir,appname)
			fontdir=os.path.join(sitepkgdir,appname)
			homedir=os.getenv('HOME')
			if not homedir:homedir=os.getenv('USERPROFILE')

		else:#Mac uses this to run from install directory
			sitepkgdir='.'
			configdir='.'
			fontdir='.'
			homedir=os.getenv('HOME')


		#If application hasn't been installed (via setup.py) then try to run from tgz directory:
		if os.path.exists("/usr/share/games/stepintochinese"):pass
		else:
			if os.path.exists(appname) and os.path.exists('stepintochinese.py'):#if yes, then probably want to be running w/o installing.
				sitepkgdir='.'
				fontdir='.'
				configdir='.'
				homedir=os.getenv('HOME')
				if not homedir:homedir=os.getenv('USERPROFILE')
			elif os.path.exists(os.path.join(sitepkgdir,appname,'sic.py')):pass
			elif os.path.exists(os.path.join(sitepkgdir,appname,'sic.py')) and OS=='win':pass
			else:
				sitepkgdir='.'
				fontdir='.'
				configdir='.'
				homedir=os.getenv('HOME')
				if not homedir:homedir=os.getenv('USERPROFILE')

		self.OS=OS
		self.sitepkgdir=sitepkgdir
		self.fontdir=fontdir
		self.configdir=configdir
		self.appname=appname
		self.homedir=homedir

		if DEBUG:
			print('configdir   =%s'%self.configdir)
			print('sitepkgdir  =%s'%self.sitepkgdir)
			print('appname     =%s'%self.appname)
			print('homedir     =%s'%self.homedir)
			print('fontdir	   =%s'%self.fontdir)
