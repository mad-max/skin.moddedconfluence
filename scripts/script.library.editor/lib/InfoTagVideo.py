

from sys import modules
from os.path import split

from xbmc import getCondVisibility, getInfoLabel


class InfoTagVideo:
    # set our default values
    g_id_media = -1
    g_content = None
    g_str_content = ""
    # set our content
    if getCondVisibility( 'Container.Content(Movies)' ):
        g_content = "movie"
        g_str_content = 157

    elif getCondVisibility( 'Container.Content(Episodes)' ):
        g_content = "episode"
        g_str_content = 20359

    elif getCondVisibility( 'Container.Content(MusicVideos)' ):
        g_content = "musicvideo"
        g_str_content = 20391

    elif getCondVisibility( '[Container.Content(tvshows) | Container.Content(seasons)]'):
        g_content = "tvshow"
        g_str_content = 20364

    if g_str_content:
        g_str_content = modules[ "__main__" ].__string__( g_str_content )

    # set our title
    g_title = getInfoLabel( "ListItem.Title" )
    g_title = g_title or getInfoLabel( "ListItem.TVShowTitle" )
    #g_title = g_title or getInfoLabel( "ListItem.Label" )
    # set our plot
    g_plot = getInfoLabel( "ListItem.Plot" )
    # set our studio (only works if the user is using the video library)
    g_studio = getInfoLabel( "ListItem.Studio" )
    # set our studio (only works if the user is using the video library)
    g_director = getInfoLabel( "ListItem.Director" )
    # set our genre (only works if the user is using the video library)
    g_genre = getInfoLabel( "ListItem.Genre" )
    # set our rating (only works if the user is using the video library)
    g_mpaa_rating = getInfoLabel( "ListItem.MPAA" )
    g_rating = getInfoLabel( "ListItem.Rating" )
    # set movie url
    g_filename_and_path = getInfoLabel( "ListItem.FilenameAndPath" )
    # set our path and filename
    #g_filename = getInfoLabel( "ListItem.FileName" )
    g_path, g_filename = split( g_filename_and_path )
    if g_path: g_path += ( "/", "\\" )[ not g_path.count( "/" ) ]
    # set our trailer duration
    g_duration = getInfoLabel( "ListItem.Duration" )
    # set our year and premiered for tvshow
    g_year = int( getInfoLabel( "ListItem.Year" ) or "0" )
    g_premiered = getInfoLabel( "ListItem.Premiered" )

    # set our id media
    if g_content is not None:
        g_id_media = modules[ "__main__" ].database.getIdMedia( g_content, g_filename_and_path, g_title )

    def __init__( self ): pass
