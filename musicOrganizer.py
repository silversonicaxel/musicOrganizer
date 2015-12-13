'''
music organizer
'''

import wx
from libs import music

hApp = wx.App()
music.CMusicOrganizerView()
hApp.MainLoop()