import urllib3
import os
import parser.py
import pickle

# Obtiene los logs de un servidor web
def obtenerLogs(url):
    http = urllib3.PoolManager()


    # Realiza una solicitud GET y obtén la respuesta
    response = http.request('GET', url)

    # Lee el contenido de la respuesta
    content = response.data

    # Procesa el contenido para obtener los logs
    # Aquí puedes usar las funciones y métodos adecuados para extraer los logs según el formato en el que estén
    # Por ejemplo, si los logs están en formato de texto plano, puedes usar funciones de manipulación de texto
    # para analizar y extraer los datos relevantes.

    # Ejemplo de procesamiento básico para imprimir el contenido del log
    with open('Logs/logs.txt', 'wb') as f:
        f.write(content)


# Trabaja con los logs del directorio para realizar un preprocesamiento del mismo obteniendo los datos del mismo
def procesar(path):
    if not os.path.exists("Logs") or len(os.listdir("Logs")) == 0:
        print("Lanzar error")

    if not os.path.exists("Logs procesados"):
        os.mkdir("Logs procesados")

    with open('Logs/' + path, 'r') as f:
        content = f.read()
    procesado = parser.definirPerfiles(content)
    pickle.dump(procesado, "Logs procesados/" + path)


# Analiza el contenido extraido de los logs para extraer conocimiento de los mismos
def analisis():
    if not os.path.exists("Logs procesados") or len(os.listdir("Logs procesados")) == 0:
        print("Lanzar error")


if __name__ == '__main__':
    # Recibirlo por flask
    path = ""

    if not os.path.exists("Logs"):
        os.mkdir("Logs")
    if len(os.listdir("Logs")) == 0:
        obtenerLogs(path)

    procesar(path)
    analisis()

