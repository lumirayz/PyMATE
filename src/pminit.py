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
configFile = ""

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

def set_config_file( opt, optstr, var, parser ):
	configFile = var

# -------------------- #
# OptionParser
# -------------------- #
parser = OptionParser()

parser.add_option( "-v", "--version", dest = "version", action = "store_true",
	default = False, help = "show version info and exit" )
parser.add_option( "-f", "--set-config-file",
	callback = set_config_file, action = "callback", type = str,
	help = "Set the configuration file." )
parser.add_option( "-c", "--add-config",
	callback = add_config, action = "callback", type = str,
	help = "Add additional configuration without editing config file." )

# -------------------- #
# Run
# -------------------- #
if( __name__ == "__main__" ):
	( options, args ) = parser.parse_args()
	
	conf = pmconfig.PMConfig()
	
	confpaths = [
		"/etc/pymate.conf",
		"~/.config/pymate/pymate.conf"
	]
	
	confpaths.append( configFile )
	
	for path in confpaths:
		if( os.path.isfile( path ) ):
			conf.parseFile( path )
	
	conf.args = args
	conf.opts = options
	
	for rule in rules:
		conf.parseLine( rule )
	
	if( options.version ):
		showVersionInfo()
		exit()
	
	gui = pmgui.PMGui( conf )
	gui.invokeMainLoop()
