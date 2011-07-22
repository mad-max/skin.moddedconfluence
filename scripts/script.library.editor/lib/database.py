"""
    Database module based on script.moviesets
"""

#Modules general
import os
import sys
from urllib import quote_plus
from traceback import print_exc
from re import DOTALL, findall, sub

# Modules XBMC
import xbmcgui
from xbmc import executehttpapi as xbmcdb


class Records:
    """ fetch records """

    def __init__( self ):
        self._set_records_format()

    def _set_records_format( self ):
        # format our records start and end
        xbmcdb( "SetResponseFormat()" )
        xbmcdb( "SetResponseFormat(OpenRecord,<records>)" )
        xbmcdb( "SetResponseFormat(CloseRecord,</records>)" )

    def commit( self, sql ):
        done = False
        try: done = ( "done" in xbmcdb( "ExecVideoDatabase(%s)" % quote_plus( sql ), ).lower() )
        except: print_exc()
        return done

    def fetch( self, sql, keys=None, index=None ):
        records = []
        try:
            records_xml = xbmcdb( "QueryVideoDatabase(%s)" % quote_plus( sql ), )
            records = findall( "<records>(.+?)</records>", records_xml, DOTALL )
        except:
            print_exc()
        return self.parseFields( records, keys, index )

    def parseFields( self, records, keys=None, index=None ):
        fields = []
        try:
            for record in records:
                record = findall( "<field>(.*?)</field>", record, DOTALL )
                if keys: record = dict( zip( keys, record ) )
                fields.append( record )
        except:
            print_exc()
        if fields and index is not None:
            try: fields = fields[ index ]
            except: print_exc()
        return fields


