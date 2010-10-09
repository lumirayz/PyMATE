# -------------------- #
# PMConfig.py
#
# Defines the PMConfig class, which handles all configuration-related things.
# -------------------- #

# -------------------- #
# Imports
# -------------------- #
# None!

# -------------------- #
# Class PMConfig
# -------------------- #
class PMConfig:
	"""Class for loading configuration."""
	
	# -------------------- #
	# Init	
	# -------------------- #
	def __init__( self ):
		self.props = dict()
	
	# -------------------- #
	# File loading/saving
	# -------------------- #
	def parseFile( self, f ):
		"""Load all configuration options in a file."""
		fd = open( f, "r" )
		nsl = list()
		for line in fd:
			line = line.rstrip( "\r\n" )
			ind = 0
			if( len( line ) < 2 ):
				continue
			while( line[0] == "\t" ):
				line = line[1:]
				ind += 1
			while( ind < len( nsl ) ):
				nsl.pop()
			if( line[0] == "[" and line[-1] == "]" ):
				nsl.append( line[1:-1] )
			else:
				self.parseLine( line, nsl )
		fd.close()
	
	def saveToFile( self, f ):
		"""Save all configuration options to a file."""
		pass
	
	# -------------------- #
	# Load a line
	# -------------------- #
	def parseLine( self, line, nsl = list() ):
		"""Parse a line."""
		data = line.split( "=", 2 )
		if( len( data ) == 2 ):
			if( data[0][-1] == "!" ):
				return
			key = data[0].strip()
			val = data[1].strip()
			self.props[ ".".join( nsl + [ key ] ) ] = val
	
	# -------------------- #
	# Properties
	# -------------------- #
	def getProperty( self, prop ):
		"""Get a property from the configration."""
		try:
			return self.props[ prop ]
		except KeyError:
			return None
	
	def setProperty( self, prop, val ):
		"""Set a property from the configuration to a value."""
		self.props[ prop ] = val
