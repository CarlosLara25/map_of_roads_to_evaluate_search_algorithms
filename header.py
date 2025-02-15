import numpy as np
import cv2
import matplotlib.pyplot as plt

class MapCity:
    def __init__(self,numPoints, seed=1, size_Window_Y=2000,size_Window_X=2000,size_Name=20):
        ''' Takes the arguments numPoints, seed=1, size_Window_Y=2000,size_Window_X=2000,size_Name=20
           And return and instance with numPoint Villages randomly (seed) into the map''' 

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
        ''' Takes value of Prob (0 < Prob < 1)
            return a set of roads to connect the villages, the smaller euclidian distance between villages
            the greater the probability of having a road '''

        import random as rd
        rd.seed(self.seed)
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
            return f"Village {PointName} does not exist in the map"

    def find_Conections_to_Village_costs(self, PointName):
        P_conections =  list(filter(lambda item: item['Names'][0] == PointName or item['Names'][1] == PointName, self.Roads))

        citiesArrivals = []
        costs = []
        for conection in P_conections:
            for k in range(2):
                if conection['Names'][k] != PointName:
                    citiesArrivals.append(conection['Names'][k])
            costs.append(conection['Dist'])

        return citiesArrivals, costs


    def get_dataframe_roads(self):
        import pandas as pd

        df_roads = pd.DataFrame([key['Names'][0]    for key in self.Roads], columns=['Village depture'])
        df_roads['Village arrival'] = [key['Names'][1]    for key in self.Roads]
        df_roads['Distance'] = [key['Dist']    for key in self.Roads]

        return df_roads
 

class Nodo:
    def __init__(self, x):                                  # Inicializar nodo con su data
        self.Name = x                                 # Padre del nodo inicalizado en NONE
        self.childs = []                              # 4 Posibles hijos inicializados en None correspondientes a su action                                            # Dato contenido
        self.actions = []                                    # Actions desde la raiz
        self.cost = 0
        self.cost_Astar = 0

