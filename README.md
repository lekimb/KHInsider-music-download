# Video-game-soundtracks-downloader
Python script para descargar álbumes de la web https://downloads.khinsider.com
> KHI offers video and PC game soundtracks for download in MP3 and lossless forms. Want to get your favourite game's OST? You have found the right place.

## Funcionamiento
El script main.py está pensado para ser ejecutado en términal pasándole una url como primer parámetro. 
```
python main.py <url>
```
La url deberá corresponderse con la página de un álbum. En el siguiente ejemplo, se descargaría el álbum "Professor Layton and the Last Specter"
```
python main.py https://downloads.khinsider.com/game-soundtracks/album/professor-layton-and-the-last-specter
```
Tal vez se prefiera escribir la url directamente en el código, en vez de tener que pasarla como parámetro. Para ello, deberán eliminarse las siguientes líneas:
```
if len(sys.argv) > 1:
    main(sys.argv[1])
else:
    print("Error: falta url como primer argumento")
```
Ahora, simplemente invocamos la función main y le pasamos una url como parámetro:
```
url = "https://downloads.khinsider.com/game-soundtracks/album/professor-layton-and-the-last-specter"
main(url)
```

## Dependencias
`requests`, `bs4`, `os`, `sys`
