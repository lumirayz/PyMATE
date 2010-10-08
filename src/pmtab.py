import wx
import os

class PMTab( wx.Panel ):
	"""Tab class."""
	def __init__( self, parent ):
		wx.Panel.__init__( self, parent )
		self.parent = parent
		self.textctrl = wx.TextCtrl( self, style = wx.TE_MULTILINE )
		self.Bind( wx.EVT_TEXT, self.onTextChange, self.textctrl )
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
		self.parent.SetPageText( self.parent.GetParent().getTabIdByContents( self ) , title )
	
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
		self.textctrl.SetValue( fd.read() )
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
		fd.write( self.textctrl.GetValue() )
		fd.close()
