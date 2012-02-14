import re
import sys
import os

if ( __name__ == "__main__" ):
    try: NumView = sys.argv[ 1 ]
    except: print "erreur parametre"
    else:
	SrcView=open(xbmc.translatePath('special://masterprofile/View_Custom%s.xml' % NumView),'r')
	NewView=open(xbmc.translatePath('special://skin/720p/View_Custom%s.xml' % NumView),'w')
	f=SrcView.readlines()
	SrcView.close
	for l in f:
		NewView.write(l)
	NewView.close
        
      
        
