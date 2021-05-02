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
    #updateEventIndex(analyzer['events'], event)
    om.put(analyzer["events"], event["id"], event)
    updateDateIndex(analyzer['dateIndex'], event)
    updateArtistIdIndex(analyzer['artists'], event)
    updateTrackIdIndex(analyzer['track_id'], event)
    updateFeatures(analyzer["content"], event)
    

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
            feature_entry = mp.newMap(maptype='PROBING', comparefunction=compareIds2)
            om.put(tree, event_value, feature_entry)
        else:
            feature_entry = me.getValue(entry)
        lt.addLast(feature_entry, event)


def addHashtag(analyzer, feature):
    pass


def addSentiment(analyzer, sentiment):
    pass


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


def firstEvents(analyzer):
    key_set = om.keySet(analyzer["events"]) 
    sub_list = lt.subList(key_set, 1, 5)
    firstEvents = lt.newList()
    for key in lt.iterator(sub_list):
        event = om.get(analyzer["events"], key)
        lt.addLast(firstEvents,event)
    return firstEvents


def lastEvents(analyzer):
    key_set = om.keySet(analyzer["events"])
    numelem = eventsSize(analyzer)
    sub_list = lt.subList(key_set, numelem-5,5)
    lastEvents = lt.newList()
    for key in lt.iterator(sub_list):
        event = om.get(analyzer["events"], key)
        lt.addLast(lastEvents,event)
    return lastEvents


def Req1(analyzer, caracteristica, limInf, limSup):
    entry = mp.get(analyzer['content'], caracteristica)
    arbol = me.getValue(entry)
    if arbol is not None:
        totalRepro = 0
        valores = om.values(arbol, limInf, limSup)
        arbol_artistas = om.newMap(omaptype="RBT")
        for valor in lt.iterator(valores):
            for evento in lt.iterator(valor):
                totalRepro += 1
                nombre_artista = evento["artist_id"]
                existe = om.get(arbol_artistas, nombre_artista)
                if existe is None:
                    om.put(arbol_artistas, nombre_artista, nombre_artista)
        lista_artistas = om.keySet(arbol_artistas)
        numArtistas = lt.size(lista_artistas)
        return totalRepro, numArtistas
    return None

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
       