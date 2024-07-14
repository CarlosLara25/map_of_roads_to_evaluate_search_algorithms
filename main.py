from header import MapCity, search_Paths

Num_villages = 10

Guanajuato = MapCity(Num_villages)    # Create an instance of MapCity with the number of villages as argument

Guanajuato.show_Map_villages()           # Show the map with the village's position 

Guanajuato.create_roads(0.9)             # Generate a number random a number of roads between villages, with a distance bigger than an stright line
Guanajuato.show_Map_roads()              # Show the map with the roads generated, are shown in stright line but they are not
print(Guanajuato.get_dataframe_roads())        # get the dataframe of the roads created


Solution = search_Paths(Guanajuato,'B0','D0')   # get the path to go from D0 to B0 using the by default 'Wide' algorithm
Solution.show_solution()

