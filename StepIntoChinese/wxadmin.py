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

import wx

try:import wx.html2 as webview
except:pass

import os,string,time
from .cfgctrl import *
from .cfgctrlobj import *
from .dict_formatter import *
DEBUG=False

class wxAdmin(wx.Dialog):

	def __init__(self,parent):
		self.parent=parent
		self.global_config=self.parent.global_config
		self.env		=parent.env
		self.global_config=self.parent.global_config
		self.SHOW_ALL=False
		self.cfgctrlobjs=[]

		wx.Dialog.__init__(
			self,None,wx.NewId(),
			self.global_config['APPNAME'],
			size=wx.Size(self.global_config['WIN_W']['value'],800),
			style=wx.RESIZE_BORDER|wx.CAPTION|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX
		)

	def reload_config(self):
		self.parent.reload_configs
		self.global_config=self.parent.global_config

	def setup(self):

		sty = wx.SP_LIVE_UPDATE
		splitter = wx.SplitterWindow (self,wx.NewId(),style=sty)#|wxSP_3D
		splitter.SetMinimumPaneSize(140)

		nb=wx.Notebook(splitter,wx.NewId(),style=wx.BK_DEFAULT)

		win = self.makeGlobalsPanel(nb)
		nb.AddPage(win, "Globals")

		win = self.makeEditorPanel(nb,"README")
		nb.AddPage(win, "ReadMe")

		#win = self.makeEditorPanel(nb,"INSTALL")
		#nb.AddPage(win, "Install")

		win = self.makeEditorPanel(nb,"LICENSE")
		nb.AddPage(win, "License")

		try:
			win = self.makeWebViewPanel(nb,"http://www.asymptopia.com")
			nb.AddPage(win, "Asymptopia")
		except:pass

		try:
			win = self.makeWebViewPanel(nb,"https://observablehq.com/@ccosse")
			nb.AddPage(win, "Observables")
		except:pass

		p2 = wx.Window(splitter, style=wx.BORDER_SUNKEN)
		p2.SetBackgroundColour("pink")
		sidebar_fname=self.parent.global_config['IMAGE_ADMIN_SIDEBAR']['value']
		sidebar_fname=os.path.join(self.env.sitepkgdir,self.parent.global_config['IMAGE_ADMIN_SIDEBAR']['path'],sidebar_fname)
		lhp_gif=wx.Image(sidebar_fname,wx.BITMAP_TYPE_GIF).ConvertToBitmap()
		wx.StaticBitmap(p2,wx.NewId(),lhp_gif)

		splitter.SetMinimumPaneSize(20)
		splitter.SplitVertically(nb, p2, 650)

	def makeWebViewPanel(self,parent,url):
		wv = webview.WebView.New(parent)
		wv.LoadURL(url)
		return wv

	def makeEditorPanel(self,parent,fname):
		p = wx.Panel(parent, -1)
		win=wx.TextCtrl(p,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
		p.win=win

		xid=wx.NewId()
		closeB=wx.Button(p,xid,"Close",(300,5),wx.DefaultSize)
		closeB.SetToolTip(wx.ToolTip('Close this window'))
		wx.EVT_BUTTON(p,xid,self.logoutCB)

		inf=open(os.path.join(self.env.sitepkgdir,self.global_config['APPNAME'],fname))
		gpl=inf.read()
		inf.close()
		win.WriteText(gpl)
		win.SetEditable(0)
		def OnCPSize(evt, win=win):
			#print 'OnCPSize'
			win.SetPosition((0,50))
			win.SetSize(evt.GetSize())
			#print evt.GetSize()

		p.Bind(wx.EVT_SIZE, OnCPSize)

		return p

	def makeGlobalsPanel(self,parent):
		p = wx.Panel(parent, -1)
		#p.SetBackgroundColour(wx.BLUE)
		win=wx.ScrolledWindow(p,wx.NewId(),wx.DefaultPosition,wx.DefaultSize,wx.VSCROLL)
		win.SetScrollRate(0,10)
		#win.SetBackgroundColour(wx.YELLOW)
		p.win=win

		xid=wx.NewId()
		saveB=wx.Button(win,xid,"Save",(270,5),wx.DefaultSize)
		saveB.SetToolTip(wx.ToolTip('Save these configuration options'))
		wx.EVT_BUTTON(win,xid,self.saveCB)

		xid=wx.NewId()
		closeB=wx.Button(win,xid,"Close",(350,5),wx.DefaultSize)
		closeB.SetToolTip(wx.ToolTip('Close this window'))
		wx.EVT_BUTTON(win,xid,self.logoutCB)

		obj_keys=list(self.global_config.keys())
		obj_keys.sort()
		ypos=40

		for idx in range(len(obj_keys)):
			obj_dict=self.global_config[obj_keys[idx]]
			if type(obj_dict).__name__ != 'dict':continue
			if obj_dict['showme']!= True and self.SHOW_ALL != True:continue
			if obj_dict['showme']<0:continue
			obj=CfgCtrlObj(win,obj_keys[idx],obj_dict,(0,ypos),(650,80))
			obj.SetBackgroundColour(wx.WHITE)
			self.cfgctrlobjs.append(obj)
			ypos+=80

		wx.ToolTip.Enable(True)
		wx.ToolTip.SetDelay(2000)

		def OnCPSize(evt, win=win):
			#print 'OnCPSize'
			win.SetPosition((0,0))
			win.SetSize(evt.GetSize())
			#print evt.GetSize()

		p.Bind(wx.EVT_SIZE, OnCPSize)

		return p

	def makeColorPanel(self, parent, color):
		p = wx.Panel(parent, -1)
		win = ColorPanel.ColoredPanel(p, color)
		p.win = win
		def OnCPSize(evt, win=win):
			win.SetPosition((0,0))
			win.SetSize(evt.GetSize())
		p.Bind(wx.EVT_SIZE, OnCPSize)
		return p


	def saveCB(self,e):

		for obj in self.cfgctrlobjs:
			obj.update()#widget.value -> obj.val['value']
			self.global_config[obj.key]=obj.obj_dict

		if 'letters' in self.global_config.keys():del self.global_config['letters']
		if 'distribution' in self.global_config.keys():del self.global_config['distribution']
		if 'scoring' in self.global_config.keys():del self.global_config['scoring']

		oufdir=os.getenv('HOME')
		if not oufdir:oufdir=os.getenv('USERPROFILE')

		oufname=os.path.join(oufdir,'.tms_config')
		ouf=open(oufname,'w')
		rval=format_dict(self.global_config,0)
		ouf.write(rval)
		ouf.close()

		#if DEBUG:print rval

		try:
			self.reload_config()
		except:# Exception,e:
			pass
			#print e

	def logoutCB(self,e):
		self.EndModal(0)
