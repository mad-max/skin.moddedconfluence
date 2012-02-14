import re
import sys
import os

if ( __name__ == "__main__" ):
    try: NumView = sys.argv[ 1 ]
    except: print "erreur parametre"
    else:
        try: os.remove(xbmc.translatePath('special://skin/1080i/View_Custom%s.xml' % NumView))
        except: print "erreur os.remove(%s)" % xbmc.translatePath('special://skin/1080i/View_Custom%s.xml' % NumView)
	try: os.remove(xbmc.translatePath('special://masterprofile/View_Custom%s.xml' % NumView))
        except: print "erreur os.remove(%s)" % xbmc.translatePath('special://masterprofile/View_Custom%s.xml' % NumView)
        try: os.rmdir(xbmc.translatePath('special://skin/media/Custom_Media%s' % NumView))
        except: print "erreur os.rmdir('%s')" % xbmc.translatePath('special://skin/media/Custom_Media%s' % NumView)
        
