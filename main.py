from header import MapCity, search_Paths

Num_villages = 15

Guanajuato = MapCity(Num_villages,seed=2)    # Creates an instance of MapCity with the number of villages as argument

Guanajuato.show_Map_villages()           # Shows the map with the village's position 

Guanajuato.create_roads(Prob=0.9)             # Generates a number random a number of roads between villages, with a distance bigger than an stright line
Guanajuato.show_Map_roads()              # Shows the map with the roads generated, are shown in stright line but they are not
print(f' The roads that connect the Villages in Guanajuato are: \n {Guanajuato.get_dataframe_roads()}')        # get the dataframe of the roads created

Map = Guanajuato
initial_Village = 'B0'
goal_Village = 'I0'


Solution_Deep = search_Paths(Map, goal_Village, initial_Village,'Deep')   # get the path to go from D0 to B0 using the 'Deep' algorithm
Solution_Deep.show_solution()

Solution_Astar = search_Paths(Map, goal_Village, initial_Village,'Astar')   # get the path to go from D0 to B0 using the 'Astar' algorithm
Solution_Astar.show_solution()

