# -------------------- #
# PMGui.py
# 
# Defines the PMGui class, which is used for all GUI calls that relate to the
# main window.
# -------------------- #

# -------------------- #
# Imports
# -------------------- #
import wx
import os
import pmpage

# -------------------- #
# Class PMGui
# -------------------- #
class PMGui( wx.Frame ):
	"""Class for handling the main window."""
	
	# -------------------- #
	# Class vars
	# -------------------- #
	about = "PyMATE\n\n"\
		\
		"Python Minimalistic and Awesome Text Editor.\n\n"\
		\
		"An editor for people that don't like lots of buttons cluttering "\
		"their workspace.\n\n"\
		\
		"Copyright (C) 2010 Lumirayz\n"\
		"License GPLv3+: GNU GPL version 3 or later "\
		"<http://gnu.org/licenses/gpl.html>.\n"\
		"This is free software: you are free to change and redistribute it.\n"\
		"There is NO WARRANTY, to the extent permitted by law."
	
	TabPositionTable = {
		"top": wx.NB_TOP,
		"bottom": wx.NB_BOTTOM,
		"left": wx.NB_LEFT,
		"right": wx.NB_RIGHT
	}
	
	TabTypeTable = {
		"notebook": wx.Notebook,
		"listbook": wx.Listbook,
		"treebook": wx.Treebook,
		"choicebook": wx.Choicebook
	}
	
	# -------------------- #
	# Init	
	# -------------------- #
	def __init__( self, config ):
		self.app = wx.App()
		wx.Frame.__init__( self, None, wx.ID_ANY, "PyMATE" )
		self.conf = config
		self.buildInit()
		self.configure()
		for arg in self.conf.args:
			if( os.path.isfile( arg ) ):
				page = self.addPageFromFile( arg )
				self.switchToPage( page )
	
	def configure( self ):
		pass
	
	# -------------------- #
	# Main Loop
	# -------------------- #
	def invokeMainLoop( self ):
		"""Start the main loop."""
		self.show()
		self.app.MainLoop()
	
	# -------------------- #
	# Functions to create the GUI
	# -------------------- #
	def buildInit( self ):
		"""Calls the GUI building functions."""
		self.buildGui()
		self.buildMenu()
		self.buildNotebook()
		self.bindEvents()
		self.SetMenuBar( self.menubar )
		self.sizer.Add( self.notebook, 1, wx.EXPAND )
		self.SetSizer( self.sizer )
	
	def buildGui( self ):
		"""Builds the main GUI."""
		self.menubar = wx.MenuBar()
		self.file_menu = wx.Menu()
		self.help_menu = wx.Menu()
		self.edit_menu = wx.Menu()
		self.sizer = wx.BoxSizer()
	
	def buildMenu( self ):
		"""Builds the menus."""
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
		self.edit_undo = self.edit_menu.Append( wx.ID_UNDO,
			"&Undo" , "Undo last action." )
		self.edit_redo = self.edit_menu.Append( wx.ID_REDO,
			"&Redo" , "Redo undone action." )
		self.menubar.Append( self.edit_menu, "&Edit" )
		self.help_about = self.help_menu.Append( wx.ID_ABOUT,
			"&About", "About the program." )
		self.menubar.Append( self.help_menu, "&Help" )
	
	def buildNotebook( self ):
		"""Builds the Notebook."""
		typ = self.conf.getProperty( "editor.tab.type" ).lower()
		try:
			typ = PMGui.TabTypeTable[ typ ]
		except KeyError:
			typ = wx.Notebook
		pos = self.conf.getProperty( "editor.tab.position" ).lower()
		try:
			pos = PMGui.TabPositionTable[ pos ]
		except KeyError:
			pos = wx.NB_LEFT
		self.notebook = typ( self, -1, style = pos )
		
	
	def bindEvents( self ):
		"""Binds the events."""
		self.Bind( wx.EVT_MENU, self.evtMenuNew, self.file_new )
		self.Bind( wx.EVT_MENU, self.evtMenuOpen, self.file_open )
		self.Bind( wx.EVT_MENU, self.evtMenuSave, self.file_save )
		self.Bind( wx.EVT_MENU, self.evtMenuSaveAs, self.file_save_as )
		self.Bind( wx.EVT_MENU, self.evtMenuClose, self.file_close )
		self.Bind( wx.EVT_MENU, self.evtMenuExit, self.file_exit )
		self.Bind( wx.EVT_MENU, self.evtMenuAbout, self.help_about )
		self.Bind( wx.EVT_MENU, self.evtMenuUndo, self.edit_undo )
		self.Bind( wx.EVT_MENU, self.evtMenuRedo, self.edit_redo )
	
	# -------------------- #
	# Util functions related to the GUI
	# -------------------- #
	def show( self ):
		"""Show the Frame."""
		self.Show()
	
	# -------------------- #
	# Event handlers
	# -------------------- #
	
	# - Related to document management
	def evtMenuNew( self, evt ):
		page = self.addPage()
		self.switchToPage( page )
	
	def evtMenuOpen( self, evt ):
		f = self.viewFileDialog( "Open File", "*", wx.OPEN )
		if( f ):
			if( self.isFileOpened( f ) ):
				page = self.getOpenedFilePage( f )
				self.switchToPage( page )
			else:
				page = self.addPageFromFile( f )
				self.switchToPage( page )
	
	def evtMenuSave( self, evt ):
		page = self.getCurrentPage()
		if( not page ):
			return
		if( page.file ):
			if( os.path.isfile( page.file ) ):
				page.saveFile()
			else:
				self.evtMenuSaveAs( evt )
		else:
			self.evtMenuSaveAs( evt )
	
	def evtMenuSaveAs( self, evt ):
		page = self.getCurrentPage()
		if( not page ):
			return
		f = self.viewFileDialog( "Save File", "*", wx.SAVE )
		if( f ):
			page.saveFile( f )
	
	def evtMenuClose( self, evt ):
		sel = self.getCurrentPage()
		if( sel ):
			self.removePage( sel )
	
	# - Related to text editing
	def evtMenuUndo( self, evt ):
		sel = self.getCurrentPage()
		if( sel ):
			sel.invokeUndo()
	
	def evtMenuRedo( self, evt ):
		sel = self.getCurrentPage()
		if( sel ):
			sel.invokeRedo()
	
	# - Related to the program
	def evtMenuExit( self, evt ):
		self.Close()
	
	def evtMenuAbout( self, evt ):
		self.viewAbout()
	
	# -------------------- #
	# Dialogs
	# -------------------- #
	def viewAbout( self ):
		"""View about dialog."""
		adlg = wx.MessageDialog( self, PMGui.about, "About PyMATE", wx.OK )
		adlg.ShowModal()
		adlg.Destroy()
		pass
	
	def viewCloseRequest( self ):
		"""Annoy the user by asking whether to close the page."""
		crdlg = wx.MessageDialog( self, "There are unsaved changes, really close?",
			"Confirmation",
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION )
		if( crdlg.ShowModal() == wx.ID_YES ):
			crdlg.Destroy()
			return 1
		else:
			crdlg.Destroy()
			return 0
	
	def viewFileDialog( self, title, mask, mode ):
		"""Ask for a file."""
		fdlg = wx.FileDialog( self, title,  "", "", mask, mode )
		if( fdlg.ShowModal() == wx.ID_OK ):
			fn = fdlg.GetFilename()
			dn = fdlg.GetDirectory()
			fdlg.Destroy()
			return os.path.join( dn, fn )
		else:
			fdlg.Destroy()
			return None
	
	# -------------------- #
	# Util functions related to pages
	# -------------------- #
	def addPage( self ):
		"""Add a page to the editor."""
		tmode = self.conf.getProperty( "editor.tab.mode" )
		tmode = tmode.lower()
		if( tmode == "full" or tmode == "workspace" ):
			page = pmpage.PMPage( self.notebook, self )
			self.notebook.AddPage( page, "" )
			page.configure()
			return page
		elif( tmode == "none" ):
			#Reserved for no-tab mode.
			pass
	
	def addPageFromFile( self, f ):
		"""Add a page to the editor and load a file."""
		page = self.addPage()
		page.loadFile( f )
		return page
	
	def removePage( self, page ):
		"""Remove a page from the editor."""
		page.invokeCloseRequest()
	
	def removePageId( self, pageid ):
		"""Remove a page id from the editor."""
		self.removePage( self.notebook.GetPage( pageid ) )
	
	def forceRemovePage( self, page ):
		"""Forcefully remove a page from the editor."""
		pageid = self.getPageId( page )
		if( pageid != -1 ):
			self.forceRemovePageId( pageid )
	
	def forceRemovePageId( self, pageid ):
		"""Forcefully remove a page id from the editor."""
		self.notebook.DeletePage( pageid )
	
	def setPageTitle( self, page, title ):
		"""Set page title."""
		pageid = self.getPageId( page )
		if( pageid != -1 ):
			self.setPageIdTitle( pageid, title )
	
	def setPageIdTitle( self, pageid, title ):
		"""Set page id title."""
		self.notebook.SetPageText( pageid, title )
		
	def switchToPage( self, page ):
		"""Switches to the specified page."""
		pc = self.notebook.GetPageCount()
		for i in range( pc ):
			pag = self.notebook.GetPage( i )
			if( pag == page ):
				self.notebook.SetSelection( i )
				return
	
	def switchToPageId( self, i ):
		"""Switches to the specified page id."""
		self.notebook.SetSelection( i )
	
	def getCurrentPage( self ):
		"""Get the currently open page."""
		return self.notebook.GetCurrentPage()
	
	def getCurrentPageId( self ):
		"""Get the currently open page id."""
		return self.notebook.GetSelection()
	
	def getPage( self, pageid ):
		"""Returns the page with the specified id."""
		return self.notebook.GetPage( pageid )
	
	def getPageId( self, page ):
		"""Returns the id of the specified page, if not found: -1."""
		pc = self.notebook.GetPageCount()
		for i in range( pc ):
			pag = self.notebook.GetPage( i )
			if( pag == page ):
				return i
		return -1
	
	def isFileOpened( self, f ):
		"""Returns whether a file is opened."""
		pc = self.notebook.GetPageCount()
		for i in range( pc ):
			page = self.notebook.GetPage( i )
			if( page.file and f ):
				if( page.file == f ):
					return True
		return False
	
	def getOpenedFilePage( self, f ):
		"""Returns the page of the opened file if this file is opened, else None."""
		pc = self.notebook.GetPageCount()
		for i in range( pc ):
			page = self.notebook.GetPage( i )
			if( page.file and f ):
				if( page.file == f ):
					return page
		return None
	
	def getOpenedFilePageId( self, f ):
		"""Returns the page id of the opened file if this file is opened, else -1."""
		pc = self.notebook.GetPageCount()
		for i in range( pc ):
			page = self.notebook.GetPage( i )
			if( page.file and f ):
				if( page.file == f ):
					return i
		return -1
