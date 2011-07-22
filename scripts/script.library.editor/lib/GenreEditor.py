
__script__       = "Genre Editor"
__author__       = "GMib"
__date__         = "31-01-2011"
__version__      = "0.0.4"


# Modules General
import os
import sys
from traceback import print_exc

# Modules XBMC
import xbmc
import xbmcgui


database = sys.modules[ "__main__" ].database
InfoTagVideo = sys.modules[ "__main__" ].InfoTagVideo

__string__ = sys.modules[ "__main__" ].__string__ # XBMC strings


class GenreEditor( xbmcgui.WindowXMLDialog ):
    xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
    xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )

    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )

        self.ex = 0
        self.title = InfoTagVideo.g_title

    def onInit( self ):
        self.listGenre = self.getControl( 120 )
        self.initialize()

    def initialize( self ):
        try:
            #if ( not self.title ):
            #    xbmcgui.Dialog().ok( "Genre Editor - Error", "Arguments missing!" )
            #    self._close_dialog()
            #    return

            xbmc.executebuiltin( 'ClearProperty(Update,true)' )
            xbmc.executebuiltin( 'SetProperty(Type,"%s")'  % InfoTagVideo.g_str_content.encode( "utf-8" ) )
            xbmc.executebuiltin( 'SetProperty(Title,"%s")' % InfoTagVideo.g_title )
            xbmc.executebuiltin( 'SetProperty(Genre,"%s")' % InfoTagVideo.g_genre )

            self.idMedia = InfoTagVideo.g_id_media #-1
            self.strContent = InfoTagVideo.g_content #None
            if self.strContent == "episode": self.strContent = "tvshow"

            if self.strContent is None:
                xbmcgui.Dialog().ok( "Genre Editor - Error", "Only Container for Movie, MusicVideo or TVShow!" )
                self._close_dialog()
                return

            #if self.idMedia < 0:
            #    xbmcgui.Dialog().ok( "Genre Editor - Error", "Media not found in DB!" )
            #    self._close_dialog()
            #    return

            # list de tous les genres pour le media selectionner selon le content [ movie, tvshow, musicvideo ]
            self.mediaGenres = database.getGenresByIdMedia( self.strContent, self.idMedia ) # id of movie's genre
            # set une copie de la liste self.mediaGenres, utiliser pour savoir s'il y a une modification
            self.defaultGenres = sorted( self.mediaGenres )
            # list des genres ajouter par l'utilisateur
            self.add_genres = []
            # affiche la liste des genres
            self.displayGenre()
        except:
            print_exc()

    def getGenres( self ):
        # list de tous les genres et selon le content [ movie, tvshow, musicvideo ]
        self.all_genres, self.genres = database.getGenres( self.strContent )
        # add genres added by user
        if self.add_genres:
            self.genres = sorted( self.genres + self.add_genres, key=lambda l: l[ 1 ].lower() )
        #  [ [ idGenre, strGenre ] ] genre[0][0]:id 1er genre, genre[0][1]:nom 1er genre
        return self.genres

    def displayGenre( self, select_idGenre="" ):
        selectitem = 0
        # get selected item for selectitem again
        select_idGenre = select_idGenre or xbmc.getInfoLabel( "Container(120).ListItem.Label2" )

        listitems = []
        for count, genre in enumerate( self.getGenres() ):
            idGenre, strGenre = genre
            #print ( idGenre, self.mediaGenres )
            icon = ( "", "GenreEditorSel.png" )[ idGenre in self.mediaGenres ]
            listitems.append( xbmcgui.ListItem( strGenre, idGenre, icon ) )
            if idGenre == select_idGenre: selectitem = count

        self.listGenre.reset()
        self.listGenre.addItems( listitems )
        self.listGenre.selectItem( selectitem )

    def onFocus( self, controlID ):
        pass

    def onClick( self, controlID ):
        try:
            if controlID == 120: #List genre
                listitem = self.listGenre.getSelectedItem()
                idSelGenre = listitem.getLabel2()
                if idSelGenre in self.mediaGenres: # unselect genre
                    self.mediaGenres.remove( idSelGenre )
                    listitem.setIconImage( "" )
                else:
                    self.mediaGenres.append( idSelGenre ) # select genre
                    listitem.setIconImage( "GenreEditorSel.png" )

                if ( not self.mediaGenres ) or self.defaultGenres == sorted( self.mediaGenres ):
                    xbmc.executebuiltin( 'ClearProperty(Update,true)' )
                else:
                    xbmc.executebuiltin( 'SetProperty(Update,true)' )

            elif controlID == 23: # Cancel button
                if xbmcgui.Dialog().yesno( 'Confirm', 'If you choose yes, informations will not be save', "Are you sure?" ):
                    self.initialize()
                    xbmc.executebuiltin( 'Control.Move(9000,-3)' )
                    self.setFocusId( 120 )
                    #self._close_dialog()

            elif controlID == 24: #Add button
                self.addGenre()

            elif controlID == 25: #Del button
                self.delSelectedGenre()

            elif controlID == 22: #save button
                genre = [ g for i, g in self.genres if i in self.mediaGenres ]
                genre = " / ".join( self.setGenresOrder( list( genre ) ) or genre )

                if self.defaultGenres != sorted( self.mediaGenres ) and xbmcgui.Dialog().yesno( 'Confirm update of genre', genre, "Are you sure?" ):
                    if database.updateGenre( self.idMedia, self.strContent, genre, self.mediaGenres ):
                        self.ex = 1
                        self._close_dialog()
        except:
            print_exc()

    def setGenresOrder( self, genres ):
        order = []
        if len( genres ) > 1:
            from dialogs import Order
            od = Order( "script-LibraryEditor-dialogs.xml", os.getcwd(), genre=genres )
            od.doModal()
            if od.isConfirmed:
                order = od.genres
            del od
        return order

    def addGenre( self ):
        try:
            choices = [ "[B]Create New Genre[/B]", "[B]Select All Genres[/B]" ]
            choices += [ strGenre for idGenre, strGenre in self.all_genres ]
            while True:
                selected = xbmcgui.Dialog().select( "Select or Create New Genre", choices )
                if selected == -1: break

                if selected == 1:
                    new_added = False
                    for idGenre, strGenre in self.all_genres:
                        if [ idGenre, strGenre ] not in self.genres:
                            self.add_genres.append( [ idGenre, strGenre ] )
                            new_added = True
                    if new_added:
                        self.displayGenre()
                    break

                add_genre = None
                genre_exist = None
                if selected >= 2:
                    idGenre, strGenre = self.all_genres[ selected - 2 ]
                    if [ idGenre, strGenre ] not in self.genres:
                        add_genre = [ idGenre, strGenre ]
                    else:
                        genre_exist = strGenre

                elif selected == 0:
                    kb = xbmc.Keyboard( '', 'Enter New Genre' )
                    kb.doModal()
                    genre_exist = ""
                    if kb.isConfirmed():
                        text = kb.getText()
                        if bool( text ):
                            idGenre, strGenre = database.addGenre( text )
                            idGenre = str( idGenre )
                            if strGenre == "genre_exist":
                                if [ idGenre, text ] not in self.genres:
                                    add_genre = [ idGenre, text ]
                                else:
                                    genre_exist = text
                            elif idGenre > 0 and strGenre:
                                add_genre = [ idGenre, strGenre ]

                if add_genre:
                    self.add_genres.append( add_genre )
                    self.displayGenre( add_genre[ 0 ] )
                    break

                if genre_exist is not None:
                    if genre_exist:
                        xbmcgui.Dialog().ok( "Error" ,"Genre already exist!", genre_exist )
                    continue
        except:
            print_exc()

    def delSelectedGenre( self ):
        try:
            listitem = self.listGenre.getSelectedItem()
            idSelGenre = listitem.getLabel2()
            genreSel = listitem.getLabel()
            if xbmcgui.Dialog().yesno( 'Confirm delete genre', "Delete this genre of %ss database!" % self.strContent, '"' + genreSel + '"', "Are you sure?" ):
                if database.deleteGenreById( idSelGenre, self.strContent ):
                    if [ idSelGenre, genreSel ] in self.add_genres: self.add_genres.remove( [ idSelGenre, genreSel ] )
                    select_idGenre = xbmc.getInfoLabel( "Container(120).ListItem(-1).Label2" ) or xbmc.getInfoLabel( "Container(120).ListItem(1).Label2" )
                    self.displayGenre( select_idGenre )
        except:
            print_exc()

    def onAction( self, action ):
        if action in [ 9, 10, 117 ]:
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        from time import sleep
        sleep( .4 )
        self.close()


def editGenre():
    ui = GenreEditor( "script-LibraryEditor-genre.xml", os.getcwd() )
    ui.doModal()
    refresh = ui.ex or xbmc.getCondVisibility( '!IsEmpty(Window.Property(Update))' )
    del ui
    return refresh
