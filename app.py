from flask import Flask, render_template, request, redirect
from jinja2.utils import markupsafe
import dependencias.analisis as analisis
import dependencias.procesado as procesado
import os

app = Flask(__name__)

#Carpeta uploads
app.config['UPLOAD_FOLDER'] = os.path.join('Logs')

#Ruta base: página principal
@app.route('/', methods=['GET', 'POST'])
def index() :
    return render_template('index.html')


#Ruta para ver los registros
@app.route('/registros', methods=['GET', 'POST'])
def registros() :
    return render_template('registros.html')


#Ruta para ver las sesiones
@app.route('/sesiones', methods=['GET', 'POST'])
def sesiones() :
    return render_template('sesiones.html')


#Ruta para ver los datos de una sesion
@app.route('/sesion', methods=['GET', 'POST'])
def sesion() :
    return render_template('sesion.html')


#Ruta de reglas
@app.route('/reglas', methods=['GET', 'POST'])
def reglas() :
    return render_template('reglas.html')


@app.route('/subir_log', methods=['POST'])
def subir_log() :
    if request.method == 'POST' :
        fichero = request.files['log']
        fichero.save(os.path.join(app.config['UPLOAD_FOLDER'], fichero.filename))
        path = app.config['UPLOAD_FOLDER'] + "/" + fichero.filename
        procesado.procesar(path)
        analisis.analizar(path)
    return redirect('/')


#Ruta para elegir partido
@app.route('/elegir_partido', methods=['GET', 'POST'])
def elegir_partido() :

    if request.method == 'POST':
        temporada = int(request.form['temporada'])
        equipo1 = request.form['equipo1'].split(",")
        equipo2 = request.form['equipo2'].split(",")
        #Solicitar partidos
        partidos = []
        partidos = Partido.obtenerPartidos(temporada, equipo1, equipo2)
        return render_template('elegir_partido.html', partidos=partidos, equipo1=equipo1, equipo2=equipo2, temporada=temporada)


if __name__ == '__main__' :
    app.run(debug=True)