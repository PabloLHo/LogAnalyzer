import os
import Ficheros.parseador as parseador
import Ficheros.analisis as analisis
import pickle
import Ficheros.procesado as procesado


# Trabaja con los logs del directorio para realizar un preprocesamiento del mismo obteniendo los datos del mismo
def procesar(path):
    if not os.path.exists("Logs") or len(os.listdir("Logs")) == 0:
        print("Lanzar error")

    if not os.path.exists("Logs procesados"):
        os.mkdir("Logs procesados")

    proc = parseador.procesarLog(path)
    proc = procesado.limitarExtensiones(proc, ("html", "htm", "pdf", "asp", "exe", "txt", "doc", "ppt", "xls", "xml", ""))
    proc = procesado.eliminarBots(proc)
    proc = procesado.definirTiempos(proc)
    proc = procesado.identificarUsuarios(proc)
    tiempoCorte = 1800
    proc = procesado.definirSesiones(proc, tiempoCorte)
    fichero_indice = open("Logs procesados/" + path, "wb")
    pickle.dump(proc, fichero_indice)


# Analiza el contenido extraido de los logs para extraer conocimiento de los mismos
def analizacion(path):
    if not os.path.exists("Logs procesados") or len(os.listdir("Logs procesados")) == 0:
        print("Lanzar error")
    fichero_procesado = open("Logs procesados/" + path, "rb")

    procesados = pickle.load(fichero_procesado)
    visitasPagina, totalPaginas, usuariosPaginas = analisis.paginasVisitadas(procesados)
    print("hola")




if __name__ == '__main__':
    # Recibirlo por flask
    path = "NASA_access_log_REDUC.txt"

    if not os.path.exists("Logs"):
        os.mkdir("Logs")
    if not os.path.exists("Logs procesados/" + path):
        procesar(path)
    analizacion(path)

