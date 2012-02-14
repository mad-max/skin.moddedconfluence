import re
import sys
import os

class Main:
    def __init__( self ):
        self.NumView = sys.argv[1]
		os.remove('special://skin/720p/Custom_View%s.xml' % self.NumView)
		os.rmdir('special://skin/media/Custom_Media%s' % self.NumView)
				
if ( __name__ == "__main__" ):
    Main()
