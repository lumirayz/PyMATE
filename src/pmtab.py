import wx
import wx.stc
import os

class PMTab( wx.Panel ):
	"""Tab class."""
	def __init__( self, parent ):
		wx.Panel.__init__( self, parent )
		self.parent = parent
		self.gui = parent.GetParent()
		self.textctrl = wx.stc.StyledTextCtrl( self, wx.ID_ANY )
		self.Bind( wx.stc.EVT_STC_CHANGE, self.onTextChange, self.textctrl )
		self.sizer = wx.BoxSizer()
		self.sizer.Add( self.textctrl, 1, wx.EXPAND )
		self.SetSizer( self.sizer )
		self.file = None
		self.edited = False
	
	def onTextChange( self, event ):
		"""Called on text change."""
		self.edited = True
		self.updateTitle()
	
	def setTitle( self, title ):
		"""Set the tab's title."""
		self.parent.SetPageText( self.gui.getTabIdByContents( self ),
			title )
	
	def updateTitle( self ):
		"""Update the title."""
		if( self.file ):
			title = os.path.basename( self.file )
			if( self.edited ):
				title += " *"
		else:
			title = "**Unsaved**"
		
		self.setTitle( title )
	
	def loadFile( self, f = None ):
		"""Load a file into this tab."""
		if( f == None ):
			if( self.file == None ):
				return #Failure to load anything.
			else:
				f = self.file
		fd = open( f, "r" )
		self.file = f
		self.textctrl.SetText( fd.read() )
		self.edited = False
		self.updateTitle()
		fd.close()
	
	def saveFile( self, f = None ):
		"""Save this tab to a file."""
		if( f == None ):
			if( self.file == None ):
				return #Failure to save anything.
			else:
				f = self.file
		fd = open( f, "w" )
		self.file = f
		self.edited = False
		self.updateTitle()
		fd.write( self.textctrl.GetText() )
		fd.close()
