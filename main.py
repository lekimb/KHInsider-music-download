#! /usr/bin/python3.6
import requests, os, bs4, sys

# Descargar álbumes de https://downloads.khinsider.com/
# Por ejemplo: https://downloads.khinsider.com/game-soundtracks/album/professor-layton-and-the-last-specter

def main(url): 
    # Inicializar Beautiful Soup
    resAlbumPage = requests.get(url)
    soup = bs4.BeautifulSoup(resAlbumPage.text, 'html.parser') 

    # Crear carpeta de descargas a partir del título del álbum
    tituloAlbum = getTituloAlbum(soup)
    carpetaDescargas = crearCarpetaDescargas(tituloAlbum) # Devuelve path carpeta de descargas

    # Obtener links de descarga y nombres de archivo (a partir de soup)
    linksWithNames = getLinksWithSongNames(soup) # Returns: array de diccionarios
    
    # Descargar archivos (a partir de la lista de links y nombre y el path de la carpeta de descargas)
    descargarArchivos(linksWithNames, carpetaDescargas)


def getTituloAlbum(soup):
    titulo = soup.select('h2')[0].getText()
    print('Descargar álbum: ', titulo)
    return titulo

def crearCarpetaDescargas(nombreCarpeta):
    carpetaDescargas = os.path.join(os.getcwd(), nombreCarpeta)
    os.makedirs(carpetaDescargas, exist_ok=True)
    return carpetaDescargas

def getLinksWithSongNames(soup):
    songlist = soup.select('#songlist')[0]
    tableRows = songlist.select('tr')
    linksWithNames = []
    for tr in tableRows:
        if tr.get('id') == 'songlist_header' or tr.get('id') == 'songlist_footer': continue
        firstLink = getSongFirstLinkFromTr(tr)
        nombreCanción = getSongNameFromTr(tr)
        secondLink = getSongSecondLinkFromFirstLink(firstLink)
        linksWithNames.append({'link': secondLink, 'nombre': nombreCanción})

    return linksWithNames


def getSongFirstLinkFromTr(tr):
    link = 'https://downloads.khinsider.com/' + tr.select('td.playlistDownloadSong a')[0].get('href')
    return link

def getSongNameFromTr(tr):
    numero = tr.select('td')[1].getText()
    nombre = tr.select('td')[2].getText()
    nombreCanción = numero + ' ' + nombre
    return nombreCanción

def getSongSecondLinkFromFirstLink(firstLink):
    res = requests.get(firstLink)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    return soup.select('.songDownloadLink')[0].parent.get('href')

def descargarArchivos(linksWithNames, carpetaDescargas): 
    contador = 0
    for item in linksWithNames:
        descargarArchivo(item['link'], item['nombre'], carpetaDescargas)
        print('Descargado:', item['nombre'])
        contador += 1
    print(contador, 'archivos descargados')

def descargarArchivo(link, nombreArchivo, carpetaDescargas):
    responseArchivo = requests.get(link)
    responseArchivo.raise_for_status()

    path = os.path.join(carpetaDescargas, nombreArchivo + '.mp3')
    mp3 = open(path, 'wb')

    for chunk in responseArchivo.iter_content(100000):
        mp3.write(chunk)
    mp3.close()



if len(sys.argv) > 1:
    main(sys.argv[1])
else:
    print("Error: falta url como primer argumento")