class search_Paths:
    def __init__(self, Map,  goal_Village, initial_Village = 'A0', algorithm = 'Wide'):
        self.Map = Map
        self.Roads = Map.Roads
        self.initial_Village = initial_Village
        self.goal_Village = goal_Village
        self.algorithm = algorithm
        self.solution = self.algorithm_selection()


    def algorithm_selection(self):
        if self.algorithm == ('Wide' or 'wide'):
            return self.solutionPaths_wide()
        elif self.algorithm == ('Deep' or 'deep'):
            return self.solutionPaths_deep()
        elif self.algorithm == ('Uniform' or 'uniform'):
            return self.solutionPaths_Uniform()
        elif self.algorithm == ('Greedy' or 'greedy'):
            return self.solutionPaths_Greedy()
        elif self.algorithm == ('Astar'):
            return self.solutionPaths_Astar()
        else:
            print('This algorithm is not content in this library, try another')

    def totalCostPath(self):
        if self.solution == None:
            print('Still there is not a solution')
        else:
            total_dist = 0
            path_solution = self.solution
         
            if len(path_solution) != None:
                aux_path =  list(filter(lambda item: item['Names'] == [self.initial_Village, path_solution[0]] or item['Names'] == [path_solution[0], self.initial_Village], self.Roads))
                total_dist += aux_path[0]['Dist']

                for i in range(len(path_solution) - 1):
                    aux_path =  list(filter(lambda item: item['Names'] == [path_solution[i], path_solution[i+1]] or item['Names'] == [path_solution[i+1], path_solution[i]], self.Roads))
                    total_dist += aux_path[0]['Dist']

                return total_dist

            return 0

    def checkSolution(self, PointName):
        if PointName.Name == self.goal_Village:
            return True
        else:
            return False

    def createTree(self, curr_nodo):                             # Recibe un nodo y lo extiende con sus posibles acciones

        childsNames = self.Map.find_Conections_to_Village(curr_nodo.Name)

        for cN in childsNames:
            aux_Node = Nodo(cN)
            aux_Node.actions = curr_nodo.actions + [cN]
            curr_nodo.childs.append(aux_Node)

        return  curr_nodo

    def createTree_Cost(self, curr_nodo):                             # Recibe un nodo y lo extiende con sus posibles acciones

        childsNames, costs = self.Map.find_Conections_to_Village_costs(curr_nodo.Name)

        for i, cN in enumerate(childsNames):
            aux_Node = Nodo(cN)
            aux_Node.actions = curr_nodo.actions + [cN]
            aux_Node.cost = curr_nodo.cost + costs[i]
            curr_nodo.childs.append(aux_Node)

        return  curr_nodo


    def solutionPaths_wide(self):

        cityNode = Nodo(self.initial_Village)                 # inicializar la pila de nodos a evaluar
        list_node = [cityNode]                       # Inicializar lista de estado evaluados
        evaluated_states = []
        result = None

        while True:
            if len(list_node)==0:                           # Verificar si la lista está vacía entonces no hay solución
                break
            #print(evaluated_states)

            curr_node = list_node.pop(0)                 # Saca el primer elemento de la lista
            if curr_node.Name in evaluated_states:            # Si el elemento ya fue evaludado continúa con el que sigue
             #     print(f'el nodo {curr_node.Name} ya ha sido evaluado')
                  continue

           # print(f'Nodo evaluado {curr_node.Name}')
            if self.checkSolution(curr_node):     # Evaluar el estado   preguntando si ya es la solucion
                  result = curr_node.actions
                  break

            evaluated_states.append(curr_node.Name)            # Agrega el nodo a la lista de evaluados
            curr_node = self.createTree(curr_node)           # expande el nodo
            for child in curr_node.childs:
                list_node.append(child)
        return result

    def show_solution(self):
        print(f'With the algorithm {self.algorithm}')
        print(f'The solution is:')
        Sol = self.initial_Village
        for Village in self.solution: 
            Sol += " -> "
            Sol += Village
        
        print(Sol)
        print(f'Total cost is: {self.totalCostPath()}')
        

    
    def solutionPaths_deep(self):

        cityNode = Nodo(self.initial_Village)                 # inicializar la pila de nodos a evaluar
        list_node = [cityNode]                       # Inicializar lista de estado evaluados
        evaluated_states = []
        result = None

        while True:
            if len(list_node)==0:                           # Verificar si la lista está vacía entonces no hay solución
                break

            curr_node = list_node.pop()                 # Saca el primer elemento de la lista
            if curr_node.Name in evaluated_states:            # Si el elemento ya fue evaludado continúa con el que sigue
                  continue

            if self.checkSolution(curr_node):     # Evaluar el estado   preguntando si ya es la solucion
                  result = curr_node.actions
                  break

            evaluated_states.append(curr_node.Name)            # Agrega el nodo a la lista de evaluados
            curr_node = self.createTree(curr_node)           # expande el nodo
            for child in curr_node.childs:
                list_node.append(child)
        return result

    def solutionPaths_Uniform(self):

        cityNode = Nodo(self.initial_Village)                 # inicializar la pila de nodos a evaluar
        list_node = [cityNode]                       # Inicializar lista de estado evaluados
        evaluated_states = []
        result = None

        while True:
            if len(list_node)==0:                           # Verificar si la lista está vacía entonces no hay solución
                break

            curr_node = list_node.pop(0)                 # Saca el primer elemento de la lista

            if curr_node.Name in evaluated_states:            # Si el elemento ya fue evaludado continúa con el que sigue
                  continue
            if self.checkSolution(curr_node):     # Evaluar el estado   preguntando si ya es la solucion
                  result = curr_node.actions
                  break

            evaluated_states.append(curr_node.Name)            # Agrega el nodo a la lista de evaluados
            curr_node = self.createTree_Cost(curr_node)           # expande el nodo
            for child in curr_node.childs:
                if list_node == [] or list_node[len(list_node)-1].cost < child.cost:
                          list_node.append(child)
                else:
                      for k in range(len(list_node)):
                            if list_node[k].cost >= child.cost:
                                  list_node.insert(k, child)
                                  break

        return result

    def getPositionOfCity(self, nameCity):
        informationCity =  list(filter(lambda item: item['Name'] == nameCity, self.Map.Villages))

        return informationCity[0]['PosY'] , informationCity[0]['PosX']

    def createTreeCost_Greedy(self, curr_nodo, pos_Solution):                             # Recibe un nodo y lo extiende con sus posibles acciones

        childsNames, costs = self.Map.find_Conections_to_Village_costs(curr_nodo.Name)

        for i, cN in enumerate(childsNames):
            aux_Node = Nodo(cN)
            aux_Node.actions = curr_nodo.actions + [cN]
            positionChild = self.getPositionOfCity(cN)
            aux_Node.cost_Astar = self.Map.euclidianDist2D(positionChild[0], pos_Solution[0],positionChild[1], pos_Solution[1])  # Agregar la parte + cost[i] convierte de greedy a A*
            curr_nodo.childs.append(aux_Node)

        return  curr_nodo

    def createTreeCost_Astar(self, curr_nodo, pos_Solution):                             # Recibe un nodo y lo extiende con sus posibles acciones

        childsNames, costs = self.Map.find_Conections_to_Village_costs(curr_nodo.Name)

        for i, cN in enumerate(childsNames):
            aux_Node = Nodo(cN)
            aux_Node.actions = curr_nodo.actions + [cN]
            positionChild = self.getPositionOfCity(cN)
            aux_Node.cost = curr_nodo.cost + costs[i]
            aux_Node.cost_Astar = self.Map.euclidianDist2D(positionChild[0], pos_Solution[0],positionChild[1], pos_Solution[1])  + aux_Node.cost # Agregar la parte + cost[i] convierte de greedy a A*
            curr_nodo.childs.append(aux_Node)

        return  curr_nodo

    def solutionPaths_Greedy(self):
        cityNode = Nodo(self.initial_Village)                 # inicializar la pila de nodos a evaluar
        list_node = [cityNode]                       # Inicializar lista de estado evaluados
        evaluated_states = []
        position_solutionCity = self.getPositionOfCity(self.goal_Village)
        result = None

        while True:
            if len(list_node)==0:                           # Verificar si la lista está vacía entonces no hay solución
                break
            curr_node = list_node.pop(0)                 # Saca el primer elemento de la lista
            if curr_node.Name in evaluated_states:            # Si el elemento ya fue evaludado continúa con el que sigue
                  continue
            if self.checkSolution(curr_node):     # Evaluar el estado   preguntando si ya es la solucion
                  result = curr_node.actions
                  break

            evaluated_states.append(curr_node.Name)            # Agrega el nodo a la lista de evaluados

            curr_node = self.createTreeCost_Greedy(curr_node,position_solutionCity)           # expande el nodo
            for child in curr_node.childs:
                #  print(f'la distancia entre el nodo {child.Name} con position {getPositionOfCity(PointDictionary,child.Name)} y el nodo solucion {solutionCity} es de {child.cost}')
                  if list_node == [] or list_node[len(list_node)-1].cost_Astar < child.cost_Astar:
                          list_node.append(child)
                  else:
                      for k in range(len(list_node)):
                            if list_node[k].cost_Astar >= child.cost_Astar:
                                  list_node.insert(k, child)
                                  break

        return result

    def solutionPaths_Astar(self):

        cityNode = Nodo(self.initial_Village)                 # inicializar la pila de nodos a evaluar
        list_node = [cityNode]                       # Inicializar lista de estado evaluados
        evaluated_states = []
        position_solutionCity = self.getPositionOfCity(self.goal_Village)
        result = None

        while True:
            if len(list_node)==0:                           # Verificar si la lista está vacía entonces no hay solución
                break
            curr_node = list_node.pop(0)                 # Saca el primer elemento de la lista
            if curr_node.Name in evaluated_states:            # Si el elemento ya fue evaludado continúa con el que sigue
                  continue
            if self.checkSolution(curr_node):     # Evaluar el estado   preguntando si ya es la solucion
                  result = curr_node.actions
                  break

            evaluated_states.append(curr_node.Name)            # Agrega el nodo a la lista de evaluados

            curr_node = self.createTreeCost_Astar(curr_node, position_solutionCity)           # expande el nodo
            for child in curr_node.childs:
                #  print(f'la distancia entre el nodo {child.Name} con position {getPositionOfCity(PointDictionary,child.Name)} y el nodo solucion {solutionCity} es de {child.cost}')
                  if list_node == [] or list_node[len(list_node)-1].cost_Astar < child.cost_Astar:
                          list_node.append(child)
                  else:
                      for k in range(len(list_node)):
                            if list_node[k].cost_Astar >= child.cost_Astar:
                                  list_node.insert(k, child)
                                  break

        return result

        



    


