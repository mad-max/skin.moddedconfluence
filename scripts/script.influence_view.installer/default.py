"""
    Simple addon installer for skinner
"""


#Modules General
import os
import sys
import urllib
from traceback import print_exc

#Modules XBMC
import xbmc
import xbmcgui
from xbmcaddon import Addon

# addon constants
#__addonID__   = "script.addon.installer" # get addon id
#__settings__  = Addon( __addonID__ ) # get Addon object

SILENT = True
DIALOG_PROGRESS = xbmcgui.DialogProgress()


def install( filename ):
    from resources.lib.extractor import extract
    print "extract : %s %s " % (filename, xbmc.translatePath( "special://skin" ) )
    return extract( filename, xbmc.translatePath( "special://skin" ) )

def notification( header="", message="", sleep=5000, icon="" ):
    """ Will display a notification dialog with the specified header and message,
        in addition you can set the length of time it displays in milliseconds and a icon image. 
    """
    xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i,%s)" % ( header, message, sleep, icon ) )

if ( __name__ == "__main__" ):
    try: zipview = sys.argv[ 1 ]
    except: print_exc()
    else:
        try: SILENT = sys.argv[ 2 ] != "false"
        except: print_exc()

        if zipview:
            ListView = ['1001','1002','1003','1004','1005','1006','1007','1008','1009','1010','1011','1012','1013','1014','1015','1016','1017','1018','1019','1020']
            ViewOK=False
            for v in ListView:
                print v;
                if xbmc.getCondVisibility("!Skin.HasSetting(ViewCustom%s_IsInstall)" % (v) ) or os.access(xbmc.translatePath('special://skin/720p/View_Custom%s.xml' % v),os.F_OK)==False:
                    print zipview
                    fp, ok = install( zipview )
                    SrcView=open(xbmc.translatePath('special://skin/720p/View_Custom.xml'),'r')
                    NewView=open(xbmc.translatePath('special://skin/720p/View_Custom%s.xml' % (v)),'w')
                    SaveView=open(xbmc.translatePath('special://masterprofile/View_Custom%s.xml' % (v)),'w')
                    f=SrcView.readlines()
                    SrcView.close
                    for l in f:
                        NewView.write(l.replace("##@@##",v))
			SaveView.write(l.replace("##@@##",v))
                    NewView.close
		    SaveView.close
                    ViewOK=True
                    xbmc.executebuiltin( "Skin.SetBool(ViewCustom%s_IsInstall)" % ( v ) )
                    try: os.remove(xbmc.translatePath('special://skin/720p/View_Custom.xml'))
                    except: print "erreur os.remove(%s)" % xbmc.translatePath('special://skin/720p/View_Custom.xml')
                    break	
                    try: os.remove(xbmc.translatePath('special://masterprofile/720p/View_Custom.xml'))
                    except: print "erreur os.remove(%s)" % xbmc.translatePath('special://masterprofile/720p/View_Custom.xml')
                    break        
			
            if ViewOK:
                xbmcgui.Dialog().ok(  "View %s installed and save in userdata" % (v), "XBMC requires restart!" )
            else:
                xbmcgui.Dialog().ok(  "Error","No more custom view available" )    
