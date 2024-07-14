from header import MapCity, search_Paths

Num_villages = 10

Guanajuato = MapCity(Num_villages)

Guanajuato.show_Map_villages()

Guanajuato.create_roads(0.9)
Guanajuato.show_Map_roads()

Solution = search_Paths(Guanajuato,'B0','D0')

Solution.show_solution()

