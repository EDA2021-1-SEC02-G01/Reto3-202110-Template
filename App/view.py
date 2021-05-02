"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("="*28)
    print("="*10 + " Reto 3 " + "="*10)
    print("="*28)
    print("1- Inicializar catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Requerimiento 1")
    print("0- Presione cualquier otra tecla para salir")


hashtag = 'user_track_hashtag_timestamp-small.csv'
sentiments = 'sentiment_values.csv'
context = 'context_content_features-small.csv'
catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        # cont es el controlador que se usará de acá en adelante
        print('Inicializando el catálogo ...\n')
        analyzer = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ...\n")
        controller.loadData(analyzer, hashtag, sentiments, context)
        print('Eventos de escucha cargados: ' +
              str(controller.eventsSize(analyzer)))
        print('Artistas únicos cargardos: ' +
              str(controller.artistsSize(analyzer)))
        print('Pistas de audio únicas cargadas: ' +
              str(controller.indexSize(analyzer)))
        print('5 primeros eventos:')
        firstEvents = controller.firstEvents(analyzer)
        for entry in lt.iterator(firstEvents):
            event = dict(me.getValue(entry))
            track_id = event["track_id"]
            user_id = event["artist_id"]
            event_id = event["id"]
            print(f"Track Id: {track_id}, " +
                  f"Artist Id: {user_id}, " +
                  f"Event Id: {user_id}")
        print('5 ultimos eventos:')
        lastEvents = controller.lastEvents(analyzer)
        for entry in lt.iterator(lastEvents):
            event = dict(me.getValue(entry))
            track_id = event["track_id"]
            user_id = event["artist_id"]
            event_id = event["id"]
            print(f"Track Id: {track_id}, " +
                  f"Artist Id: {user_id}, " +
                  f"Event Id: {user_id}")
    elif int(inputs[0]) == 3:
        caracteristica = input('Ingrese la característica de contenido deseada: ').lower()
        limInf = float(input("Ingrese el limite inferior: "))
        limSup = float(input("Ingrese el limite superior: "))   
        print("Cargando la informacion...")   
        print()  
        respuesta = controller.Req1(analyzer, caracteristica, limInf, limSup)
        if respuesta is not None:
            totalRepro, numArtistas = respuesta
            print(f"{caracteristica} is between {limInf} and {limSup}")
            print(f"Total Reproductions: {totalRepro}")
            print(f"Total Unique Artists: {numArtistas}")
            print()
    else:
        sys.exit(0)
sys.exit(0)
