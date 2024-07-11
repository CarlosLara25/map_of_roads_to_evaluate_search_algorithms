import numpy as np
import cv2
import matplotlib.pyplot as plt

class MapCity:
    def __init__(self,numPoints, seed=1, size_Window_Y=2000,size_Window_X=2000,size_Name=20):
        self.numPoints = numPoints
        self.seed = seed
        self.size_Window_Y = size_Window_Y
        self.size_Window_X = size_Window_X
        self.size_Name = size_Name 
        self.Points = self.createPoints()
        self.Names = self.createNames()
        self.Map = self.fillMap() 


    def createNames(self):
        img = cv2.imread('names.jpg')
        list_names = []

        for i in range(self.numPoints):
            imagen_i = np.zeros((37,40,3))
            imagen_i = img[37*int(i/16)+3:37*int(i/16)+40,40*(i%16)+8:40*(i%16)+48,:]  
            list_names.append(imagen_i)
        
        return list_names

    def createPoints(self):
        import random as rd 
        rd.seed(self.seed)
        Points = np.array([[rd.randint(self.size_Name,self.size_Window_Y-self.size_Name), rd.randint(self.size_Name,self.size_Window_X-self.size_Name)] for i in range(self.numPoints)])
        return Points


    def buildMap(self):
        myMap = np.full((self.size_Window_Y,self.size_Window_X,3),255)
        return myMap


    def fillMap(self):
        myMap = self.buildMap()
        for i in range(np.size(self.Points,0)):
            myMap[self.Points[i,0]-18:self.Points[i,0]+19,self.Points[i,1]-20:self.Points[i,1]+20,:] = self.Names[i]

        return myMap

    def show_Map_cities(self,figsize_=(15,15)):
        fig = plt.figure(figsize = figsize_)
        plt.imshow(self.Map)
        plt.show()

