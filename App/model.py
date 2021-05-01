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

    analyzer['dateIndex'] = om.newMap(omaptype='RBT',comparefunction=compareDates)

    analyzer['sentiments'] = om.newMap(omaptype='RBT',
                                       comparefunction=None)

    analyzer['content'] = mp.newMap(maptype='PROBING')
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

    analyzer['events'] = om.newMap(omaptype='RBT', comparefunction=compareIds1)

    analyzer['track_id'] = om.newMap(omaptype='RBT')

    analyzer['artists'] = om.newMap(omaptype='RBT', comparefunction=compareIds1)

    analyzer['created_at'] = om.newMap(omaptype='RBT')

    return analyzer


# Funciones para agregar informacion al catalogo
def addEvent(analyzer, event):
    """
    Agrega un evento a la lista de eventos del catalogo
    """
    updateEventIndex(analyzer['events'], event)
    updateDateIndex(analyzer['dateIndex'], event)
    updateArtistIdIndex(analyzer['artists'], event)
    updateTrackIdIndex(analyzer['track_id'], event)
    

def updateDateIndex(index, event):
    """
    Se toma la fecha del evento y se busca si ya existe en el arbol
    dicha fecha. Si es así, se adiciona a su lista de eventos.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea.
    """
    occurreddate = event['created_at']
    eventdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(index, eventdate.date())
    if entry is None:
        dateEntry = mp.newMap(maptype='PROBING', comparefunction=compareIds2)
        om.put(index, eventdate.date(), dateEntry)
    else:
        dateEntry = me.getValue(entry)
    lt.addLast(dateEntry, event)


def updateEventIndex(map, event):
    """
    Agrega cada uno de los events al e
    """
    id = event['id']
    entry = om.get(map, id)
    om.put(map, id, entry)


def updateTrackIdIndex(index, event):
    """
    Crea un indice con los track_id
    """
    track_id = event['track_id']
    entry = om.get(index, track_id)
    if entry is None:
        track_entry = mp.newMap(maptype='PROBING', comparefunction=compareIds2)
        om.put(index, track_id, track_entry)
    else:
        track_entry = me.getValue(entry)
    lt.addLast(track_entry, event)


def updateArtistIdIndex(index, event):
    """
    Crea un indice con los artist_id
    """
    artist_id = event['artist_id']
    entry = om.get(index, artist_id)
    if entry is None:
        artist_entry = mp.newMap(maptype='PROBING', comparefunction=compareIds2)
        om.put(index, artist_id, artist_entry)
    else:
        artist_entry = me.getValue(entry)
    lt.addLast(artist_entry, event)
    

def addFeature(analyzer, feature):
    #lt.addLast(analyzer['tracks'], feature)
    #updateContent(analyzer['content'], feature)
    #updateArtistIndex(analyzer['artists'], feature)
    pass


def updateContent(content, feature):
    llaves = mp.keySet(analyzer)
    for llave in llaves:
        entry = mp.get(content, llave)
        arbol = me.getValue(entry)
        dataEntry = om.get(arbol, float(feature[llave]))
        if dataEntry is None:
            listadeFeatures = lt.newList('ARRAY_LIST')
            om.put(arbol, float(feature[llave]), listadeFeatures)
        else:
            listadeFeatures = me.getValue(dataEntry)
        lt.addLast(listadeFeatures, feature)
    


def updateArtistIndex(map, feature):
    artist_id = feature['artist_id']
    om.put(map, artist_id, feature)


def addSentiment(analyzer, sentiment):
    pass


def updateBPMIndex(map, feature):
    """
    Se toma el tempo y se busca si ya existe en el arbol
    dicho tempo.  Si es asi, se adiciona a su lista de tempos
    y se actualiza el indice de tipos de tempos.

    Si no se encuentra creado un nodo para ese tempo en el arbol,
    se crea y se actualiza el indice de tipos de tempos.
    """
    tempo = round(float(feature['tempo']))
    tempoExists = om.contains(map, tempo)
    if tempoExists:
        entry = om.get(map, tempo)
        tracksForTempo = me.getValue(entry)
    else:
        tracksForTempo = mp.newMap()
        om.put(map, tempo, tracksForTempo)
    mp.put(tracksForTempo, feature['track_id'], feature)
    return map


# Funciones para creacion de datos


# Funciones de consulta

def eventsSize(analyzer):
    """
    Número de eventos de escucha cargados
    """
    return om.size(analyzer['events'])


def artistsSize(analyzer):
    """
    Número de artistas únicos cargados
    """
    return om.size(analyzer['artists'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['dateIndex'])


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
    if (value1 == value2):
        return 0
    elif (value1 > value2):
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

# Funciones de ordenamiento

def Req1(analyzer, caracteristica, limInf, limSup):
    entry = mp.get(analyzer['content'], caracteristica)
    arbol = me.getValue(entry)
    if arbol is not None:
        valores = om.values(arbol, limInf, limSup)
        for valor in valores:
            mp.valueSet(valor)
        