class Database( Records ):
    """ Main database class based on /xbmc/video/VideoDatabase.cpp 
        http://wiki.xbmc.org/index.php?title=Database
    """

    def __init__( self, *args, **kwargs ):
        Records.__init__( self )

    def getFileId( self, strFilenameAndPath ):
        """ Return id file """
        try:
            # SplitPath
            strPath, strFileName = os.path.split( strFilenameAndPath )
            if strPath: strPath += ( "/", "\\" )[ not strPath.count( "/" ) ]
            idPath = self.getPathId( strPath )
            if ( idPath >= 0 ):
                sql = "select idFile from files where strFileName like '%s' and idPath=%i" % ( strFileName, idPath )
                idFile = "".join( self.fetch( sql, index=0 ) )
                return int( idFile )
        except:
            print_exc()
        return -1

    def getPathId( self, strPath ):
        """ Return id path """
        try:
            sql = "select idPath from path where strPath like '%s'" % strPath
            idPath = "".join( self.fetch( sql, index=0 ) )
            if not idPath:
                if strPath.startswith( "ftp://" ) or strPath.startswith( "smb://" ):
                    for ipath, spath in self.fetch( "select idPath, strPath from path" ):
                        if strPath == sub( "(.*?://)(.*?@)(.*?)", "\\1", spath ):
                            idPath = ipath
                            break
            if idPath:
                return int( idPath )
        except:
            print_exc()
        return -1

    def getIdMedia( self, strContent, strFilenameAndPath, strTitle ):
        if strContent == "movie":
            return self.getMovie( strFilenameAndPath, strTitle )[ 0 ]

        if strContent == "tvshow":
            strPath = os.path.split( strFilenameAndPath )[ 0 ]
            if strPath: strPath += ( "/", "\\" )[ not strPath.count( "/" ) ]
            return self.getTvShow( strPath, strTitle )[ 0 ]

        if strContent == "episode":
            return self.getEpisode( strFilenameAndPath, strTitle )[ 0 ]

        if strContent == "musicvideo":
            return self.getMusicVideo( strFilenameAndPath, strTitle )[ 0 ]

    def getEpisode( self, strFilenameAndPath, strTitle ):
        """ Return id episode, title, empty """
        try:
            idFile = self.getFileId( strFilenameAndPath )
            if ( idFile == -1 ):
                sql = "select idEpisode, c00 from episode where c00 like \"%s\"" % strTitle
            else:
                sql = "select idEpisode, c00 from episode where idFile=%i" % int( idFile )
            episode = self.fetch( sql, index=0 )
            return int( episode[ 0 ] ), episode[ 1 ], ""
        except:
            print_exc()
        return -1, "", ""

    def getMovie( self, strFilenameAndPath, strTitle ):
        """ Return id movie, title, genre """
        try:
            idFile = self.getFileId( strFilenameAndPath )
            if ( idFile == -1 ):
                sql = "select idMovie, c00, c14 from movie where c00 like \"%s\"" % strTitle
            else:
                sql = "select idMovie, c00, c14 from movie where idFile=%i" % int( idFile )
            movie = self.fetch( sql, index=0 )
            return int( movie[ 0 ] ), movie[ 1 ], movie[ 2 ]
        except:
            print_exc()
        return -1, "", ""

    def getMusicVideo( self, strFilenameAndPath, strTitle ):
        """ Return id music video, title, genre """
        try:
            idFile = self.getFileId( strFilenameAndPath )
            if ( idFile == -1 ):
                sql = "select idMVideo, c00, c11 from musicvideo where c00 like \"%s\"" % strTitle
            else:
                sql = "select idMVideo, c00, c11 from musicvideo where idFile=%i" % int( idFile )
            musicvideo = self.fetch( sql, index=0 )
            return int( musicvideo[ 0 ] ), musicvideo[ 1 ], musicvideo[ 2 ]
        except:
            print_exc()
        return -1, "", ""

    def getTvShow( self, strPath, strTitle ):
        """ Return id tvshow, title, genre """
        try:
            iFound = 0
            idPath = self.getPathId( strPath )
            if ( idPath == -1 ):
                sql = "select idShow, c00, c08 from tvshow where c00 like \"%s\"" % strTitle
                iFound = 1
            else:
                sql = "select idShow from tvshowlinkpath where tvshowlinkpath.idPath=%i" % int( idPath )
                idTvShow = "".join( self.fetch( sql, index=0 ) )
                if not idTvShow.isdigit():
                    strPath1 = strPath
                    strParent = os.path.dirname( strPath1 )
                    while ( iFound == 0 ) and ( strPath1 != strParent ):
                        sql = "select idShow from path,tvshowlinkpath where tvshowlinkpath.idPath=path.idPath and strPath like '%s'" % strParent
                        idTvShow = "".join( self.fetch( sql, index=0 ) )
                        if idTvShow.isdigit(): iFound = 2
                        strPath1 = strParent
                        strParent = os.path.dirname( strPath1 )

                if idTvShow.isdigit():
                    sql = "select idShow, c00, c08 from tvshow where idShow=%i" % int( idTvShow )
                    iFound = 1

            if iFound > 0:
                tvshow = self.fetch( sql, index=0 )
                return int( tvshow[ 0 ] ), tvshow[ 1 ], tvshow[ 2 ]
        except:
            print_exc()
        return -1, "", ""

    def getGenres( self, strContent=None ):
        # list de tous les genres [[ idGenre, strGenre ], ...]
        all_genres = []
        try:
            sql_data = 'SELECT idGenre, strGenre FROM genre ORDER BY LOWER(strGenre)'
            all_genres = self.fetch( sql_data )
        except:
            print_exc()

        # list de tous les genres [[ idGenre, strGenre ], ...] selon le content [ movie, tvshow, musicvideo ]
        genres = []
        try:
            if strContent is not None:
                sql_data = 'SELECT genre.idGenre, strGenre FROM genre,genrelink%s WHERE genrelink%s.idGenre=genre.idGenre GROUP BY genre.idGenre ORDER BY LOWER(strGenre)'
                genres = self.fetch( sql_data % ( strContent, strContent, ) )
        except:
            print_exc()

        return all_genres, genres

    def getGenresByIdMedia( self, strContent, idMedia ):
        """ return all genres by media id """
        try:
            strId = { "movie": "idMovie", "tvshow": "idShow", "musicvideo": "idMVideo" }[ strContent ]
            sql = 'SELECT idGenre FROM genrelink%s WHERE %s=%i' % ( strContent, strId, idMedia )
            return [ i[ 0 ] for i in self.fetch( sql ) ]
        except:
            print_exc()
        return []

    def getGenreByName( self, strSearch ):
        """ return idgenre and strgenre of search """
        try:
            sql = 'select distinct idGenre, strGenre from genre where strGenre like \"%s\"'
            genre = self.fetch( sql % strSearch, index=0 )
            if genre: return int( genre[ 0 ] ), genre[ 1 ]
        except:
            print_exc()
        return -1, ""

    def addGenre( self, newGenre ):
        """ add new genre and return idgenre and strgenre of new genre """
        try:
            idGenre, strGenre = self.getGenreByName( newGenre )
            if idGenre > -1:
                return idGenre, "genre_exist"
            if newGenre:
                # AddToTable("genre", "idGenre", "strGenre", strGenre);
                sql = "insert into genre (idGenre, strGenre) values( NULL, '%s')"
                if self.commit( sql % newGenre ):
                    idGenre, strGenre = self.getGenreByName( newGenre )
            return idGenre, strGenre
        except:
            print_exc()
        return -1, ""

    def deleteGenreById( self, idGenre, strContent="" ):
        """ delete idgenre on genre table or genrelink """
        OK = False
        try:
            found = 0
            sql_delete = 'DELETE FROM genre%s WHERE idGenre=%i'

            if strContent:
                OK = self.commit( sql_delete % ( "link" + strContent, int( idGenre ) ) )

                sql_count = 'SELECT count(*) FROM genrelink%s WHERE idGenre=%i'
                contents = [ "movie", "tvshow", "musicvideo" ]
                contents.remove( strContent )
                for content in contents:
                    found = int( "".join( self.fetch( sql_count % ( content, int( idGenre ) ), index=0 ) ) or "0" )
                    if found: break

            if not found:
                OK = self.commit( sql_delete % ( "", int( idGenre ) ) )
        except:
            print_exc()
        return OK

    def updateGenre( self, idMedia, strContent, strGenre, listIdGenres ):
        OK = False
        try:
            sql_update = None
            if strContent == "movie":
                sql_update = 'UPDATE movie SET c14=\"%s\" WHERE idMovie=%i'
                sql_delete = 'DELETE FROM genrelinkmovie WHERE idMovie=%i'
                sql_insert = 'INSERT INTO genrelinkmovie ("idGenre","idMovie") VALUES (%i,%i)'

            elif strContent == "tvshow":
                sql_update = 'UPDATE tvshow SET c08=\"%s\" WHERE idShow=%i'
                sql_delete = 'DELETE FROM genrelinktvshow WHERE idShow=%i'
                sql_insert = 'INSERT INTO genrelinktvshow ("idGenre","idShow") VALUES (%i,%i)'

            elif strContent == "musicvideo":
                sql_update = 'UPDATE musicvideo SET c11=\"%s\" WHERE idMVideo=%i'
                sql_delete = 'DELETE FROM genrelinkmusicvideo WHERE idMVideo=%i'
                sql_insert = 'INSERT INTO genrelinkmusicvideo ("idGenre","idMVideo") VALUES (%i,%i)'

            if sql_update:
                # update media genres of table movie or tvshow or musicvideo
                OK = self.commit( sql_update % ( strGenre, int( idMedia ) ) )

                # delete default media genres of genrelink
                OK = self.commit( sql_delete % int( idMedia ) )

                # insert new genres AddGenreToMovie
                for idGenre in listIdGenres:
                    OK = self.commit( sql_insert % ( int( idGenre ), int( idMedia ) ) )
        except:
            print_exc()
        return OK

    def setDetail( self, strDetail, idMedia, field, strTable=None ):
        OK = False
        try:
            if strTable:
                strField = { "movie": "idMovie", "tvshow": "idShow", "episode": "idEpisode", "musicvideo": "idMVideo" }[ strTable ]
                sql = "update %s set c%02u=\"%s\" where %s=%u" % ( strTable, int( field ), strDetail, strField, idMedia )
                print "Changing %s:id:%i new c%02u=\"%s\"" % ( strTable, idMedia, int( field ), strDetail )#, sql
                OK = self.commit( sql )
        except:
            print_exc()
        return OK
