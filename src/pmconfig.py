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
	# Defaults
	# -------------------- #
	defaults = dict( {
		"editor": {
			"dialog": { "config_unsaved_close": "1" },
			"tab": {
				"mode": "full",
				"type": "notebook",
				"position": "left",
				"show_full_path": "0",
				"max_name_length": "20"
			},
			"indent": {
				"auto": "1",
				"spaces": "0",
				"tabsize": "2",
			},
			"font": {
				"face": "Monospace"
			},
			"cosmetic": {
				"line_numbers": "0",
				"wrap_mode": "none",
				"indentation_guides": "0",
				"background_color": "#1111AA",
				"view_whitespace": "never",
				"view_eol": "0",
				"longline": {
					"marker": "line",
					"length": "80",
					"color": "#FF0000"
				}
			}
		}
	} )
	
	# -------------------- #
	# File loading/saving
	# -------------------- #
	def parseFile( self, f ):
		"""Load all configuration options in a file."""
		# How it works:
		# First opens a file, initializes namespace list.
		# Loops every line in the file:
		#  If the length of the file < 2, don't bother.
		#  Removes trailing \r\n, checks indentation and stores in ind.
		#  Checks indentation length with namespace length, trimming namespace list
		#  if needed.
		#  Checks if the line is in the format r"^\[(.*)\]$". (without regex)
		#  If True:
		#   Append the part in braces to namespace list.
		#  Else:
		#   Call parseLine on the file, giving it line and namespace list.
		fd = open( f, "r" )
		nsl = list()
		for line in fd:
			line = line.rstrip( "\r\n" )
			ind = 0
			if( len( line ) <= 2 ):
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
		# How it works:
		# Split the string using "=".
		# If the split is succesful, continue.
		# If there's an "!" before the split, don't bother.
		# Get the key and value pair.
		# Apply to self.props.
		data = line.split( "=", 2 )
		if( len( data ) == 2 ):
			if( data[0][-1] == "!" ):
				return
			key = data[0].strip()
			val = data[1].strip()
			self.props[ ".".join( nsl + [ key ] ) ] = val
	
	# -------------------- #
	# Load a dict
	# -------------------- #
	def loadDict( self, di, ns = list() ):
		"""Load a dictionary."""
		for key, val in di.items():
			if( type( val ) == dict ):
				self.loadDict( val, ns + [ key ] )
			elif( type( val ) == str ):
				self.props[ ".".join( ns + [ key ] ) ] = val
	
	# -------------------- #
	# Defaults
	# -------------------- #
	def loadDefaults( self ):
		"""Load the default dictionary."""
		self.loadDict( PMConfig.defaults )
	
	# -------------------- #
	# toDict
	# -------------------- #
	def toDict( self ):
		di = dict()
		for key, val in self.props.items():
			data = key.split( "." )
			ns = data[:-1]
			key = data[-1]
			ptr = di
			for loc in ns:
				try:
					ptr = ptr[loc]
				except KeyError:
					ptr[loc] = dict()
					ptr = ptr[loc]
			ptr[key] = val
		return di
	
	# -------------------- #
	# dictToConfig
	# -------------------- #
	def dictToConfig( self, di, ns = list() ):
		buff = ""
		for key, val in di.items():
			if( type( val ) == dict ):
				buff += "\t" * len( ns ) + "[" + key + "]\n"
				buff += self.dictToConfig( val, ns + [ key ] )
			elif( type( val ) == str ):
				buff += "\t" * len( ns ) + key + " = " + val + "\n"
		return buff
	
	# -------------------- #
	# Dumps
	# -------------------- #
	def dumpConfiguration( self, pretty = False ):
		if( pretty ):
			di = self.toDict()
			return self.dictToConfig( di )
		else:
			buff = ""
			for prop, val in self.props.items():
				buff += prop + " = " + val + "\n"
			return buff
	
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
