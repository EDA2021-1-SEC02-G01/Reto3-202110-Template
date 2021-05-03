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
    print("3- Requerimiento 1: Caracterizar las reproducciones")
    print("4- Requerimiento 2: Encontrar musica para festejar")
    print("5- Requerimiento 3: Encontrar muscia para estudiar")
    print("6- Requerimiento 4: Estudiar los generos musicales")
    print("7- Requerimiento 5: Indicar el genero musical mas esuchado en el tiempo")
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
        print()
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
        print()
    elif int(inputs[0]) == 3:
        caracteristica = input('Ingrese la característica de contenido deseada: ').lower()
        limInf = float(input("Ingrese el limite inferior: "))
        limSup = float(input("Ingrese el limite superior: "))   
        print("Cargando la informacion...")   
        print()  
        respuesta = controller.Req1(analyzer, caracteristica, limInf, limSup)
        if respuesta is not None:
            totalRepro, numArtistas = respuesta
            print("+++++ Req No. 1 results... +++++")
            print(f"{caracteristica} is between {limInf} and {limSup}")
            print(f"Total Reproductions: {totalRepro}  |  Total Unique Artists: {numArtistas}")
            print()
    elif int(inputs[0]) == 4:
        energyMin = float(input("Ingrese el limite inferior de la caracteristica Energy: "))
        energyMax = float(input("Ingrese el limite superior de la caracteristica Energy: "))
        danceabilityMin = float(input("Ingrese el limite inferior de la caracteristica Danceability: "))
        danceabilityMax = float(input("Ingrese el limite superior de la caracteristica Danceability: "))
        print("Cargando informacion...")
        print()
        num_tracks, random_tracks = controller.musicaFestejar(analyzer, energyMin, energyMax, danceabilityMin, danceabilityMax)
        print(f"Energy is between {energyMin} and {energyMax}")
        print(f"Danceability is between {danceabilityMin} and {danceabilityMax}")
        print(f"Total de tracks en eventos: {num_tracks}")
        print()
        print("--- Unique track_id ---")
        cuenta = 1
        for event in lt.iterator(random_tracks):
            track_id = event["track_id"]
            energy = event["energy"]
            danceability = event["danceability"]
            print(f"Track {cuenta}: {track_id} with energy of {energy} and danceability of {danceability}")
            cuenta += 1
    elif int(inputs[0]) == 5:
        limInf1 = float(input("El valor mínimo del rango para Instrumentalness: "))
        limSup1 = float(input("El valor máximo del rango para Instrumentalness: "))
        limInf2 = float(input("El valor mínimo del rango para el Tempo: "))
        limSup2 = float(input("El valor máximo del rango para el Tempo: "))
        print("Cargando la informacion...")   
        print() 
        respuesta = controller.Req3(analyzer, limInf1, limSup1, limInf2, limSup2)
        if respuesta is not None:
            num_tracks, random5Tracks = respuesta
            print(f"Instrumentalness is between {limInf1} and {limSup1}")
            print(f"Tempo is between {limInf2} and {limSup2}")
            print(f"Total unique tracks in events: {num_tracks}")
            print()
            print("--- Unique track_id ---")
            cuenta = 1
            for event in lt.iterator(random5Tracks):
                track_id = event["track_id"]
                instrumentalness = event["instrumentalness"]
                tempo = event["tempo"]
                print(f"Track {cuenta}: {track_id} with instrumentalness of {instrumentalness} and tempo of {tempo}")
                cuenta += 1
    else:
        sys.exit(0)
sys.exit(0)
