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
tiempoCorte = 1800
formatoLog = "CLF"


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
    global log, registrosPorPagina, logsExistentes
    registros = log['procesado']['registros'][0:registrosPorPagina] if log else None
    columnas = log['procesado']['columnas'] if log else None
    tam = len(log['procesado']['registros']) if log else None
    return render_template('registros.html', registros=registros, columnas=columnas, tam=tam, registrosPorPagina=registrosPorPagina, logsExistentes=logsExistentes)


@app.route('/ajax', methods=["GET", "POST"])
def ajax():
    global log, registrosPorPagina, logsExistentes
    registros = log['procesado']['registros'] if log else None
    if request.method == "POST":
        pag = request.form['value']
        antes = (int(pag) - 1) * registrosPorPagina
        ahora = int(pag) * registrosPorPagina
        datos_modificados = registros[antes:ahora]
        return render_template("tabla.html", datos_modificados=datos_modificados, logsExistentes=logsExistentes)


@app.route('/invasores', methods=['GET', 'POST'])
def bots():
    global log, logsExistentes
    bots = log['datosBots'] if log else None
    tam = dict()
    if log:
        for bot in bots:
            tam[bot] = len(bots[bot]["host"])
    columnas = ["host", "numeroVisitas", "tiempoUsado"]
    return render_template('invasores.html', bots=bots, columnas=columnas, tam=tam, logsExistentes=logsExistentes)


@app.route('/invasor', methods=['GET', 'POST'])
def bot():
    global log, logsExistentes
    host = request.url.split("=")[1]
    if "bot" in host:
        tipo = "bot"
    elif "spider" in host:
        tipo = "spider"
    else:
        tipo = "crawler"
    bots = log['datosBots'] if log else None
    columnas = log['procesado']['columnas'] if log else None
    return render_template('invasor.html', host=host, tipo=tipo, bots=bots, columnas=columnas, logsExistentes=logsExistentes)


#Ruta para ver las sesiones
@app.route('/sesiones', methods=['GET', 'POST'])
def sesiones():
    global log, registrosPorPagina, logsExistentes
    sesiones = log['sesionesOrdenadas'][0:registrosPorPagina] if log else None
    tam = len(log['sesionesOrdenadas']) if log else None
    columnas = ['idSesion', 'host', 'numeroVisitas']
    return render_template('sesiones.html', sesiones=sesiones, columnas=columnas, tam=tam, registrosPorPagina=registrosPorPagina, logsExistentes=logsExistentes)


@app.route('/ajaxSesiones', methods=["GET", "POST"])
def ajaxSesiones():
    global log, registrosPorPagina, logsExistentes
    sesiones = log['sesionesOrdenadas'] if log else None
    if request.method == "POST":
        pag = request.form['value']
        antes = (int(pag) - 1) * registrosPorPagina
        ahora = int(pag) * registrosPorPagina
        datos_modificados = sesiones[antes:ahora]
        return render_template("tablaSesiones.html", datos_modificados=datos_modificados, logsExistentes=logsExistentes)


#Ruta para ver los datos de una sesion
@app.route('/sesion', methods=['GET', 'POST'])
def sesion():
    global log, registrosPorPagina, logsExistentes
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

    return render_template('sesion.html', sesion=sesion, columnas=columnas, porPaginas=porPaginas, extensiones=extensiones, logsExistentes=logsExistentes)


#Ruta para ver los datos de un host
@app.route('/host', methods=['GET', 'POST'])
def host():
    global log, logsExistentes
    aux = request.url.split("=")[1]
    host = log['host'][aux] if log else None
    visitasDiarias = log['visitasHostDiarias'][aux] if log else None
    paginasHost = None

    if log:
        paginasHost = dict()
        for usuario in host['sesiones']:
            for sesion in host['sesiones'][usuario]:
                for visita in range(len(host['sesiones'][usuario][sesion]["visitas"])):
                    pagina = host['sesiones'][usuario][sesion]["visitas"][visita]["pagina"]
                    if not paginasHost.keys().__contains__(pagina):
                        paginasHost[pagina] = { "visitas": 0, "tiempo": 0}
                    paginasHost[pagina]["visitas"] += 1
                    if (visita + 1) < len(host['sesiones'][usuario][sesion]["visitas"]):
                        if (host['sesiones'][usuario][sesion]["visitas"][visita + 1]["Timestamp"] - host['sesiones'][usuario][sesion]["visitas"][visita]["Timestamp"]) < 1800:
                            paginasHost[pagina]["tiempo"] += host['sesiones'][usuario][sesion]["visitas"][visita + 1]["Timestamp"] - host['sesiones'][usuario][sesion]["visitas"][visita]["Timestamp"]

    return render_template('host.html', direccion=aux, host=host, visitasDiarias=visitasDiarias, paginasHost=paginasHost, logsExistentes=logsExistentes)



