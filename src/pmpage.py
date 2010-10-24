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
	
	view_whitespace_modes = {
		"always": wx.stc.STC_WS_VISIBLEALWAYS,
		"after_indent": wx.stc.STC_WS_VISIBLEAFTERINDENT,
		"never": wx.stc.STC_WS_INVISIBLE
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
		self.titleUpdate = True
		self.buildGUI()
		self.bindEvents()
	
	def configure( self ):
		self.updateTitle()
		wm = self.conf.getProperty( "editor.cosmetic.wrap_mode" ).lower()
		try:
			self.stc.SetWrapMode( PMPage.wrap_modes[wm] )
		except KeyError:
			pass #Invalid wrap_mode!
		ts = int( self.conf.getProperty( "editor.indent.tabsize" ) )
		self.stc.SetTabWidth( ts )
		# -- DOESN'T WORK --
		bkg = self.conf.getProperty( "editor.cosmetic.background_color" )
		color = wx.Colour()
		color.SetFromName( bkg )
		self.stc.SetBackgroundColour( color )
		# --
		self.stc.SetIndentationGuides(
			bool( int( self.conf.getProperty( "editor.cosmetic.indentation_guides" ) ) )
		)
		self.stc.SetViewEOL(
			bool( int( self.conf.getProperty( "editor.cosmetic.view_eol" ) ) )
		)
		vw = self.conf.getProperty( "editor.cosmetic.view_whitespace" ).lower()
		try:
			self.stc.SetViewWhiteSpace( PMPage.view_whitespace_modes[ vw ] )
		except KeyError:
			pass
		self.stc.SetUseTabs(
			not bool( int( self.conf.getProperty( "editor.indent.spaces" ) ) )
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
		self.auto_indent = bool( int( self.conf.getProperty( "editor.indent.auto" ) ) )
	
	# -------------------- #
	# GUI init
	# -------------------- #
	def buildGUI( self ):
		self.stc = wx.stc.StyledTextCtrl( self, wx.ID_ANY )
		
		self.stc.StyleSetFont( 0, wx.Font( 8, wx.FONTFAMILY_MODERN,
			wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0,
				self.conf.getProperty( "editor.font.face" ),
			wx.FONTENCODING_SYSTEM ) );
		
		if( self.conf.getProperty( "editor.cosmetic.line_numbers" ) == "1" ):
			self.stc.SetMarginType( 1, wx.stc.STC_MARGIN_NUMBER )
		
		self.sizer = wx.BoxSizer()
		self.sizer.Add( self.stc, 1, wx.EXPAND )
		self.SetSizer( self.sizer )
	
	def bindEvents( self ):
		self.Bind( wx.stc.EVT_STC_CHANGE, self.evtSTCOnTextChange, self.stc )
		self.Bind( wx.stc.EVT_STC_CHARADDED, self.evtSTCOnCharAdded, self.stc )
	
	# -------------------- #
	# Event Handlers
	# -------------------- #
	def evtSTCOnTextChange( self, evt ):
		self.edited = True
		if( self.titleUpdate ):
			self.updateTitle()
	
	def evtSTCOnCharAdded( self, evt ):
		if( self.auto_indent and chr( evt.GetKey() ) == "\n" ):
			curline = self.stc.GetCurrentLine()
			self.stc.SetLineIndentation( curline, self.stc.GetLineIndentation( curline - 1 ) )
			pos = self.stc.GetLineIndentPosition( curline )
			self.stc.SetAnchor( pos )
			self.stc.SetCurrentPos( pos )
	
	# -------------------- #
	# Util
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
	
	def setText( self, text ):
		"""Set the contents of the page."""
		self.stc.SetText( text )
	
	def setTitleUpdate( self, update ):
		"""Set whether the title should update automatically."""
		self.titleUpdate = update
	
	def setEdited( self, edited ):
		"""Set whether this page should be considered modified."""
		self.edited = edited
		if( self.titleUpdate ):
			self.updateTitle()
	
	# -------------------- #
	# Invokes from PMGui
	# -------------------- #
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
		self.setText( fd.read() )
		self.edited = False
		self.titleUpdate = True
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
		self.titleUpdate = True
		self.updateTitle()
		fd.write( self.stc.GetText() )
		fd.close()
