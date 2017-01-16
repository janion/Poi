'''
Created on 13 Jun 2016

@author: Janion
'''
import wx
import wx.lib.scrolledpanel as scrolled
from scipy.misc import fromimage
from scipy.misc import toimage
import numpy as np

class EditorWindow(wx.Frame):
     
    def __init__(self, parent, idd, title, pix=(16, 16), img=None, action=None):
        wx.Frame.__init__(self, parent, idd, title, size=(500, 670))
        self.panel = wx.Panel(self, -1)
        self.scrollPanel = scrolled.ScrolledPanel(self.panel)
        self.innerPanel = wx.Panel(self.scrollPanel, -1)
        
        self.action = action
        
        innerSizer = wx.BoxSizer(wx.VERTICAL)
        innerSizer.Add(self.innerPanel, 1, wx.ALL|wx.EXPAND, 5)
        self.scrollPanel.SetSizer(innerSizer)
        
        self.pixSize = 25
        self.createPixels(pix, img)
        
        self.resetScrolledPane()
        self.scrollPanel.SetScrollRate(10, 10)
        
        doneBtn = wx.Button(self.panel, -1, "Done")
        doneBtn.Bind(wx.EVT_BUTTON, self.done)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.createMenuPanel(), 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.createRecentColourPanel(), 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.scrollPanel, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(doneBtn, 0, wx.ALL|wx.EXPAND, 10)
        
        self.panel.SetSizer(sizer)
        
################################################################################

    def done(self, event):
        if self.action != None:
            newData = np.zeros((len(self.btns[0]), (len(self.btns)), 3))
            for x in xrange(len(self.btns)):
                for y in xrange(len(self.btns[x]) ):
                    newData[y, x] = self.btns[x][y].GetBackgroundColour()
                     
            self.action(toimage(newData))
            self.Destroy()
        
################################################################################

    def resetScrolledPane(self):
        self.scrollPanel.SetVirtualSize((10 + (self.pixX * self.pixSize), 10 + (self.pixY * self.pixSize)))
        
################################################################################

    def addColumn(self, event):
        self.pixX += 1
        self.btns.append([None for y in xrange(self.pixY)])
        
        x = self.pixX - 1
        for y in xrange(self.pixY):
            self.btns[x][y] = self.createPixel((10 + (self.pixSize * x), 10 + (self.pixSize * y)), self.innerPanel)
        self.resetScrolledPane()
        
################################################################################

    def removeColumn(self, event):
        if len(self.btns) > 1:
            for btn in self.btns[-1]:
                btn.Destroy()
            
            self.btns = self.btns[:len(self.btns) - 1]
                
            self.pixX -= 1
            self.resetScrolledPane()
        
################################################################################

    def moveLeft(self, event):
        for x in xrange(1, self.pixX):
            for y in xrange(self.pixY):
                self.btns[x - 1][y].SetBackgroundColour(self.btns[x][y].GetBackgroundColour())
                
        for y in xrange(self.pixY):
            self.btns[self.pixX - 1][y].SetBackgroundColour(wx.BLACK)
        
        self.panel.Refresh()
        
################################################################################

    def moveRight(self, event):
        for x in xrange(self.pixX - 1, 0, -1):
            for y in xrange(self.pixY):
                self.btns[x][y].SetBackgroundColour(self.btns[x - 1][y].GetBackgroundColour())
                
        for y in xrange(self.pixY):
            self.btns[0][y].SetBackgroundColour(wx.BLACK)
        
        self.panel.Refresh()
        
