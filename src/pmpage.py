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

# -------------------- #
# Class PMPage
# -------------------- #
class PMPage( wx.Panel ):
	"""Class for handling pages."""
	
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
	
	def initialize( self ):
		self.updateTitle()
	
	# -------------------- #
	# GUI init
	# -------------------- #
	def buildGUI( self ):
		self.stc = wx.stc.StyledTextCtrl( self, wx.ID_ANY )
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
			title = os.path.basename( self.file )
			if( self.edited ):
				title += " *"
		else:
			title = "**Unsaved**"
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
