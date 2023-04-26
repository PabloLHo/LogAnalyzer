import pickle
from flask import Flask, render_template, request, redirect
from jinja2.utils import markupsafe
import dependencias.analisis as analisis
import dependencias.procesado as procesado
import os

app = Flask(__name__)

#Carpeta uploads
app.config['UPLOAD_FOLDER'] = os.path.join('Logs')

#Estructura principal
logsExistentes = os.listdir("Logs procesados")
log = None


#Ruta base: página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    global logsExistentes
    return render_template('index.html', log=log, logsExistentes=logsExistentes)


#Ruta para ver los registros
@app.route('/registros', methods=['GET', 'POST'])
def registros():
    global log
    registros = log['procesado'] if log is not None else None
    print(registros['contenido']['199.72.81.55'])
    return render_template('registros.html', registros=registros)


#Ruta para ver las sesiones
@app.route('/sesiones', methods=['GET', 'POST'])
def sesiones():
    return render_template('sesiones.html')


#Ruta para ver los datos de una sesion
@app.route('/sesion', methods=['GET', 'POST'])
def sesion():
    return render_template('sesion.html')


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