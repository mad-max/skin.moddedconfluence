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
__addonID__   = "skin.glass.svn" # get addon id
__settings__  = Addon( __addonID__ ) # get Addon object
__localize__    = __settings__.getLocalizedString


REPO_PACKAGE_DIR = "special://home/addons/packages/"

SILENT = True
DIALOG_PROGRESS = xbmcgui.DialogProgress()


def download( url, destination=REPO_PACKAGE_DIR  ):
    try:
        if not SILENT:
            DIALOG_PROGRESS.create( __settings__.getAddonInfo( "name" ) )
        destination = xbmc.translatePath( destination ) + os.path.basename( url )
        def _report_hook( count, blocksize, totalsize ):
            if not SILENT: 
                percent = int( float( count * blocksize * 100 ) / totalsize )
                DIALOG_PROGRESS.update( percent, "Downloading: %s " % url, "to: %s" % destination )
        fp, h = urllib.urlretrieve( url, destination, _report_hook )
        print fp, h
        return fp
    except:
        print_exc()
    if not SILENT:
        DIALOG_PROGRESS.close()
    return ""


def install( filename ):
    from resources.lib.extractor import extract
    return extract( filename, xbmc.translatePath( "special://skin" ) )


def notification( header="", message="", sleep=5000, icon=__settings__.getAddonInfo( "icon" ) ):
    """ Will display a notification dialog with the specified header and message,
        in addition you can set the length of time it displays in milliseconds and a icon image. 
    """
    xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i,%s)" % ( header, message, sleep, icon ) )


if ( __name__ == "__main__" ):
    try: testurl = sys.argv[ 1 ]
    except: print_exc()
    else:
        try:
            NAME = sys.argv[ 2 ]
            SILENT = sys.argv[ 3 ] != "false"
        except: print_exc()
        print "LE SCRIPT EST RENDU A FAIRE CECI 'download' " + testurl

        newaddon = download( testurl )
        print "resultat de newaddon " + newaddon

        if newaddon:
            fp, ok = install( newaddon )
            print fp, ok
        if newaddon:
            ListView = ['1001','1002','1003','1004','1005','1006','1007','1008','1009','1010','1011','1012','1013','1014','1015','1016','1017','1018','1019','1020']
            print ListView
            ViewOK=False    
            for v in ListView:
                print v;
                if xbmc.getCondVisibility("!Skin.HasSetting(ViewCustom%s_IsInstall)" % (v) ) or os.access(xbmc.translatePath('special://skin/1080i/View_Custom%s.xml' % v),os.F_OK)==False:
                    print testurl
                    fp, ok = install( testurl )
                    SrcView=open(xbmc.translatePath('special://skin/720p/View_Custom.xml'),'r')
                    NewView=open(xbmc.translatePath('special://skin/1080i/View_Custom%s.xml' % (v)),'w')
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
                    xbmc.executebuiltin( "Skin.SetString(ViewCustom%s_Name,%s)" % ( v, NAME ) )
                    try: os.remove(xbmc.translatePath('special://skin/720p/View_Custom.xml'))
                    except: print "erreur os.remove(%s)" % xbmc.translatePath('special://skin/720p/View_Custom.xml')
                    break    
                    try: os.remove(xbmc.translatePath('special://masterprofile/720p/View_Custom.xml'))
                    except: print "erreur os.remove(%s)" % xbmc.translatePath('special://masterprofile/720p/View_Custom.xml')
                    break        
            
            if ViewOK:
                #xbmcgui.Dialog().ok(  "View %s installed and save in userdata" % (v), "XBMC requires restart!" )
                xbmcgui.Dialog().ok(  xbmc.getLocalizedString(31152) %v, xbmc.getLocalizedString(31153) )
            else:
                #xbmcgui.Dialog().ok(  "Error","No more custom view available." )
                xbmcgui.Dialog().ok(  xbmc.getLocalizedString(257),xbmc.getLocalizedString(31154) )
