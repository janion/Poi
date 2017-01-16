'''
Created on 12 Jan 2017

@author: Janion
'''

import wx
import Image
import os
import threading
from scipy.misc import fromimage

from src.gui.ProgressBar import GaugeFrame
from src.image.ImageCompressor import ImageCompressor
from src.image.ImageExporter import ImageExporter
from src.gui.editor.EditorWindow import EditorWindow

# TODO:
# Dialog before exiting without save
# Undo edit

################################################################################
################################################################################

class Window(wx.Frame):
    
    imgTypes = "Bitmap Image (*.bmp)|*.bmp|"\
               "JPEG Image (*.jpg)|*.jpg|"\
               "All files (*.*)|*.*"
    exportType = "Binary File (*.bin)|*.bin"
    
    IMAGE_HEIGHT = 16
               
    dir = os.getcwd()
    
    def __init__(self, parent, idd, title):
        wx.Frame.__init__(self, parent, idd, title, size=(500, 500))
        self.scrollPanel = wx.ScrolledWindow(self)
        
        self.scrollPanel.SetVirtualSize((500, 500))
        self.scrollPanel.SetScrollRate(20,20)
        
        self.img = None
        self.btns = None
        self.display = None
        self.pixSize = 25
        
        self.setupMenu()
            
################################################################################
            
    def setupMenu(self):
        self.menuBar = wx.MenuBar()
        
        menu1 = wx.Menu()
        menu1.Append(101, "Open Image")
        menu1.Append(102, "Save Image")
        menu1.AppendSeparator()
        menu1.Append(103, "Quit")
        self.menuBar.Append(menu1, "File")
        
        menu2 = wx.Menu()
        menu2.Append(201, "Compress Image")
        menu2.Append(204, "Edit Image")
        menu2.AppendSeparator()
        menu2.Append(202, "Export")
        menu2.AppendSeparator()
        menu2.Append(203, "Reload Image").Enable(False)
        self.menuBar.Append(menu2, "Image")
        
        self.SetMenuBar(self.menuBar)
        
        self.Bind(wx.EVT_MENU, self.openImage, id=101)
        self.Bind(wx.EVT_MENU, self.saveImage, id=102)
        self.Bind(wx.EVT_MENU, self.close, id=103)
        
        self.Bind(wx.EVT_MENU, self.compressImage, id=201)
        self.Bind(wx.EVT_MENU, self.exportImage, id=202)
        self.Bind(wx.EVT_MENU, self.editImage, id=204)
        
################################################################################

    def saveImage(self, event):
        if self.img != None:
            dlg = wx.FileDialog(
                self, message="Save",
                defaultDir=self.dir, 
                defaultFile="",
                wildcard=self.imgTypes,
                style=wx.SAVE
                )
    
            # Show the dialog and retrieve the user response. If it is the OK response, 
            # process the data.
            if dlg.ShowModal() == wx.ID_OK:
                # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()
                self.img.save(paths[0])

                dlg.Destroy()
        
################################################################################

    def editImage(self, event):
        if self.img == None or self.img.size[1] == self.IMAGE_HEIGHT:
            editor = EditorWindow(self, -1, "Edit Image", img=self.img, action=self.setImage)
            editor.Show()
        else:
            dlg = wx.MessageDialog(self, 'The image needs to be compressed before editing',
                                   'Unable To Edit', wx.OK
                                    )
            dlg.ShowModal()
            dlg.Destroy()
        
################################################################################

    def close(self, event):
        self.Destroy()
        
################################################################################

    def compressImage(self, event):
        if self.img != None:
            compressor = ImageCompressor()
            size = self.img.size
            self.createProgressDialog()
            
            workThread = threading.Thread(target=compressor.compressImageThreaded,
                                          args=(self.img, self.IMAGE_HEIGHT,
                                                int(self.IMAGE_HEIGHT * (float(size[0]) / size[1])),
                                                self.updateProgressDialog,
                                                self.progressDialogIsCancelled,
                                                self.destroyProgressDialogAndSetImage)
                                          )
            workThread.start()
        
