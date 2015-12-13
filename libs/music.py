'''
class about gui operations
'''

import os
import wx
from libs import files

class CMusicOrganizerView(object):
    _S_ICON_NORMAL = 'ready'
    _S_ICON_OK = 'ok'
    _S_ICON_ERROR = 'error'
    
    sMusicRepository = ''
    sMusicSource = ''
    aMusicSongs = []
    bCheckSourceDirectoryOnlySongs = True

    def __init__(self):
        ''' font '''
        self.hFontLabel = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Arial')

        '''frame'''
        self.hFrame = wx.Frame(None, wx.ID_ANY, 'Music Organizer 1.0', size=(650, 450), style=wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.hFrame.Center()
        
        '''panel'''
        self.hPanel = wx.Panel(self.hFrame, wx.ID_ANY)

        '''music repository box'''
        sGuessedRepositoryTextfield = files.CFileSystemOperations.getRepositoryDirectory()
        self.hRepositoryBox = wx.BoxSizer(wx.HORIZONTAL)
        self.hRepositoryLabel = wx.StaticText(self.hPanel, label = 'Music Repository')
        self.hRepositoryTextfield = wx.TextCtrl(self.hPanel)
        self.hRepositoryTextfield.SetFont(self.hFontLabel)
        self.hRepositoryTextfield.Bind(wx.EVT_TEXT, self.forceDefaultStyle)
        self.hRepositoryTextfield.AppendText(sGuessedRepositoryTextfield)
        self.hRepositoryBox.Add(self.hRepositoryLabel, flag=wx.RIGHT, border=8)
        self.hRepositoryBox.Add(self.hRepositoryTextfield, proportion=1)

        '''music source box'''
        self.hSourceBox = wx.BoxSizer(wx.HORIZONTAL)
        self.hSourceLabel = wx.StaticText(self.hPanel, label = 'Music Source')
        self.hSourceTextfield = wx.TextCtrl(self.hPanel)
        self.hSourceTextfield.SetFont(self.hFontLabel)
        self.hSourceTextfield.Bind(wx.EVT_TEXT, self.forceDefaultStyle)
        self.hSourceBox.Add(self.hSourceLabel, flag=wx.RIGHT, border=8)
        self.hSourceBox.Add(self.hSourceTextfield, proportion=1)
        
        '''music grid songs'''
        self.hSongsList = wx.ListCtrl(self.hPanel, size=(-1,285), style=wx.LC_REPORT|wx.BORDER_SUNKEN|wx.LC_VRULES)
        self.hSongsList.InsertColumn(0, 'N', wx.LIST_FORMAT_LEFT, 50)
        self.hSongsList.InsertColumn(1, 'Track', wx.LIST_FORMAT_LEFT, 180)
        self.hSongsList.InsertColumn(2, 'Album', wx.LIST_FORMAT_LEFT, 180)
        self.hSongsList.InsertColumn(3, 'Artist', wx.LIST_FORMAT_LEFT, 180)
        self.hSongsList.InsertColumn(4, 'Year', wx.LIST_FORMAT_LEFT, 50)

        '''buttons'''
        self.hButtonAnalyze = wx.Button(self.hPanel, label = 'Analyze')
        self.hButtonAnalyze.Bind(wx.EVT_BUTTON, self.handlerAnalyze)
        self.hButtonOrganize = wx.Button(self.hPanel, label = 'Organize')
        self.hButtonOrganize.Bind(wx.EVT_BUTTON, self.handlerOrganize)
        self.hButtonOrganize.Disable()
        self.hButtonReset = wx.Button(self.hPanel, label = 'Reset')
        self.hButtonReset.Bind(wx.EVT_BUTTON, self.handlerReset)
        self.hButtonsBox = wx.BoxSizer(wx.HORIZONTAL)
        self.hButtonsBox.Add(self.hButtonAnalyze, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.hButtonsBox.Add(self.hButtonOrganize, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.hButtonsBox.Add(self.hButtonReset, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        
        '''footer bar'''
        self.hFooterImagePanel = wx.Panel(self.hPanel, wx.ID_ANY)
        self.hFooterImage = wx.StaticBitmap(self.hFooterImagePanel)
        self.hFooterImage.SetPosition((1,1))
        self.hFooterImage.SetBitmap(wx.Bitmap("img/" + self._S_ICON_NORMAL + ".png"))
        self.hFooterStatusLabel = wx.StaticText(self.hPanel, label = 'Ready')
        self.hFooterBox = wx.BoxSizer(wx.HORIZONTAL)
        self.hFooterBox.Add(self.hFooterImagePanel, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.hFooterBox.Add(self.hFooterStatusLabel, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        
        
        '''container'''
        self.hPanelBox = wx.BoxSizer(wx.VERTICAL)
        self.hPanelBox.Add(self.hRepositoryBox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 5)
        self.hPanelBox.Add(self.hSourceBox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 5)   
        self.hPanelBox.Add(self.hSongsList, 0, wx.ALL | wx.EXPAND, 5)
        self.hPanelBox.Add(self.hButtonsBox)
        self.hPanelBox.Add(self.hFooterBox)
        
        self.hPanel.SetSizer(self.hPanelBox)
        
        '''footer bar'''
        self.hFrame.CreateStatusBar()
        self.hFrame.SetStatusText("Music Organizer 1.0")
        self.hFrame.Show(True)
        
    
    def handlerAnalyze(self, event):
        try:
            '''destination path'''
            self.sMusicRepository = self.hRepositoryTextfield.GetValue()
            self.hFileSystemOp = files.CFileSystemOperations(self.sMusicRepository)
            
            '''directory files path'''
            self.sMusicSource = self.hSourceTextfield.GetValue()
            aListSongs = self.hFileSystemOp.readDirectorySongs(self.sMusicSource)
            
            '''empty song list'''
            self.hSongsList.DeleteAllItems()
            
            # songs data to rename the file system files
            self.aMusicSongs = self.hFileSystemOp.getDataSongs(aListSongs)
            nIndex = 0
            for aSong in self.aMusicSongs:
                self.hSongsList.InsertStringItem(nIndex, aSong[self.hFileSystemOp._N_POS_NUMTRACK])
                self.hSongsList.SetStringItem(nIndex, 1, aSong[self.hFileSystemOp._N_POS_TITLE])
                self.hSongsList.SetStringItem(nIndex, 2, aSong[self.hFileSystemOp._N_POS_ALBUM])
                self.hSongsList.SetStringItem(nIndex, 3, aSong[self.hFileSystemOp._N_POS_ARTIST])
                self.hSongsList.SetStringItem(nIndex, 4, aSong[self.hFileSystemOp._N_POS_YEAR])
                
                if nIndex % 2:
                    self.hSongsList.SetItemBackgroundColour(nIndex, (230,230,230))
                else:
                    self.hSongsList.SetItemBackgroundColour(nIndex, (255, 250, 250))
                nIndex += 1
                
            for nIndexColumn in range(self.hSongsList.GetColumnCount()):
                self.hSongsList.SetColumnWidth(nIndexColumn, wx.LIST_AUTOSIZE)
            
            self.hButtonOrganize.Enable()
            self.manageFooterStatus(self._S_ICON_NORMAL, "Directory analyzed.")
        except:
            self.hSongsList.DeleteAllItems()
            self.hButtonOrganize.Disable()
            self.manageFooterStatus(self._S_ICON_ERROR, "Error during the analysis of the directory.")
        return True
        
    def handlerOrganize(self, event):
        try:
            self.hSourceTextfield.SetValue(self.sMusicSource) 
            self.hFileSystemOp.manageDirectorySongs(self.sMusicSource, self.aMusicSongs)
            self.hButtonOrganize.Disable()
            self.hButtonReset.Disable()
            
            if(self.hFileSystemOp.checkSourceDirectoryOnlySongs()):
                sOrganizedDirMessage = "Directory organized."
            else:
                sOrganizedDirMessage = "Directory organized. Some files are still in the source Directory."
            self.manageFooterStatus(self._S_ICON_OK, sOrganizedDirMessage)
        except:
            self.manageFooterStatus(self._S_ICON_ERROR, "Error during the organization of the directory.")            
        return True
        
    def handlerReset(self, event):
        self.hSourceTextfield.SetValue('')
        self.hSongsList.DeleteAllItems()
        self.hButtonOrganize.Disable()
        self.manageFooterStatus(self._S_ICON_NORMAL, "Ready.")
        return True




    def forceDefaultStyle(self, event):
        hEventObject = event.GetEventObject()
        hEventObject.SetStyle(0, len(self.hRepositoryTextfield.GetValue()), wx.TextAttr(wx.BLACK))
        hEventObject.SetFont(self.hFontLabel)
    
    
    def manageFooterStatus(self, sIcon, sMessage):
        if os.path.isfile('img/' + sIcon + '.png'):
            sIconFooter = 'img/' + sIcon + '.png'
        else:
            sIconFooter = 'img/' + self._S_ICON_NORMAL
        self.hFooterImage.SetBitmap(wx.Bitmap(sIconFooter))
        self.hFooterStatusLabel.SetLabel(sMessage)
        
