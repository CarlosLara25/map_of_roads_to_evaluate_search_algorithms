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
        self.Map_villages = self.fillMap() 
        self.Villages = self.build_villages_list()
        self.Roads = None
        self.Map_roads = None


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

    def show_Map_villages(self,figsize_=(15,15)):
        fig = plt.figure(figsize = figsize_)
        plt.imshow(self.Map_villages)
        plt.show()        

    def build_villages_list(self):
        PointDictionary = []
        Names_letter = "ABCDEFGHIJKLMNOP"    # 16 VALORES
        Names_number = "012345"               # 6 X 16 

        for i in range (self.numPoints):
            A = {'Name': Names_letter[i%16]+Names_number[int(i/16)], 'PosY': self.Points[i,0], 'PosX': self.Points[i,1],'Paths':[]}
            PointDictionary.append(A)

        return PointDictionary

    def euclidianDist2D(self, x1,x2,y1,y2):
        import math
        return math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

    def create_roads(self, Prob):  # probability of road between two villages is in funtion of the distance
     # being accepted if rd.random() < (1 - dEuclidiana/(Prob*size_window_x))
        import random as rd
        point_dic_X = self.Villages.copy()
        point_dic_X.sort(key=lambda d: d['PosX'])
        Paths = [] 

        def distRoads(val):
            noise = rd.random()/2 + 0.01                 # valores obtenidos (0.01 hasta 0.51)
            road = (1+noise) * val      # un road estará entre 101 y 151 % de su distancia euclidiana
            return int(road)


        for i in range(self.numPoints):
            for j in range(i+1,self.numPoints):
                dEuclidiana = self.euclidianDist2D(point_dic_X[i]['PosX'],point_dic_X[j]['PosX'],point_dic_X[i]['PosY'],point_dic_X[j]['PosY'])
                if (rd.random() < (1 - dEuclidiana/(Prob*1.4*self.size_Window_X))):   # Aprox 1.4*size_window_x es la maxima dist posible
                    Path_aux = {'Names': [point_dic_X[i]['Name'],point_dic_X[j]['Name']], 'Dist': distRoads(dEuclidiana)}
                    Paths.append(Path_aux)
        
        self.Roads = Paths
    
    def create_Map_roads(self, figsize_=(15,15)):

        def printOnePath(myMap, Path, PointDictionary):
            P_in =  list(filter(lambda item: item['Name'] == Path['Names'][0], PointDictionary))
            P_out =  list(filter(lambda item: item['Name'] == Path['Names'][1], PointDictionary))

            distE = self.euclidianDist2D(P_in[0]['PosX'],P_out[0]['PosX'],P_in[0]['PosY'],P_out[0]['PosY'])             
            NPseparation = int(distE/20)+1   # Obtener número de puntos a partir de la distancia euclidiana entre los dos puntos
            dY = int((P_out[0]['PosY'] - P_in[0]['PosY'])/NPseparation)
            dX = int((P_out[0]['PosX'] - P_in[0]['PosX'])/NPseparation)

            for i in range(NPseparation+1):
                en_Y = P_in[0]['PosY']+i*dY
                en_X = P_in[0]['PosX']+i*dX
                myMap[en_Y-2:en_Y+2,en_X-2:en_X+2,:] = 0

            return myMap

        def printPaths(my_map, myPaths, PointDictionary):
            for myPath in myPaths:
                my_map = printOnePath(my_map, myPath, PointDictionary)

            return my_map

        my_map = self.Map_villages.copy()
        self.Map_roads = printPaths(my_map, self.Roads, self.Villages)  

    def show_Map_roads(self,figsize_=(15,15)):
        self.create_Map_roads()
        fig = plt.figure(figsize = figsize_)
        plt.imshow(self.Map_roads)
        plt.show()      
    
    def find_Conections_to_Village(self, PointName):
        ''' Takes an argument: a Village name
        return connections if they exist '''
        names_villages =  list(map(lambda item: item['Name'], self.Villages))
        
        if PointName in names_villages:

            P_conections =  list(filter(lambda item: item['Names'][0] == PointName or item['Names'][1] == PointName, self.Roads))

            citiesArrivals = []

            for conection in P_conections:
                for k in range(2):
                    if conection['Names'][k] != PointName:
                        citiesArrivals.append(conection['Names'][k])

            return citiesArrivals

        else:
            print(names_villages)
            return f"Village {PointName} does not exist in the map"


class finder_algorithms:
    def __init__(self):
        pass
    