################################################################################

    def exportImage(self, event):
        if self.img != None:
            if self.img.size[1] == self.IMAGE_HEIGHT:
                dlg = wx.FileDialog(
                    self, message="Save",
                    defaultDir=self.dir, 
                    defaultFile="",
                    wildcard=self.exportType,
                    style=wx.SAVE
                    )
        
                # Show the dialog and retrieve the user response. If it is the OK response, 
                # export the image.
                if dlg.ShowModal() == wx.ID_OK:
                    # This returns a Python list of files that were selected.
                    paths = dlg.GetPaths()
                    exporter = ImageExporter()
                    exporter.imgToBinaryFile(self.img, paths[0])
        
                dlg.Destroy()
            else:
                dlg = wx.MessageDialog(self, 'The image needs to be compressed before exporting',
                                       'Unable To Export', wx.OK
                                        )
                dlg.ShowModal()
                dlg.Destroy()
        
################################################################################

    def openImage(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.dir, 
            defaultFile="",
            wildcard=self.imgTypes,
            style=wx.OPEN
            )

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            self.img = Image.open(paths[0])
            self.showImage()

        dlg.Destroy()
        
################################################################################

    def setImage(self, img):
        self.img = img
        self.showImage()
        
################################################################################

    def showImage(self):
        self.scrollPanel.Scroll(0, 0)
        
        if self.display != None:
            self.display.Destroy()
        
        if self.btns != None:
            for btns in self.btns:
                for btn in btns:
                    btn.Destroy()
        
        self.display = None
        self.btns = None
        
        if self.img.size[1] != 16:
            self.showBigImage()
        else:
            self.showPixelImage()

################################################################################

    def showPixelImage(self):
        
        data = fromimage(self.img)
        (pixX, pixY) = self.img.size
        
        self.btns = [[None for y in xrange(pixY)] for x in xrange(pixX)]
            
        for x in xrange(pixX):
            for y in xrange(pixY):
                self.btns[x][y] = wx.StaticText(self.scrollPanel, -1, '',
                                                size=(self.pixSize, self.pixSize),
                                                pos=(10 + (self.pixSize * x), 10 + (self.pixSize * y))
                                                )
                if data is not None:
                    self.btns[x][y].SetBackgroundColour(data[y, x])

################################################################################

    def showBigImage(self):
        bmp = self.pilImageToWxBitmap(self.img)
        
        if self.display != None:
            self.display.Destroy()
        self.display = wx.StaticBitmap(self.scrollPanel, -1, bmp, pos=(10, 10))
        self.scrollPanel.SetVirtualSize(bmp.GetSize())

################################################################################

    def createProgressDialog(self):
        self.progress = GaugeFrame(self)
        self.progress.Show()

################################################################################

    def progressDialogIsCancelled(self):
        return self.progress.GetTitle()=="Cancelling..."

################################################################################

    def destroyProgressDialogAndSetImage(self, img=None):
        wx.CallAfter(self.progress.Destroy)
        if img != None:
            wx.CallAfter(self.setImage, img)

################################################################################

    def updateProgressDialog(self, value):
        wx.CallAfter(self.progress.updateGauge, value)
        
################################################################################
################################################################################
        
    def wxBitmapToPilImage( self, myBitmap ):
        return self.wxImageToPilImage( self.wxBitmapToWxImage( myBitmap ) )
        
################################################################################

    def wxBitmapToWxImage( self, myBitmap ):
        return wx.ImageFromBitmap( myBitmap )
        
################################################################################

    def pilImageToWxBitmap(self, myPilImage):
        return self.wxImageToWxBitmap(self.pilImageToWxImage(myPilImage))
        
################################################################################
    
    def pilImageToWxImage(self, myPilImage):
        myWxImage = wx.EmptyImage(myPilImage.size[0], myPilImage.size[1])
        myWxImage.SetData(myPilImage.convert('RGB').tostring())
        return myWxImage
        
################################################################################
    
    def wxImageToWxBitmap( self, myWxImage ):
        return myWxImage.ConvertToBitmap()
        
################################################################################
################################################################################



