Programa para construir mapa de ciudades con N numero de pueblos ditribuidos en la ciudad

Con el objetivo de crear caminos entre los pueblos y con ello poder aplicar algoritmos de busqueda de trayectoria

En un escenario de 2000*2000 (configurable)
Generear N Puntos(Villages) y asignarles un nombre "Desde A0 hasta Z0" Después A1 si es necesario, y asi sucesivamente

Crear las distancias euclidianas entre cada uno y crear una distancia de carretera entre ellas sumandoles al valor de la distancia recta un valor aleatorio (10 a 250).

Dibujarlas con un circulo centrada en su posición y su nombre adentro

Una vez concluido el mapa, pueden llamrase algoritmos de busqueda para encontrar trayectorias entre dos pueblos 
Hasta ahora se han agregado los algoritmos: Busqueda por amplitud 'Wide', busqueda por profundidad 'Deep' y busqueda uniforme 'Uniform'