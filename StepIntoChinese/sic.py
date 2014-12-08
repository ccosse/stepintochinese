#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
#from wxPython.wx import *
import wx
import pygame
from pygame.locals import *
from cp import *
from button import *
from random import *
from environment import *
from dict_formatter import *
from wxadmin import *
from cfgmgr import *

DEBUG=1

class StepIntoChineseApp(wx.App):
	
	def __init__(self,appdir):
		wx.App.__init__(self, 0)
		prog=StepIntoChinese(appdir)
		prog.run()

	def OnButton(self, evt):
		pass
		#self.on_exit()

class StepIntoChinese(ChineseParser):
	
	def __init__(self,appdir):
		
		ChineseParser.__init__(self)
		
		self.appdir=appdir
		self.env=Environment('StepIntoChinese')
		self.SITEPKGDIR=self.env.sitepkgdir
		self.HOMEDIR=self.env.homedir
		self.config_mgr=CfgMgr(self)
		
		self.W=None
		self.H=None
		self.bgImage=None
		self.ytop=0
		self.screen=None
		self.bkg=None
		
		self.myfont=None
		self.myfont_large=None
		self.myfont_medium=None
		self.myfont_small=None
		self.bigfont=None
		self.medfont=None
 		self.hudfont=None
 
		self.submission=None
		self.whichkeys=None
		self.last_direction=None
		self.search_direction=1
		self.ysearch=None
		self.side=0
		
		self.DMODE=1
		self.SMODE=2
		self.SHIFT=0
		self.KDOWN=0
		self.KUP=0
		self.KRIGHT=0
		self.KLEFT=0
		self.TDOWN=0
		self.SCREENSAVER=0
		self.AMFULLSCREEN=0

		#wx stuff:
		self.login_button=None
		self.loginbuttongroup=None
		self.loginbuttons=None
		self.login_button=None
		self.global_config=self.load_config()
		self.button_imgpaths={'login_button':os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Images','login_button.gif'),}
		self.admin=wxAdmin(self)
		self.admin.setup()

		
	def update_dependents_on_relative_dimensions(self):
		#ie adminbutton which is pygame.sprite.RenderPlain(Group..)
		if self.login_button!=None:
			self.login_button=Button(self.button_imgpaths['login_button'])
			self.loginbuttongroup=pygame.sprite.Group([self.login_button])
			self.loginbuttons=pygame.sprite.RenderPlain(self.loginbuttongroup)
			self.login_button.rect.center=(#NOTE: THIS IS *CENTER*
				self.global_config['WIN_W']['value']/2,
				self.global_config['WIN_H']['value']-self.login_button.get_height()+5
			)
		#set display mode
		if pygame.display.get_init():
			screen=pygame.display.set_mode((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
			self.screen=screen
		
			self.bkg=pygame.Surface(screen.get_size())
			self.bkg=self.bkg.convert()
			self.bkg.fill(self.global_config['COLOR_BG']['value'])

		if self.global_config['IMAGE_BG']['value']!='':
			try:
				self.bgImage=pygame.image.load(os.path.join(self.global_config['IMAGE_BG']['path'],self.global_config['IMAGE_BG']['value']))#os.path.join(self.sitepkgdir,self.global_config['APPNAME'],'Images','sunset01.jpg')
				self.bgImage=pygame.transform.scale(self.bgImage, (self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
			except Exception,e:
				self.bgImage=None

				
	def flip(self):
		pygame.display.flip()
		
	def progress_message(self,msglist):
		fg_hud=self.global_config['COLOR_WHITE']['value']
		bg_hud=self.global_config['COLOR_BG']['value']
		self.screen.fill(self.global_config['COLOR_BG']['value'])
		self.draw_credit(0)
		self.ytop=self.global_config['WIN_H']['value']/2-20
		for midx in range(len(msglist)):
			please_wait_surface=self.myfont.render(
				msglist[midx],1,
				fg_hud,
				bg_hud 
			)
			pws_w=please_wait_surface.get_size()[0]
			pws_h=please_wait_surface.get_size()[1]
			self.screen.blit(please_wait_surface,(self.global_config['WIN_W']['value']/2.-pws_w/2,self.ytop))
			self.ytop+=pws_h
			
		#Admin Button
		self.loginbuttons.draw(self.screen)

		self.flip()
		self.handle_events_during_load()
		
	def fitlines(self,thestring,splitchars,thefont,wmax):
		lines=[]
		surf=thefont.render(thestring,1,self.global_config['COLOR_BG']['value'])
		
		if surf.get_width()<=wmax:
			
			lines.append(thestring)
			return lines
			
		else:
			splitchar_idx=0
			maxoccurs=0
			for scidx in range(len(splitchars)):
				count=thestring.count(splitchars[scidx])
				if count>maxoccurs:
					splitchar_idx=scidx
					maxoccurs=count
				
			split_string=string.split(thestring,splitchars[splitchar_idx],1000)
			newstring=""
			error_count=0
			while len(split_string):
				
				chunk=split_string.pop(0)
				
				if splitchars[splitchar_idx]=='/':
					tmpstring="%s/%s"%(newstring,chunk)
				else:
					tmpstring="%s %s"%(newstring,chunk)
				
				surf=thefont.render(tmpstring,1,self.global_config['COLOR_BG']['value'])
				
				if surf.get_width()<=wmax:
					newstring=tmpstring
					if not len(split_string):lines.append(newstring)#ie if there's more,then try to fit it on
				elif error_count>10:
					newstring=tmpstring
					if not len(split_string):lines.append(newstring)#okay, we've tried that, now bail! (hack)
					error_count=0
				else:
					newstring=string.replace(newstring,'/ /','/')
					newstring=string.lstrip(newstring)
					lines.append(newstring)
					split_string.insert(0,chunk)#right here
					error_count+=1
					newstring=''
				
		return lines
	
		
	def get_word_div(self):
		
		#Get big Chinese chars w/corresponding pinyin in variable Red(freq) centered underneath each char
		
		target_string=''
		pinyin_string=''
		target_list=[]
		pinyin_list=[]
		pinyin_freqs=[]
		
		#Up here so can use for target_string in next section iff ['FLASHCARD_STYLE']['value']==2
		for lidx in range(len(self.dict[self.whichkeys[self.idx]]['romanization'])):
			pinyin_string="%s%s "%(pinyin_string,self.dict[self.whichkeys[self.idx]]['romanization'][lidx])
			pinyin_list.append(self.dict[self.whichkeys[self.idx]]['romanization'][lidx])
			pinyin_freqs.append(self.dict[self.whichkeys[self.idx]]['frequencies'][lidx])

		if self.DMODE==3 and self.global_config['FLASHCARD_STYLE']['value']==0:#traditional
			target_string=self.dict[self.whichkeys[self.idx]]['traditional']
			
		elif self.DMODE==3 and self.global_config['FLASHCARD_STYLE']['value']==1:#simplified
			target_string=self.dict[self.whichkeys[self.idx]]['simplified']

		elif self.DMODE==3 and self.global_config['FLASHCARD_STYLE']['value']==2 and self.side==0:#pinyin only
			target_string=pinyin_string
		elif self.DMODE==3 and self.global_config['FLASHCARD_STYLE']['value']==2 and self.side==1:#pinyin only
			target_string=self.dict[self.whichkeys[self.idx]]['traditional']

		elif self.DMODE==3 and self.global_config['FLASHCARD_STYLE']['value']==3 and self.side==0:#translation only
			target_string=self.dict[self.whichkeys[self.idx]]['translation']
		elif self.DMODE==3 and self.global_config['FLASHCARD_STYLE']['value']==3 and self.side==1:#translation only
			target_string=self.dict[self.whichkeys[self.idx]]['traditional']

		elif self.DMODE==2:target_string=self.dict[self.whichkeys[self.idx]]['simplified']
		elif self.DMODE==1:target_string=self.dict[self.whichkeys[self.idx]]['traditional']
		else:target_string=self.dict[self.whichkeys[self.idx]]['traditional']+u' '+self.dict[self.whichkeys[self.idx]]['simplified']
		
		
		for lidx in range(len(target_string)):
			if target_string[lidx]==' ' and lidx==len(target_string)-1:continue
			target_list.append(target_string[lidx])
		
		atmp=None
		if self.DMODE==3 and self.global_config['FLASHCARD_STYLE']['value']==2 and self.side==0:
			atmp=self.myfont.render(target_string,1,self.global_config['COLOR_BG']['value'])
		elif self.DMODE==3 and self.global_config['FLASHCARD_STYLE']['value']==3 and self.side==0:
			atmp=self.myfont.render(target_string,1,self.global_config['COLOR_BG']['value'])
		else:atmp=self.bigfont.render(target_string,1,self.global_config['COLOR_BG']['value'])
		
		btmp=self.myfont.render(pinyin_string,1,self.global_config['COLOR_BG']['value'])
		
		vspc=10
		ws=atmp.get_width()
		hs=atmp.get_height()+vspc+btmp.get_height()
		
		rsurf=pygame.Surface((ws,hs))
		tlcx=0
		tlcy=0
		centers=[]
		for tidx in range(len(target_list)):
			#green for translation:
			color=None
			font=None
			if self.DMODE==3 and self.global_config['FLASHCARD_STYLE']['value']==2 and self.side==0:
				color=self.global_config['COLOR_CHINESE']['value']
				font=self.myfont
			elif self.DMODE==3 and self.global_config['FLASHCARD_STYLE']['value']==3 and self.side==0:
				color=self.global_config['COLOR_TRANSLATION']['value']
				font=self.myfont
			else:
				color=self.global_config['COLOR_CHINESE']['value']
				font=self.bigfont
			
			csurf=font.render(target_list[tidx],1,color)
			
			rsurf.blit(csurf,(tlcx,tlcy))
			centers.append(tlcx+csurf.get_width()/2)
			tlcx+=csurf.get_width()
		
		if self.DMODE==3 and self.side==0:
			#rescale the surface, if necessary,so that it fits:
			if rsurf.get_width()>self.global_config['WIN_W']['value']:
				sf=float(self.global_config['WIN_W']['value']/float(rsurf.get_width()))
				new_w=int(rsurf.get_width()*sf)
				new_h=int(rsurf.get_height()*sf)
				rsurf=pygame.transform.scale(rsurf,(new_w,new_h))
			return rsurf
			
		tlcy=atmp.get_height()+vspc
		psurf=None
		for pidx in range(len(pinyin_list)):
			freq=pinyin_freqs[pidx]
			fcolor=self.get_freq_color(freq)#redder=more frequent
			if self.DMODE==0:psurf=self.myfont_medium.render('Traditional',1,fcolor)
			else:psurf=self.myfont.render(pinyin_list[pidx],1,fcolor)
			rsurf.blit(psurf,(centers[pidx]-psurf.get_width()/2,tlcy))
			#NEED:Traditional/Simplified labels instead of pinyin for DMODE==0
			
		if self.DMODE==0:
			freq=pinyin_freqs[pidx]
			fcolor=(100+min(freq,155),100-min(freq,100),100-min(freq,100))#redder=more frequent
			psurf=self.myfont_medium.render('Simplified',1,fcolor)
			rsurf.blit(psurf,(centers[2]-psurf.get_width()/2,tlcy))
		
		#rescale the surface, if necessary,so that it fits:
		if rsurf.get_width()>self.global_config['WIN_W']['value']:
			sf=float(self.global_config['WIN_W']['value']/float(rsurf.get_width()))
			new_w=int(rsurf.get_width()*sf)
			new_h=int(rsurf.get_height()*sf)
			rsurf=pygame.transform.scale(rsurf,(new_w,new_h))

		return rsurf
	
	def get_freq_color(self,freq):
		return (100+min(freq,155),100-min(freq,100),100-min(freq,100))
	
	def get_defn_div(self,dy_avail):
		
		#this returns surface of middle section/strip of application -- with the pinyin(s), unicode(s), freq(s) & definition(s)
		
		bigfont=self.bigfont
		medfont=self.medfont
		myfont=myfont_large=self.myfont_large
		myfont_medium=self.myfont_medium
		myfont_small=self.myfont_small
		myfont_xsmall=self.myfont_xsmall
		myfonts=[myfont_large,myfont_medium,myfont_small,myfont_xsmall]
		
		for fidx in range(len(myfonts)):
			
			ytop=0#local variable
			
			hudfont=self.hudfont
			
			
			defn_surf=pygame.Surface((800,600))#oversized initially, cram to tlcxy, then chop
			defn_surf.fill(self.global_config['COLOR_BG']['value'])
			
			TranslationLabel='Translation    '#located here b/c (usually) determines aligned lhs of defn surfs
			translabeltmpsurf=myfont.render(TranslationLabel,1,self.global_config['COLOR_BG']['value'])
			LJUST=self.global_config['LMARGIN']['value']+translabeltmpsurf.get_width()
			#find widest pinyin prefix to left-justify pinyin defns:
			for lidx in range(len(self.dict[self.whichkeys[self.idx]]['romanization'])):
				line="%c"%(self.dict[self.whichkeys[self.idx]]['traditional'][lidx])
				csurf=medfont.render(line,1,self.global_config['COLOR_FG']['value'])
				pinyin=self.dict[self.whichkeys[self.idx]]['romanization'][lidx]
				freq=self.dict[self.whichkeys[self.idx]]['frequencies'][lidx]
				pinyin=" %s (%4s)(%03d):"%(pinyin,'FFFF',freq)
				pinyin_surf=myfont.render(pinyin,1,self.global_config['COLOR_FG']['value'])
				wtot=self.global_config['LMARGIN']['value']+csurf.get_width()+pinyin_surf.get_width()
				if wtot>LJUST:LJUST=wtot
				
			for lidx in range(len(self.dict[self.whichkeys[self.idx]]['romanization'])):
				
				ytop_last=ytop
				line=''
				if 0:pass
				elif self.DMODE==0:line="%c"%(self.dict[self.whichkeys[self.idx]]['traditional'][lidx])
				elif self.DMODE==1:line="%c"%(self.dict[self.whichkeys[self.idx]]['traditional'][lidx])
				elif self.DMODE==2:line="%c"%(self.dict[self.whichkeys[self.idx]]['simplified'][lidx])
				elif self.DMODE==3:line="%c"%(self.dict[self.whichkeys[self.idx]]['traditional'][lidx])
				
				csurf=medfont.render(line,1,self.global_config['COLOR_CSURF']['value'])
				defn_surf.blit(csurf,(self.global_config['LMARGIN']['value'],ytop))
				
				pinyin_color=self.global_config['COLOR_FG']['value']
				pinyin=None
				pinyin_translation=None
				
				pinyin=self.dict[self.whichkeys[self.idx]]['romanization'][lidx]
				pinyin=" %s"%(pinyin)
				pinyin_translation="%s"%(self.dict[self.dict[self.whichkeys[self.idx]]['traditional'][lidx]]['translation'])
				pinyin_surface=None
				
				
				ustr=self.whichkeys[self.idx][lidx]
				y=`ustr`
				freq=self.dict[self.whichkeys[self.idx]]['frequencies'][lidx]
				freq_str="(%4s)(%03d):"%(y[-5:-1],freq)
				
				freq_surf=myfont.render(freq_str,1,self.global_config['COLOR_FG']['value'])
				
				if self.SMODE==1:
					pinyin_surf=myfont.render(pinyin,1,self.global_config['COLOR_BG']['value'])
					split_search_string=string.split(self.submission,' ')
					CONDITION=False
					for ssidx in range(len(split_search_string)):
						if len(split_search_string[ssidx])==0:continue
						substr=split_search_string[ssidx]
						if string.find(pinyin,substr)>-1:
							CONDITION=True
							lidx=string.find(pinyin,substr)
							if lidx<0:lidx=len(pinyin)
							ridx=lidx+len(substr)
							if ridx>len(pinyin):ridx=lidx
							pre_surf=myfont.render(pinyin[0:lidx],1,self.global_config['COLOR_BG']['value'])
							
							pinyin_surf.blit(pre_surf,(0,0))
							
							if lidx<len(pinyin):
								hi_surf=myfont.render(substr,1,self.global_config['COLOR_HILIGHT']['value'])
								pinyin_surf.blit(hi_surf,(0+pre_surf.get_width(),0))
								post_surf=myfont.render(pinyin[ridx:len(pinyin)],1,self.global_config['COLOR_FG']['value'])
								pinyin_surf.blit(post_surf,(0+pre_surf.get_width()+hi_surf.get_width(),0))
								
					if not CONDITION:
						pinyin_surf=myfont.render(pinyin,1,self.global_config['COLOR_FG']['value'])		
				else:#not searching either translations, so no hilighting of this field possible
					pinyin_surf=myfont.render(pinyin,1,self.global_config['COLOR_FG']['value'])
				
				
				defn_surf.blit(pinyin_surf,(self.global_config['LMARGIN']['value']+csurf.get_width(),ytop))
				
				
				#Search for unicode and hilight if found:
				if self.SMODE==3:
					if string.find(freq_str,self.submission)>-1:	
						parensurf=myfont.render("(",1,self.global_config['COLOR_FG']['value'])
						hi_surf=myfont.render(self.submission,1,self.global_config['COLOR_HILIGHT']['value'])
						tlcy=ytop
						freq_surf.blit(hi_surf,(parensurf.get_width(),0))
						
						

				#ALWAYS NEED RED-SCALE FREQ ACCORDING TO SAME FORMULA IN GET_CHAR_DIV()
				#RIGHT JUSTIFIED, RHS EDGES ALIGNED @x=LJUST
				parensurf=myfont.render("(FFFF)(",1,self.global_config['COLOR_FG']['value'])
				
				freq_color=self.get_freq_color(freq)
				freqstr="%03d"%(freq)
				hi_surf=myfont.render(freqstr,1,freq_color)

				tlcy=ytop
				freq_surf.blit(hi_surf,(parensurf.get_width(),0))
				
				tlcx=LJUST-freq_surf.get_width()
				defn_surf.blit(freq_surf,(tlcx,tlcy))
				
				lines=self.fitlines(pinyin_translation,[' ','/'],myfonts[fidx],self.global_config['WIN_W']['value']-LJUST)
				
				if self.SMODE==2:
					for tridx in range(len(lines)):
						translation=lines[tridx]
						lidx=string.find(translation,self.submission)
						if lidx<0:lidx=len(translation)
						ridx=lidx+len(self.submission)
						if ridx>len(translation):ridx=lidx
						#handle 2 possible cases separately:
						line="%s"%(translation[0:lidx])
						pre_surf=myfonts[fidx].render(line,1,self.global_config['COLOR_FG']['value'])
						defn_surf.blit(pre_surf,(LJUST,ytop))
						
						if lidx<len(translation):
							#print 'lidx=',lidx
							#hilighted substring
							line="%s"%(translation[lidx:ridx])
							hi_surf=myfonts[fidx].render(line,1,self.global_config['COLOR_HILIGHT']['value'])
							defn_surf.blit(hi_surf,(LJUST+pre_surf.get_width(),ytop))
							
							#default colored remainder of string
							line="%s"%(translation[ridx:len(translation)])
							post_surf=myfonts[fidx].render(line,1,self.global_config['COLOR_FG']['value'])
							defn_surf.blit(post_surf,(LJUST+pre_surf.get_width()+hi_surf.get_width(),ytop))
						
						ytop+=pre_surf.get_height()+5
					
				else:#pinyin keys or unicode
					for tridx in range(len(lines)):
						line="%s"%(lines[tridx])
						surf=myfonts[fidx].render(line,1,self.global_config['COLOR_FG']['value'])
						defn_surf.blit(surf,(LJUST,ytop))
						ytop+=surf.get_height()+5
						
	
			###############################################################
			#TRANSLATION LABEL:
			###############################################################
			surf=myfont.render(TranslationLabel,1,self.global_config['COLOR_WHITE']['value'])
			defn_surf.blit(surf,(self.global_config['LMARGIN']['value'],ytop))
			
			surf=myfont.render(":",1,self.global_config['COLOR_WHITE']['value'])
			defn_surf.blit(surf,(LJUST-surf.get_width(),ytop))
			
			###############################################################
			#TRANSLATION LINE:
			###############################################################
			translation=self.dict[self.whichkeys[self.idx]]['translation']
			lines=self.fitlines(translation,[' ','/'],myfonts[fidx],self.global_config['WIN_W']['value']-LJUST)
			
			if self.SMODE==2:
				for tridx in range(len(lines)):
					#print 'tridx=',tridx
					translation=lines[tridx]
					lidx=string.find(translation,self.submission)
					if lidx<0:lidx=len(translation)
					ridx=lidx+len(self.submission)
					if ridx>len(translation):ridx=lidx
					
					line="%s"%(translation[0:lidx])
					pre_surf=myfonts[fidx].render(line,1,self.global_config['COLOR_TRANSLATION']['value'])
					defn_surf.blit(pre_surf,(LJUST,ytop))
				
					if lidx<len(translation):
						#print 'lidx=',lidx
						#hilighted substring
						line="%s"%(translation[lidx:ridx])
						hi_surf=myfonts[fidx].render(line,1,self.global_config['COLOR_HILIGHT']['value'])
						defn_surf.blit(hi_surf,(LJUST+pre_surf.get_width(),ytop))
						
						#default colored remainder of string
						line="%s"%(translation[ridx:len(translation)])
						post_surf=myfonts[fidx].render(line,1,self.global_config['COLOR_TRANSLATION']['value'])
						defn_surf.blit(post_surf,(LJUST+pre_surf.get_width()+hi_surf.get_width(),ytop))
						
					ytop+=pre_surf.get_height()+10
					
				if ytop_last+csurf.get_height()>ytop:
					ytop=ytop_last+csurf.get_height()+5#2-3 rows of small font might not have added-up to vspace nec for next row
			
			else:
				for tridx in range(len(lines)):
					line="%s"%(lines[tridx])
					surf=myfonts[fidx].render(line,1,self.global_config['COLOR_TRANSLATION']['value'])
					defn_surf.blit(surf,(LJUST,ytop))
					ytop+=surf.get_height()+5
			
			if ytop<=dy_avail:return defn_surf
			
		return defn_surf		
		
	
	def load_config(self):
		
		if DEBUG:print 'stepintochinese.load_config'
		
		#configdir	=self.env.configdir
		#if DEBUG:print configdir
		
		homedir=os.getenv('HOME')
		if not homedir:homedir=os.getenv('USERPROFILE')
		infname=os.path.join(homedir,'.stepintochinese_config')
		
		if not os.path.exists(infname):
			master_fname=os.path.join('.','.stepintochinese_config_master')
			if self.env.OS=='win':
				cmd="copy %s \"%s\""%(master_fname,os.path.join(homedir,'.stepintochinese_config'))
				os.system(cmd)
			else:
				cmd="cp %s %s"%(master_fname,os.path.join(homedir,'.stepintochinese_config'))
				os.system(cmd)
		
		fname_flashcards=os.path.join(self.env.homedir,'.stepintochinese_flashcards')
		if not os.path.exists(fname_flashcards):
			ouf=open(fname_flashcards,'w')
			ouf.write('[]')
			ouf.close()
		
			
		inf=open(infname)
		content=inf.read()
		
		content=string.strip(content)
		
		config=eval(content)
		inf.close()
		return config
	
	def reload_configs(self):
		self.global_config=self.load_config()
		self.update_dependents_on_relative_dimensions()
	
	def run(self):
		
		inf=open(os.path.join(self.env.homedir,'.stepintochinese_flashcards'))
		self.flashkeys=eval(inf.read())
		inf.close()
		
		if DEBUG:print 'self.flashkeys=',self.flashkeys
		
		for fkidx in range(len(self.flashkeys)):#convert from ascii_desc -> unicode
			try:
				if DEBUG:print 'converting ascii -> unicode',fkidx
				if DEBUG:print fkidx,'/',len(self.flashkeys),self.flashkeys[fkidx]
				sfk=string.split(self.flashkeys[fkidx],'/',100000)
				
				ufk=u''
				for sfkidx in range(len(sfk)):	
					if sfk[sfkidx]=='':continue
					ufk+=unicodedata.lookup(sfk[sfkidx])
				self.flashkeys[fkidx]=ufk#converted back to unicode
			except Exception,e:print e
		
		
		pygame.init()
		fontdir=os.path.join(self.env.sitepkgdir,'StepIntoChinese','Font')
		self.bigfont=pygame.font.Font(os.path.join(fontdir,'sunglobe.ttf'),130)
		self.medfont=pygame.font.Font(os.path.join(fontdir,'sunglobe.ttf'),32)
		
		self.myfont_large=pygame.font.Font(os.path.join(fontdir,'aqua_pfont.ttf'),26)
		self.myfont_medium=pygame.font.Font(os.path.join(fontdir,'aqua_pfont.ttf'),22)
		self.myfont_small=pygame.font.Font(os.path.join(fontdir,'aqua_pfont.ttf'),18)
		self.myfont_xsmall=pygame.font.Font(os.path.join(fontdir,'aqua_pfont.ttf'),14)
		self.myfont=self.myfont_large
		
		self.myfont=pygame.font.Font(os.path.join(fontdir,'aqua_pfont.ttf'),26)
		self.hudfont=pygame.font.Font(os.path.join(fontdir,'aqua_pfont.ttf'),14)
		#self.hudfont=pygame.font.SysFont('Latin',18,0,0)
		
		bigfont=self.bigfont
		medfont=self.medfont
		myfont=self.myfont
		hudfont=self.hudfont
		
		screen=pygame.display.set_mode((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
		self.screen=screen
		self.SCREENSAVER=self.global_config['SCREENSAVER_ON_AT_START']['value']
		
		
		pygame.display.set_caption("Step Into Chinese")
		self.bkg=pygame.Surface(screen.get_size())
		self.bkg=self.bkg.convert()
		self.bkg.fill(self.global_config['COLOR_BG']['value'])
		
		self.login_button=Button(self.button_imgpaths['login_button'])
		self.login_button.rect.center=(#NOTE: THIS IS *CENTER*
			self.global_config['WIN_W']['value']/2,
			self.global_config['WIN_H']['value']-self.login_button.get_height()+5
		)

		self.loginbuttongroup=pygame.sprite.Group([self.login_button])
		self.loginbuttons=pygame.sprite.RenderPlain(self.loginbuttongroup)

		pygame.event.set_blocked(MOUSEMOTION)
		
		parser.setFeature(feature_namespaces, 0)
		parser.setContentHandler(self)
		infname=fontdir=os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'sic.xml')
		inf=open(infname)
		parser.parse(inf)
		inf.close()
		self.post_process()
		
		self.idx=12368#8995#12368(hello)#6267(large)
		self.submission='hello'
		submission_surface=None
	
		self.whichkeys=None
		self.last_direction=+1
		
		
		if self.global_config['IMAGE_BG']['value']!='':
			try:
				self.bgImage=pygame.image.load(os.path.join(self.global_config['IMAGE_BG']['path'],self.global_config['IMAGE_BG']['value']))#os.path.join(self.sitepkgdir,self.global_config['APPNAME'],'Images','sunset01.jpg')
				self.bgImage=pygame.transform.scale(self.bgImage, (self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
			except Exception,e:
				self.bgImage=None
				
		
		#THE MAIN LOOP:
		while True:
			
			try:
				###############################################################
				#BACKGROUND COLOR and IMG:
				###############################################################
				screen.blit(self.bkg,(0,0))
				if self.bgImage:self.screen.blit(self.bgImage,(0,0))
				self.ytop=self.global_config['LMARGIN']['value']
				
				
				###############################################################
				#DECIDE WHAT TO DO BASED ON DMODE:
				###############################################################
				if self.DMODE==3 and self.side==0:
					self.whichkeys=self.flashkeys
					surf=self.get_word_div()
					surf.set_colorkey(self.global_config['COLOR_BG']['value'])
					screen.blit(surf,(self.global_config['WIN_W']['value']/2-surf.get_width()/2,self.global_config['WIN_H']['value']/2-surf.get_height()/2))
					self.flip()
					self.wait_mouse()
					continue
					
				elif self.DMODE==3:self.whichkeys=self.flashkeys
				elif self.DMODE==1 or self.DMODE==2:self.whichkeys=self.dictkeys
				else:self.whichkeys=self.distkeys
	
				
				###############################################################
				#BIG CHINESE CHARS w/COLOR_SCALED PINYIN(freq) UNDERNEATHE
				###############################################################
				surf=self.get_word_div()
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				screen.blit(surf,(self.global_config['WIN_W']['value']/2-surf.get_width()/2,self.ytop))
				self.ytop+=surf.get_height()+10
				
				
				###############################################################
				#HILIGHTED ROMANIZATION:
				###############################################################
				dy_defn=self.global_config['WIN_H']['value']-130-self.ytop
				surf=self.get_defn_div(dy_defn)
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				screen.blit(surf,(self.global_config['WIN_W']['value']/2-surf.get_width()/2,self.ytop))
				self.ytop+=surf.get_height()+10
				
				###############################################################
				#SUPPRESS SEARCH/POSITION/HUD INFOS IN FLASHCARD MODE
				###############################################################
				if self.DMODE==3:
					pygame.display.flip()
					self.wait_mouse()
					continue
				
				###############################################################
				#SEARCH SUBMISSION
				###############################################################
				prefix="Search[SMODE=%d]: "%(self.SMODE)
				prefix_surface=myfont.render(prefix,1,self.global_config['COLOR_FG']['value'],self.global_config['COLOR_BG']['value'])
				prefix_surface.set_colorkey(self.global_config['COLOR_BG']['value'])
				screen.blit(prefix_surface,(self.global_config['LMARGIN']['value'],self.global_config['WIN_H']['value']-130))
			
				submission_surface=myfont.render(self.submission,1,self.global_config['COLOR_HILIGHT']['value'],self.global_config['COLOR_BG']['value'])
				submission_surface.set_colorkey(self.global_config['COLOR_BG']['value'])
				screen.blit(submission_surface,(self.global_config['LMARGIN']['value']+prefix_surface.get_width(),self.global_config['WIN_H']['value']-130))
				
				###############################################################
				#SMODE STATUS HEADER:F1
				###############################################################
				msg=[
					'SearchMode (F1): Search Pinyin Translations',#This not used b/c redundant w/(DMODE=0,SMODE=2)
					'SearchMode (F1): Search Pinyin Romanizations',
					'SearchMode (F1): Search English Translations',
					'SearchMode (F1): Search Unicode Keys',
				]
				line="%s"%(msg[self.SMODE])
				surf=hudfont.render(line,1,self.global_config['COLOR_SMODE']['value'])
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				screen.blit(surf,(self.global_config['LMARGIN']['value'],self.global_config['WIN_H']['value']-surf.get_height()-35))
				self.ytop+=surf.get_height()+10
				

				###############################################################
				#SCREENSAVER STATUS: (RHS)
				###############################################################
				#align left edges of status messages on lower right:
				longest_surf=hudfont.render('Flashcard Style (F4): Translation',1,self.global_config['COLOR_SMODE']['value'])
				lhs=self.global_config['WIN_W']['value']-self.global_config['LMARGIN']['value']-longest_surf.get_width()-5
				
				msg=[
					'Screensaver Mode (F3): OFF',
					'Screensaver Mode (F3): ON',
				]
				line="%s"%(msg[self.SCREENSAVER])
				surf=hudfont.render(line,1,self.global_config['COLOR_SMODE']['value'])
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				screen.blit(surf,(lhs,self.global_config['WIN_H']['value']-surf.get_height()-35))
				

				###############################################################
				#DMODE STATUS HEADER:F2 (LHS)
				###############################################################
				msg=[
					'DisplayMode(F2): Singles',
					'DisplayMode(F2): Traditional',
					'DisplayMode(F2): Simplified',
					'DisplayMode(F2): Flashcards',
				]
				line="%s"%(msg[self.DMODE])
				surf=hudfont.render(line,1,self.global_config['COLOR_DMODE']['value'])
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				screen.blit(surf,(self.global_config['LMARGIN']['value'],self.global_config['WIN_H']['value']-surf.get_height()-15))
				#self.ytop+=surf.get_height()+10
				
				
				###############################################################
				#FLASHCARD DISPLAY MODE: F4 (RHS)
				###############################################################
				msg=[
					'Flashcard Style (F4): Traditional',
					'Flashcard Style (F4): Simplified',
					'Flashcard Style (F4): Pinyin',
					'Flashcard Style (F4): Translation',
				]
				line="%s"%(msg[self.global_config['FLASHCARD_STYLE']['value']])
				surf=hudfont.render(line,1,self.global_config['COLOR_SMODE']['value'])
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				screen.blit(surf,(lhs,self.global_config['WIN_H']['value']-surf.get_height()-15))
				self.ytop+=surf.get_height()+10
				
				
				###############################################################
				#SCALE/RULER ACROSS BOTTOM:
				###############################################################
				pygame.draw.line(screen,self.global_config['COLOR_CHINESE']['value'],(self.global_config['LMARGIN']['value'],self.global_config['WIN_H']['value']-60),(self.global_config['WIN_W']['value']-2*self.global_config['LMARGIN']['value'],self.global_config['WIN_H']['value']-60),1)#main horizontal rule
				
				line="%04d/%d "%(self.idx,len(self.whichkeys))
				surf=myfont.render(line,1,self.global_config['COLOR_FG']['value'])
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				
				percentage_through_resource=float(self.idx)/float(len(self.whichkeys)-1)
				
				radius=3
				xpos=self.global_config['LMARGIN']['value']+int(percentage_through_resource*float(self.global_config['WIN_W']['value']-20))-radius/2
				ypos=self.global_config['WIN_H']['value']-60-radius/2+1
				pos=(xpos,ypos)
				pygame.draw.circle(screen,self.global_config['COLOR_HILIGHT']['value'], pos, radius, 0)#NEED:change to rectangular vbar
				
				tlcx=self.global_config['LMARGIN']['value']+int(percentage_through_resource*float(self.global_config['WIN_W']['value']-20))-surf.get_width()/2
				if tlcx<self.global_config['LMARGIN']['value']:tlcx=self.global_config['LMARGIN']['value']
				elif tlcx+surf.get_width()>self.global_config['WIN_W']['value']-10:tlcx=self.global_config['WIN_W']['value']-10-surf.get_width()
				yfracprog=self.global_config['WIN_H']['value']-60-surf.get_height()
				screen.blit(surf,(tlcx,yfracprog))
				
				#Admin Button
				self.loginbuttons.draw(self.screen)
				
				#Display Flip
				pygame.display.flip()
				
				
				###################################################################
				#SCREENSAVER CUT-OFF
				###################################################################
				BYPASS_WAIT_MOUSE=0
				if self.SCREENSAVER:
					BYPASS_WAIT_MOUSE=1
					last_idx=self.idx
					tstart=time.time()
					tend=tstart+self.global_config['TSLEEP_SCREENSAVER']['value']
					dt=tend-tstart
					if self.submission!='':
						#print 'start',`self.submission`,self.DMODE,self.search_direction
						if 0:pass
						#elif self.SMODE==0:self.idx=self.search_pinyin_translations(self.submission,self.DMODE,self.search_direction)
						elif self.SMODE==1:self.idx=self.search_pinyin(self.submission,self.DMODE,self.search_direction)
						elif self.SMODE==2:self.idx=self.search_english_translations(self.submission,self.DMODE,self.search_direction)
						elif self.SMODE==3:self.idx=self.search_unicode_keys(self.submission,self.DMODE,self.search_direction)
						#print 'back'
					else:
						self.idx=int(random()*len(self.whichkeys))
					while time.time()<tend:
						time.sleep(1)
						for e in pygame.event.get([KEYDOWN,MOUSEBUTTONDOWN]):
							if DEBUG:print `e`
							self.SCREENSAVER=0
							self.idx=last_idx#So it feels like you stopped it (else jumps once more)
							tend=time.time()
				
							
				###################################################################
				#WAIT FOR EVENT
				###################################################################
				if not BYPASS_WAIT_MOUSE:self.wait_mouse()
				
				#good idea?
				pygame.event.pump()
					
				
			except Exception,ex:
				if DEBUG:print `ex`
				self.idx+=self.last_direction
				if self.idx>len(self.whichkeys)-1:self.idx=0
				elif self.idx<0:self.idx=len(self.whichkeys)-1
				


	def handle_events_during_load(self):
		
		for event in pygame.event.get(QUIT):
			self.on_exit()
		
		elist=pygame.event.get()
		for e in elist:
			
			if e.type==KEYDOWN:
				
				if pygame.key.name(e.key)=='escape':self.on_exit()
				elif e.type == QUIT:self.on_exit()
				elif e.key==K_F9:self.go_help()
				elif e.key==K_F10:self.go_credit(1)
				elif e.key==K_F11:self.go_screenshot()
				elif e.key==K_7:
					if self.AMFULLSCREEN==True:
						try:
							s=pygame.display.set_mode((0,0))
							self.AMFULLSCREEN=False
						except Exception,e:print e
					else:
						try:
							s=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
							self.AMFULLSCREEN=True
						except Exception,e:print e
					
				#elif e.key==K_F12:self.AMFULLSCREEN=pygame.display.toggle_fullscreen()
				elif e.key==K_LSHIFT:self.SHIFT=1
				elif e.key==K_RSHIFT:self.SHIFT=1
			
			elif e.type==KEYUP:
				if e.key==K_LSHIFT:self.SHIFT=0
				elif e.key==K_RSHIFT:self.SHIFT=0
			
			elif e.type==MOUSEBUTTONDOWN:	
				if self.login_button.rect.collidepoint(pygame.mouse.get_pos()):
					self.AMFULLSCREEN=0
					self.screen=pygame.display.set_mode((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
					time.sleep(1)
					rval=self.admin.ShowModal()

					
			
	def wait_mouse(self):
		
		for event in pygame.event.get(QUIT):self.on_exit()
			
		e=None
		FLAG=0
		
		if self.TDOWN and time.time()-self.TDOWN>1:
			#Give chance to ffw/rew by 1,dx
			if DEBUG:print 'TDOWN'
			if self.KDOWN:
					if DEBUG:print 'KDOWN'
					self.idx-=1;self.last_direction=-1
					if self.idx<0:self.idx=len(self.whichkeys)-1#wraps
					for e in pygame.event.get([KEYUP]):
						if e.key==K_DOWN:
							self.KLEFT=self.KRIGHT=self.KUP=self.KDOWN=self.TDOWN=0
						return
				
			if self.KUP:
					if DEBUG:print 'KUP'
					self.idx+=1;self.last_direction=+1
					if self.idx>len(self.whichkeys)-1:self.idx=1
					for e in pygame.event.get([KEYUP]):
						if e.key==K_UP:
							self.KLEFT=self.KRIGHT=self.KUP=self.KDOWN=self.TDOWN=0
						return
			
			if self.KRIGHT:
					if DEBUG:print 'KRIGHT'
					self.idx+=self.global_config['DX_FFW_REW']['value'];self.last_direction=+1
					if self.idx>len(self.whichkeys)-1:self.idx=1
					for e in pygame.event.get([KEYUP]):
						if e.key==K_RIGHT:
							self.KLEFT=self.KRIGHT=self.KUP=self.KDOWN=self.TDOWN=0
						return
			
			if self.KLEFT:
					if DEBUG:print 'KLEFT'
					self.idx-=self.global_config['DX_FFW_REW']['value'];self.last_direction=-1
					if self.idx<0:self.idx+=len(self.whichkeys)
					for e in pygame.event.get([KEYUP]):
						if e.key==K_LEFT:
							self.KLEFT=self.KRIGHT=self.KUP=self.KDOWN=self.TDOWN=0
						return
			FLAG=1#If didn't return, then we're waiting, so only wait below for event if one is pending
			
		if FLAG or self.TDOWN:
			if pygame.event.peek([KEYDOWN,KEYUP]):
				e=pygame.event.wait()
			else:
				return
				
		else:
			e=pygame.event.wait()
		
		if e.type == MOUSEBUTTONDOWN:
		
			if 0:pass
			elif e.button==4:
				self.idx+=1;self.last_direction=1
			elif e.button==5:
				self.idx-=1;self.last_direction=-1
			
			elif self.login_button.rect.collidepoint(pygame.mouse.get_pos()):
				self.AMFULLSCREEN=0
				self.screen=pygame.display.set_mode((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
				rval=self.admin.ShowModal()
					
			if self.idx<0:self.idx=len(self.whichkeys)-1#wraps
			if self.idx>len(self.whichkeys)-1:self.idx=1
			
		
		elif e.type==KEYUP:
			self.KDOWN=self.TDOWN=self.KUP=self.KDOWN=self.KRIGHT=self.KLEFT=0
			if e.key==K_LSHIFT or e.key==K_RSHIFT:self.SHIFT=0
				
		elif e.type==KEYDOWN:
			
			if e.key==K_LSHIFT or e.key==K_RSHIFT:self.SHIFT=1
			elif e.key==K_LALT or e.key==K_RALT:pass
			elif e.key==K_LCTRL or e.key==K_RCTRL:pass
			elif e.key == K_ESCAPE:self.on_exit()
			
			elif e.key==K_HOME:self.side=0#Front of flashcard
			elif e.key==K_END:self.side=1#Back of flashcard
			elif e.key==K_DELETE:self.delete_flashcard()#can only delete from DMODE=3
			
			
			elif e.key==K_F1:
				self.SMODE+=1
				if self.SMODE>3:self.SMODE=1

			elif e.key==K_F2:
				self.DMODE+=1
				if self.DMODE==3 and len(self.flashkeys)>0:
					self.idx=0
					self.whichkeys=self.flashkeys
				elif self.DMODE>=3:#skip if no flashkeys yet
					self.DMODE=0
					
			elif e.key==K_F3:
				self.DMODE=1#Hardcoding Traditional @screensaver
				self.SCREENSAVER=1
				if DEBUG:print 'dnSCREENSAVER=',self.SCREENSAVER
			
			#NOTE:No need to save globals here; this is for dynamic; set default @admin
			elif e.key==K_F4:
				self.global_config['FLASHCARD_STYLE']['value']+=1
				if self.global_config['FLASHCARD_STYLE']['value']>3:
					self.global_config['FLASHCARD_STYLE']['value']=0

			elif e.key==K_F5:self.add_flashcard()
			elif e.key==K_F6:self.delete_flashcard()

			elif e.key==K_F9:self.go_help()
			elif e.key==K_F10:self.go_credit(1)
			elif e.key==K_F11:self.go_screenshot()
			elif e.key==K_F7:
				if self.AMFULLSCREEN==True:
					try:
						s=pygame.display.set_mode((0,0))
						self.AMFULLSCREEN=False
					except Exception,e:print e
				else:
					try:
						s=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
						self.AMFULLSCREEN=True
					except Exception,e:print e
				
			elif e.key==K_F12:
				self.AMFULLSCREEN=pygame.display.toggle_fullscreen()
				if DEBUG:print 'self.AMFULLSCREEN=',self.AMFULLSCREEN

			elif pygame.key.name(e.key)=='return':
				if self.DMODE==3:return
				ridx=self.idx
				if self.SHIFT==1:self.search_direction=-1
				else:self.search_direction=+1
				
				if 0:pass
				elif self.SMODE==3:ridx=self.search_unicode_keys(self.submission,self.DMODE,self.search_direction)#dummy:unicode
				elif self.SMODE==2:ridx=self.search_english_translations(self.submission,self.DMODE,self.search_direction)#collective translation
				elif self.SMODE==1:ridx=self.search_pinyin(self.submission,self.DMODE,self.search_direction)#dummy:pinyin_translation
				elif self.SMODE==0:ridx=self.search_pinyin_translations(self.submission,self.DMODE,self.search_direction)#pinyin
				
				if ridx:self.idx=ridx
				
			elif e.key==K_UP:
				self.KUP=1
				self.TDOWN=time.time()
				self.side=0
				self.idx+=1;self.last_direction=+1
				if self.idx>len(self.whichkeys)-1:self.idx=0
			
			elif e.key==K_DOWN:
				self.KDOWN=1
				self.TDOWN=time.time()
				self.side=0
				self.idx-=1;self.last_direction=-1
				if self.idx<0:self.idx=len(self.whichkeys)-1#wraps
			
			elif e.key==K_RIGHT:
				if self.DMODE==3:return
				self.KRIGHT=1
				self.TDOWN=time.time()
				self.side=0
				self.idx=self.idx+500
				if self.idx>len(self.whichkeys):self.idx-=len(self.whichkeys)
				self.current_search_index=self.idx
			
			elif e.key==K_LEFT:
				if self.DMODE==3:return
				self.KLEFT=1
				self.TDOWN=time.time()
				self.side=0
				self.idx-=500
				if self.idx<0:self.idx+=len(self.whichkeys)
				self.current_search_index=self.idx
			
			elif pygame.key.name(e.key)==('backspace'):
				self.submission=self.submission[:-1]
			
			elif pygame.key.name(e.key)==('space'):
				self.submission+=' '

			else:
				if DEBUG:print e
				newchar=pygame.key.name(e.key)
				if len(newchar)>1:return
				if self.SHIFT:newchar=string.upper(newchar)
				self.submission=self.submission+newchar
				
	def draw_credit(self,mode):
		
		linesize=self.myfont.size('text to determine font size')
		
		msgs=[
			u'',
			u'Step Into Chinese v0.12',
			u'December 7, 2014',
			u'',
			u'Asymptopia Software | Software@theLimit',
			u'www.asymptopia.org',
			u'',
			u'Author:Charles B. Coss'+u'\xe9',
			u'Contact:ccosse@asymptopia.org', 
		]
		
		y0=self.global_config['WIN_H']['value']/4-len(msgs)/2.*linesize[1]
		fg_hud=None
		bg_hud=None
		
		for msg_idx in range(len(msgs)):
			
			if msg_idx>=3:
				font=self.myfont_small
				fg_hud=self.global_config['COLOR_TRANSLATION']['value']
			else:
				font=self.myfont_large
				fg_hud=self.global_config['COLOR_HILIGHT']['value']
			
			bg_hud=self.global_config['COLOR_BG']['value']
			credit_surface=font.render(
				msgs[msg_idx],1,
				fg_hud,
				bg_hud 
			)	
			cs_w=credit_surface.get_size()[0]
			cs_h=credit_surface.get_size()[1]
			self.screen.blit(credit_surface,(self.global_config['WIN_W']['value']/2.-cs_w/2.,y0+msg_idx*linesize[1]))
			
			if msg_idx>4 and mode==0:break
				
	
	def go_credit(self,mode):		
		self.screen.fill(self.global_config['COLOR_BG']['value'])
		self.draw_credit(mode)		
		self.flip()
		while 1:
			breakout=0
			for event in pygame.event.get([KEYUP]):
				if event.type == KEYUP:breakout=1
				self.KDOWN=0
				self.TDOWN=0
			if breakout:break
		
	def go_help(self):
		self.screen.fill(self.global_config['COLOR_BG']['value'])
		infname=os.path.join(self.env.sitepkgdir,self.global_config['APPNAME'],'Images','StepIntoChinese-Keyboard.png')
		self.keymap_surface=pygame.image.load(infname)#os.path.join(self.sitepkgdir,self.global_config['APPNAME'],'Images','sunset01.jpg')
		self.keymap_surface=pygame.transform.scale(self.keymap_surface, (self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
		self.screen.blit(self.keymap_surface,(0,0))
		
		self.flip()
		while 1:
			breakout=0
			for event in pygame.event.get([KEYUP]):
				if event.type == KEYUP:breakout=1
				self.KDOWN=0
				self.TDOWN=0
			if breakout:break

		
	def go_screenshot(self):
		display_surface=pygame.display.get_surface()
		tstamp=self.mktstamp()
		oufname="StepIntoChinese_%s.bmp"%(tstamp)
		try:
			homedir=os.getenv('HOME')
			if not homedir:homedir=os.getenv('USERPROFILE')
			oufname=os.path.join(homedir,oufname)
		except Exception,e:
			if DEBUG:print `e`
		
		pygame.image.save(display_surface,oufname)
	
	def mktstamp(self):
		#tstamp which increases monotonically with time
		t=time.localtime()
		YYYY="%d"%t[0]
		MM="%02d"%t[1]
		DD="%02d"%t[2]
		hh="%02d"%t[3]
		mm="%02d"%t[4]
		ss="%02d"%t[5]
		tstamp="%s%s%s%s%s%s"%(YYYY,MM,DD,hh,mm,ss)
		return tstamp
	
	def save_flashkeys(self):
		
		if DEBUG:print 'converting unicode -> ascii for save'
		ouflist=[]
		for kidx in range(len(self.flashkeys)):
			strkey=unicodedata.name(self.flashkeys[kidx][0])
			for fkidx in range(1,len(self.flashkeys[kidx])):
				strkey+='/'
				strkey+=unicodedata.name(self.flashkeys[kidx][fkidx])
			
			ouflist.append(strkey)
		
		oufname=os.path.join(self.env.homedir,'.stepintochinese_flashcards')
		ouf=open(oufname,'w')
		ouf.write(`ouflist`)
		ouf.close()
		
	def add_flashcard(self):
		if self.DMODE==3:return
		if DEBUG:print 'add flashcard'
		key=self.whichkeys[self.idx]
		if self.flashkeys.count(self.whichkeys[self.idx])>0:return
		self.flashkeys.append(key)#1,2,3...N chars long
		self.save_flashkeys()
	
	def delete_flashcard(self):
		if self.DMODE!=3:return
		if DEBUG:print 'delete flashcard'
		self.flashkeys.remove(self.flashkeys[self.idx])
		self.save_flashkeys()
		if len(self.flashkeys)<1:
			self.DMODE=2
			return
		

	def on_exit(self):
		lines=[
			'',
			'**********************************************************',
			'*                                                        *',
			'*   You are using version 0.12 from December 7, 2014      *',
			'*                                                        *',
			'*                http://www.asymptopia.org               *',
			'*                                                        *',
			'*         AsymptopiaSoftware | Software@theLimit         *',
			'*                                                        *',
			'**********************************************************',
			'',
		]

		for line in lines:print line
		pygame.quit()
		sys.exit()

parser = make_parser()

if __name__=='__main__':
	x=StepIntoChinese()
	x.run()
