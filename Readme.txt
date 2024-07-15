Creates a map of a city with N villages distributed into the city.

The escenary is created by default 2000*2000 (configurable)
The N Villages are named A0, B0, C0,...A1,....ZN

After that, Roads to connect the villages are created randomly(seed), with a distance larger than the stright distance (simulating real roads)

Search algorithms can be applied to find paths between two cities
Wide, Deep, Uniform, Greedy, Astar



Programa para construir mapa de ciudades con N numero de pueblos ditribuidos en la ciudad

En un escenario de 2000*2000 (configurable)
Generear N Puntos(Villages) y asignarles un nombre "Desde A0 hasta Z0" Después A1 si es necesario, y asi sucesivamente

Crear caminos que unen los pueblos con una distancia de carretera igual a la distancia recta entre ellas mas un valor aleatorio (10 a 250).

Una vez concluido el mapa, pueden llamarse algoritmos de busqueda para encontrar trayectorias entre dos pueblos 
Hasta ahora se han agregado los algoritmos: Busqueda por amplitud 'Wide', busqueda por profundidad 'Deep', busqueda uniforme 'Uniform', greedy 'Greedy', A estrella 'Astar'