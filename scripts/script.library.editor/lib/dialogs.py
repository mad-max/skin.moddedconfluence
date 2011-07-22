
# Modules XBMC
import xbmc
import xbmcgui


class Order( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )

        self.genres = kwargs[ "genre" ]
        self.isConfirmed = False

    def onInit( self ):
        self.controlList = self.getControl( 3 )
        self.setContainer()

    def setContainer( self, selectitem=0 ):
        listitems = [ xbmcgui.ListItem( genre ) for genre in self.genres ]
        self.controlList.reset()
        self.controlList.addItems( listitems )
        self.controlList.selectItem( selectitem )

    def move( self, iterable, item, n ):
        # move down(+1) or up(-1)
        it = iterable.index( item ) + n
        if it < 0: it = len( iterable )
        elif it >= len( iterable ): it = 0
        iterable.remove( item )
        iterable.insert( it, item )
        return iterable.index( item ), iterable

    def onFocus( self, controlID ):
        pass

    def onClick( self, controlID ):
        if controlID in [ 9121, 9122 ]:
            genre = xbmc.getInfoLabel( "Container(3).ListItem.Label" )
            selectitem, self.genres = self.move( self.genres, genre, ( 1, -1 )[ controlID - 9121 ] )
            self.setContainer( selectitem )

        elif controlID in [ 5, 6 ]:
            self.isConfirmed = controlID == 5
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 9, 10, 117 ]:
            self.isConfirmed = False
            self._close_dialog()

    def _close_dialog( self ):
        self.close()

