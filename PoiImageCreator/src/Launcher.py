'''
Created on 12 Jan 2017

@author: Janion
'''

import wx
from src.gui.Gui import Window

if __name__ == '__main__':
    app = wx.App()
    fr = Window(None, -1, 'Image encryptor')
    fr.Show()
    app.MainLoop()
    
    