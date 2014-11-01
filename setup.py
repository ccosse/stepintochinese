#!/usr/bin/env python
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
import os,sys
APPNAME='StepIntoChinese'

for sitepkgdir in sys.path:
	if sitepkgdir[-13:]=='site-packages':break


path=os.path.join('/var/games/',APPNAME)
if os.path.exists(path):
	cmd="rm -rf %s"%path
	os.system(cmd)

os.mkdir(path)


cmd="cp -r  Flashcards %s"%(path)
os.system(cmd)

cmd="cp -r  Font %s"%(path)
os.system(cmd)

#cmd="chmod -R 777 /var/games/%s"%(APPNAME)
#os.system(cmd)

cmd="cp  .stepintochinese_config_master %s"%(path)
os.system(cmd)




cmd="rm -rf %s/%s"%(sitepkgdir,APPNAME)
print cmd
os.system(cmd)

cmd="cp -r %s %s"%(APPNAME,sitepkgdir)
print cmd
os.system(cmd)

cmd="cp stepintochinese.py /usr/local/bin/stepintochinese"
print cmd
os.system(cmd)

cmd="chmod +x /usr/local/bin/stepintochinese"
print cmd
os.system(cmd)

#cmd="chmod -R 755 %s/%s"%(sitepkgdir,APPNAME)
#print cmd
#os.system(cmd)


##########################################################	
print '****************************************'
print '*                                      *'
print '*           Setup Complete             *'
print '*                                      *'
print '* Run: /usr/local/bin/stepintochinese  *'
print '*                                      *'
print '*      Checkout more software at:      *'
print '*      http://www.asymptopia.org       *'
print '*                                      *'
print '****************************************'
