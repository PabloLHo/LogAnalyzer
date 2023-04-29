import os


def definirColumnas(cadena, formatoLog):
    linea = cadena.split("\n")[0]
    if formatoLog == "EPA":
        campos = ['host', 'fechaHora', 'offset', 'metodo', 'pagina', 'protocolo', 'resultado', 'tam']
    elif formatoLog == "CLF" or formatoLog == "ECLF":
        campos = ['host', 'password', 'usuario', 'fechaHora', 'offset', 'metodo', 'pagina', 'protocolo', 'resultado', 'tam', 'url', 'cliente', 'ip2', 'responseTime']
    else:
        campos = ['host', 'usuario', 'fecha', 'hora', 'servicio', 'servidor', 'servidor IP', 'tiempo uso', 'bytes cliente', 'bytes servidor', 'resultado', 'windows code',
                  'metodo', 'objetivo', 'parametros']
    sep = linea.split('\"')
    parte1 = ''.join(sep[0:2])
    aux = parte1.replace('"', '').replace('[', '').replace(']', '').split(' ')
    aux.append(sep[3:])
    return campos[:len(aux)-1]


def definirPerfiles(cadena, columnas):

    perfiles = dict()
    registros = list()

    for linea in cadena.split("\n"):
        ip = linea.split(' - ')[0]
        if ip not in perfiles.keys():
            perfiles[ip] = list()
        perfiles[ip].append(linea)
        registros.append(procesarLinea(linea, columnas))

    return perfiles, registros


def procesarLinea(linea, columnas):

    sep = linea.split('\"')
    parte1 = ''.join(sep[0:2])
    aux = parte1.replace('"', '').replace('[', '').replace(']', '').split(' ')
    aux.append(sep[3:])

    toRet = dict()
    cont = 0
    for i in range(len(columnas)):
        if i == 7 and aux[i].isnumeric():   #Errores en los que no aparece el protocolo
            toRet[columnas[i]] = '-'
        else:
            toRet[columnas[i]] = aux[cont]
            cont += 1

    return toRet


def procesarPerfil(ip, perfiles, columnas):

    nuevaLista = list()

    for linea in perfiles[ip]:
        nuevaLista.append(procesarLinea(linea, columnas))

    perfiles[ip] = nuevaLista


def procesarLog(fichero, formatoLog):

    with open(fichero, encoding='utf8') as f:
        cadena = f.read()

    columnas = definirColumnas(cadena, formatoLog)

    toRet, registros = definirPerfiles(cadena, columnas)

    for perfil in toRet.keys():
        procesarPerfil(perfil, toRet, columnas)

    return {'contenido': toRet, 'columnas': columnas, 'registros': registros}
