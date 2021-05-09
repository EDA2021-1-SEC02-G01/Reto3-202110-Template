"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import datetime
import random
import copy
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos
listas, una para los videos, otra para las categorias de
los mismos.
"""


# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'events': None,
                'dateIndex': None,
                'sentiments': None,
                'content': None,
                }

    analyzer['sentiments'] = mp.newMap(maptype='PROBING')

    analyzer['content'] = mp.newMap(maptype="PROBING")
    #Instrumentalness: Crea un tree con los valores
    instrumentalnessTree = om.newMap(comparefunction=compareValues)
    mp.put(analyzer['content'], 'instrumentalness', instrumentalnessTree)
    #Liveness: Crea un tree con los valores
    livenessTree = om.newMap(comparefunction=compareValues)
    mp.put(analyzer['content'], 'liveness', livenessTree)
    #Speechiness: Crea un tree con los valores
    speechinessTree = om.newMap(comparefunction=compareValues)
    mp.put(analyzer['content'], 'speechiness', speechinessTree)
    #Danceability: Crea un tree con los valores
    danceabilityTree = om.newMap(comparefunction=compareValues)
    mp.put(analyzer['content'], 'danceability', danceabilityTree)
    #Valence: Crea un tree con los valores
    valenceTree = om.newMap(comparefunction=compareValues)
    mp.put(analyzer['content'], 'valence', valenceTree)
    #Loudness: Crea un tree con los valores
    loudnessTree = om.newMap(comparefunction=compareValues)
    mp.put(analyzer['content'], 'loudness', loudnessTree)
    #Tempo: Crea un tree con los valores
    tempoTree = om.newMap(comparefunction=compareValues)
    mp.put(analyzer['content'], 'tempo', tempoTree)
    #Acousticness: Crea un tree con los valores
    acousticnessTree = om.newMap(comparefunction=compareValues)
    mp.put(analyzer['content'], 'acousticness', acousticnessTree)
    #Energy: Crea un tree con los valores
    energyTree = om.newMap(comparefunction=compareValues)
    mp.put(analyzer['content'], 'energy', energyTree)

    analyzer['events'] = lt.newList("ARRAY_LIST", cmpfunction=compareIds2)

    analyzer['track_id'] = om.newMap(omaptype='RBT')

    analyzer['artists'] = om.newMap(omaptype='RBT', comparefunction=compareIds1)

    analyzer['created_at'] = om.newMap(omaptype='RBT', comparefunction=compareTime)

    analyzer['created_at-hashtag'] = om.newMap(omaptype='RBT', comparefunction=compareTime)

    return analyzer


# Funciones para agregar informacion al catalogo
def addEvent(analyzer, event):
    """
    Agrega un evento a la lista de eventos del catalogo
    """
    event["hashtag"] = lt.newList()
    lt.addLast(analyzer["events"], event)


def addHashtag(analyzer, feature, posEvent):
    foundEvent = False
    while not foundEvent and posEvent<lt.size(analyzer["events"]):
        event = lt.getElement(analyzer["events"], posEvent)
        if event['user_id'] == feature["user_id"] and event["track_id"] == feature["track_id"] and event["created_at"] == feature["created_at"]:
            lt.addLast(event["hashtag"],feature["hashtag"].strip())
            foundEvent = True
        elif event["created_at"] > feature["created_at"]:
            foundEvent = True
        else:
            posEvent += 1
    return posEvent

def addSentiment(analyzer, sentiment):
    vader = None
    if sentiment["vader_avg"] != "":
        vader = float(sentiment["vader_avg"])
    mp.put(analyzer["sentiments"], sentiment["hashtag"].lower(), vader)
    

def crearArboles(analyzer):
    for event in lt.iterator(analyzer["events"]):
        cevent = copy.copy(event)
        updateDateIndex(analyzer['created_at'], cevent)
        updateArtistIdIndex(analyzer['artists'], cevent)
        updateTrackIdIndex(analyzer['track_id'], cevent)
        updateFeatures(analyzer["content"], cevent)
    

def updateDateIndex(index, event):
    """
    Se toma la fecha del evento y se busca si ya existe en el arbol
    dicha fecha. Si es así, se adiciona a su lista de eventos.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea.
    """
    occurreddate = event['created_at']
    eventdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(index, eventdate.time())
    if entry is None:
        eventList = lt.newList("ARRAY_LIST", cmpfunction=compareIds2)
        om.put(index, eventdate.time(), eventList)
    else:
        eventList = me.getValue(entry)
    lt.addLast(eventList, event)


def updateTrackIdIndex(index, event):
    """
    Crea un indice con los track_id
    """
    track_id = event['track_id']
    entry = om.get(index, track_id)
    if entry is None:
        eventList = lt.newList("ARRAY_LIST", cmpfunction=compareIds2)
        om.put(index, track_id, eventList)
    else:
        eventList = me.getValue(entry)
    lt.addLast(eventList, event)


def updateArtistIdIndex(index, event):
    """
    Crea un indice con los artist_id
    """
    artist_id = event['artist_id']
    entry = om.get(index, artist_id)
    if entry is None:
        eventList = lt.newList("ARRAY_LIST", cmpfunction=compareIds2)
        om.put(index, artist_id, eventList)
    else:
        eventList = me.getValue(entry)
    lt.addLast(eventList, event)


def updateFeatures(index, event):
    features = ["instrumentalness",
                "liveness",
                "speechiness",
                "danceability",
                "valence",
                "loudness",
                "tempo",
                "acousticness",
                "energy"]
    for feature in features:
        tree_entry = mp.get(index, feature)
        tree = me.getValue(tree_entry)
        event_value = float(event[feature])
        entry = om.get(tree, event_value)
        if entry is None:
            eventList = lt.newList("ARRAY_LIST", cmpfunction=compareIds2)
            om.put(tree, event_value, eventList)
        else:
            eventList = me.getValue(entry)
        lt.addLast(eventList, event)


# Funciones para creacion de datos

def pistasPorGenero(index, genero, minTempo, maxTempo):
    if genero in ["Reggae", "Down-tempo", "Chill-out", "Hip-hop", "Jazz and Funk", "Pop", "R&B", "Rock", "Metal"]:
        if genero == "Reggae":
            minTempo = 60
            maxTempo = 90
        elif genero == "Down-tempo":
            minTempo = 70
            maxTempo = 100
        elif genero == "Chill-out":
            minTempo = 90
            maxTempo = 120
        elif genero == "Hip-hop":
            minTempo = 85
            maxTempo = 115
        elif genero == "Jazz and Funk":
            minTempo = 120
            maxTempo = 125
        elif genero == "Pop":
            minTempo = 100
            maxTempo = 130
        elif genero == "R&B":
            minTempo = 60
            maxTempo = 80
        elif genero == "Rock":
            minTempo = 110
            maxTempo = 140
        elif genero == "Metal":
            minTempo = 100
            maxTempo = 160
    pistas = om.values(index, minTempo, maxTempo)
    return pistas, minTempo, maxTempo

# Funciones de consulta

def eventsSize(analyzer):
    """
    Número de eventos de escucha cargados
    """
    return lt.size(analyzer['events'])


def artistsSize(analyzer):
    """
    Número de artistas únicos cargados
    """
    return om.size(analyzer['artists'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['created_at'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['track_id'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['dateIndex'])


def firstEvents(analyzer): 
    firstEvents = lt.subList(analyzer["events"], 1, 5)
    return firstEvents


def lastEvents(analyzer):
    lastEvents = lt.subList(analyzer["events"], -5, 5)
    return lastEvents


def Req1(analyzer, caracteristica, limInf, limSup):
    try:
        entry = mp.get(analyzer['content'], caracteristica)
        arbol = me.getValue(entry)
        if arbol is not None:
            totalRepro = 0
            valores = om.values(arbol, limInf, limSup)
            arbol_artistas = om.newMap(omaptype="RBT")
            for lista in lt.iterator(valores):
                for evento in lt.iterator(lista):
                    totalRepro += 1
                    nombre_artista = evento["artist_id"]
                    existe = om.get(arbol_artistas, nombre_artista)
                    if existe is None:
                        om.put(arbol_artistas, nombre_artista, nombre_artista)
            lista_artistas = om.keySet(arbol_artistas)
            numArtistas = lt.size(lista_artistas)
            return totalRepro, numArtistas
    except Exception:
        return None



def Req3(analyzer, limInf1, limSup1, limInf2, limSup2):
    try:
        entry = mp.get(analyzer['content'], "instrumentalness")
        arbolInstr = me.getValue(entry)
        valoresInstr = om.values(arbolInstr, limInf1, limSup1)
        arbol_Tempo = om.newMap(omaptype="RBT", comparefunction=compareValues)
        for lista in lt.iterator(valoresInstr):
            for evento in lt.iterator(lista):
                tempo = float(evento["tempo"])
                existe = om.get(arbol_Tempo, tempo)
                if existe is None:
                    eventList = lt.newList("ARRAY_LIST", cmpfunction=compareValues)
                    om.put(arbol_Tempo, evento["tempo"], eventList)
                else:
                    eventList = me.getValue(existe)
                lt.addLast(eventList, evento)
        valoresTempo = om.values(arbol_Tempo, limInf2, limSup2)
        unique_tracks = mp.newMap(maptype="PROBING")
        for lista in lt.iterator(valoresTempo):
            for evento in lt.iterator(lista):
                mp.put(unique_tracks, evento["track_id"], evento)
        total_tracks = mp.valueSet(unique_tracks)
        num_tracks = lt.size(total_tracks)
        random5Tracks = lt.newList()
        res = [random.randrange(1, num_tracks, 1) for i in range(5)]
        for num in res:
            eventoRandom = lt.getElement(total_tracks, num)
            lt.addLast(random5Tracks, eventoRandom)
        return num_tracks, random5Tracks
    except Exception:
        return None

def musicaFestejar(analyzer, energyMin, energyMax, danceabilityMin, danceabilityMax):
    """
    Requerimiento 2: Encontrar musica para festejar
    """
    entry = mp.get(analyzer['content'], 'energy')
    arbolEnergy = me.getValue(entry)
    valoresEnergy = om.values(arbolEnergy, energyMin, energyMax)
    arbolDance = om.newMap(omaptype='RBT', comparefunction=compareValues)
    for valor in lt.iterator(valoresEnergy):
        for evento in lt.iterator(valor):
            dance = float(evento['danceability'])
            existe = om.get(arbolDance, dance)
            if existe is None:
                eventList = lt.newList('ARRAY_LIST', cmpfunction=compareValues)
                om.put(arbolDance, dance, eventList)
            else:
                eventList = me.getValue(existe)
            lt.addLast(eventList, evento)
    valoresDance = om.values(arbolDance, danceabilityMin, danceabilityMax)
    tracks_unicas = mp.newMap(maptype='PROBING')
    for lista in lt.iterator(valoresDance):
        for evento in lt.iterator(lista):
            mp.put(tracks_unicas, evento['track_id'], evento)
    listaUnicas = mp.valueSet(tracks_unicas)
    num_tracks = lt.size(listaUnicas)
    res = [random.randrange(1, num_tracks, 1) for i in range(5)]
    random_tracks = lt.newList('ARRAY_LIST')
    for numero in res:
        chosen_track = lt.getElement(listaUnicas, numero)
        lt.addLast(random_tracks, chosen_track)
    return num_tracks, random_tracks


def Req4(analyzer, genero, minTempo, maxTempo):
    entry = mp.get(analyzer['content'], 'tempo')
    arbolTempo = me.getValue(entry)
    pistas, minTempo, maxTempo = pistasPorGenero(arbolTempo, genero, minTempo, maxTempo)
    uniqueArtists = mp.newMap(maptype="PROBING")
    lista_Repro = lt.newList("ARRAY_LIST")
    for valor in lt.iterator(pistas):
        for evento in lt.iterator(valor):
            lt.addLast(lista_Repro, evento)
            mp.put(uniqueArtists, evento["artist_id"], evento["artist_id"])
    artistList = mp.valueSet(uniqueArtists)
    total_Artistas = lt.size(artistList)
    total_Repro = lt.size(lista_Repro)
    diezPrimeros = lt.subList(artistList, 1, 10)
    return diezPrimeros, total_Artistas, total_Repro, minTempo, maxTempo


def Req5(analyzer, time1, time2):
    arbolHoras = analyzer["created_at"] #Sacamos el arbol organizado por horas
    valoresHoras = om.values(arbolHoras, time1, time2) #Sacar los valores del arbol en el rango de horas
    arbolPorTempo = om.newMap(omaptype="RBT", comparefunction=compareValues) #Crear un arbol vacio organizado por tempo
    for lista in lt.iterator(valoresHoras): #Recorrer la lista de listas
        for evento in lt.iterator(lista): #Recorrer cada lista de eventos
            tempo = float(evento['tempo']) #Abstraer el tempo del evento
            existe = om.get(arbolPorTempo, tempo) #Revisar si el tempo ya fue creado en el arbol de tempo
            if existe is None: #Si no esta creado
                eventList = lt.newList('ARRAY_LIST', cmpfunction=compareValues) # Crear una lista vacia
                om.put(arbolPorTempo, tempo, eventList) #Agregar la lista al nodo de tempo respectivo
            else: #Si está creado
                eventList = me.getValue(existe) #Recuperar la lista del nodo
            lt.addLast(eventList, evento) #Agregar el evento del rango de horas a la lista del respectivo nodo de tempo
    mapaPorGenero = mp.newMap(maptype="PROBING") #Se crea un diccionario vacio
    mapaPorSize =  om.newMap(omaptype="RBT") #Se crea un arbol vacio
    for genero in ["Reggae", "Down-tempo", "Chill-out", "Hip-hop", "Jazz and Funk", "Pop", "R&B", "Rock", "Metal"]: #Por cada genero que existe
        pistas, minTempo, maxTempo = pistasPorGenero(arbolPorTempo, genero, None, None) #Se saca la lista de listas con los eventos por genero
        listaEventos = lt.newList("ARRAY_LIST", cmpfunction=compareIds2) #Se crea una lista vacia donde se guardaran los eventos por genero
        for lista in lt.iterator(pistas): #Se recorre la lista de listas
            for evento in lt.iterator(lista): #Se recorre cada lista de eventos
                lt.addLast(listaEventos, evento) #Se añade el evento a la lista del genero
        sizeLista = lt.size(listaEventos) #Se saca el tamaño de la lista del genero
        mp.put(mapaPorGenero, genero, listaEventos) #Se agrega la lista de eventos al mapa con llave el respectivo genero
        om.put(mapaPorSize, sizeLista, genero) #Se agrega al mapaPorSize el numero de reps del genero como llave y el genero como valor
    mayorsize = om.maxKey(mapaPorSize)
    entry = om.get(mapaPorSize, mayorsize)
    mayorGenero = me.getValue(entry)
    entry = mp.get(mapaPorGenero, mayorGenero) #Se sacan los eventos del genero que más se repitió
    eventosMayorGenero = me.getValue(entry)
    uniqueTracks = mp.newMap(maptype="PROBING") #Se crea un mapa vacio para sacar los track_id unicos
    for evento in lt.iterator(eventosMayorGenero):
        existe = mp.get(uniqueTracks, evento["track_id"])
        if existe is None:
            lista_hashtags = lt.newList()
            mp.put(uniqueTracks, evento["track_id"], lista_hashtags)
        else:
            lista_hashtags = me.getValue(existe)
        for hashtag in lt.iterator(evento["hashtag"]): #Se recorre la lista de hashtags del evento
            lt.addLast(lista_hashtags, hashtag) #Se agrega cada ht a la lista de ht de la pista única
    llavesTrackId = mp.keySet(uniqueTracks)
    totalUniqueTracks = lt.size(llavesTrackId)
    random10Tracks = lt.subList(llavesTrackId, random.randint(1, totalUniqueTracks-10), 10)
    sample = lt.newList()
    for trackId in lt.iterator(random10Tracks):
        entry = mp.get(uniqueTracks, trackId)
        hashtagsEvento = me.getValue(entry)
        vaderAvg = 0
        totalHt = 0
        for hashtag in lt.iterator(hashtagsEvento):
            entry = mp.get(analyzer["sentiments"], hashtag.lower())
            if entry is not None:
                vader = me.getValue(entry)
                if vader is not None:
                    vaderAvg += vader
                    totalHt += 1
        if totalHt > 0:
            vaderAvg /= totalHt
        lt.addLast(sample, (trackId, totalHt, round(vaderAvg, 1)))

    return om.size(arbolPorTempo), mapaPorSize, totalUniqueTracks, sample


# Funciones utilizadas para comparar elementos dentro de una lista


def compareIds1(id1, id2):
    """
    Compara dos eventos para un arbol
    """
    if (str(id1) == str(id2)):
        return 0
    elif str(id1) > str(id2):
        return 1
    else:
        return -1


def compareIds2(id1, id2):
    """
    Compara dos eventos para una lista
    """
    return id1>id2['key']


def compareValues(value1, value2):
    """
    Compara dos valores
    """
    if (float(value1) == float(value2)):
        return 0
    elif (float(value1) > float(value2)):
        return 1
    else:
        return -1


def compareTime(time1, time2):
    """
    Compara dos fechas
    """
    if (time1 == time2):
        return 0
    elif (time1 > time2):
        return 1
    else:
        return -1

# Funciones de ordenamiento
       