def definirPerfiles(cadena) :

    perfiles = dict()

    for linea in cadena.split() :
        ip = linea.split(' - ')[0]
        if ip not in perfiles.keys() :
            perfiles[ip] = {'entradas' : list()}
        perfiles[ip]['entradas'].append(linea[(len(ip) + 3):])

    return perfiles


def procesarLinea(linea) :

    toRet = dict()
    toRet['nombre'] = linea.split(' ')[0]
    resto = linea[(len(toRet['nombre'] + 1)):]
    toRet['fecha'] = resto.split(']')[0][1:]
    resto = resto[(len(toRet['fecha'] + 3)):]
    toRet['peticion'] = resto.split('"')[1]
    resto = resto[(len(toRet['peticion'] + 3)):]
    aux = resto.split(' ')[0]
    toRet['codigoEstado'] = int(aux)
    resto = resto[(len(aux + 1)):]
    aux = resto.split(' ')[0]
    toRet['tamObjeto'] = int(aux)
    resto = resto[(len(aux + 1)):]
    toRet['url'] = resto.split('"')[1]
    resto = resto[(len(toRet['url'] + 3)):]
    toRet['cliente'] = resto.split('"')[1]
    toRet['responseTime'] = float(resto.split('response-time=')[1])

    return toRet


def procesarPerfil(ip, perfiles) :

    nuevaLista = list()

    for linea in perfiles[ip]['entradas'] :
        nuevaLista.append(procesarLinea(linea))

    perfiles[ip]['entradas'] = nuevaLista


def procesarLog (fichero) :

    with open(fichero, encoding='utf8') as f :
        cadena = f.read()

    toRet = definirPerfiles(cadena)

    for perfil in toRet.keys() :
        procesarPerfil(perfil, toRet)

    return toRet