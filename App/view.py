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
from DISClib.ADT import map as mp
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
    print("7- Requerimiento 5: Indicar el genero musical mas escuchado en el tiempo")
    print("0- Presione cualquier otra tecla para salir")


hashtag = 'user_track_hashtag_timestamp-small.csv'
sentiments = 'sentiment_values.csv'
context = 'context_content_features-small.csv'

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
        controller.loadData(analyzer, hashtag, sentiments, context) #Se cargan los archivos
        print('Eventos de escucha cargados: ' +
              str(controller.eventsSize(analyzer))) #Se imprime el total de eventos cargados
        print('Artistas únicos cargardos: ' +
              str(controller.artistsSize(analyzer))) #Se imprime el total de artistas unicos cargados
        print('Pistas de audio únicas cargadas: ' +
              str(controller.indexSize(analyzer))) #Se imprime el total de pistas de audio unicas
        print()
        print('5 primeros eventos:') #Se imprimen los 5 primeros eventos
        firstEvents = controller.firstEvents(analyzer)
        for event in lt.iterator(firstEvents):
            track_id = event["track_id"]
            user_id = event["artist_id"]
            event_id = event["id"]
            print(f"Track Id: {track_id}, " +
                  f"Artist Id: {user_id}, " +
                  f"Event Id: {user_id}")
        print('5 ultimos eventos:') #Se imprimen los 5 ultimos eventos
        lastEvents = controller.lastEvents(analyzer)
        for event in lt.iterator(lastEvents):
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
    elif int(inputs[0]) == 6:
        genre_list = ["Reggae", "Down-tempo", "Chill-out", "Hip-hop", "Jazz and Funk", "Pop", "R&B", "Rock", "Metal"]
        print("Los generos más comunes son:")
        for cosa in genre_list:
            print(f"- {cosa}")
        generos = input("Ingrese los generos que desea buscar separados por comas: ")
        generos = generos.replace(" ", "").split(",")
        total_Repro = 0
        tuplas = []
        for genero in generos:
            if genero not in genre_list:
                print(f"El genero {genero} no se encuentra en nuestros registros. Se creará {genero}")
                minTempo = input(f"Ingrese el valor mínimo del Tempo para {genero}: ")
                maxTempo = input(f"Ingrese el valor máximo del Tempo para {genero}: ") 
                respuesta = controller.Req4(analyzer, genero, minTempo, maxTempo)
            else:
                respuesta = controller.Req4(analyzer, genero, None, None)
            diezPrimeros, total_Artistas, genre_repro, minTempo, maxTempo = respuesta
            info = (genero, diezPrimeros, total_Artistas, genre_repro, minTempo, maxTempo)
            tuplas.append(info)
            total_Repro += genre_repro
        print()
        print("+"*5 + " Req No. 4 Results... " + "+"*5)
        print(f"Total reproductions: {total_Repro}")
        print()
        for info in tuplas:
            genero, diezPrimeros, total_Artistas, genre_repro, minTempo, maxTempo = info
            print("="*7 + f" {genero.upper()} " + "="*7)
            print(f"For {genero} the tempo is between {minTempo} and {maxTempo} BPM")
            print(f"{genero} reproductions: {genre_repro} with {total_Artistas} different artists")
            print("-"*5 + f" Some artists for {genero}" + "-"*5)
            cuenta = 1
            for artista in lt.iterator(diezPrimeros):
                print(f"Artist {cuenta}: {artista}")
                cuenta += 1
            print()
    elif int(inputs[0]) == 7:
        time1 = input("Ingrese el limite inferior del horario a buscar: ")
        time2 = input("Ingrese el limite superior del horario a buscar: ")
        total_repro, mapaPorSize, totalUniqueTracks, sample = controller.Req5(analyzer, time1.strip(), time2.strip())
        print()
        print("+"*5 + " Req No. 5 Results... " + "+"*5)
        print(f"There is a total of {total_repro} reproductions between {time1} and {time2}")
        print("="*25 + " GENRE SORTED REPRODUCTIONS " + "="*25)
        i = 1
        tamanioMapa = lt.size(om.keySet(mapaPorSize))
        while i <= tamanioMapa:
            mayor = om.maxKey(mapaPorSize)
            entry = om.get(mapaPorSize, mayor)
            genero = me.getValue(entry)
            if i == 1:
                primerGenero = genero
            print(f"TOP {i}: {genero} with {mayor} reps")
            om.deleteMax(mapaPorSize)
            i += 1
        print("...")
        print()
        print("="*25 + f" {primerGenero} SENTIMENT ANALYSIS " + "="*25)
        print(f"{primerGenero} has {totalUniqueTracks} unique tracks...")
        print("10 random tracks by total hashtags are...")
        i = 1
        for info in lt.iterator(sample):
            trackId, totalHt, vaderAvg = info
            print(f"TOP {i} track: {trackId} with {totalHt} hashtags and VADER = {vaderAvg}")
            i += 1
    else:
        sys.exit(0)
sys.exit(0)
