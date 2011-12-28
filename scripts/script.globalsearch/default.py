import os, sys
import xbmc, xbmcaddon

__scriptname__    = "Global Search"
__author__        = "ronie"
__scriptid__      = "script.globalsearch"
__version__       = "0.0.3"
__settings__      = xbmcaddon.Addon(id=__scriptid__)
__language__      = __settings__.getLocalizedString
__version__       = __settings__.getAddonInfo('version')
__cwd__           = __settings__.getAddonInfo('path')

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) )

sys.path.append (BASE_RESOURCE_PATH)


if ( __name__ == "__main__" ):
    keyboard = xbmc.Keyboard( '', __language__(32101), False )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        searchstring = keyboard.getText()
        import gui
        window = "main"
        ui = gui.GUI( "script-globalsearch-main.xml" , __cwd__, "Default", searchstring=searchstring )
        ui.doModal()
        del ui
        sys.modules.clear()
