import xbmc
from xbmcgui import Window
import re
import sys
import os
import zipfile

def unzip( filename, destination=None, report=False ):
    from zipfile import ZipFile
    base_dir = ""

    zip = ZipFile( filename, "r" )
    namelist = zip.namelist()
    total_items = len( namelist ) or 1
    diff = 100.0 / total_items
    percent = 0

    if os.path.isdir( base_dir ):
        shutil2.rmtree( base_dir )
    os.makedirs( base_dir )
    for count, item in enumerate( namelist ):
        percent += diff
        if report:
            if DIALOG_PROGRESS.iscanceled():
                break
            DIALOG_PROGRESS.update( int( percent ), _( 188 ) % ( count + 1, total_items ), item, _( 110 ) )
            #print round( percent, 2 ), item
        if not item.endswith( "/" ):
            root, name = os.path.split( item )
            directory = os.path.normpath( os.path.join( destination, root ) )
            if not os.path.isdir( directory ): os.makedirs( directory )
            file( os.path.join( directory, name ), "wb" ).write( zip.read( item ) )
    zip.close()
    del zip
    return base_dir, True

    return "", False
    
class Main:
    def __init__( self ):
        #self.ZipSource = sys.argv[1]
	fz="C:\Documents and Settings\trioual\Desktop\ProtoVue.zip","r"
	ListView = ['1001','1002','1003','1004','1005','1006','1007','1008','1009','1010']
	for v in ListView:
		print v;
		if xbmc.getCondVisibility("!Skin.HasSetting(ViewCustom%s_IsThere)" % (v) ):
			#-- Cette vue n'est pas installée
			unzip(fz,xbmc.translatePath( "special://skin/" ))
			SrcView=open('special://skin/720p/View_Custom.xml','r')
			NewView=open('special://skin/720p/View_Custom%s.xml' % (v),'w')
			f=NewView.readlines()
			SrcView.close
			for l in f:
				NewView.write(l.replace("##@@##",v))
			NewView.close
			break	
		
if ( __name__ == "__main__" ):
    Main()
