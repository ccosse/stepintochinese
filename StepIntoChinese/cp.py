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
import xml,sys,os,string,unicodedata,time,math
from xml.sax import make_parser
from xml.sax import saxutils
from xml.sax.handler import feature_namespaces

DEBUG=False

class XDXFParser(xml.sax.ContentHandler):
	def __init__(self):
		self.inKey=False
		self.in_arContent=False
		self.current_key=''
		self.content=''

	def error(self, exception):
		if DEBUG:print(exception)

	def normalize_whitespace(self,text):
		"Remove redundant whitespace from a string"
		return ' '.join(text.split())

	def handle_events_durning_load(self):
		print('override me')

	def progress_message(self,msglist):
		print('override me')

class ChineseParser(XDXFParser):

	def __init__(self):
		XDXFParser.__init__(self)
		self.ar_count=0
		self.k_count=0

		self.splitkey=None
		self.romanization=None
		self.dictkeys=None
		self.distkeys=None
		self.flashkeys=[]
		self.article=None
		self.dict={}
		self.dist={}
		self.dlist=[]
		self.current_search_index=0
		self.max_freq=0

	def startElement(self,name,attrs):
		if name=='ar':
			self.ar_count+=1
			self.in_arContent=True
		elif name=='k':
			self.k_count+=1
			self.inKey=True
			self.romanization=None

	def characters(self,ch):
		if self.inKey:
			self.splitkey=ch.split(u' ',1)

		elif self.in_arContent:
			try:self.article+=ch
			except:pass

	def endElement(self,name):
		if name=='ar':
			self.in_arContent=False

			#Now store the entry:
			try:

				ch=self.normalize_whitespace(self.article)
				if not len(ch):return

				lidx=ch.index('[')
				ridx=ch.index(']')
				self.romanization=ch[lidx+1:ridx]
				split_romanization=self.romanization.split(u' ',199)
				self.translation=ch[ridx+1:]

				cjktraditional=[]
				cjksimplified=[]
				for cidx in range(len(self.splitkey[0])):
					cjktraditional.append(unicodedata.name(self.splitkey[0][cidx]))
					cjksimplified.append(unicodedata.name(self.splitkey[1][cidx]))

				#print self.romanization,self.translation
				entry={
					'traditional':self.splitkey[0],		#uchar string
					'simplified':self.splitkey[1],		#uchar string
					'cjktraditional':cjktraditional,
					'cjksimplified':cjksimplified,
					'romanization':split_romanization,	#list of morphenes
					'frequencies':[],					#filled by post-process with romanized morphene frequencies
					'translation':self.translation,
				}

				if entry['traditional'] in self.dict.keys():
					#print 'already have: ',`entry['traditional']`,entry['romanization']#fontset more likely to have traditional, if any
					#print 'proof:',self.dict[entry['traditional']]['romanization']
					pass
				else:self.dict[entry['traditional']]=entry


				#Add to distro:
				for item in entry['traditional']:
					try:self.dist[item]+=1
					except:self.dist[item]=1


				if math.fmod(len(self.dict.keys()),100)==0:
					msglist=[
						"Words  :%6d"%(len(self.dict.keys())),
						"Symbols:%6d"%(len(self.dist.keys()))
					]
					self.progress_message(msglist)

			except:
				if DEBUG:print(sys.exc_info())

			self.article=u''

		if name=='k':
			self.inKey=False

	def search_unicode_keys(self,target,mode,direction):#SMODE=3  (mode=DMODE)

		utarget_str="u'\\u%s'"%(target)
		utarget=eval(utarget_str)
		#print type(utarget),utarget_str

		self.whichkeys=None
		if mode:self.whichkeys=self.dictkeys
		else:self.whichkeys=self.distkeys

		startpoint=self.current_search_index
		endpoint=self.current_search_index+direction*len(self.whichkeys)
		csi=startpoint

		for kidx in range(startpoint,endpoint,direction):#return kidx=csi
			for sidx in range(len(self.whichkeys[csi])):#search substrings
				if self.whichkeys[csi][sidx]==utarget:
					self.current_search_index=csi+direction
					if DEBUG:print('search_unicode_keys...returning ',csi)
					if DEBUG:print(self.whichkeys[kidx])
					return csi

			csi+=direction
			if csi>len(self.whichkeys)-1:csi=0
			elif csi<0:csi=len(self.whichkeys)-1

		return None


	def search_english_translations(self,target,mode,direction):#SMODE=2  (mode=DMODE)
		if DEBUG:print('search_english_translations...')
		if target=='':return None

		self.whichkeys=None
		if mode:self.whichkeys=self.dictkeys
		else:self.whichkeys=self.distkeys

		startpoint=self.current_search_index
		endpoint=self.current_search_index+direction*len(self.whichkeys)
		csi=startpoint

		for tridx in range(startpoint,endpoint,direction):
			try:

				translation=self.dict[self.whichkeys[csi]]['translation']

				if translation.find(target)>-1:
					self.current_search_index=csi+direction
					if DEBUG:print('search_english_translations...returning ',csi)
					return csi

				csi+=direction
				if csi>len(self.whichkeys)-1:csi=0
				elif csi<0:csi=len(self.whichkeys)-1

			except:# Exception,e:
				if DEBUG:print(sys.exc_info())
				csi+=direction

		#we have reached the endpoint w/o success
		self.current_search_index=csi
		if DEBUG:print('search_translations...returning None')
		return None


	def search_pinyin_translations(self,target,mode,direction):#SMODE=0; unused b/c redundant w/(DMODE=1,SMODE=2)
		return self.search_pinyin(target,mode,direction)

	def search_pinyin(self,target,mode,direction):#SMODE=1

		if target=='':return None

		self.whichkeys=None
		if mode:self.whichkeys=self.dictkeys
		else:self.whichkeys=self.distkeys

		startpoint=self.current_search_index
		endpoint=self.current_search_index-len(self.whichkeys)
		if direction>0:endpoint=self.current_search_index+len(self.whichkeys)-1

		csi=self.current_search_index
		if csi>len(self.whichkeys):
			csi=0
			self.current_search_index=csi


		target_frags=target.split(' ')

		for pyidx in range(startpoint,endpoint,direction):
			try:

				entry_romanization=self.dict[self.whichkeys[csi]]['romanization']


				#if target="mu goo" -> ['mu','goo'] then condition is both are in entry romanization...*any order* (mu goo can occur goo mu)
				BINGO=None

				for frag in target_frags:
					#need this frag to occur in at least one of entry_romanization items
					BINGO=False
					for item in entry_romanization:
						if item.find(frag)>-1:BINGO=True
					if not BINGO:break


				if BINGO:
					self.current_search_index=csi+direction
					return csi

				csi+=direction
				if csi>len(self.whichkeys)-1:csi=0
				elif csi<0:csi=len(self.whichkeys)-1

			except:# Exception,e:
				if DEBUG:print(sys.exc_info())
				csi+=direction

		#we have reached the endpoint w/o success
		self.current_search_index=csi
		return None


	def post_process(self):
		if DEBUG:print("ar_count:\t%s"%(self.ar_count))
		if DEBUG:print("k_count:\t%s"%(self.ar_count))

		#create the unsorted dlist:
		self.dlist=[]
		for key in self.dist.keys():
			self.dlist.append((key,self.dist[key]))

		#now sort it:
		msg="Sorting..."
		for idx1 in range(len(self.dlist)):
			for idx2 in range(idx1):
				if self.dlist[idx1][1]>self.dlist[idx2][1]:
					tmp=self.dlist[idx1]
					self.dlist[idx1]=self.dlist[idx2]
					self.dlist[idx2]=tmp
			if math.fmod(idx1,10)==0:
				msg="Sorting...%d/%d"%(idx1,len(self.dlist))
				self.progress_message([msg])
				self.handle_events_during_load()

		#fill-in romanized morphene frequencies:
		if DEBUG:print('Transfering symbol frequency information to each entry object...')
		for key in list(self.dict.keys()):
			entry=self.dict[key]
			for ridx in range(len(entry['romanization'])):
				if DEBUG:print('{}/{} {}'.format(ridx,len(entry['romanization']),entry['romanization']))
				try:
					tradkey=entry['traditional'][ridx]
					freq=self.dist[tradkey]
					if freq>self.max_freq:self.max_freq=freq
					self.dict[key]['frequencies'].append(freq)
				except: #Exception,e:
					if DEBUG:print(sys.exc_info())

		#A common dictkeys list for sync of indices
		if DEBUG:print('Done Transferring symbol freq info')
		self.dictkeys=list(self.dict.keys())

		#So F5 Display mode goes most-2-least frequently used:
		self.distkeys=[]#self.dist.keys()
		for idx1 in range(len(self.dlist)):
			self.distkeys.append(self.dlist[idx1][0])
		if DEBUG:print('Done with cp.post_process')
