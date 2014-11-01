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
import wx,os
from environment import *

DEBUG=0

class CfgCtrlObj(wx.Panel):
	def __init__(self,cp,key,obj_dict):
		if DEBUG:print key
		if DEBUG:print obj_dict
		self.key=key
		self.obj_dict=obj_dict
		self.label=None
		self.env=Environment("StepIntoChinese")#only need this for paths to Actor images ...
		wx.Panel.__init__(self,cp,wx.NewId(),wx.DefaultPosition,wx.DefaultSize,style=wx.FULL_REPAINT_ON_RESIZE)
		
		sbox=wx.StaticBox(self,-1,key,wx.DefaultPosition,wx.DefaultSize);
		self.sbsizer=wx.StaticBoxSizer(sbox,wx.HORIZONTAL);
		sizer=wx.BoxSizer(wx.HORIZONTAL)
		
		widget_width=150;
		widget_height=35;
		wsize=wx.Size(widget_width,widget_height);
		self.label_size=wx.Size(20,widget_height);
		self.button_size=wx.Size(widget_width,widget_height);
		
		sizer.Add(self.sbsizer,1,wx.GROW,1);
		
		wxPushBStr="wx.PushB"
		wxSliderStr="wx.Slider"
		wxCheckBoxStr="wx.CheckBox"
		wxComboBoxStr="wx.ComboBox"
		wxColourDialogStr="wx.ColourDialog"
		wxSpinCtrlStr="wx.SpinCtrl"
		wxTextCtrlStr="wx.TextCtrl"
		wxFileDialogStr="wx.FileDialog"
		
		defaultBID=wx.NewId()
		defaultB=wx.Button(self,defaultBID,"Default",wx.DefaultPosition,self.button_size)
		self.defaultB=defaultB#for bgcolor on ColorSelect
		wx.EVT_BUTTON(defaultB,defaultBID,self.DefaultCB)
		
		
		if False:pass
		elif obj_dict['wtype']==wxSliderStr:self.SetupSlider()
		elif obj_dict['wtype']==wxCheckBoxStr:self.SetupCheckBox()
		elif obj_dict['wtype']==wxColourDialogStr:self.SetupColourDialog()
		elif obj_dict['wtype']==wxPushBStr:self.SetupPushB()
		elif obj_dict['wtype']==wxComboBoxStr:self.SetupComboBox()
		elif obj_dict['wtype']==wxSpinCtrlStr:self.SetupSpinCtrl()
		elif obj_dict['wtype']==wxFileDialogStr:self.SetupFileDialog()
		
		default_buttons_sizer=wx.BoxSizer(wx.VERTICAL)
		default_buttons_sizer.Add(defaultB,2,wx.EXPAND)
		self.sbsizer.Add(default_buttons_sizer,0)#,wx.GROW
		
		self.SetSizer(sizer)
		self.SetAutoLayout(True)
		self.Layout()
		self.Refresh()
		
		tooltip=wx.ToolTip(self.obj_dict['tooltip'])
		self.SetToolTip(tooltip)
		if DEBUG:print self.GetToolTip().GetTip()
		
		
	def SetupSlider(self):
		self.widget=wx.Slider(
			self,
			wx.NewId(),
			int(self.obj_dict['value']*self.obj_dict['divisor']),
			int(self.obj_dict['min']),
			int(self.obj_dict['max']),
			style=self.obj_dict['style'],
			size=self.button_size
		)
		
		self.sbsizer.Add(self.widget)

		sliderID=wx.NewId()
		div=self.obj_dict['divisor']
		if div==1.:label_str="%.0f"%(self.obj_dict['value'])
		if div==10.:label_str="%.1f"%(self.obj_dict['value'])
		if div==100.:label_str="%.2f"%(self.obj_dict['value'])
		if div==1000.:label_str="%.3f"%(self.obj_dict['value'])
		if div==10000.:label_str="%.4f"%(self.obj_dict['value'])
		
		self.label=wx.StaticText(self,sliderID,label_str,size=self.button_size)
		self.sbsizer.Add(self.label)
		
		#wx.EVT_BUTTON(self.defaultB,self.defaultBID,self.defaultCB)
		wx.EVT_SCROLL(self.widget,self.SliderCB)
		
	def SetupColourDialog(self):
		colordata=wx.ColourData()
		colordata.SetChooseFull(True)
		colordata.SetColour(wx.Colour(self.obj_dict['value'][0],self.obj_dict['value'][1],self.obj_dict['value'][2]))
		self.widget=wx.ColourDialog(self,colordata)
		#self.widget.GetColourData().SetColour(wx.Colour(self.obj_dict['value'][0],self.obj_dict['value'][1],self.obj_dict['value'][2]))
		#print self.widget.GetColourData().GetColour(),wx.Colour(self.obj_dict['value'][0],self.obj_dict['value'][1],self.obj_dict['value'][2])
		
		showColourDialogBID=wx.NewId()
		self.showColourDialogB=wx.Button(self,showColourDialogBID,"ShowDialog",size=self.button_size)
		self.showColourDialogB.SetBackgroundColour(wx.Colour(self.obj_dict['value'][0],self.obj_dict['value'][1],self.obj_dict['value'][2]))
		self.sbsizer.Add(self.showColourDialogB)
		wx.EVT_BUTTON(self.showColourDialogB,showColourDialogBID,self.ShowColourDialogCB)
		
		label_str=''
		self.label=wx.StaticText(self,wx.NewId(),label_str,size=self.button_size)
		self.label.SetLabel(`self.obj_dict['value']`)
		self.sbsizer.Add(self.label)

		self.defaultB.SetBackgroundColour(self.obj_dict['default'])
	
	def SetupPushB(self):
		pass
		
	def SetupComboBox(self):
		cbID=wx.NewId()
		self.widget=wx.ComboBox(self,cbID,size=self.button_size,choices=[])
		for idx in range(len(self.obj_dict['default'])):
			self.widget.Append(self.obj_dict['default'][idx])
		self.widget.SetValue(self.obj_dict['value'])
		self.sbsizer.Add(self.widget)
		wx.EVT_COMBOBOX(self,cbID,self.ComboCB)
		
		if self.obj_dict['icon']:
			#in this version, if icon, then actor.
			fname=os.path.abspath(os.path.join(self.env.sitepkgdir,self.env.appname,'Actors',self.obj_dict['value'],'icon.gif'))
			gif=wx.Image(fname,wx.BITMAP_TYPE_GIF).ConvertToBitmap()
			self.bmp=wx.StaticBitmap(self,-1,gif)
			self.sbsizer.Add(self.bmp)
		else:
			self.label=wx.StaticText(self,wx.NewId(),'',size=self.button_size)
			self.sbsizer.Add(self.label)

	def SetupSpinCtrl(self):
			SpinCtrlID=wx.NewId()
			self.widget=wx.SpinCtrl(self,SpinCtrlID,size=self.button_size)
			self.widget.SetRange(self.obj_dict['min'],self.obj_dict['max'])
			self.widget.SetValue(int(self.obj_dict['value']))
			self.sbsizer.Add(self.widget)
			wx.EVT_SPINCTRL(self.widget,SpinCtrlID,self.SpinCtrlCB)
			
			label_str=''
			self.label=wx.StaticText(self,wx.NewId(),label_str,size=self.button_size)
			self.label.SetLabel(`self.obj_dict['value']`)
			self.sbsizer.Add(self.label)

	
	def SetupCheckBox(self):
		CheckBoxID=wx.NewId()
		self.widget=wx.CheckBox(self,CheckBoxID,"",size=self.button_size)
		self.widget.SetValue(int(self.obj_dict['value']))
		self.sbsizer.Add(self.widget)
		wx.EVT_CHECKBOX(self.widget,CheckBoxID,self.CheckBoxCB)
		label_str=''
		self.label=wx.StaticText(self,wx.NewId(),label_str,size=self.button_size)
		self.label.SetLabel(`self.obj_dict['value']`)
		self.sbsizer.Add(self.label)
		self.CheckBoxCB(None)#to set the label after label exists

	def SetupFileDialog(self):
		FileDialogID=wx.NewId()
		self.widget=wx.FileDialog(
			self,
			message="Choose file",
			#defaultDir=self.obj_dict['path'],
		)
		"""
		if os.path.exists(os.path.join(self.env.sitepkgdir,self.env.appname,self.obj_dict['path'],self.obj_dict['value'])):
			#print self.key,'1',os.path.join(self.env.sitepkgdir,self.env.appname,self.obj_dict['path'],self.obj_dict['value'])
			self.widget.SetPath(os.path.join(self.env.sitepkgdir,self.env.appname,self.obj_dict['path']))
			self.widget.SetFilename(self.obj_dict['value'])
		elif os.path.exists(os.path.join(self.env.configdir,self.obj_dict['path'])):
			#print self.key,'2',os.path.join(self.env.sitepkgdir,self.env.appname,self.obj_dict['path'],self.obj_dict['value'])
			self.widget.SetPath(os.path.join(self.env.configdir,self.obj_dict['path']))
			self.widget.SetFilename(self.obj_dict['value'])
		else:
			#print self.key,'3',os.path.join(self.env.sitepkgdir,self.env.appname,self.obj_dict['path'],self.obj_dict['value'])
			self.widget.SetPath('./')
			self.widget.SetFilename(self.obj_dict['value'])
		"""	
		fdID=wx.NewId()
		self.fdB=wx.Button(self,fdID,"ShowDialog",size=self.button_size)
		self.sbsizer.Add(self.fdB)
		wx.EVT_BUTTON(self.fdB,fdID,self.FileDialogCB)
		
		label_str=''
		self.label=wx.StaticText(self,wx.NewId(),label_str,size=self.button_size)
		self.label.SetLabel(self.obj_dict['value'])
		self.sbsizer.Add(self.label)
	
	def SpinCtrlCB(self,evt):
		value_str="%02d"%(self.widget.GetValue())
		self.label.SetLabel(value_str)

	def SliderCB(self,evt):
		if DEBUG:print 'SliderCB: ',self.widget.GetValue()
		div=self.obj_dict['divisor']
		if div==1.:label_str="%.0f"%(self.widget.GetValue()/self.obj_dict['divisor'])
		if div==10.:label_str="%.1f"%(self.widget.GetValue()/self.obj_dict['divisor'])
		if div==100.:label_str="%.2f"%(self.widget.GetValue()/self.obj_dict['divisor'])
		if div==1000.:label_str="%.3f"%(self.widget.GetValue()/self.obj_dict['divisor'])
		if div==10000.:label_str="%.4f"%(self.widget.GetValue()/self.obj_dict['divisor'])
		self.label.SetLabel(label_str)

	def CheckBoxCB(self,e):
		if self.widget.GetValue():value_str="On"
		else:value_str="Off"
		self.label.SetLabel(value_str)
		
	def ShowColourDialogCB(self,e):
		if self.widget.ShowModal()==wx.ID_OK:pass
		else:return
		self.label.SetLabel(`self.obj_dict['value']`)		
		self.showColourDialogB.SetBackgroundColour(self.widget.GetColourData().GetColour().Get())

	def FileDialogCB(self,e):
		if self.widget.ShowModal()==wx.ID_OK:
			path=self.widget.GetPaths()[0]
			fpath=os.path.join(str(os.path.dirname(path)),str(os.path.basename(path)))
			if not os.path.exists(fpath):return
			self.obj_dict['path']=str(os.path.dirname(path))
			self.obj_dict['value']=str(os.path.basename(path))
			self.label.SetLabel(self.obj_dict['value'])
	
	
	def ComboCB(self,e):
		newval=self.widget.GetValue()
		if DEBUG:print 'ComboCB:',newval
		if self.obj_dict['icon']:
			fname=os.path.abspath(os.path.join(self.env.sitepkgdir,self.env.appname,'Actors',newval,'icon.gif'))
			self.bmp.SetBitmap(wx.Image(fname,wx.BITMAP_TYPE_GIF).ConvertToBitmap())
		
		
	def DefaultCB(self,e):
		
		self.Layout()
		
		if False:pass
		elif self.obj_dict['wtype']=='wx.ColourDialog':
			self.obj_dict['value']=self.obj_dict['default']
			self.label.SetLabel(`self.obj_dict['value']`)
			
			c=wx.Colour(self.obj_dict['default'][0],self.obj_dict['default'][1],self.obj_dict['default'][2]);
			#self.widget.GetColourData().SetColour(c);
			#self.widget.GetColourData().SetColour(self.obj_dict['value'])#seems 2B broken!
			colordata=wx.ColourData()
			colordata.SetChooseFull(True)
			colordata.SetColour(c)
			self.widget=wx.ColourDialog(self,colordata)
		
			self.showColourDialogB.SetBackgroundColour(self.obj_dict['value'])
			#Set value of widget, b/c widget is what gets queried @ SaveCB
			#print dir(self.widget)
			#print dir(self.widget.GetColourData())
		
		elif self.obj_dict['wtype']=='wx.CheckBox':
			self.widget.SetValue(int(self.obj_dict['default']))
			self.CheckBoxCB(None)
			
		elif self.obj_dict['wtype']=='wx.FileDialog':
			self.obj_dict['value']=self.obj_dict['default']
			self.label.SetLabel(self.obj_dict['default'])
			
			if os.path.exists(os.path.join(self.obj_dict['path'],self.obj_dict['default'])):#don't use '' for path! 
				self.obj_dict['path']=self.obj_dict['path']
				self.obj_dict['value']=self.obj_dict['default']
				
			
		elif self.obj_dict['wtype']=='wx.ComboBox':
			self.widget.SetValue(self.obj_dict['value'])
			self.ComboCB(None)
			
		elif self.obj_dict['wtype']=='wx.TextCtrl':
			self.widget.SetValue(self.obj_dict['default'])
			
		elif self.obj_dict['wtype']=='wx.Slider':
			self.widget.SetValue(int(self.obj_dict['default']*self.obj_dict['divisor']))
			self.SliderCB(None)
			
		elif self.obj_dict['wtype']=='wx.ImageDialog':
			self.obj_dict['value']=self.obj_dict['default']
			self.label.SetLabel(self.obj_dict['value'])

		elif self.obj_dict['wtype']=='wx.SpinCtrl':
			self.widget.SetValue(int(self.obj_dict['default']))
			self.SpinCtrlCB(None)
		
		
	def update(self):
		if self.obj_dict['wtype']=='wx.ComboBox':
			self.obj_dict['value']=str(self.widget.GetValue())
			
		elif self.obj_dict['wtype']=='wx.TextCtrl':
			self.obj_dict['value']=str(self.widget.GetValue())
			
		elif self.obj_dict['wtype']=='wx.ImageDialog':
			#self.val['value']=os.path.basename(self.widget.GetFile())
			if DEBUG:print 'value=',self.obj_dict['value'],self.label.GetLabel()
			
		elif self.obj_dict['wtype']=='wx.FontDialog':
			if DEBUG:print 'update wx.FontDialog'
			data=wx.FontData()
			data.EnableEffects(True)
			data.SetColour(wx.BLACK)
			#self.val['value']=data.GetChosenFont().GetFamily()
			#print data.GetChosenFont().GetFaceName()
			#self.label.SetLabel(data.GetChosenFont().GetFaceName())
			
		elif self.obj_dict['wtype']=='wx.FileDialog':
			if DEBUG:print 'wx.FileDialog update'
			try:
				if DEBUG:print '0 path=',self.obj_dict['path']#,self.label.GetLabel()
				if DEBUG:print '0 value=',self.obj_dict['value']#,self.label.GetLabel()
				if os.path.exists(self.widget.GetPath()):#don't use '' for path! 
					self.obj_dict['path']=str(os.path.dirname(self.widget.GetPath()))
					self.obj_dict['value']=str(os.path.basename(self.widget.GetPath()))
					if DEBUG:print '1 path=',self.obj_dict['path']#,self.label.GetLabel()
					if DEBUG:print '1 value=',self.obj_dict['value']#,self.label.GetLabel()
			except Exception,e:
				if DEBUG:print 'Line 368 cfgctrlobj.py: ',e
				if DEBUG:print dir(self.widget)
				if DEBUG:print self.widget.GetPath()#returns str
				if DEBUG:print self.widget.GetPaths()#returns unicode list
				if DEBUG:print self.widget.GetFilename()#returns string
				if DEBUG:print self.widget.GetFilenames()#returns unicode list
				
			
		elif self.obj_dict['wtype']=='wx.SpinCtrl':
			self.obj_dict['value']=int(self.widget.GetValue())#was float
			if DEBUG:print 'value=',self.obj_dict['value'],self.label.GetLabel()

		elif self.obj_dict['wtype']=='wx.CheckBox':
			self.obj_dict['value']=int(self.widget.GetValue())
			if DEBUG:print 'value=',self.obj_dict['value'],self.label.GetLabel()

		elif self.obj_dict['wtype']=='wx.Slider':
			self.obj_dict['value']=float(self.widget.GetValue())/self.obj_dict['divisor']#was float
			if DEBUG:print 'value=',self.obj_dict['value'],self.label.GetLabel()

		elif self.obj_dict['wtype']=='wx.ColourDialog':
			#LEAVE OFF: @default need to SetColourData -- need refer to wx API...TBC.
			data=self.widget.GetColourData()
			#print data,dir(data)
			#print data.GetColour(),data.GetColour().Get()
			#print type(data.GetColour().Get())
			t=data.GetColour().Get()
			self.obj_dict['value']=(t[0],t[1],t[2])
			#print t[0],t[1],t[2]
			self.label.SetLabel(`self.obj_dict['value']`)
		
		"""
		elif self.obj_dict['wtype']=='wx.ColourDialog':
			#LEAVE OFF: @default need to SetColourData -- need refer to wx API...TBC.
			data=self.widget.GetColourData()
			self.obj_dict['value']=data.GetColour().Get()
			self.label.SetLabel(`self.obj_dict['value']`)
		"""
