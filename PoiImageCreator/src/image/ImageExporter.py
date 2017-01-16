'''
Created on 12 Jan 2017

@author: Janion
'''

import numpy as np
from scipy.misc import fromimage
from scipy.misc import toimage

class ImageExporter():

        
    def imgToBinaryFile(self, img, fileName):
        
        # Work out how many original pixels there are
        size = img.size
        
        # Get data from original image
        data = fromimage(img)
        
        str1 = ""
        
        # Compress pixels into new image data
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                byt = data[y, x]
                for i in xrange(len(byt) - 1, -1, -1):
                    str1 += chr(byt[i])
        
            
        with open(fileName, "wb") as csvfile:
            csvfile.write(bytearray(str1[::-1]))    
                