#Ruta de reglas
@app.route('/reglas', methods=['GET', 'POST'])
def reglas():
    global log, registrosPorPagina, logsExistentes
    totalPaginas = list(log['totalPaginas'].items()) if log else None
    totalVisitasPorTiempos = sorted(log['totalPaginas'].items(), key=lambda item: item[1]['visitas'], reverse=True) if log else None
    paginasSeguidasOrdenado = log['paginasSeguidasOrdenado'][:registrosPorPagina] if log else None
    ordenadoSinFin = log['ordenadoSinFin'][:registrosPorPagina] if log else None
    ordenadoFin = log['ordenadoFin'][:registrosPorPagina] if log else None
    paginasBots = log['paginasBots'] if log else None
    ordenadoInicio = log['inicioOrdenado'][:registrosPorPagina] if log else None
    totalVisitas = totalPaginas[:registrosPorPagina] if log else None
    totalVisitasReves = totalPaginas[-registrosPorPagina:] if log else None
    totalVisitasPorTiempos2 = totalVisitasPorTiempos[:registrosPorPagina] if log else None
    totalVisitasPorTiemposReves = totalVisitasPorTiempos[-registrosPorPagina:] if log else None
    return render_template('reglas.html', totalVisitas=totalVisitas, totalVisitasReves=totalVisitasReves,
                           paginasSeguidasOrdenado=paginasSeguidasOrdenado, ordenadoSinFin=ordenadoSinFin, ordenadoFin=ordenadoFin,
                           totalVisitasPorTiempos=totalVisitasPorTiempos2, totalVisitasPorTiemposReves=totalVisitasPorTiemposReves,
                           paginasBots=paginasBots, ordenadoInicio=ordenadoInicio, logsExistentes=logsExistentes)


@app.route('/paginas', methods=['GET', 'POST'])
def paginas():
    global log, registrosPorPagina, logsExistentes
    totalPaginas = list(log['totalPaginas'].items())[0:registrosPorPagina] if log else None
    tam = len(log['totalPaginas']) if log else None
    return render_template('paginas.html', totalPaginas=totalPaginas, tam=tam, registrosPorPagina=registrosPorPagina, logsExistentes=logsExistentes)


@app.route('/ajaxPaginas', methods=["GET", "POST"])
def ajaxPaginas():
    global log, registrosPorPagina, logsExistentes
    totalPaginas = list(log['totalPaginas'].items()) if log else None
    if request.method == "POST":
        pag = request.form['value']
        antes = (int(pag) - 1) * registrosPorPagina
        ahora = int(pag) * registrosPorPagina
        datos_modificados = totalPaginas[antes:ahora]
        return render_template("tablaPaginas.html", datos_modificados=datos_modificados, logsExistentes=logsExistentes)


@app.route('/pagina', methods=['GET', 'POST'])
def pagina():
    global log, logsExistentes
    aux = request.url.split("=")[1]
    aux = aux.replace("%2F", "/")
    totalPaginas = log['totalPaginas'][aux] if log else None
    visitasPagina = log['paginasHosts'][aux][:registrosPorPagina] if log else None
    estructura = log['paginasSeguidasOrdenado'] if log else None
    paginasSeguidasOrdenado = list()
    paginasAnterioresOrdenado = list()
    if log:
        for (k, v) in estructura:
            if k[0] == aux:
                paginasSeguidasOrdenado.append((k[1], v))
            elif k[1] == aux:
                paginasAnterioresOrdenado.append((k[0], v))
    return render_template('pagina.html', direccion=aux, totalPaginas=totalPaginas, visitasPagina=visitasPagina, paginasSeguidasOrdenado=paginasSeguidasOrdenado[:registrosPorPagina],
                           paginasAnterioresOrdenado=paginasAnterioresOrdenado[:registrosPorPagina], logsExistentes=logsExistentes)


@app.route('/subir_log', methods=['POST'])
def subir_log():
    global log, logsExistentes, tiempoCorte, formatoLog
    if request.method == 'POST':
        e = int(request.form['existente'])
        tiempoCorte = int(request.form["tiempo"])
        formatoLog = request.form["formato"]
        if e > -1:
            path = logsExistentes[e].split("/")[len(logsExistentes[e].split("/")) - 1]
            fichero_procesado = open("Logs procesados/" + path, "rb")
            log = pickle.load(fichero_procesado)
        else:
            fichero = request.files['log']
            if fichero.filename != '':
                fichero.save(os.path.join(app.config['UPLOAD_FOLDER'], fichero.filename))
                path = app.config['UPLOAD_FOLDER'] + "/" + fichero.filename
                proc, procOriginal, bots = procesado.procesar(path,tiempoCorte, formatoLog)
                analisis.analizar(path, proc, procOriginal, bots, tiempoCorte)

                path = fichero.filename.split("/")[len(fichero.filename.split("/")) - 1]
                fichero_procesado = open("Logs procesados/" + path, "rb")
                log = pickle.load(fichero_procesado)
                logsExistentes = os.listdir("Logs procesados")
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)