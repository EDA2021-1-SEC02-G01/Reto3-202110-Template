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
                'content': None,
                'artists': None,
                'unique-tracks': None
                }

    analyzer['events'] = lt.newList('ARRAY_LIST')
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',comparefunction=compareDates)
    analyzer['sentiments'] = om.newMap(omaptype='RBT',
                                       comparefunction=None)
    analyzer['content'] = om.newMap(omaptype='RBT')
    analyzer['BPM'] = om.newMap(omaptype='RBT')
    analyzer['artists'] = om.newMap(omaptype='RBT', comparefunction=compareIds1)
    analyzer['tracks'] = lt.newList('ARRAY_LIST')
    return analyzer


# Funciones para agregar informacion al catalogo
def addEvent(analyzer, event):
    lt.addLast(analyzer['events'], event)
    updateDateIndex(analyzer['dateIndex'], event)
    

def updateDateIndex(map, event):
    """
    Se toma la fecha del evento y se busca si ya existe en el arbol
    dicha fecha. Si es así, se adiciona a su lista de eventos.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea.
    """
    occurreddate = event['created_at']
    eventdate = datetime.datetime.strptime(occurreddate, '%d-%m-%y %H:%M')
    entry = om.get(map, eventdate.date())
    if entry is None:
        dateEntry = newDataEntry(event)
        om.put(map, eventdate.date(), dateEntry)
    else:
        dateEntry = me.getValue(entry)
    addDateIndex(dateEntry, event)


def addDateIndex(dateEntry, event):
    """
    Actualiza el map para la fecha respectiva
    """
    track_id = event['track_id']
    mp.put(dateEntry, track_id, event)


def newDataEntry(event):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = mp.newMap(maptype='PROBING', comparefunction=compareIds2)
    return entry


def addFeature(analyzer, feature):
    lt.addLast(analyzer['tracks'], feature)
    updateBPMIndex(analyzer['BPM'], feature)
    updateArtistIndex(analyzer['artists'], feature)


def updateArtistIndex(map, feature):
    artist_id = feature['artist_id']
    om.put(map, artist_id, feature)


def addSentiment(analyzer, sentiment):
    pass


def updateBPMIndex(map, feature):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
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
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return lt.size(analyzer['tracks'])


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
    Compara dos eventos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareIds2(id1, id2):
    """
    Compara dos eventos
    """
    return id1>id2['key']


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
