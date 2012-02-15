# Modules generaux
# Generals modules
import os, sys, urllib
from xml.dom.minidom import parse
from traceback import print_exc

# Modules XBMC
# XBMC modules
import xbmc, xbmcgui
from xbmcaddon import Addon
import xbmcvfs

# Constantes de l Add-on
# Add-on constants
_Addon = Addon( "script.gui.CustomViewsInstaller" )
_AddonDir = _Addon.getAddonInfo( "path" )
_Language = _Addon.getLocalizedString
_UrlRoot = "http://glass.googlecode.com/files/"
_TargetPath = xbmc.translatePath( os.path.join(_AddonDir, "resources/media") )

class MainGui( xbmcgui.WindowXML ):
    # ID de la liste de gauche gerant les vues
    # ID of the left list managing views
    CONTROL_VIEWS = 550
    CONTROL_SKINS = 999
    # Liste de toutes les vues disponibles
    # List of all availables views
    _ListAllViews = []
    # Liste des vues filtrees
    # List of filtered views
    _ListViews = []
    # Liste des skins avec Toutes comme valeur par defaut
    # List of skins with All as default value
    _ListSkins = [xbmc.getLocalizedString(593)]
    _ListItemSkins = [xbmcgui.ListItem(xbmc.getLocalizedString(593),"","","")]

    # Verifie si une vues est deja installee
    # Check if a view is already installed
    def viewIsInstalled( self, _viewName ):
        _listViewNumber = ['1001']
        _foundView = False
        for v in _listViewNumber:
            _name = xbmc.getInfoLabel( "Skin.String(ViewCustom%s_Name)" % (v) )
            if _name == _viewName:
                _foundView = True
        return _foundView


    # MAJ de la liste des vues installees
    # Refresh installed views list
    def refreshInstalledViews( self, _viewName ):
        _list = []
        for _view in self._ListViews:
            _label = _view.getLabel()
            if _label == _viewName:
                if self.viewIsInstalled( _label ):
                    _view.select(True)
                else:
                    _view.select(False)
            _list.append(_view)
        self._ListViews = _list
        _list = []
        for _view in self._ListAllViews:
            _label = _view.getLabel()
            if _label == _viewName:
                if self.viewIsInstalled( _label ):
                    _view.select(True)
                else:
                    _view.select(False)
            _list.append(_view)
        self._ListAllViews = _list
        try:
            # Affichage de la liste filtree
            # Display filtered list
            self.control_view_list = self.getControl( self.CONTROL_VIEWS )
            self.control_view_list.reset()
            self.control_view_list.addItems( self._ListViews )
            self.setFocusId( self.CONTROL_VIEWS )
        except:
            print_exc()

    
    # Initialisation de la liste a partir du fichier XML
    # List init using XML file
    def loadAllViews( self ):
        try:
            _doc = parse(urllib.urlopen(_UrlRoot+"Custom_Views_List.xml"))
            _flagXML = True
        except:
            xbmcgui.Dialog().ok(  xbmc.getLocalizedString(31156), xbmc.getLocalizedString(31157) )
            _flagXML = False
        if _flagXML:
            _progress = xbmcgui.DialogProgress()
            _progress.create('Download miniatures')
            # Recherche du nombre de vues pour calcul du pas de progression
            # Get the number of views to calculate the progression step
            _nbViews = 0
            for view in _doc.getElementsByTagName('view'):
               _nbViews = _nbViews + 1
            _step = int(round(100 / _nbViews,0))
            # Pour chaque vue
            # For each view
            _cpt = 0
            for view in _doc.getElementsByTagName('view'):
                _label = view.getElementsByTagName('label')[0].childNodes[0].data
                _label2 = view.getElementsByTagName('label2')[0].childNodes[0].data
                _url = view.getElementsByTagName('url')[0].childNodes[0].data
                _icon = view.getElementsByTagName('icon')[0].childNodes[0].data
                _autor = view.getElementsByTagName('autor')[0].childNodes[0].data
                _version = view.getElementsByTagName('version')[0].childNodes[0].data
                _skin = view.getElementsByTagName('skin')[0].childNodes[0].data
                _comment = view.getElementsByTagName('comment')[0].childNodes[0].data
                _fullNameIcon = os.path.join(_TargetPath, _icon)
                _progress.update( _cpt, _icon )
                # Si la vignette n est pas presente on la telecharge
                # Download thumbnail if not present
                if not xbmcvfs.exists(_fullNameIcon):
                    try:
                        urllib.urlretrieve(_UrlRoot+_icon, _fullNameIcon)
                    except:
                        print_exc()
                # Ajout du skin dans la liste si pas present
                # Add skin in list if not present
                if self._ListSkins.count(_skin) == 0:
                    self._ListSkins.append(_skin)
                    _listitem = xbmcgui.ListItem(_skin,"","","")
                    self._ListItemSkins.append(_listitem)
                _cpt = _cpt + _step
                # Ajout de la vue personnalisee
                # Add custom view
                _listitem = xbmcgui.ListItem(_label,_label2,_fullNameIcon,_fullNameIcon)
                _listitem.setProperty("url",_UrlRoot+_url)
                _listitem.setProperty("autor",_autor)
                _listitem.setProperty("version",_version)
                _listitem.setProperty("skin",_skin)
                _listitem.setProperty("comment",_comment)
                # On verifie si la vue est deja installee ou non
                # Check if view is already installed or not
                if self.viewIsInstalled( _label ):
                    _listitem.select(True)
                else:
                    _listitem.select(False)
                self._ListViews.append(_listitem)
                self._ListAllViews.append(_listitem)

    # Affichage des views d un skin
    # Display views of a skin
    def displaySkinViews( self, skinID ):
        # Purge de la liste
        # Flush the list
        self._ListViews = []
        if skinID == xbmc.getLocalizedString(593):
            self._ListViews = self._ListAllViews
        else:
            # Pour chaque vue on controle son skin
            # For each view we check his skin
            for view in self._ListAllViews:
                _skin = view.getProperty("skin")
                if _skin == skinID:
                    self._ListViews.append(view)
        try:
            # Affichage de la liste filtree
            # Display filtered list
            self.control_view_list = self.getControl( self.CONTROL_VIEWS )
            self.control_view_list.reset()
            self.control_view_list.addItems( self._ListViews )
            self.setFocusId( self.CONTROL_VIEWS )
        except:
            print_exc()


    # Initialisation de l ecran
    # Screen init
    def onInit( self ):
        if len(self._ListAllViews) == 0:
            """
            # on verifie si le dossier pour le cache existe sinon on le cree
            # Check if cache directory exists otherwise craete it
            if not xbmcvfs.exists(_CachePath):
                xbmcvfs.mkdir(_CachePath)
            """
            # Si premier chargement on initialise la liste
            # If first load then init the list
            self.loadAllViews()
            try:
                self.control_skin_list = self.getControl( self.CONTROL_SKINS )
                self.control_skin_list.reset()
                self.control_skin_list.addItems( self._ListItemSkins )
                self.control_view_list = self.getControl( self.CONTROL_VIEWS )
                self.control_view_list.reset()
                self.control_view_list.addItems( self._ListAllViews )
                self.setFocusId( self.CONTROL_VIEWS )
            except:
                print_exc()
        else:
            # Sinon on affiche simplement
            # Else display only
            self.setFocusId( self.CONTROL_VIEWS )


    def onFocus( self, controlID ):
        pass

    def onClick( self, controlID ):
        try:
            # Clique sur un item de la liste des vues
            # Clic on an item of the views list
            if controlID == self.CONTROL_VIEWS:
                # On recupere l URL d installation
                # Get the installation URL
                _name = xbmc.getInfoLabel( "container(550).listitem.label" )
                _url = xbmc.getInfoLabel( "container(550).listitem.Property(url)" )
                # Execution du script d installation si la vue n est pas deja installee sinon avertissement
                # Installation script execution if view is not installed else warning
                if self.control_view_list.getSelectedItem().isSelected():
                    xbmcgui.Dialog().ok(  xbmc.getLocalizedString(31158) %_name, "")
                else:
                    xbmc.executebuiltin("RunScript(special://skin/scripts/script.glassview/default.py,%s,%s,true)" %(_url, _name))
                    xbmc.sleep( 2000 )
                    self.refreshInstalledViews( _name )
            # Clique sur un item de la liste des themes (filtre)
            # Clic on an item of the skins list (filter)
            if controlID == self.CONTROL_SKINS:
                # On recupere l URL d installation
                # Get the installation URL
                _skin = xbmc.getInfoLabel( "container(9001).listitem.label" )
                print("Filtre sur skin ",_skin)
                self.displaySkinViews( _skin )
        except:
            print_exc()

    def onAction( self, action ):
        if action in [ 9, 10, 92, 117 ]:
            self._close_dialog()

    def _close_dialog( self ):
        self.close()
        # execute sleep for animation work on close
        xbmc.sleep( 500 )


def Main():
    try:
        w = MainGui( "CustomViewsList.xml", _AddonDir )
        w.doModal()
        del w
    except:
        print_exc()


if ( __name__ == "__main__" ):
    Main()
