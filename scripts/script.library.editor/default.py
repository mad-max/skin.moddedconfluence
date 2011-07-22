
# based on script.genre-editor
__script__       = "XBMC Library Editor"
__author__       = "Frost, GMib"
__date__         = "11-02-2011"
__version__      = "1.0.0"


# Modules General
import os
import sys
from traceback import print_exc

# Modules XBMC
import xbmc
import xbmcgui

__string__ = xbmc.getLocalizedString

# Modules Custom
from lib.database import Database
database = Database()
from lib.InfoTagVideo import InfoTagVideo


class _Info:
    def __init__( self, keys=[ "builtin", "extra" ], values=sys.argv[ 1: ] ):
        self.__info__ = dict( zip( keys, values ) )

    def __getattr__( self, namespace ):
        return self[ namespace ]

    def __getitem__( self, namespace ):
        return self.get( namespace )

    #def __setattr__( self, key, default="" ):
    #    self.__info__[ key ] = default

    def __setitem__( self, key, default="" ):
        self.__info__[ key ] = default

    def get( self, key, default="" ):
        return self.__info__.get( key, default ).upper()

    def isempty( self ):
        return not bool( self.__info__ )


class Main:
    def __init__( self, *args, **kwargs ):
        try:
            # parse args
            self.args = _Info()

            if self.args.isempty():
                self.select_builtin()

            if self.args.builtin == "EDIT_GENRE":
                self.edit_genre()

            elif self.args.builtin == "EDIT_MPAA":
                self.edit_mpaa( InfoTagVideo.g_mpaa_rating )

            elif self.args.builtin == "EDIT_RATING":
                self.edit_rating( InfoTagVideo.g_rating )

            elif self.args.builtin in [ "EDIT_YEAR", "EDIT_PREMIERED" ]:
                if InfoTagVideo.g_content in [ "tvshow", "episode" ]:
                    self.edit_premiered( InfoTagVideo.g_premiered )
                else:
                    self.edit_year( str( InfoTagVideo.g_year ) )

            elif self.args.builtin == "EDIT_PLOT":
                self.edit_plot( InfoTagVideo.g_plot )
        except:
            print_exc()

    def keyboard( self, default="", heading=__string__( 1027 ), bigtext=False, hidden=False ):
        xbmc.executebuiltin( "Skin.Reset(KeyboardBigText)" )
        try:
            if bigtext:
                xbmc.executebuiltin( "Skin.SetBool(KeyboardBigText)" )
                xbmc.sleep( 250 )
            kb = xbmc.Keyboard( default, heading, hidden )
            kb.doModal()
            if kb.isConfirmed():
                return kb.getText()
        except:
            print_exc()
        xbmc.executebuiltin( "Skin.Reset(KeyboardBigText)" )
        return default

    def edit_genre( self ):
        import lib.GenreEditor as editor
        if editor.editGenre(): self.refresh()

    def edit_mpaa( self, strMPAA ):
        newMPAA = self.keyboard( strMPAA, 'Enter desired MPAA Rating')
        if newMPAA and ( newMPAA != strMPAA ):
            field = { "movie": "12", "tvshow": "13", "episode": "", "musicvideo": "" }[ InfoTagVideo.g_content ]
            if field: self.confirmSetDetail( newMPAA, field, "mpaa" )

    def edit_rating( self, strRating ):
        newRating = self.keyboard( strRating, 'Enter desired Rating' )
        if newRating and ( newRating != strRating ) and newRating.replace( ".", "" ).isdigit():
            if not ( 0.0 <= float( newRating ) <= 10.0 ):
                xbmcgui.Dialog().ok( "Error! [%s]" % newRating, 'Enter rating between 0.0 to 10.0' )
                self.edit_rating( strRating )
            else:
                field = { "movie": "05", "tvshow": "04", "episode": "03", "musicvideo": "" }[ InfoTagVideo.g_content ]
                if field: self.confirmSetDetail( "%.5f" % float( newRating ), field, "rating" )

    def edit_plot( self, plot ):
        newPlot = self.keyboard( plot, 'Enter desired Plot', bigtext=True )
        if newPlot and ( newPlot != plot ):
            field = { "movie": "01", "tvshow": "01", "episode": "01", "musicvideo": "08" }[ InfoTagVideo.g_content ]
            if field: self.confirmSetDetail( newPlot, field, "plot" )

    def edit_premiered( self, premiered ):
        premiered = "/".join( [ premiered[ -2: ], premiered[ 5:7 ], premiered[ :4 ] ] )
        n_pre = xbmcgui.Dialog().numeric( 1, 'Enter desired premiered', premiered )
        if n_pre and ( n_pre.replace( " ", "0" ) != premiered ):
            n_pre = n_pre.replace( " ", "0" ).split( "/" )
            n_pre.reverse()
            self.confirmSetDetail( "-".join( n_pre ), "05", "premiered" )

    def edit_year( self, year ):
        n_year = xbmcgui.Dialog().numeric( 0, 'Enter desired year', year )
        if n_year and n_year.isdigit() and ( n_year != year ):
            if not ( 1901 <= int( n_year ) <= 2025 ):
                xbmcgui.Dialog().ok( "Error! [%s]" % n_year, 'Enter year between 1901 to 2025.' )
                self.edit_year( year )
            else:
                self.confirmSetDetail( n_year, "07", "year" )

    def confirmSetDetail( self, strDetail, field, strField ):
        line1 = "Changing %s:id:%i" % ( InfoTagVideo.g_content, InfoTagVideo.g_id_media, )
        line2 = "New %s:'%s'" % ( strField, strDetail, )
        if xbmcgui.Dialog().yesno( 'Confirm', line1, line2, "Are you sure?" ):
            if database.setDetail( strDetail, InfoTagVideo.g_id_media, field, InfoTagVideo.g_content ):
                self.refresh()

    def refresh( self ):
        movieinfo = xbmc.getCondVisibility( 'Window.IsVisible(movieinformation)' )
        if movieinfo: xbmc.executebuiltin( 'Dialog.Close(movieinformation)' )
        xbmc.sleep( 750 )
        xbmc.executebuiltin( 'Container.Refresh' )
        if movieinfo:
            xbmc.executebuiltin( "SetFocus(50)" )
            xbmc.sleep( 250 )
            xbmc.executebuiltin( "Action(Info)" )

    def select_builtin( self ):
        builtins = {
            "EDIT_GENRE":   self.setText( "Edit Genre",         InfoTagVideo.g_genre ),
            "EDIT_MPAA":    self.setText( "Edit MPAA Rating", ( InfoTagVideo.g_mpaa_rating or "?" ) ),
            "EDIT_RATING" : self.setText( "Edit Rating",      ( InfoTagVideo.g_rating or "0.0" ) ),
            "EDIT_YEAR":    self.setText( "Edit Year",     str( InfoTagVideo.g_year ) ),
            "EDIT_PLOT":    self.setText( "Edit Plot",          InfoTagVideo.g_plot[ :40 ]+"..." ),
            }
        if InfoTagVideo.g_content == "movie":
            pass#builtins.update( {  } )

        elif InfoTagVideo.g_content in [ "tvshow", "episode" ]:
            builtins[ "EDIT_YEAR" ] = self.setText( "Edit Premiered", InfoTagVideo.g_premiered )
            if InfoTagVideo.g_content == "episode":
                del builtins[ "EDIT_MPAA" ], builtins[ "EDIT_GENRE" ]

        elif InfoTagVideo.g_content == "musicvideo":
            del builtins[ "EDIT_MPAA" ], builtins[ "EDIT_RATING" ]

        builtins = sorted( builtins.items(), key=lambda l: l[ 1 ].lower() )
        heading = "[%s] %s" % ( InfoTagVideo.g_str_content.encode( "utf-8" ), InfoTagVideo.g_title )

        selected = xbmcgui.Dialog().select( heading, [ v for k, v in builtins ] )
        if selected >= 0: self.args[ "builtin" ] = builtins[ selected ][ 0 ]

    def setBold( self, text ):
        return "[B]%s[/B]" % text

    def setColor( self, text, color="88FFFFFF" ):
        return "[COLOR=%s][%s][/COLOR]" % ( color, text )

    def setText( self, text1, text2 ):
        return "%s %s" % ( self.setBold( text1 ), self.setColor( text2 ) )



if ( __name__ == "__main__" ):
    #xbmc.executebuiltin( "exportlibrary(video,false,f:\\)" )
    if InfoTagVideo.g_id_media > 0:
        Main()
    else:
        xbmcgui.Dialog().ok( InfoTagVideo.g_title, "Error this %s not found in database!" % InfoTagVideo.g_content )
    xbmc.executebuiltin( "Skin.Reset(KeyboardBigText)" )
