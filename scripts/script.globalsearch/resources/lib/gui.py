import sys, re, datetime
import xbmc, xbmcgui
import contextmenu, infodialog

__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__version__    = sys.modules[ "__main__" ].__version__
__settings__   = sys.modules[ "__main__" ].__settings__
__language__   = sys.modules[ "__main__" ].__language__
__cwd__        = sys.modules[ "__main__" ].__cwd__

ACTION_CANCEL_DIALOG  = ( 9, 10, 216, 247, 257, 275, 61467, 61448, )
ACTION_CONTEXT_MENU = ( 117, )
ACTION_OSD = ( 122, )
ACTION_SHOW_GUI = ( 18, )
ACTION_SHOW_INFO = ( 11, )


def log(txt):
    message = 'script.globalsearch: %s' % txt
    xbmc.log(msg=message, level=xbmc.LOGNOTICE)


class GUI( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )
        self.searchstring = kwargs[ "searchstring" ]
        log('script started')


    def onInit( self ):
        if self.searchstring == '':
            self._close()
        else:
            self._hide_controls()
            self._load_settings()
            self._reset_variables()
            self._init_variables()
            self._fetch_items()


    def _fetch_items( self ):
        if self.movies == 'true':
            self._fetch_movies()
        if self.tvshows == 'true' or self.episodes == 'true':
            self._fetch_tvshows()
        if self.episodes == 'true':
            self._fetch_episodes()
        if self.musicvideos == 'true':
            self._fetch_musicvideos()
        if self.artists == 'true':
            self._fetch_artists()
        if self.albums == 'true':
            self._fetch_albums()
        if self.songs == 'true':
            self._fetch_songs()
        self._setfocus()


    def _hide_controls( self ):
        self.getControl( 119 ).setVisible( False )
        self.getControl( 129 ).setVisible( False )
        self.getControl( 139 ).setVisible( False )
        self.getControl( 149 ).setVisible( False )
        self.getControl( 159 ).setVisible( False )
        self.getControl( 169 ).setVisible( False )
        self.getControl( 179 ).setVisible( False )
        self.getControl( 189 ).setVisible( False )
        self.getControl( 198 ).setVisible( False )
        self.getControl( 199 ).setVisible( False )


    def _reset_controls( self ):
        self.getControl( 111 ).reset()
        self.getControl( 121 ).reset()
        self.getControl( 131 ).reset()
        self.getControl( 141 ).reset()
        self.getControl( 151 ).reset()
        self.getControl( 161 ).reset()
        self.getControl( 171 ).reset()
        self.getControl( 181 ).reset()


    def _load_settings( self ):
        self.movies = __settings__.getSetting( "movies" )
        self.tvshows = __settings__.getSetting( "tvshows" )
        self.episodes = __settings__.getSetting( "episodes" )
        self.musicvideos = __settings__.getSetting( "musicvideos" )
        self.artists = __settings__.getSetting( "artists" )
        self.albums = __settings__.getSetting( "albums" )
        self.songs = __settings__.getSetting( "songs" )


    def _reset_variables( self ):
        self.foundmovies= 'false'
        self.foundtvshows= 'false'
        self.foundseasons= 'false'
        self.foundepisodes= 'false'
        self.foundmusicvideos= 'false'
        self.foundartists= 'false'
        self.foundalbums= 'false'
        self.foundsongs= 'false'
        self.getControl( 190 ).setLabel( '[B]' + xbmc.getLocalizedString(194) + '[/B]' )


    def _init_variables( self ):
        self.fetch_seasonepisodes = 'false'
        self.fetch_albumssongs = 'false'
        self.fetch_songalbum = 'false'
        self.playingtrailer = 'false'
        self.tvshowidlist = []
        self.tvshowfanartlist = []
        self.getControl( 198 ).setLabel( '[B]' + __language__(32299) + '[/B]' )
        self.Player = MyPlayer()
        self.Player.gui = self


    def _fetch_movies( self ):
        self.getControl( 191 ).setLabel( '[B]' + xbmc.getLocalizedString(342) + '[/B]' )
        count = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"fields": ["streamDetails", "genre", "studio", "year", "tagline", "plot", "plotoutline", "runtime", "fanart", "thumbnail", "file", "trailer", "playcount", "rating", "mpaa", "director"] }, "id": 1}')
        json_temp = json_query.replace('}]}','').replace('}]','').replace('"}','"')
        json_response = re.compile( "{(.*?)}", re.DOTALL ).findall(json_temp)
        for movieitem in json_response:
            findmoviename = re.search( '"label":"(.*?)","', movieitem )
            if findmoviename:
                moviename = (findmoviename.group(1))
                moviematch = re.search( '.*' + self.searchstring + '.*', moviename, re.I )
                if moviematch:
                    count = count + 1
                    movie = (moviematch.group(0))
                    finddirector = re.search( '"director":"(.*?)","', movieitem )
                    if finddirector:
                        director = (finddirector.group(1))
                    else:
                        director = ""
                    findfanart = re.search( '"fanart":"(.*?)","', movieitem )
                    if findfanart:
                        fanart = (findfanart.group(1))
                    else:
                        fanart = ""
                    findpath = re.search( '"file":"(.*?)","', movieitem )
                    if findpath:
                        path = (findpath.group(1))
                    else:
                        path = ""
                    findgenre = re.search( '"genre":"(.*?)","', movieitem )
                    if findgenre:
                        genre = (findgenre.group(1))
                    else:
                        genre = ""
                    findmpaa = re.search( '"mpaa":"(.*?)","', movieitem )
                    if findmpaa:
                        mpaa = (findmpaa.group(1))
                    else:
                        mpaa = ""
                    findplaycount = re.search( '"playcount":(.*?),"', movieitem )
                    if findplaycount:
                        playcount = (findplaycount.group(1))
                    else:
                        playcount = ""
                    findplot = re.search( '"plot":"(.*?)","', movieitem )
                    if findplot:
                        plot = (findplot.group(1))
                    else:
                        plot = ""
                    findoutline = re.search( '"plotoutline":"(.*?)","', movieitem )
                    if findoutline:
                        outline = (findoutline.group(1))
                    else:
                        outline = ""
                    findrating = re.search( '"rating":(.*?),"', movieitem )
                    if findrating:
                        rating = findrating.group(1)
                        rating = str( round( float(rating),1 ) )
                    else:
                        rating = ""
                    findruntime = re.search( '"runtime":"(.*?)","', movieitem )
                    if findruntime:
                        runtime = (findruntime.group(1))
                    else:
                        runtime = ""
                    findstudio = re.search( '"studio":"(.*?)","', movieitem )
                    if findstudio:
                        studio = (findstudio.group(1))
                    else:
                        studio = ""
                    findtagline = re.search( '"tagline":"(.*?)","', movieitem )
                    if findtagline:
                        tagline = (findtagline.group(1))
                    else:
                        tagline = ""
                    findthumb = re.search( '"thumbnail":"(.*?)","', movieitem )
                    if findthumb:
                        thumb = (findthumb.group(1))
                    else:
                        thumb = ""
                    findtrailer = re.search( '"trailer":"(.*?)","', movieitem )
                    if findtrailer:
                        trailer = (findtrailer.group(1))
                    else:
                        trailer = ""
                    findaudiochannels = re.search( '"channels":(.*?),"', movieitem )
                    if findaudiochannels:
                        audiochannels = (findaudiochannels.group(1))
                    else:
                        audiochannels = ""
                    findaudiocodec = re.search( '"codec":"(.*?)","l', movieitem )
                    if findaudiocodec:
                        audiocodec = (findaudiocodec.group(1))
                    else:
                        audiocodec = ""
                    findvideoaspect = re.search( '"aspect":(.*?),"', movieitem )
                    if findvideoaspect:
                        aspect = (findvideoaspect.group(1))
                        if float(aspect) <= 1.4859:
                            videoaspect = str(1.33)
                        elif float(aspect) <= 1.7190:
                            videoaspect = str(1.66)
                        elif float(aspect) <= 1.8147:
                            videoaspect = str(1.78)
                        elif float(aspect) <= 2.0174:
                            videoaspect = str(1.85)
                        elif float(aspect) <= 2.2738:
                            videoaspect = str(2.20)
                        else:
                            videoaspect = str(2.35)
                    else:
                        videoaspect = ""
                    findvideoresolution = re.search( '"height":(.*?),"', movieitem )
                    if findvideoresolution:
                        height = (findvideoresolution.group(1))
                        if int(height) <= 480:
                            videoresolution = str(480)
                        elif int(height) <= 544:
                            videoresolution = str(540)
                        elif int(height) <= 576:
                            videoresolution = str(576)
                        elif int(height) <= 720:
                            videoresolution = str(720)
                        else:
                            videoresolution = str(1080)
                    else:
                        videoresolution = ""
                    findvideocodec = re.search( '[0-9]{3},"codec":"(.*?)","d', movieitem )
                    if findvideocodec:
                        videocodec = (findvideocodec.group(1))
                    else:
                        videocodec = ""
                    findyear = re.search( '"year":(.*)', movieitem )
                    if findyear:
                        year = (findyear.group(1))
                    else:
                        year = ""
                    listitem = xbmcgui.ListItem(label=movie, iconImage='DefaultVideo.png', thumbnailImage=thumb)
                    listitem.setProperty( "icon", thumb )
                    listitem.setProperty( "fanart_image", fanart )
                    listitem.setProperty( "genre", genre )
                    listitem.setProperty( "plot", plot )
                    listitem.setProperty( "plotoutline", outline )
                    listitem.setProperty( "duration", runtime )
                    listitem.setProperty( "studio", studio )
                    listitem.setProperty( "tagline", tagline )
                    listitem.setProperty( "year", year )
                    listitem.setProperty( "trailer", trailer )
                    listitem.setProperty( "playcount", playcount )
                    listitem.setProperty( "rating", rating )
                    listitem.setProperty( "mpaa", mpaa )
                    listitem.setProperty( "director", director )
                    listitem.setProperty( "videoresolution", videoresolution )
                    listitem.setProperty( "videocodec", videocodec )
                    listitem.setProperty( "videoaspect", videoaspect )
                    listitem.setProperty( "audiocodec", audiocodec )
                    listitem.setProperty( "audiochannels", audiochannels )
                    listitem.setProperty( "path", path )
                    self.getControl( 111 ).addItem( listitem )
        if count > 0:
            self.foundmovies= 'true'
            xbmcgui.lock()
            self.getControl( 110 ).setLabel( str(count) )
            self.getControl( 119 ).setVisible( True )
            xbmcgui.unlock()
        else:
            self.foundmovies= 'false'


    def _fetch_tvshows( self ):
        self.getControl( 191 ).setLabel( '[B]' + xbmc.getLocalizedString(20343) + '[/B]' )
        count = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"fields": ["genre", "studio", "premiered", "plot", "fanart", "thumbnail", "file", "playcount", "year", "mpaa", "episode", "rating"] }, "id": 1}')
        json_response = re.compile( "{(.*?)}", re.DOTALL ).findall(json_query)
        for tvshowitem in json_response:
            findtvshowid = re.search( '"tvshowid":(.*?),"', tvshowitem )
            if findtvshowid:
                tvshowid = (findtvshowid.group(1))
                self.tvshowidlist.append(tvshowid)
            findtvshowfanart = re.search( '"fanart":"(.*?)","', tvshowitem )
            if findtvshowfanart:
                tvshowfanart = (findtvshowfanart.group(1))
                self.tvshowfanartlist.append(tvshowfanart)
            if self.tvshows == 'true':
                findtvshowname = re.search( '"label":"(.*?)","', tvshowitem )
                if findtvshowname:
                    tvshowname = (findtvshowname.group(1))
                    tvshowmatch = re.search( '.*' + self.searchstring + '.*', tvshowname, re.I )
                    if tvshowmatch:
                        count = count + 1
                        tvshow = (tvshowmatch.group(0))
                        findepisode = re.search( '"episode":(.*?),"', tvshowitem )
                        if findepisode:
                            episode = (findepisode.group(1))
                        else:
                            episode = ""
                        findfanart = re.search( '"fanart":"(.*?)","', tvshowitem )
                        if findfanart:
                            fanart = (findfanart.group(1))
                        else:
                            fanart = ""
                        findgenre = re.search( '"genre":"(.*?)","', tvshowitem )
                        if findgenre:
                            genre = (findgenre.group(1))
                        else:
                            genre = ""
                        findmpaa = re.search( '"mpaa":"(.*?)","', tvshowitem )
                        if findmpaa:
                            mpaa = (findmpaa.group(1))
                        else:
                            mpaa = ""
                        findplaycount = re.search( '"playcount":(.*?),"', tvshowitem )
                        if findplaycount:
                            playcount = (findplaycount.group(1))
                        else:
                            playcount = ""
                        findplot = re.search( '"plot":"(.*?)","', tvshowitem )
                        if findplot:
                            plot = (findplot.group(1))
                        else:
                            plot = ""
                        findpremiered = re.search( '"premiered":"(.*?)","', tvshowitem )
                        if findpremiered:
                            premiered = (findpremiered.group(1))
                        else:
                            premiered = ""
                        findrating = re.search( '"rating":(.*?),"', tvshowitem )
                        if findrating:
                            rating = (findrating.group(1))
                            rating = str( round( float(rating),1 ) )
                        else:
                            rating = ""
                        findstudio = re.search( '"studio":"(.*?)","', tvshowitem )
                        if findstudio:
                            studio = (findstudio.group(1))
                        else:
                            studio = ""
                        findthumb = re.search( '"thumbnail":"(.*?)","', tvshowitem )
                        if findthumb:
                            thumb = (findthumb.group(1))
                        else:
                            thumb = ""
                        findpath = re.search( '"tvshowid":(.*?),"', tvshowitem )
                        if findpath:
                            path = (findpath.group(1))
                            path = 'videodb://2/2/' + path + '/'
                        else:
                            path = ""
                        findyear = re.search( '"year":(.*)', tvshowitem )
                        if findyear:
                            year = (findyear.group(1))
                        else:
                            year = ""
                        listitem = xbmcgui.ListItem(label=tvshow, iconImage='DefaultVideo.png', thumbnailImage=thumb)
                        listitem.setProperty( "icon", thumb )
                        listitem.setProperty( "episode", episode )
                        listitem.setProperty( "mpaa", mpaa )
                        listitem.setProperty( "year", year )
                        listitem.setProperty( "fanart_image", fanart )
                        listitem.setProperty( "genre", genre )
                        listitem.setProperty( "plot", plot )
                        listitem.setProperty( "premiered", premiered )
                        listitem.setProperty( "studio", studio )
                        listitem.setProperty( "rating", rating )
                        listitem.setProperty( "playcount", playcount )
                        listitem.setProperty( "path", path )
                        self.getControl( 121 ).addItem( listitem )
        if self.tvshows == 'true':
            if count > 0:
                self.foundtvshows= 'true'
                xbmcgui.lock()
                self.getControl( 120 ).setLabel( str(count) )
                self.getControl( 129 ).setVisible( True )
                xbmcgui.unlock()
            else:
                self.foundtvshows= 'false'


    def _fetch_seasons( self ):
        self.getControl( 191 ).setLabel( '[B]' + xbmc.getLocalizedString(20343) + '[/B]' )
        count = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetSeasons", "params": {"fields": ["showtitle", "season", "fanart", "thumbnail", "playcount", "episode"], "tvshowid":%s }, "id": 1}' % self.tvshowid)
        json_response = re.compile( "{(.*?)}", re.DOTALL ).findall(json_query)
        for seasonitem in json_response:
            findtvshowname = re.search( '"showtitle":"(.*?)","', seasonitem )
            if findtvshowname:
                tvshowname = (findtvshowname.group(1))
                tvshowmatch = re.search( '.*' + self.searchstring + '.*', tvshowname, re.I )
                if tvshowmatch:
                    count = count + 1
                    tvshow = (tvshowmatch.group(0))
                    findepisode = re.search( '"episode":(.*?),"', seasonitem )
                    if findepisode:
                        episode = (findepisode.group(1))
                    else:
                        episode = ""
                    findfanart = re.search( '"fanart":"(.*?)","', seasonitem )
                    if findfanart:
                        fanart = (findfanart.group(1))
                    else:
                        fanart = ""
                    findpath = re.search( '"season":(.*?),"', seasonitem )
                    if findpath:
                        path = (findpath.group(1))
                        path = 'videodb://2/2/' + self.tvshowid + '/' + path + '/'
                    else:
                        path = ""
                    findseason = re.search( '"label":"(.*?)","', seasonitem )
                    if findseason:
                        season = (findseason.group(1))
                    else:
                        season = ""
                    findplaycount = re.search( '"playcount":(.*?),"', seasonitem )
                    if findplaycount:
                        playcount = (findplaycount.group(1))
                    else:
                        playcount = ""
                    findthumb = re.search( '"thumbnail":"(.*?)"', seasonitem )
                    if findthumb:
                        thumb = (findthumb.group(1))
                    else:
                        thumb = ""
                    listitem = xbmcgui.ListItem(label=season, iconImage='DefaultVideo.png', thumbnailImage=thumb)
                    listitem.setProperty( "icon", thumb )
                    listitem.setProperty( "episode", episode )
                    listitem.setProperty( "fanart_image", fanart )
                    listitem.setProperty( "tvshowtitle", tvshow )
                    listitem.setProperty( "playcount", playcount )
                    listitem.setProperty( "path", path )
                    self.getControl( 131 ).addItem( listitem )
        if count > 0:
            self.foundseasons= 'true'
            xbmcgui.lock()
            self.getControl( 130 ).setLabel( str(count) )
            self.getControl( 139 ).setVisible( True )
            xbmcgui.unlock()
        else:
            self.foundseasons= 'false'


    def _fetch_episodes( self ):
        self.getControl( 191 ).setLabel( '[B]' + xbmc.getLocalizedString(20360) + '[/B]' )
        count = 0
        for tvshowid in self.tvshowidlist:
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "fields": ["streamDetails", "plot", "firstaired", "runtime", "season", "episode", "showtitle", "thumbnail", "file", "playcount", "director", "rating"], "tvshowid":%s }, "id": 1}' % tvshowid)
            json_temp = json_query.replace('}]}','').replace('}],"v',',"v')
            json_response = re.compile( "{(.*?)}", re.DOTALL ).findall(json_temp)
            fanart = self.tvshowfanartlist[0]
            del self.tvshowfanartlist[0]
            for episodeitem in json_response:
                if self.fetch_seasonepisodes == 'true':
                    findepisodename = re.search( '"showtitle":"(.*?)","', episodeitem )
                else:
                    findepisodename = re.search( '"label":"(.*?)","', episodeitem )
                if findepisodename:
                    episodename = (findepisodename.group(1))
                    episodematch = re.search( '.*' + self.searchstring + '.*', episodename, re.I )
                    if episodematch:
                        count = count + 1
                        if self.fetch_seasonepisodes == 'true':
                            tvshowname = (episodematch.group(0))
                        else:
                            episode = (episodematch.group(0))
                        finddirector = re.search( '"director":"(.*?)","', episodeitem )
                        if finddirector:
                            director = (finddirector.group(1))
                        else:
                            director = ""
                        findepisodenumber = re.search( '"episode":(.*?),"', episodeitem )
                        if findepisodenumber:
                            episodenumber = (findepisodenumber.group(1))
                        else:
                            episodenumber = ""
                        findpath = re.search( '"file":"(.*?)","', episodeitem )
                        if findpath:
                            path = (findpath.group(1))
                        else:
                            path = ""
                        findpremiered = re.search( '"firstaired":"(.*?)","', episodeitem )
                        if findpremiered:
                            premiered = (findpremiered.group(1))
                        else:
                            premiered = ""
                        findplot = re.search( '"plot":"(.*?)","', episodeitem )
                        if findplot:
                            plot = (findplot.group(1))
                        else:
                            plot = ""
                        findrating = re.search( '"rating":(.*?),"', episodeitem )
                        if findrating:
                            rating = (findrating.group(1))
                            rating = str( round( float(rating),1 ) )
                        else:
                            rating = ""
                        findruntime = re.search( '"runtime":"(.*?)","', episodeitem )
                        if findruntime:
                            runtime = (findruntime.group(1))
                        else:
                            runtime = ""
                        findseason = re.search( '"season":(.*?),"', episodeitem )
                        if findseason:
                            seasonnumber = (findseason.group(1))
                        else:
                            seasonnumber = ""
                        if self.fetch_seasonepisodes == 'true':
                            findepisode = re.search( '"label":"(.*?)","', episodeitem )
                            if findepisode:
                                episode = (findepisode.group(1))
                            else:
                                episode = ""
                        else:
                            findtvshowname = re.search( '"showtitle":"(.*?)","', episodeitem )
                            if findtvshowname:
                                tvshowname = (findtvshowname.group(1))
                            else:
                                tvshowname = ""
                        findplaycount = re.search( '"playcount":(.*?),"', episodeitem )
                        if findplaycount:
                            playcount = (findplaycount.group(1))
                        else:
                            playcount = ""
                        findthumb = re.search( '"thumbnail":"(.*?)"', episodeitem )
                        if findthumb:
                            thumb = (findthumb.group(1))
                        else:
                            thumb = ""
                        findaudiochannels = re.search( '"channels":(.*?),"', episodeitem )
                        if findaudiochannels:
                            audiochannels = (findaudiochannels.group(1))
                        else:
                            audiochannels = ""
                        findaudiocodec = re.search( '"codec":"(.*?)","l', episodeitem )
                        if findaudiocodec:
                            audiocodec = (findaudiocodec.group(1))
                        else:
                            audiocodec = ""
                        findvideoaspect = re.search( '"aspect":(.*?),"', episodeitem )
                        if findvideoaspect:
                            aspect = (findvideoaspect.group(1))
                            if float(aspect) <= 1.4859:
                                videoaspect = str(1.33)
                            elif float(aspect) <= 1.7190:
                                videoaspect = str(1.66)
                            elif float(aspect) <= 1.8147:
                                videoaspect = str(1.78)
                            elif float(aspect) <= 2.0174:
                                videoaspect = str(1.85)
                            elif float(aspect) <= 2.2738:
                                videoaspect = str(2.20)
                            else:
                                videoaspect = str(2.35)
                        else:
                            videoaspect = ""
                        findvideoresolution = re.search( '"height":(.*?),"', episodeitem )
                        if findvideoresolution:
                            height = (findvideoresolution.group(1))
                            if int(height) <= 480:
                                videoresolution = str(480)
                            elif int(height) <= 544:
                                videoresolution = str(540)
                            elif int(height) <= 576:
                                videoresolution = str(576)
                            elif int(height) <= 720:
                                videoresolution = str(720)
                            else:
                                videoresolution = str(1080)
                        else:
                            videoresolution = ""
                        findvideocodec = re.search( '[0-9]{3},"codec":"(.*?)","d', episodeitem )
                        if findvideocodec:
                            videocodec = (findvideocodec.group(1))
                        else:
                            videocodec = ""
                        listitem = xbmcgui.ListItem(label=episode, iconImage='DefaultVideo.png', thumbnailImage=thumb)
                        listitem.setProperty( "icon", thumb )
                        listitem.setProperty( "episode", episodenumber )
                        listitem.setProperty( "plot", plot )
                        listitem.setProperty( "rating", rating )
                        listitem.setProperty( "director", director )
                        listitem.setProperty( "fanart_image", fanart )
                        listitem.setProperty( "season", seasonnumber )
                        listitem.setProperty( "duration", runtime )
                        listitem.setProperty( "tvshowtitle", tvshowname )
                        listitem.setProperty( "premiered", premiered )
                        listitem.setProperty( "playcount", playcount )
                        listitem.setProperty( "videoresolution", videoresolution )
                        listitem.setProperty( "videocodec", videocodec )
                        listitem.setProperty( "videoaspect", videoaspect )
                        listitem.setProperty( "audiocodec", audiocodec )
                        listitem.setProperty( "audiochannels", audiochannels )
                        listitem.setProperty( "path", path )
                        self.getControl( 141 ).addItem( listitem )
        if count > 0:
            self.foundepisodes= 'true'
            xbmcgui.lock()
            self.getControl( 140 ).setLabel( str(count) )
            self.getControl( 149 ).setVisible( True )
            xbmcgui.unlock()
        else:
            self.foundepisodes= 'false'


    def _fetch_musicvideos( self ):
        self.getControl( 191 ).setLabel( '[B]' + xbmc.getLocalizedString(20389) + '[/B]' )
        count = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMusicVideos", "params": {"fields": ["streamDetails", "runtime", "genre", "studio", "artist", "album", "year", "plot", "fanart", "thumbnail", "file", "playcount", "director"] }, "id": 1}')
        json_temp = json_query.replace('}]}','').replace('}]','').replace('"}','"')
        json_response = re.compile( "{(.*?)}", re.DOTALL ).findall(json_temp)
        for musicvideoitem in json_response:
            findmusicvideoname = re.search( '"label":"(.*?)","', musicvideoitem )
            if findmusicvideoname:
                musicvideoname = (findmusicvideoname.group(1))
                musicvideomatch = re.search( '.*' + self.searchstring + '.*', musicvideoname, re.I )
                if musicvideomatch:
                    count = count + 1
                    musicvideo = (musicvideomatch.group(0))
                    findalbum = re.search( '"album":"(.*?)","', musicvideoitem )
                    if findalbum:
                        album = (findalbum.group(1))
                    else:
                        album = ""
                    findartist = re.search( '"artist":"(.*?)","', musicvideoitem )
                    if findartist:
                        artist = (findartist.group(1))
                    else:
                        artist = ""
                    finddirector = re.search( '"director":"(.*?)","', musicvideoitem )
                    if finddirector:
                        director = (finddirector.group(1))
                    else:
                        director = ""
                    findfanart = re.search( '"fanart":"(.*?)","', musicvideoitem )
                    if findfanart:
                        fanart = (findfanart.group(1))
                    else:
                        fanart = ""
                    findpath = re.search( '"file":"(.*?)","', musicvideoitem )
                    if findpath:
                        path = (findpath.group(1))
                    else:
                        path = ""
                    findgenre = re.search( '"genre":"(.*?)","', musicvideoitem )
                    if findgenre:
                        genre = (findgenre.group(1))
                    else:
                        genre = ""
                    findplot = re.search( '"plot":"(.*?)","', musicvideoitem )
                    if findplot:
                        plot = (findplot.group(1))
                    else:
                        plot = ""
                    findduration = re.search( '"duration":(.*?),"', musicvideoitem )
                    if findduration:
                        duration = (findduration.group(1))
                        duration = (findduration.group(1))
                        duration = str(datetime.timedelta(seconds=int(duration)))
                        if duration[0] == '0':
                            duration = duration[2:]
                    else:
                        duration = ""
                    findstudio = re.search( '"studio":"(.*?)","', musicvideoitem )
                    if findstudio:
                        studio = (findstudio.group(1))
                    else:
                        studio = ""
                    findthumb = re.search( '"thumbnail":"(.*?)","', musicvideoitem )
                    if findthumb:
                        thumb = (findthumb.group(1))
                    else:
                        thumb = ""
                    findplaycount = re.search( '"playcount":(.*?),"', musicvideoitem )
                    if findplaycount:
                        playcount = (findplaycount.group(1))
                    else:
                        playcount = ""
                    findaudiochannels = re.search( '"channels":(.*?),"', musicvideoitem )
                    if findaudiochannels:
                        audiochannels = (findaudiochannels.group(1))
                    else:
                        audiochannels = ""
                    findaudiocodec = re.search( '"codec":"(.*?)","l', musicvideoitem )
                    if findaudiocodec:
                        audiocodec = (findaudiocodec.group(1))
                    else:
                        audiocodec = ""
                    findvideoaspect = re.search( '"aspect":(.*?),"', musicvideoitem )
                    if findvideoaspect:
                        aspect = (findvideoaspect.group(1))
                        if float(aspect) <= 1.4859:
                            videoaspect = str(1.33)
                        elif float(aspect) <= 1.7190:
                            videoaspect = str(1.66)
                        elif float(aspect) <= 1.8147:
                            videoaspect = str(1.78)
                        elif float(aspect) <= 2.0174:
                            videoaspect = str(1.85)
                        elif float(aspect) <= 2.2738:
                            videoaspect = str(2.20)
                        else:
                            videoaspect = str(2.35)
                    else:
                        videoaspect = ""
                    findvideoresolution = re.search( '"height":(.*?),"', musicvideoitem )
                    if findvideoresolution:
                        height = (findvideoresolution.group(1))
                        if int(height) <= 480:
                            videoresolution = str(480)
                        elif int(height) <= 544:
                            videoresolution = str(540)
                        elif int(height) <= 576:
                            videoresolution = str(576)
                        elif int(height) <= 720:
                            videoresolution = str(720)
                        else:
                            videoresolution = str(1080)
                    else:
                        videoresolution = ""
                    findvideocodec = re.search( '[0-9]{3},"codec":"(.*?)","d', musicvideoitem )
                    if findvideocodec:
                        videocodec = (findvideocodec.group(1))
                    else:
                        videocodec = ""
                    findyear = re.search( '"year":(.*)', musicvideoitem )
                    if findyear:
                        year = (findyear.group(1))
                    else:
                        year = ""
                    listitem = xbmcgui.ListItem(label=musicvideo, iconImage='DefaultVideo.png', thumbnailImage=thumb)
                    listitem.setProperty( "icon", thumb )
                    listitem.setProperty( "album", album )
                    listitem.setProperty( "artist", artist )
                    listitem.setProperty( "fanart_image", fanart )
                    listitem.setProperty( "director", director )
                    listitem.setProperty( "genre", genre )
                    listitem.setProperty( "plot", plot )
                    listitem.setProperty( "duration", duration )
                    listitem.setProperty( "studio", studio )
                    listitem.setProperty( "year", year )
                    listitem.setProperty( "playcount", playcount )
                    listitem.setProperty( "videoresolution", videoresolution )
                    listitem.setProperty( "videocodec", videocodec )
                    listitem.setProperty( "videoaspect", videoaspect )
                    listitem.setProperty( "audiocodec", audiocodec )
                    listitem.setProperty( "audiochannels", audiochannels )
                    listitem.setProperty( "path", path )
                    self.getControl( 151 ).addItem( listitem )
        if count > 0:
            self.foundmusicvideos= 'true'
            xbmcgui.lock()
            self.getControl( 150 ).setLabel( str(count) )
            self.getControl( 159 ).setVisible( True )
            xbmcgui.unlock()
        else:
            self.foundmusicvideos= 'false'


    def _fetch_artists( self ):
        self.getControl( 191 ).setLabel( '[B]' + xbmc.getLocalizedString(133) + '[/B]' )
        count = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetArtists", "params": {"fields": ["genre", "description", "fanart", "thumbnail", "formed", "disbanded", "born", "yearsactive", "died", "mood", "style"] }, "id": 1}')
        json_response = re.compile( "{(.*?)}", re.DOTALL ).findall(json_query)
        for artistitem in json_response:
            findartistname = re.search( '"artist":"(.*?)","', artistitem )
            if findartistname:
                artistname = (findartistname.group(1))
                artistmatch = re.search( '.*' + self.searchstring + '.*', artistname, re.I )
                if artistmatch:
                    count = count + 1
                    artist = (artistmatch.group(0))
                    findpath = re.search( '"artistid":(.*?),"', artistitem )
                    if findpath:
                        path = (findpath.group(1))
                        path = 'musicdb://2/' + path + '/'
                    else:
                        path = ""
                    findborn = re.search( '"born":"(.*?)","', artistitem )
                    if findborn:
                        born = (findborn.group(1))
                    else:
                        born = ""
                    finddescription = re.search( '"description":"(.*?)","', artistitem )
                    if finddescription:
                        description = (finddescription.group(1))
                    else:
                        description = ""
                    finddied = re.search( '"died":"(.*?)","', artistitem )
                    if finddied:
                        died = (finddied.group(1))
                    else:
                        died = ""
                    finddisbanded = re.search( '"disbanded":"(.*?)","', artistitem )
                    if finddisbanded:
                        disbanded = (finddisbanded.group(1))
                    else:
                        disbanded = ""
                    findfanart = re.search( '"fanart":"(.*?)","', artistitem )
                    if findfanart:
                        fanart = (findfanart.group(1))
                    else:
                        fanart = ""
                    findformed = re.search( '"formed":"(.*?)","', artistitem )
                    if findformed:
                        formed = (findformed.group(1))
                    else:
                        formed = ""
                    findgenre = re.search( '"genre":"(.*?)","', artistitem )
                    if findgenre:
                        genre = (findgenre.group(1))
                    else:
                        genre = ""
                    findmood = re.search( '"mood":"(.*?)","', artistitem )
                    if findmood:
                        mood = (findmood.group(1))
                    else:
                        mood = ""
                    findstyle = re.search( '"style":"(.*?)","', artistitem )
                    if findstyle:
                        style = (findstyle.group(1))
                    else:
                        style = ""
                    findthumb = re.search( '"thumbnail":"(.*?)","', artistitem )
                    if findthumb:
                        thumb = (findthumb.group(1))
                    else:
                        thumb = ""
                    findyearsactive = re.search( '"yearsactive":"(.*?)"', artistitem )
                    if findyearsactive:
                        yearsactive = (findyearsactive.group(1))
                    else:
                        yearsactive = ""
                    listitem = xbmcgui.ListItem(label=artist, iconImage='DefaultArtist.png', thumbnailImage=thumb)
                    listitem.setProperty( "icon", thumb )
                    listitem.setProperty( "artist_born", born )
                    listitem.setProperty( "artist_died", died )
                    listitem.setProperty( "artist_formed", formed )
                    listitem.setProperty( "artist_disbanded", disbanded )
                    listitem.setProperty( "artist_yearsactive", yearsactive )
                    listitem.setProperty( "artist_mood", mood )
                    listitem.setProperty( "artist_style", style )
                    listitem.setProperty( "fanart_image", fanart )
                    listitem.setProperty( "artist_genre", genre )
                    listitem.setProperty( "artist_description", description )
                    listitem.setProperty( "path", path )
                    self.getControl( 161 ).addItem( listitem )
        if count > 0:
            self.foundartists= 'true'
            xbmcgui.lock()
            self.getControl( 160 ).setLabel( str(count) )
            self.getControl( 169 ).setVisible( True )
            xbmcgui.unlock()
        else:
            self.foundartists= 'false'


    def _fetch_albums( self ):
        self.getControl( 191 ).setLabel( '[B]' + xbmc.getLocalizedString(132) + '[/B]' )
        count = 0
        if self.fetch_albumssongs == 'true':
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": {"fields": ["description", "label", "artist", "genre", "year", "thumbnail", "fanart", "theme", "type", "mood", "style", "rating"], "artistid":%s }, "id": 1}' % self.artistid)
        else:
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": {"fields": ["description", "label", "artist", "genre", "year", "thumbnail", "fanart", "theme", "type", "mood", "style", "rating"] }, "id": 1}')
        json_response = re.compile( "{(.*?)}", re.DOTALL ).findall(json_query)
        for albumitem in json_response:
            if self.fetch_albumssongs == 'true':
                findalbumname = re.search( '"artist":"(.*?)","', albumitem )
            else:
                findalbumname = re.search( '"label":"(.*?)","', albumitem )
            if findalbumname:
                albumname = (findalbumname.group(1))
                albummatch = re.search( '.*' + self.searchstring + '.*', albumname, re.I )
                if albummatch:
                    count = count + 1
                    if self.fetch_albumssongs == 'true':
                        artist = (albummatch.group(0))
                    else:
                        album = (albummatch.group(0))
                    if self.fetch_albumssongs == 'true':
                        findalbum = re.search( '"label":"(.*?)","', albumitem )
                        if findalbum:
                            album = (findalbum.group(1))
                        else:
                            album = ""
                    else:
                        findartist = re.search( '"artist":"(.*?)","', albumitem )
                        if findartist:
                            artist = (findartist.group(1))
                            if self.fetch_songalbum == 'true':
                                if not artist == self.artistname:
                                    count = count - 1
                                    return
                        else:
                            artist = ""
                    findpath = re.search( '"albumid":(.*?),"', albumitem )
                    if findpath:
                        path = (findpath.group(1))
                        path = 'musicdb://3/' + path + '/'
                    else:
                        path = ""
                    findlabel = re.search( '"album_label":"(.*?)","', albumitem )
                    if findlabel:
                        label = (findlabel.group(1))
                    else:
                        label = ""
                    finddescription = re.search( '"description":"(.*?)","', albumitem )
                    if finddescription:
                        description = (finddescription.group(1))
                    else:
                        description = ""
                    findfanart = re.search( '"fanart":"(.*?)","', albumitem )
                    if findfanart:
                        fanart = (findfanart.group(1))
                    else:
                        fanart = ""
                    findgenre = re.search( '"genre":"(.*?)","', albumitem )
                    if findgenre:
                        genre = (findgenre.group(1))
                    else:
                        genre = ""
                    findmood = re.search( '"mood":"(.*?)","', albumitem )
                    if findmood:
                        mood = (findmood.group(1))
                    else:
                        mood = ""
                    findrating = re.search( '"rating":(.*?),"', albumitem )
                    if findrating:
                        rating = (findrating.group(1))
                        if rating == '48':
                            rating = ""
                        else:
                            rating = (findrating.group(1))
                    else:
                        rating = ""
                    findstyle = re.search( '"style":"(.*?)","', albumitem )
                    if findstyle:
                        style = (findstyle.group(1))
                    else:
                        style = ""
                    findtheme = re.search( '"theme":"(.*?)","', albumitem )
                    if findtheme:
                        theme = (findtheme.group(1))
                    else:
                        theme = ""
                    findtype = re.search( '"type":"(.*?)","', albumitem )
                    if findtype:
                        albumtype = (findtype.group(1))
                    else:
                        albumtype = ""
                    findthumb = re.search( '"thumbnail":"(.*?)","', albumitem )
                    if findthumb:
                        thumb = (findthumb.group(1))
                    else:
                        thumb = ""
                    findyear = re.search( '"year":(.*)', albumitem )
                    if findyear:
                        year = (findyear.group(1))
                    else:
                        year = ""
                    listitem = xbmcgui.ListItem(label=album, iconImage='DefaultAlbumCover.png', thumbnailImage=thumb)
                    listitem.setProperty( "icon", thumb )
                    listitem.setProperty( "artist", artist )
                    listitem.setProperty( "album_label", label )
                    listitem.setProperty( "genre", genre )
                    listitem.setProperty( "fanart_image", fanart )
                    listitem.setProperty( "album_description", description )
                    listitem.setProperty( "album_theme", theme )
                    listitem.setProperty( "album_style", style )
                    listitem.setProperty( "album_rating", rating )
                    listitem.setProperty( "album_type", albumtype )
                    listitem.setProperty( "album_mood", mood )
                    listitem.setProperty( "year", year )
                    listitem.setProperty( "path", path )
                    self.getControl( 171 ).addItem( listitem )
        if count > 0:
            self.foundalbums= 'true'
            xbmcgui.lock()
            self.getControl( 170 ).setLabel( str(count) )
            self.getControl( 179 ).setVisible( True )
            xbmcgui.unlock()
        else:
            self.foundalbums= 'false'


    def _fetch_songs( self ):
        self.getControl( 191 ).setLabel( '[B]' + xbmc.getLocalizedString(134) + '[/B]' )
        count = 0
        if self.fetch_albumssongs == 'true':
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": {"fields": ["artist", "album", "genre", "duration", "year", "file", "thumbnail", "fanart", "comment", "rating", "track", "playcount"], "artistid":%s }, "id": 1}' % self.artistid)
        else:
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": {"fields": ["artist", "album", "genre", "duration", "year", "file", "thumbnail", "fanart", "comment", "rating", "track", "playcount"] }, "id": 1}')
        json_response = re.compile( "{(.*?)}", re.DOTALL ).findall(json_query)
        for songitem in json_response:
            if self.fetch_albumssongs == 'true':
                findsongname = re.search( '"artist":"(.*?)","', songitem )
            else:
                findsongname = re.search( '"label":"(.*?)","', songitem )
            if findsongname:
                songname = (findsongname.group(1))
                songmatch = re.search( '.*' + self.searchstring + '.*', songname, re.I )
                if songmatch:
                    count = count + 1
                    if self.fetch_albumssongs == 'true':
                        artist = (songmatch.group(0))
                    else:
                        song = (songmatch.group(0))
                    findalbum = re.search( '"album":"(.*?)","', songitem )
                    if findalbum:
                        album = (findalbum.group(1))
                    else:
                        album = ""
                    if self.fetch_albumssongs == 'true':
                        findsong = re.search( '"label":"(.*?)","', songitem )
                        if findsong:
                            song = (findsong.group(1))
                        else:
                            song = ""
                    else:
                        findartist = re.search( '"artist":"(.*?)","', songitem )
                        if findartist:
                            artist = (findartist.group(1))
                        else:
                            artist = ""
                    findcomment = re.search( '"comment":"(.*?)","', songitem )
                    if findcomment:
                        comment = (findcomment.group(1))
                    else:
                        comment = ""
                    findduration = re.search( '"duration":(.*?),"', songitem )
                    if findduration:
                        duration = (findduration.group(1))
                        duration = str(datetime.timedelta(seconds=int(duration)))
                        if duration[0] == '0':
                            duration = duration[2:]
                    else:
                        duration = ""
                    findfanart = re.search( '"fanart":"(.*?)","', songitem )
                    if findfanart:
                        fanart = (findfanart.group(1))
                    else:
                        fanart = ""
                    findpath = re.search( '"file":"(.*?)","', songitem )
                    if findpath:
                        path = (findpath.group(1))
                    else:
                        path = ""
                    findgenre = re.search( '"genre":"(.*?)","', songitem )
                    if findgenre:
                        genre = (findgenre.group(1))
                    else:
                        genre = ""
                    findthumb = re.search( '"thumbnail":"(.*?)","', songitem )
                    if findthumb:
                        thumb = (findthumb.group(1))
                    else:
                        thumb = ""
                    findtrack = re.search( '"track":(.*?),"', songitem )
                    if findtrack:
                        track = (findtrack.group(1))
                    else:
                        track = ""
                    findplaycount = re.search( '"playcount":(.*?),"', songitem )
                    if findplaycount:
                        playcount = (findplaycount.group(1))
                    else:
                        playcount = ""
                    findrating = re.search( '"rating":(.*?),"', songitem )
                    if findrating:
                        rating = (findrating.group(1))
                        rating = str( int(rating) - 48)
                    else:
                        rating = ""
                    findyear = re.search( '"year":(.*)', songitem )
                    if findyear:
                        year = (findyear.group(1))
                    else:
                        year = ""
                    listitem = xbmcgui.ListItem(label=song, iconImage='DefaultAlbumCover.png', thumbnailImage=thumb)
                    listitem.setProperty( "icon", thumb )
                    listitem.setProperty( "artist", artist )
                    listitem.setProperty( "album", album )
                    listitem.setProperty( "genre", genre )
                    listitem.setProperty( "comment", comment )
                    listitem.setProperty( "track", track )
                    listitem.setProperty( "rating", rating )
                    listitem.setProperty( "playcount", playcount )
                    listitem.setProperty( "duration", duration)
                    listitem.setProperty( "fanart_image", fanart)
                    listitem.setProperty( "year", year )
                    listitem.setProperty( "path", path )
                    self.getControl( 181 ).addItem( listitem )
        if count > 0:
            self.foundsongs= 'true'
            xbmcgui.lock()
            self.getControl( 180 ).setLabel( str(count) )
            self.getControl( 189 ).setVisible( True )
            xbmcgui.unlock()
        else:
            self.foundsongs= 'false'


    def _getTvshow_SeasonsEpisodes( self ):
        self.fetch_seasonepisodes = 'true'
        listitem = self.getControl( 121 ).getSelectedItem()
        self.tvshowid = listitem.getProperty('path')[14:-1]
        self.tvshowidlist = [self.tvshowid]
        self.tvshowfanartlist = [listitem.getProperty('fanart_image')]
        self.searchstring = listitem.getLabel()
        self._reset_variables()
        self._hide_controls()
        self._reset_controls()
        self._fetch_seasons()
        self._fetch_episodes()
        self._setfocus()
        self.fetch_seasonepisodes = 'false'


    def _getArtist_AlbumsSongs( self ):
        self.fetch_albumssongs = 'true'
        listitem = self.getControl( 161 ).getSelectedItem()
        self.artistid = listitem.getProperty('path')[12:-1]
        self.searchstring = listitem.getLabel()
        self._reset_variables()
        self._hide_controls()
        self._reset_controls()
        self._fetch_albums()
        self._fetch_songs()
        self._setfocus()
        self.fetch_albumssongs = 'false'


    def _getSong_Album( self ):
        self.fetch_songalbum = 'true'
        listitem = self.getControl( 181 ).getSelectedItem()
        self.artistname = listitem.getProperty('artist')
        self.searchstring = listitem.getProperty('album')
        self._reset_variables()
        self._hide_controls()
        self._reset_controls()
        self._fetch_albums()
        self._setfocus()
        self.fetch_songalbum = 'false'


    def _play_video( self, path ):
        self._close()
        xbmc.Player().play( path )


    def _play_audio( self, path, listitem ):
        self._close()
        xbmc.Player().play( path, listitem )


    def _play_trailer( self ):
        self.playingtrailer = 'true'
        self.getControl( 100 ).setVisible( False )
        self.Player.play( self.trailer )


    def _trailerstopped( self ):
        self.getControl( 100 ).setVisible( True )
        self.playingtrailer = 'false'


    def _play_album( self ):
        self._close()
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": {"fields": ["file", "fanart"], "albumid":%s }, "id": 1}' % self.albumid)
        json_response = re.compile( "{(.*?)}", re.DOTALL ).findall(json_query)
        playlist = xbmc.PlayList(0)
        playlist.clear()
        for songitem in json_response:
            findsongpath = re.search( '"file":"(.*?)","label"', songitem )
            if findsongpath:
                song = (findsongpath.group(1))
                findfanart = re.search( '"fanart":"(.*?)","file"', songitem )
                if findfanart:
                    fanart = (findfanart.group(1))
                else:
                    fanart = ""
                listitem = xbmcgui.ListItem()
                listitem.setProperty( "fanart_image", fanart )
                playlist.add( url=song, listitem=listitem )
        xbmc.Player().play( playlist )


    def _browse_video( self, path ):
        self._close()
        xbmc.executebuiltin('ActivateWindow(Videos,' + path + ',return)')


    def _browse_audio( self, path ):
        self._close()
        xbmc.executebuiltin('ActivateWindow(MusicLibrary,' + path + ',return)')


    def _browse_album( self ):
        listitem = self.getControl( 171 ).getSelectedItem()
        path = listitem.getProperty('path')
        self._close()
        xbmc.executebuiltin('ActivateWindow(MusicLibrary,' + path + ',return)')


    def _setfocus( self ):
        xbmcgui.lock()
        self.getControl( 190 ).setLabel( '' )
        self.getControl( 191 ).setLabel( '' )
        if self.foundmovies == 'true':
            self.setFocus( self.getControl( 111 ) )
        elif self.foundtvshows == 'true':
            self.setFocus( self.getControl( 121 ) )
        elif self.foundseasons == 'true':
            self.setFocus( self.getControl( 131 ) )
        elif self.foundepisodes == 'true':
            self.setFocus( self.getControl( 141 ) )
        elif self.foundmusicvideos == 'true':
            self.setFocus( self.getControl( 151 ) )
        elif self.foundartists == 'true':
            self.setFocus( self.getControl( 161 ) )
        elif self.foundalbums == 'true':
            self.setFocus( self.getControl( 171 ) )
        elif self.foundsongs == 'true':
            self.setFocus( self.getControl( 181 ) )
        else:
            self.getControl( 199 ).setVisible( True )
            self.setFocus( self.getControl( 198 ) )
        self.getControl( 198 ).setVisible( True )
        xbmcgui.unlock()


    def _showContextMenu( self ):
        labels = ()
        functions = ()
        controlId = self.getFocusId()
        x, y = self.getControl( controlId ).getPosition()
        w = self.getControl( controlId ).getWidth()
        h = self.getControl( controlId ).getHeight()
        if controlId == 111:
            labels += ( xbmc.getLocalizedString(13346), )
            functions += ( self._showInfo, )
            listitem = self.getControl( 111 ).getSelectedItem()
            self.trailer = listitem.getProperty('trailer')
            if self.trailer:
                labels += ( __language__(32205), )
                functions += ( self._play_trailer, )
        elif controlId == 121:
            labels += ( xbmc.getLocalizedString(20351), __language__(32201), )
            functions += ( self._showInfo, self._getTvshow_SeasonsEpisodes, )
        elif controlId == 131:
            labels += ( __language__(32204), )
            functions += ( self._showInfo, )
        elif controlId == 141:
            labels += ( xbmc.getLocalizedString(20352), )
            functions += ( self._showInfo, )
        elif controlId == 151:
            labels += ( xbmc.getLocalizedString(20393), )
            functions += ( self._showInfo, )
        elif controlId == 161:
            labels += ( xbmc.getLocalizedString(21891), __language__(32202), )
            functions += ( self._showInfo, self._getArtist_AlbumsSongs, )
        elif controlId == 171:
            labels += ( xbmc.getLocalizedString(13351), __language__(32203), )
            functions += ( self._showInfo, self._browse_album, )
        elif controlId == 181:
            labels += ( xbmc.getLocalizedString(658), __language__(32206), )
            functions += ( self._showInfo, self._getSong_Album, )
        context_menu = contextmenu.GUI( "script-globalsearch-contextmenu.xml" , __cwd__, "Default", area=( x, y, w, h, ), labels=labels )
        context_menu.doModal()
        if context_menu.selection is not None:
            functions[ context_menu.selection ]()
        del context_menu


    def _showInfo( self ):
        items = []
        controlId = self.getFocusId()
        if controlId == 111:
            listitem = self.getControl( controlId ).getSelectedItem()
            content = "movies"
        elif controlId == 121:
            listitem = self.getControl( controlId ).getSelectedItem()
            content = "tvshows"
        elif controlId == 131:
            listitem = self.getControl( controlId ).getSelectedItem()
            content = "seasons"
        elif controlId == 141:
            listitem = self.getControl( controlId ).getSelectedItem()
            content = "episodes"
        elif controlId == 151:
            listitem = self.getControl( controlId ).getSelectedItem()
            content = "musicvideos"
        elif controlId == 161:
            listitem = self.getControl( controlId ).getSelectedItem()
            content = "artists"
        elif controlId == 171:
            listitem = self.getControl( controlId ).getSelectedItem()
            content = "albums"
        elif controlId == 181:
            listitem = self.getControl( controlId ).getSelectedItem()
            content = "songs"
        info_dialog = infodialog.GUI( "script-globalsearch-infodialog.xml" , __cwd__, "Default", listitem=listitem, content=content )
        info_dialog.doModal()
        if info_dialog.action is not None:
            if info_dialog.action == 'play_movie':
                listitem = self.getControl( 111 ).getSelectedItem()
                path = listitem.getProperty('path')
                self._play_video(path)
            elif info_dialog.action == 'play_trailer':
                listitem = self.getControl( 111 ).getSelectedItem()
                self.trailer = listitem.getProperty('trailer')
                self._play_trailer()
            elif info_dialog.action == 'browse_tvshow':
                listitem = self.getControl( 121 ).getSelectedItem()
                path = listitem.getProperty('path')
                self._browse_video(path)
            elif info_dialog.action == 'browse_season':
                listitem = self.getControl( 131 ).getSelectedItem()
                path = listitem.getProperty('path')
                self._browse_video(path)
            elif info_dialog.action == 'play_episode':
                listitem = self.getControl( 141 ).getSelectedItem()
                path = listitem.getProperty('path')
                self._play_video(path)
            elif info_dialog.action == 'play_musicvideo':
                listitem = self.getControl( 151 ).getSelectedItem()
                path = listitem.getProperty('path')
                self._play_video(path)
            elif info_dialog.action == 'browse_artist':
                listitem = self.getControl( 161 ).getSelectedItem()
                path = listitem.getProperty('path')
                self._browse_audio(path)
            elif info_dialog.action == 'play_album':
                listitem = self.getControl( 171 ).getSelectedItem()
                self.albumid = listitem.getProperty('path')[12:-1]
                self._play_album()
            elif info_dialog.action == 'browse_album':
                listitem = self.getControl( 171 ).getSelectedItem()
                path = listitem.getProperty('path')
                self._browse_audio(path)
            elif info_dialog.action == 'play_song':
                listitem = self.getControl( 181 ).getSelectedItem()
                path = listitem.getProperty('path')
                self._play_audio(path, listitem)
        del info_dialog


    def _newSearch( self ):
        keyboard = xbmc.Keyboard( '', __language__(32101), False )
        keyboard.doModal()
        if ( keyboard.isConfirmed() ):
            self.searchstring = keyboard.getText()
            self._reset_controls()
            self.onInit()


    def onClick( self, controlId ):
        if controlId == 111:
            listitem = self.getControl( 111 ).getSelectedItem()
            path = listitem.getProperty('path')
            self._play_video(path)
        elif controlId == 121:
            listitem = self.getControl( 121 ).getSelectedItem()
            path = listitem.getProperty('path')
            self._browse_video(path)
        elif controlId == 131:
            listitem = self.getControl( 131 ).getSelectedItem()
            path = listitem.getProperty('path')
            self._browse_video(path)
        elif controlId == 141:
            listitem = self.getControl( 141 ).getSelectedItem()
            path = listitem.getProperty('path')
            self._play_video(path)
        elif controlId == 151:
            listitem = self.getControl( 151 ).getSelectedItem()
            path = listitem.getProperty('path')
            self._play_video(path)
        elif controlId == 161:
            listitem = self.getControl( 161 ).getSelectedItem()
            path = listitem.getProperty('path')
            self._browse_audio(path)
        elif controlId == 171:
            listitem = self.getControl( 171 ).getSelectedItem()
            self.albumid = listitem.getProperty('path')[12:-1]
            self._play_album()
        elif controlId == 181:
            listitem = self.getControl( 181 ).getSelectedItem()
            path = listitem.getProperty('path')
            self._play_audio(path, listitem)
        elif controlId == 198:
            self._newSearch()


    def onAction( self, action ):
        if action in ACTION_CANCEL_DIALOG:
            if self.playingtrailer == 'false':
                self._close()
            else:
                self.Player.stop()
                self._trailerstopped()
        elif action in ACTION_CONTEXT_MENU:
            self._showContextMenu()
        elif action in ACTION_OSD:
            if self.playingtrailer == 'true' and xbmc.getCondVisibility('videoplayer.isfullscreen'):
                xbmc.executebuiltin("ActivateWindow(12901)")
        elif action in ACTION_SHOW_GUI:
            if self.playingtrailer == 'true':
                self.Player.stop()
                self._trailerstopped()
        elif action in ACTION_SHOW_INFO:
            self._showInfo()


    def _close( self ):
            log('script stopped')
            self.close()


class MyPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__( self )


    def onPlayBackEnded( self ):
       self.gui._trailerstopped()


    def onPlayBackStopped( self ):
       self.gui._trailerstopped()

