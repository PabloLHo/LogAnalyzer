import os
import parseador
import pickle
import procesado


# Trabaja con los logs del directorio para realizar un preprocesamiento del mismo obteniendo los datos del mismo
def procesar(path):
    if not os.path.exists("Logs") or len(os.listdir("Logs")) == 0:
        print("Lanzar error")

    if not os.path.exists("Logs procesados"):
        os.mkdir("Logs procesados")

    proc = parseador.procesarLog(path)
    print(len(proc))
    proc = procesado.eliminarBots(proc)
    print(len(proc))
    proc = procesado.definirTiempos(proc)
    proc = procesado.identificarUsuarios(proc)
    tiempoCorte = 1800
    proc = procesado.definirSesiones(proc, tiempoCorte)
    pickle.dump(proc, "Logs procesados/" + path)


# Analiza el contenido extraido de los logs para extraer conocimiento de los mismos
def analisis():
    if not os.path.exists("Logs procesados") or len(os.listdir("Logs procesados")) == 0:
        print("Lanzar error")


if __name__ == '__main__':
    # Recibirlo por flask
    path = "Logs/NASA_access_log_REDUC.txt"

    if not os.path.exists("Logs"):
        os.mkdir("Logs")

    procesar(path)
    analisis()

