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
    sesiones = log["numSesiones"] if log is not None else None
    usuarios = len(log["visitasUsuarioDiarias"]) if log is not None else None
    tam = len(log['procesado']['registros']) if log is not None else None
    paginas = len(log['totalPaginas']) if log is not None else None
    visitasPaginas = log['totalPaginas'] if log is not None else None
    return render_template('index.html', log=log, logsExistentes=logsExistentes, tam=tam, numUsuarios=usuarios, numPaginas=paginas, numSesiones=sesiones,
                           totalPaginas=visitasPaginas)


#Ruta para ver los registros
@app.route('/registros', methods=['GET', 'POST'])
def registros():
    global log, registrosPorPagina
    registros = log['procesado']['registros'][0:registrosPorPagina] if log is not None else None
    columnas = log['procesado']['columnas'] if log is not None else None
    tam = len(log['procesado']['registros']) if log is not None else None
    return render_template('registros.html', registros=registros, columnas=columnas, tam=tam, registrosPorPagina=registrosPorPagina)


@app.route('/ajax', methods=["GET", "POST"])
def ajax():
    global log, registrosPorPagina
    registros = log['procesado']['registros'] if log is not None else None
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
    sesiones = log['sesionesOrdenadas'][0:registrosPorPagina] if log is not None else None
    tam = len(log['sesionesOrdenadas']) if log is not None else None
    columnas = ['idSesion', 'host', 'numeroVisitas']
    return render_template('sesiones.html', sesiones=sesiones, columnas=columnas, tam=tam, registrosPorPagina=registrosPorPagina)


@app.route('/ajaxSesiones', methods=["GET", "POST"])
def ajaxSesiones():
    global log, registrosPorPagina
    sesiones = log['sesionesOrdenadas'] if log is not None else None
    if request.method == "POST":
        pag = request.form['value']
        antes = (int(pag) - 1) * registrosPorPagina
        ahora = int(pag) * registrosPorPagina
        datos_modificados = sesiones[antes:ahora]
        return render_template("tablaSesiones.html", pagina=int(pag), datos_modificados=datos_modificados)


#Ruta para ver los datos de una sesion
@app.route('/sesion', methods=['GET', 'POST'])
def sesion():
    usuario = request.url.split("=")[1]
    return render_template('sesion.html', usuario=usuario)


#Ruta para ver los datos de un host
@app.route('/host', methods=['GET', 'POST'])
def host():
    usuario = request.url.split("=")[1]
    return render_template('host.html', usuario=usuario)


#Ruta de reglas
@app.route('/reglas', methods=['GET', 'POST'])
def reglas():
    return render_template('reglas.html')


@app.route('/subir_log', methods=['POST'])
def subir_log():
    global log, logsExistentes
    if request.method == 'POST':
        e = int(request.form['existente'])
        if e > -1:
            log = analisis.analizar(logsExistentes[e])
        else:
            fichero = request.files['log']
            if fichero.filename != '':
                fichero.save(os.path.join(app.config['UPLOAD_FOLDER'], fichero.filename))
                path = app.config['UPLOAD_FOLDER'] + "/" + fichero.filename
                procesado.procesar(path)
                log = analisis.analizar(path)
                logsExistentes = os.listdir("Logs procesados")
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)