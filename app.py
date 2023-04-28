import pickle
from flask import Flask, render_template, request, redirect
from jinja2.utils import markupsafe
import dependencias.analisis as analisis
import dependencias.procesado as procesado
import os

app = Flask(__name__)

#Carpeta uploads
app.config['UPLOAD_FOLDER'] = os.path.join('Logs')

#Variables globales
logsExistentes = os.listdir("Logs procesados")
log = None
registrosPorPagina = 10


#Ruta base: página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    global log, logsExistentes
    sesiones = log["numSesiones"] if log else None
    usuarios = len(log["visitasUsuarioDiarias"]) if log else None
    tam = len(log['procesado']['registros']) if log else None
    paginas = len(log['totalPaginas']) if log else None
    visitasPaginas = log['totalPaginas'] if log else None
    extensiones = log['repeticionExtensiones'] if log else None
    datosBots = log['datosBots'] if log else None
    if log is not None:
        visitasDiarias = dict()
        for usuario in log["visitasUsuarioDiarias"]:
            for dia in log["visitasUsuarioDiarias"][usuario]:
                if not visitasDiarias.keys().__contains__(dia):
                    visitasDiarias[dia] = {"Tiempo": 0, "Visitas": 0}
                visitasDiarias[dia]["Visitas"] += log["visitasUsuarioDiarias"][usuario][dia]["numeroVisitas"]
                visitasDiarias[dia]["Tiempo"] += log["visitasUsuarioDiarias"][usuario][dia]["tiempo"]
        visitasDiarias = dict(sorted(visitasDiarias.items()))
    else:
        visitasDiarias = None

    return render_template('index.html', log=log, logsExistentes=logsExistentes, tam=tam, numUsuarios=usuarios,
                           numPaginas=paginas, numSesiones=sesiones,
                           totalPaginas=visitasPaginas, extensiones=extensiones, visitasDiarias=visitasDiarias, datosBots=datosBots)


#Ruta para ver los registros
@app.route('/registros', methods=['GET', 'POST'])
def registros():
    global log, registrosPorPagina
    registros = log['procesado']['registros'][0:registrosPorPagina] if log else None
    columnas = log['procesado']['columnas'] if log else None
    tam = len(log['procesado']['registros']) if log else None
    return render_template('registros.html', registros=registros, columnas=columnas, tam=tam, registrosPorPagina=registrosPorPagina)


@app.route('/ajax', methods=["GET", "POST"])
def ajax():
    global log, registrosPorPagina
    registros = log['procesado']['registros'] if log else None
    if request.method == "POST":
        pag = request.form['value']
        antes = (int(pag) - 1) * registrosPorPagina
        ahora = int(pag) * registrosPorPagina
        datos_modificados = registros[antes:ahora]
        return render_template("tabla.html", pagina=int(pag), datos_modificados=datos_modificados)


#Ruta para ver las sesiones
@app.route('/sesiones', methods=['GET', 'POST'])
def sesiones():
    global log, registrosPorPagina
    sesiones = log['sesionesOrdenadas'][0:registrosPorPagina] if log else None
    tam = len(log['sesionesOrdenadas']) if log else None
    columnas = ['idSesion', 'host', 'numeroVisitas']
    return render_template('sesiones.html', sesiones=sesiones, columnas=columnas, tam=tam, registrosPorPagina=registrosPorPagina)


@app.route('/ajaxSesiones', methods=["GET", "POST"])
def ajaxSesiones():
    global log, registrosPorPagina
    sesiones = log['sesionesOrdenadas'] if log else None
    if request.method == "POST":
        pag = request.form['value']
        antes = (int(pag) - 1) * registrosPorPagina
        ahora = int(pag) * registrosPorPagina
        datos_modificados = sesiones[antes:ahora]
        return render_template("tablaSesiones.html", pagina=int(pag), datos_modificados=datos_modificados)


#Ruta para ver los datos de una sesion
@app.route('/sesion', methods=['GET', 'POST'])
def sesion():
    global log, registrosPorPagina
    id = int(request.url.split("=")[1])
    sesion = log['sesionesOrdenadas'][id-1] if log else None
    columnas = log['procesado']['columnas'] if log else None
    porPaginas = None
    extensiones = dict()
    if sesion :
        porPaginas = dict()
        for visita in sesion['visitas'] :
            extension = visita['pagina'].split("/")[len(visita['pagina'].split("/")) - 1]
            extension = extension.split(".")[len(extension.split(".")) - 1]
            if visita['pagina'] not in porPaginas :
                porPaginas[visita['pagina']] = 1
            else :
                porPaginas[visita['pagina']] += 1
            if extensiones.keys().__contains__(extension):
                extensiones[extension] += 1
            else:
                extensiones[extension] = 1

    return render_template('sesion.html', sesion=sesion, columnas=columnas, porPaginas=porPaginas, extensiones=extensiones)


#Ruta para ver los datos de un host
@app.route('/host', methods=['GET', 'POST'])
def host():
    global log
    aux = request.url.split("=")[1]
    host = log['host'][aux] if log else None
    visitasDiarias = log['visitasHostDiarias'][aux] if log else None
    return render_template('host.html', direccion=aux, host=host, visitasDiarias=visitasDiarias)


#Ruta de reglas
@app.route('/reglas', methods=['GET', 'POST'])
def reglas():
    global log, registrosPorPagina
    totalPaginas = list(log['totalPaginas'].items()) if log else None
    totalVisitasPorTiempos = sorted(log['totalPaginas'].items(), key=lambda item: item[1]['visitas'], reverse=True)
    paginasSeguidasOrdenado = log['paginasSeguidasOrdenado'][:registrosPorPagina] if log else None
    ordenadoSinFin = log['ordenadoSinFin'][:registrosPorPagina] if log else None
    ordenadoFin = log['ordenadoFin'][:registrosPorPagina] if log else None
    return render_template('reglas.html', totalVisitas=totalPaginas[:registrosPorPagina], totalVisitasReves=totalPaginas[-registrosPorPagina:],
                           paginasSeguidasOrdenado=paginasSeguidasOrdenado, ordenadoSinFin=ordenadoSinFin, ordenadoFin=ordenadoFin,
                           totalVisitasPorTiempos=totalVisitasPorTiempos[:registrosPorPagina], totalVisitasPorTiemposReves=totalVisitasPorTiempos[-registrosPorPagina:])


@app.route('/subir_log', methods=['POST'])
def subir_log():
    global log, logsExistentes
    if request.method == 'POST':
        e = int(request.form['existente'])
        if e > -1:
            path = logsExistentes[e].split("/")[len(logsExistentes[e].split("/")) - 1]
            fichero_procesado = open("Logs procesados/" + path, "rb")
            log = pickle.load(fichero_procesado)
        else:
            fichero = request.files['log']
            if fichero.filename != '':
                fichero.save(os.path.join(app.config['UPLOAD_FOLDER'], fichero.filename))
                path = app.config['UPLOAD_FOLDER'] + "/" + fichero.filename
                proc, procOriginal, bots = procesado.procesar(path)
                analisis.analizar(path, proc, procOriginal, bots)

                path = fichero.filename.split("/")[len(fichero.filename.split("/")) - 1]
                fichero_procesado = open("Logs procesados/" + path, "rb")
                log = pickle.load(fichero_procesado)
                logsExistentes = os.listdir("Logs procesados")
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)