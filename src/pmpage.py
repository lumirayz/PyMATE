# -------------------- #
# PMPage.py
#
# Defines the PMPage class, which is a wrapper around wx.Panel that contains a
# wx.stc.StyledTextCtrl.
# -------------------- #

# -------------------- #
# Imports
# -------------------- #
import wx
import wx.stc
import os
import pmconfig

# -------------------- #
# Class PMPage
# -------------------- #
class PMPage( wx.Panel ):
	"""Class for handling pages."""
	
	# -------------------- #
	# Class variables
	# -------------------- #
	wrap_modes = {
		"none": wx.stc.STC_WRAP_NONE,
		"word": wx.stc.STC_WRAP_WORD
	}
	
	long_line_markers = {
		"none": wx.stc.STC_EDGE_NONE,
		"line": wx.stc.STC_EDGE_LINE,
		"background": wx.stc.STC_EDGE_BACKGROUND
	}
	
	# -------------------- #
	# Init
	# -------------------- #
	def __init__( self, parent, gui ):
		wx.Panel.__init__( self, parent )
		self.gui = gui
		self.conf = self.gui.conf
		self.edited = False
		self.file = None
		self.buildGUI()
		self.bindEvents()
	
	def configure( self ):
		self.updateTitle()
		wm = self.conf.getProperty( "editor.cosmetic.wrap_mode" ).lower()
		try:
			self.stc.SetWrapMode( PMPage.wrap_modes[wm] )
		except KeyError:
			pass #Invalid wrap_mode!
		# -- DOESN'T WORK --
		bkg = self.conf.getProperty( "editor.cosmetic.background_color" )
		color = wx.Colour()
		color.SetFromName( bkg )
		self.stc.SetBackgroundColour( color )
		# --
		self.stc.SetIndentationGuides(
			bool( int( self.conf.getProperty( "editor.cosmetic.indentation_guides" ) ) )
		)
		llm = self.conf.getProperty( "editor.cosmetic.longline.marker" ).lower()
		try:
			self.stc.SetEdgeMode( PMPage.long_line_markers[llm] )
			lll = int( self.conf.getProperty( "editor.cosmetic.longline.length" ) )
			self.stc.SetEdgeColumn( lll )
			llc = self.conf.getProperty( "editor.cosmetic.longline.color" )
			color = wx.Colour()
			color.SetFromName( llc )
			self.stc.SetEdgeColour( color )
		except KeyError:
			pass
	
	# -------------------- #
	# GUI init
	# -------------------- #
	def buildGUI( self ):
		self.stc = wx.stc.StyledTextCtrl( self, wx.ID_ANY )
		
		if( self.conf.getProperty( "editor.cosmetic.line_numbers" ) == "1" ):
			self.stc.SetMarginType( 1, wx.stc.STC_MARGIN_NUMBER )
		
		self.sizer = wx.BoxSizer()
		self.sizer.Add( self.stc, 1, wx.EXPAND )
		self.SetSizer( self.sizer )
	
	def bindEvents( self ):
		self.Bind( wx.stc.EVT_STC_CHANGE, self.evtSTCOnTextChange, self.stc )
	
	# -------------------- #
	# Event Handlers
	# -------------------- #
	def evtSTCOnTextChange( self, evt ):
		self.edited = True
		self.updateTitle()
	
	# -------------------- #
	# Util function related to title
	# -------------------- #
	def setTitle( self, title ):
		"""Set the page's title."""
		self.gui.setPageTitle( self, title )
	
	def updateTitle( self ):
		"""Updates the page's title."""
		if( self.file ):
			if( self.conf.getProperty( "editor.tab.show_full_path" ) == "1" ):
				title = os.path.abspath( self.file )
			else:
				title = os.path.basename( self.file )
			if( self.edited ):
				title += " *"
		else:
			title = "**Unsaved**"
		mlen = int( self.conf.getProperty( "editor.tab.max_name_length" ) )
		if( len( title ) > mlen ):
			title = title[:mlen - 3] + "..."
		
		self.setTitle( title )
	
	# -------------------- #
	# Invokes from PMGui
	# -------------------- #
	def invokeUndo( self ):
		self.stc.Undo()
	
	def invokeRedo( self ):
		self.stc.Redo()
	
	def invokeCloseRequest( self ):
		if( self.edited ):
			answer = self.gui.viewCloseRequest()
			if( answer == 0 ): #Cancel
				pass
			elif( answer == 1 ): #Just close
				self.gui.forceRemovePage( self )
		else:
			self.gui.forceRemovePage( self )
	
	# -------------------- #
	# File saving/loading
	# -------------------- #
	def loadFile( self, f = None ):
		"""Load a file into this page, or reload if nothing specified."""
		if( f == None ):
			if( self.file == None ):
				return
			else:
				f = self.file
		fd = open( f, "r" )
		self.file = f
		self.stc.SetText( fd.read() )
		self.edited = False
		self.updateTitle()
		fd.close()
	
	def saveFile( self, f = None ):
		"""Save this page to a file, or the current file if no file specified."""
		if( f == None ):
			if( self.file == None ):
				return
			else:
				f = self.file
		fd = open( f, "w" )
		self.file = f
		self.edited = False
		self.updateTitle()
		fd.write( self.stc.GetText() )
		fd.close()
