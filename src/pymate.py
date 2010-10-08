import wx
import os

from pmtab import *

class PyMATE( wx.Frame ):
	def __init__( self ):
		wx.Frame.__init__( self, None, wx.ID_ANY, "PyMATE" )
		self.menubar = wx.MenuBar()
		self.file_menu = wx.Menu()
		self.help_menu = wx.Menu()
		self.edit_menu = wx.Menu()
		self.sizer = wx.BoxSizer()
		self.notebook = wx.Notebook( self, -1, wx.DefaultPosition, wx.DefaultSize, wx.NB_TOP )
		
		self.file_new = self.file_menu.Append( wx.ID_NEW,
			"&New", "Create a new file." )
		self.file_open = self.file_menu.Append( wx.ID_OPEN,
			"&Open" , "Open a file." )
		self.file_save = self.file_menu.Append( wx.ID_SAVE,
			"&Save" , "Save current file." )
		self.file_save_as = self.file_menu.Append( wx.ID_SAVEAS,
			"Save &As" , "Save current file as." )
		self.file_menu.AppendSeparator()
		self.file_close = self.file_menu.Append( wx.ID_CLOSE,
			"&Close" , "Close the current tab." )
		self.file_exit = self.file_menu.Append( wx.ID_EXIT,
			"E&xit" , "Terminate the program." )
		self.menubar.Append( self.file_menu, "&File" )
		self.menubar.Append( self.edit_menu, "&Edit" )
		self.help_about = self.help_menu.Append( wx.ID_ABOUT,
			"&About", "About the program." )
		self.menubar.Append( self.help_menu, "&Help" )
		
		self.Bind( wx.EVT_MENU, self.onNew, self.file_new )
		self.Bind( wx.EVT_MENU, self.onOpen, self.file_open )
		self.Bind( wx.EVT_MENU, self.onSaveNow, self.file_save )
		self.Bind( wx.EVT_MENU, self.onSaveAs, self.file_save_as )
		self.Bind( wx.EVT_MENU, self.onClose, self.file_close )
		self.Bind( wx.EVT_MENU, self.exit, self.file_exit )
		self.Bind( wx.EVT_MENU, self.onAbout, self.help_about )
		
		self.SetMenuBar( self.menubar )
		
		self.sizer.Add( self.notebook, 1, wx.EXPAND )
		self.SetSizer( self.sizer )
	
	def onAbout( self, event ):
		"""Called on about."""
		aboutdlg = wx.MessageDialog( self,
			"MATE rewrite in Python.",
			"About PyMATE" )
		aboutdlg.ShowModal()
		aboutdlg.Destroy()
	
	def onNew( self, event ):
		"""Called on new."""
		tab = self.addTab()
	
	def onClose( self, event ):
		"""Called on close."""
		sel = self.getCurrentTabId()
		if( sel != -1 ):
			self.notebook.DeletePage( sel )
	
	def onOpen( self, event ):
		"""Called on open."""
		fdlg = wx.FileDialog( self, "Open File",  "", "", "*", wx.OPEN )
		if( fdlg.ShowModal() == wx.ID_OK ):
			fn = fdlg.GetFilename()
			dn = fdlg.GetDirectory()
			f = os.path.join( dn, fn )
			if( not self.fileOpened( f ) ):
				tab = self.addTab()
				tab.loadFile( f )
				self.switchToTab( tab )
			else:
				tab = self.getOpenedFileTab( f )
				self.switchToTab( tab )
	
	def onSaveNow( self, event ):
		"""Called on save."""
		if( not self.getCurrentTab() ):
			return
		
		tab = self.getCurrentTab()
		if( tab.file ):
			if( os.path.isfile( tab.file ) ):
				tab.saveFile( tab.file )
			else:
				self.onSaveAs( event )
		else:
			self.onSaveAs( event )
	
	def onSaveAs( self, event ):
		"""Called on "Save As" and saving new files."""
		if( not self.getCurrentTab() ):
			return
		
		fdlg = wx.FileDialog( self, "Save File",  "", "", "*", wx.SAVE )
		if( fdlg.ShowModal() == wx.ID_OK ):
			tab = self.getCurrentTab()
			fn = fdlg.GetFilename()
			dn = fdlg.GetDirectory()
			f = os.path.join( dn, fn )
			tab.saveFile( f )
	
	def exit( self, event ):
		"""Exit program."""
		self.Close()
	
	def fileOpened( self, f ):
		"""Returns wether a file is opened."""
		tc = self.notebook.GetPageCount()
		for i in range( tc ):
			tab = self.notebook.GetPage( i )
			if( tab.file and f ):
				if( os.path.samefile ( tab.file, f ) ):
					return True
		return False
	
	def getOpenedFileTab( self, f ):
		"""Returns the tab of a currently opened file."""
		tc = self.notebook.GetPageCount()
		for i in range( tc ):
			tab = self.notebook.GetPage( i )
			if( tab.file and f ):
				if( tab.file == f ):
					return tab
		return None
	
	def getOpenedFileTabId( self, f ):
		"""Returns the tab ID of a currently opened file."""
		tc = self.notebook.GetPageCount()
		for i in range( tc ):
			tab = self.notebook.GetPage( i )
			if( tab.file and f ):
				if( tab.file == f ):
					return i
		return -1
	
	def getCurrentTabId( self ):
		"""Get the Id of the current tab."""
		return self.notebook.GetSelection()
	
	def getCurrentTab( self ):
		"""Get the current tab of the wx.Notebook"""
		return self.notebook.GetCurrentPage()
	
	def getTabIdByContents( self, tab ):
		"""Get a tab Id based on its contents."""
		tc = self.notebook.GetPageCount()
		for i in range( tc ):
			tb = self.notebook.GetPage( i )
			if( tb == tab ):
				return i
		return -1
	
	def addTab( self ):
		"""Add a PMTab to the wx.Notebook and return it."""
		tab = PMTab( self.notebook )
		self.notebook.AddPage( tab, "**Unsaved**" )
		return tab
	
	def switchToTab( self, tab ):
		"""Switches to a set tab."""
		tc = self.notebook.GetPageCount()
		for i in range( tc ):
			tb = self.notebook.GetPage( i )
			if( tb == tab ):
				self.notebook.SetSelection( i )
				return		
	
	def show( self ):
		"""Show the window."""
		self.Show()