################################################################################

    def createMenuPanel(self):
        self.colour = wx.BLACK
        
        colourBtn = wx.Button(self.panel, -1, "Colour")
        self.colourBox = wx.StaticText(self.panel, -1, '', size=colourBtn.GetSize())
        self.colourBox.SetBackgroundColour(self.colour)

        colBox = wx.StaticBox(self.panel, -1, "Columns")
        colBoxSizer = wx.StaticBoxSizer(colBox, wx.HORIZONTAL)
        colMinusBtn = wx.Button(self.panel, -1, "-", size=(30, 30))
        colPlusBtn = wx.Button(self.panel, -1, "+", size=(30, 30))
        colBoxSizer.Add(colMinusBtn, 1, wx.TOP|wx.LEFT, 5)
        colBoxSizer.Add(colPlusBtn, 1, wx.TOP|wx.LEFT, 5)

        moveBox = wx.StaticBox(self.panel, -1, "Move Image")
        moveBoxSizer = wx.StaticBoxSizer(moveBox, wx.HORIZONTAL)
        moveLeftBtn = wx.Button(self.panel, -1, "<-", size=(30, 30))
        moveRightBtn = wx.Button(self.panel, -1, "->", size=(30, 30))
        moveBoxSizer.Add(moveLeftBtn, 1, wx.TOP|wx.LEFT, 5)
        moveBoxSizer.Add(moveRightBtn, 1, wx.TOP|wx.LEFT, 5)
        
        colourSizer = wx.BoxSizer(wx.HORIZONTAL)
        colourSizer.Add(colourBtn, 0, wx.ALL|wx.EXPAND, 5)
        colourSizer.Add(self.colourBox, 0, wx.ALL|wx.EXPAND, 5)
        colourSizer.Add(colBoxSizer, 1, wx.ALL|wx.EXPAND, 5)
        colourSizer.Add(moveBoxSizer, 1, wx.ALL|wx.EXPAND, 5)
        
        colourBtn.Bind(wx.EVT_BUTTON, self.chooseColour)
        colMinusBtn.Bind(wx.EVT_BUTTON, self.removeColumn)
        colPlusBtn.Bind(wx.EVT_BUTTON, self.addColumn)
        moveLeftBtn.Bind(wx.EVT_BUTTON, self.moveLeft)
        moveRightBtn.Bind(wx.EVT_BUTTON, self.moveRight)
        
        return colourSizer
        
################################################################################

    def createRecentColourPanel(self):
        box = wx.StaticBox(self.panel, -1, "Recent")
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        self.recents = []
        for x in xrange(10):
            self.recents.append(self.createPixel((0, 0), self.panel, False))
            boxSizer.Add(self.recents[x], 0, wx.TOP|wx.LEFT, 5)
            self.recents[x].Bind(wx.EVT_LEFT_DOWN, self.recentSelected)
        
        colourSizer = wx.BoxSizer(wx.HORIZONTAL)
        colourSizer.Add(boxSizer, 0, wx.ALL|wx.EXPAND, 5)
        
        return colourSizer
        
################################################################################

    def recentSelected(self, event):
        self.setPaintColour(event.GetEventObject().GetBackgroundColour())
        
################################################################################

    def saveRecentlyUsedColour(self):
        for x in xrange(len(self.recents) - 1, 0, -1):
            self.recents[x].SetBackgroundColour(self.recents[x - 1].GetBackgroundColour())
            self.recents[x].Refresh()
        self.recents[0].SetBackgroundColour(self.colourBox.GetBackgroundColour())
        self.recents[0].Refresh()
        
################################################################################

    def colourIsRecent(self, colour):
        for x in xrange(len(self.recents)):
            if self.recents[x].GetBackgroundColour() == colour:
                return True
        
        return False
        
################################################################################

    def chooseColour(self, event):
        dlg = wx.ColourDialog(self)

        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            self.setPaintColour(dlg.GetColourData().GetColour())

        dlg.Destroy()
        
################################################################################

    def setPaintColour(self, colour):
        if colour != self.colour:
            self.colour = colour
            self.colourBox.SetBackgroundColour(self.colour)
            self.colourBox.Refresh()
            
            if not self.colourIsRecent(colour):
                self.saveRecentlyUsedColour()
        
################################################################################

    def createPixels(self, pix, img):
        if img != None:
            data = fromimage(img)
            (self.pixX, self.pixY) = img.size
        else:
            data = None
            (self.pixX, self.pixY) = pix
        
        self.btns = [[None for y in xrange(self.pixY)] for x in xrange(self.pixX)]
            
        for x in xrange(self.pixX):
            for y in xrange(self.pixY):
                self.btns[x][y] = self.createPixel((10 + (self.pixSize * x), 10 + (self.pixSize * y)), self.innerPanel)
                if data is not None:
                    self.btns[x][y].SetBackgroundColour(data[y, x])
        
################################################################################

    def createPixel(self, pos, panel, isColourable=True):
        btn = wx.StaticText(panel, -1, '', size=(self.pixSize, self.pixSize), pos=pos)
        btn.SetBackgroundColour(wx.BLACK)
        
        if isColourable:
            btn.Bind(wx.EVT_LEFT_DOWN, self.setColour)
            btn.Bind(wx.EVT_MOTION, self.setColour)
        
        return btn
        
################################################################################

    def setColour(self, event):
        if event.LeftIsDown():
            event.GetEventObject().SetBackgroundColour(self.colour)
            event.GetEventObject().Refresh()
        