#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
from pc_queue import pc_queue
from threading import Thread

class Extracter(Thread):
    def __init__(self, filename,outputBuffer, maxFramesToLoad = 9999):
        Thread.__init__(self, name = "Extracter")
        self.filename = filename
        self.outputBuffer = outputBuffer
        self.maxFramesToLoad = maxFramesToLoad
    def run(self):
        # open video file
        vidcap = cv2.VideoCapture(self.filename)
        # read first image
        success, image =vidcap.read()
        count = 0
        while success and count < self.maxFramesToLoad:
            self.outputBuffer.insert(image)
            success, image = vidcap.read()
            print(f'Reading frame {count} {success}')
            count += 1
        print('Frame Extraction Complete')
        self.outputBuffer.end()

class Converter(Thread):
    def __init__(self, inputBuffer, outputBuffer):
        Thread.__init__(self, name = "Converter")
        self.inputBuffer = inputBuffer
        self.outputBuffer = outputBuffer
    def run(self):
        image = self.inputBuffer.remove()
        count = 0
        while image is not None:
            print(f'Converting Frame {count}')
            grayscale  = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            self.outputBuffer.insert(grayscale)
            image = self.inputBuffer.remove()
            count += 1
        print('Frame Conversion Complete')
        self.outputBuffer.end()
    
class Displayer(Thread):
    def __init__(self, inputBuffer):
        Thread.__init__(self, name = "Displayer")
        self.inputBuffer = inputBuffer
    def run(self):
        image = self.inputBuffer.remove()
        count = 0
        while image is not None:
            print(f'Displaying Frame {count}')
            cv2.imshow("Frame", image)
            if cv2.waitKey(42) and 0xFF == ord('q'):
                break
            image = self.inputBuffer.remove()
            count += 1
        print('Finished Displaying')
        cv2.destroyAllWindows()
                                            
if __name__ == "__main__":
    
    # filename of clip to load
    filename = 'clip.mp4'

    # extraction queue  
    extraction_queue = pc_queue()
    conversion_queue = pc_queue()

    # extract the frames
    Extracter(filename,extraction_queue,72).start()
    # convert the frames
    Converter(extraction_queue,conversion_queue).start()
    # display the frames
    Displayer(conversion_queue).start()
