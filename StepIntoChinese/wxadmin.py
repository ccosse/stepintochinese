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
import os,sys,string,time
import wx
from cfgctrl import *

DEBUG=0

class wxAdmin(wx.Dialog):
	
	def __init__(self,parent):
		
		self.cfgctrl=None
		self.lhp_gif=None
		self.splitter=None
		self.simulator=None
		
		self.parent		=parent
		self.env		=parent.env
		#self.configdir	=self.env.configdir
		self.sitepkgdir	=self.env.SITEPKGDIR
		self.homedir	=self.env.HOMEDIR
		self.global_config=self.parent.global_config
		
		wx.Dialog.__init__(
			self,None,wx.NewId(),
			self.global_config['APPNAME'],
			size=wx.Size(self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']),
			style=wx.RESIZE_BORDER|wx.CAPTION|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX
		)
	
	def reload_config(self):
		self.parent.reload_configs
		self.global_config=self.parent.global_config
		
	def setup(self):
		splitter = wx.SplitterWindow (self,wx.NewId(),style=wx.NO_3D)#|wxSP_3D
		splitter.SetMinimumPaneSize(self.global_config['SPLITTER_OFFSET']['value'])
		
		lhp=wx.Panel(splitter,wx.NewId())
		rhp=wx.Panel(splitter,wx.NewId())
		
		fbox=wx.BoxSizer(wx.HORIZONTAL)
		fbox.Add(splitter,1,wx.GROW)
		self.SetSizer(fbox)
		self.SetAutoLayout(True)
		####fbox.Fit(self)
		fbox.Layout()
		
		
		lhp.SetSize((self.global_config['SPLITTER_OFFSET']['value'],600))
		lhp.SetBackgroundColour((255,255,255))
		sidebar_fname=self.parent.global_config['IMAGE_ADMIN_SIDEBAR']['value']
		if DEBUG:print 'sidebar_fname=',sidebar_fname
		sidebar_fname=os.path.join(self.env.SITEPKGDIR,self.parent.global_config['IMAGE_ADMIN_SIDEBAR']['path'],sidebar_fname)
		if DEBUG:print 'sidebar_fname=',sidebar_fname
		lhp_gif=wx.Image(sidebar_fname,wx.BITMAP_TYPE_GIF).ConvertToBitmap()
		wx.StaticBitmap(lhp,wx.NewId(),lhp_gif,(0,0))
		self.lhp_gif=lhp_gif
		
		size=wx.Size(self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value'])
		self.SetSize(size);
		splitter.SplitVertically(lhp,rhp,lhp.GetSize()[0])
		splitter.SetSashPosition(lhp.GetSize()[0]);
		
		
		tabs=['Globals','Readme','Asymptopia','GPL']
		nb=wx.Notebook(rhp,wx.NewId(),style=wx.NB_TOP|wx.NB_FIXEDWIDTH)
		
		for idx in range(len(tabs)):
			cfgctrl=CfgCtrl(self,nb)
			nb.AddPage(cfgctrl,tabs[idx],0)
			cfgctrl.setup(tabs[idx])
				
		rhpbox=wx.BoxSizer(wx.VERTICAL);
		rhpbox.Add(nb,1,wx.EXPAND);
		rhp.SetSizer(rhpbox);
		rhp.SetAutoLayout(True);
		rhpbox.Fit(rhp);
		rhpbox.Layout();
		
