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
import wx
from .cfgctrlobj import *
from .dict_formatter import *

DEBUG=0

class CfgCtrl(wx.Panel):
	def __init__(self,admin,nb):
		self.sizer=None
		self.cp=None
		self.cpsizer=None
		self.name=None
		self.cfgctrlobjs=[]
		self.SHOW_ALL=False
		self.admin=admin
		self.global_config=admin.global_config
		wx.Panel.__init__(self,nb,wx.NewId(),wx.DefaultPosition,wx.DefaultSize,style=wx.FULL_REPAINT_ON_RESIZE)

	def setup(self,name):
		self.name=name
		button_height=self.global_config['CONFIG_WIDGET_H']['value']
		if self.admin.env.OS=='win':button_height=20
		if self.admin.env.OS=='win':button_height=20
		button_size=wx.Size(100,button_height)

		toolbar=wx.ToolBar(self,wx.NewId(),style=wx.TB_HORIZONTAL)
		self.sizer=wx.BoxSizer(wx.VERTICAL);
		self.sizer.Add(toolbar,0,wx.EXPAND);

		xpos=0
		if name=='Globals':
			#SAVE BUTTON
			xid=wx.NewId()
			saveB=wx.Button(toolbar,xid,"Save",size=button_size,pos=wx.Point(xpos,0))
			toolbar.AddControl(saveB)
			saveB.SetToolTip(wx.ToolTip('Save these configuration options'))
			wx.EVT_BUTTON(toolbar,xid,self.saveCB)
			xpos+=100

			#LOGOUT BUTTON
			xid=wx.NewId()
			logoutB=wx.Button(toolbar,xid,"Hide",size=button_size,pos=wx.Point(xpos,0))
			logoutB.SetToolTip(wx.ToolTip('Hide the Administrator Control Panel.'))
			toolbar.AddControl(logoutB)
			wx.EVT_BUTTON(toolbar,xid,self.logoutCB)
			xpos+=100

			#SHOW_ALL TOGGLE
			xid=wx.NewId()
			showallB=wx.CheckBox(toolbar,xid,"ShowAll",size=button_size,pos=wx.Point(xpos,0))
			showallB.SetValue(False)
			showallB.SetToolTip(wx.ToolTip('Show all configurable parameters, including those hidden by default'))
			toolbar.AddControl(showallB)
			wx.EVT_CHECKBOX(toolbar,xid,self.showallCB)

			self.load()

		elif self.name=='Readme':self.reload('Readme')
		elif self.name=='GPL':self.reload('GPL')
		elif self.name=='Asymptopia':self.reload('Asymptopia')

		self.SetSizer(self.sizer)
		self.SetAutoLayout(True)
		self.Layout()
		#panel.get_installed()

	def reload(self,target):
		if False:pass
		elif target=='Readme':
			editor=wx.TextCtrl(self,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
			inf=open(os.path.join(self.admin.env.SITEPKGDIR,self.global_config['APPNAME'],'README'))
			gpl=inf.read()
			inf.close()
			if DEBUG:print(dir(editor))
			editor.WriteText(gpl)
			editor.SetEditable(0)
			self.cp=editor
			self.cp.SetSizer(self.sizer)
			self.sizer.Add(self.cp,1,wx.EXPAND,1)

		elif target=='GPL':
			editor=wx.TextCtrl(self,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
			inf=open(os.path.join(self.admin.env.SITEPKGDIR,self.global_config['APPNAME'],'LICENSE'))
			gpl=inf.read()
			inf.close()
			if DEBUG:print(dir(editor))
			editor.WriteText(gpl)
			editor.SetEditable(0)
			self.cp=editor
			self.cp.SetSizer(self.sizer)
			self.sizer.Add(self.cp,1,wx.EXPAND,1)


		elif target=='Asymptopia':
			editor=wx.TextCtrl(self,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
			inf=open(os.path.join(self.admin.env.SITEPKGDIR,self.global_config['APPNAME'],'ASYMPTOPIA'))
			gpl=inf.read()
			inf.close()
			if DEBUG:print(dir(editor))
			editor.WriteText(gpl)
			editor.SetEditable(0)
			self.cp=editor
			self.cp.SetSizer(self.sizer)
			self.sizer.Add(self.cp,1,wx.EXPAND,1)


	def recreate_cp(self):

		self.cfgctrlobjs=[]

		if self.cp:
			self.sizer.Detach(self.cp)
			del self.cp
			self.cp=None

		self.cp=wx.ScrolledWindow(self,-1,wx.DefaultPosition,wx.DefaultSize,wx.VSCROLL)
		self.cp.SetBackgroundColour(wx.Colour(0,100,100))
		self.cp.SetScrollRate(0,10)
		self.cpsizer=wx.BoxSizer(wx.VERTICAL)
		self.cp.SetSizer(self.cpsizer)
		self.cpsizer.Fit(self.cp)
		self.cp.SetAutoLayout(True)
		self.cp.Layout()
		self.cp.Refresh()
		self.sizer.Add(self.cp,2,wx.GROW)

	def load(self):
		self.recreate_cp()
		obj_keys=self.global_config.keys()
		obj_keys.sort()
		for idx in range(len(obj_keys)):
			obj_dict=self.global_config[obj_keys[idx]]
			if type(obj_dict).__name__ != 'dict':continue
			if obj_dict['showme']!= True and self.SHOW_ALL != True:continue
			if obj_dict['showme']<0:continue
			obj=CfgCtrlObj(self.cp,obj_keys[idx],obj_dict)
			self.cpsizer.Add(obj,0,wx.EXPAND)#WRONG ARG FORMAT .. needs wx.Size()
			self.cfgctrlobjs.append(obj);

		self.Layout()
		wx.ToolTip.Enable(True)
		wx.ToolTip.SetDelay(2000)

	def saveCB(self,e):

		for obj in self.cfgctrlobjs:
			obj.update()#widget.value -> obj.val['value']
			self.global_config[obj.key]=obj.obj_dict

		if 'letters' in self.global_config.keys():del self.global_config['letters']
		if 'distribution' in self.global_config.keys():del self.global_config['distribution']
		if 'scoring' in self.global_config.keys():del self.global_config['scoring']

		oufdir=os.getenv('HOME')
		if not oufdir:oufdir=os.getenv('USERPROFILE')

		oufname=os.path.join(oufdir,'.stepintochinese_config')
		ouf=open(oufname,'w')
		rval=format_dict(self.global_config,0)
		ouf.write(rval)
		ouf.close()

		if DEBUG:print(rval)

		try:
			self.reload_config()
		except:# Exception,e:
			print(sys.exc_info())



	def reload_config(self):
		if DEBUG:print('CfgCtrl.reload_config')
		self.admin.reload_config()
		self.global_config=self.admin.global_config

	def logoutCB(self,e):
		self.admin.EndModal(0)

	def showallCB(self,e):
		if self.SHOW_ALL==False:
			self.SHOW_ALL=True
		else:
			self.SHOW_ALL=False
		self.load()
