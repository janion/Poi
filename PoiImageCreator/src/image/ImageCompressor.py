'''
Created on 12 Jan 2017

@author: Janion
'''

import wx
import numpy as np
from scipy.misc import fromimage
from scipy.misc import toimage

class ImageCompressor():
    
    def compressImage(self, img, newHeight, newWidth):
        
        # Get data from original image
        data = fromimage(img)
        newData = np.zeros((newHeight, newWidth, 3))
        
        # Work out how many original pixels are compressed into each new pixel
        size = img.size
        pixToMergeX = size[0] / float(newWidth)
        pixToMergeY = size[1] / float(newHeight)
        totalToMerge = pixToMergeX * pixToMergeY
        
        # Compress pixels into new image data
        for x in xrange(size[0]):
            print x
            for y in xrange(size[1]):
                newX = int(x / pixToMergeX)
                newY = int(y / pixToMergeY)
                
                for i in xrange(3):
                    newData[newY, newX][i] += data[y, x][i] / totalToMerge
         
        # Create image from data
        newImg = toimage(newData)
        
        return newImg
    
    def compressImageThreaded(self, img, newHeight, newWidth, updateAction, cancelCheck, afterAction):
        
        # Get data from original image
        data = fromimage(img)
        newData = np.zeros((newHeight, newWidth, 3))
        
        # Work out how many original pixels are compressed into each new pixel
        size = img.size
        pixToMergeX = size[0] / float(newWidth)
        pixToMergeY = size[1] / float(newHeight)
        totalToMerge = pixToMergeX * pixToMergeY
        
        # Compress pixels into new image data
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                newX = int(x / pixToMergeX)
                newY = int(y / pixToMergeY)
                
                for i in xrange(3):
                    newData[newY, newX][i] += data[y, x][i] / totalToMerge
            
            if cancelCheck():
                break
            updateAction(int(100 * (float(x) / size[0])))
         
        if cancelCheck():
            afterAction()
        else:
            # Create image from data
            newImg = toimage(newData)
            afterAction(newImg)
        
        