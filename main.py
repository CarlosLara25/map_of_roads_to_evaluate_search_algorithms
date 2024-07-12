from header import MapCity

Num_villages = 10

Guanajuato = MapCity(Num_villages)

Guanajuato.show_Map_villages()

Guanajuato.create_roads(0.9)
Guanajuato.show_Map_roads()


print(Guanajuato.find_Conections_to_Village('H0'))
