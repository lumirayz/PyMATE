# -------------------- #
# PMInit.py
#
# Initializes PyMATE.
# -> Parses command-line arguments.
# -> Loads configuration.
# -> Switches to PMGui.
# -------------------- #

# -------------------- #
# Imports
# -------------------- #
from optparse import OptionParser
import pmconfig
import pmgui
import os

# -------------------- #
# Init
# -------------------- #
rules = list()

# -------------------- #
# Functions
# -------------------- #
def showVersionInfo():
	"""Function to show version information."""
	print( "PyMATE\n\n"\
			"Copyright (C) 2010 Lumirayz\n"\
			"License GPLv3+: GNU GPL version 3 or later "\
			"<http://gnu.org/licenses/gpl.html>.\n"\
			"This is free software: you are free to change and redistribute it.\n"\
			"There is NO WARRANTY, to the extent permitted by law." )

def add_config( opt, optstr, var, parser ):
	"""Add a rule to the configuration."""
	rules.append( var )

# -------------------- #
# OptionParser
# -------------------- #
parser = OptionParser()

parser.add_option( "-v", "--version", dest = "version", action = "store_true",
	default = False, help = "show version info and exit" )
parser.add_option( "-f", "--set-config-file", dest = "configFile",
	help = "Set the configuration file.", default = None )
parser.add_option( "-c", "--add-config",
	callback = add_config, action = "callback", type = str,
	help = "Add additional configuration without editing config file." )

# -------------------- #
# Run
# -------------------- #
if( __name__ == "__main__" ):
	( options, args ) = parser.parse_args()
	
	conf = pmconfig.PMConfig()
	conf.loadDefaults()
	
	if( options.version ):
		showVersionInfo()
		exit()
	
	confpaths = [
		"/usr/share/pymate/pymate.conf",
		"~/.config/pymate/pymate.conf",
		os.path.abspath( os.path.dirname( __file__ ) ) + "/pymate.conf"
	]
	
	for path in confpaths:
		if( os.path.isfile( path ) ):
			conf.parseFile( path )
	
	configFile = options.configFile
	if( configFile ):
		
		if( os.path.isfile( configFile ) ):
			conf.parseFile( configFile )
		else:
			print( "error: Specified configuration file( " + configFile + " ) doesn't exist." )
			exit()
	
	conf.args = args
	conf.opts = options
	
	for rule in rules:
		conf.parseLine( rule )
	
	gui = pmgui.PMGui( conf )
	gui.invokeMainLoop()
