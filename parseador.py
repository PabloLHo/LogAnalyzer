def definirPerfiles(cadena):

    perfiles = dict()

    for linea in cadena.split("\n"):
        ip = linea.split(' - ')[0]
        if ip not in perfiles.keys():
            perfiles[ip] = {'entradas': list()}
        perfiles[ip]['entradas'].append(linea[(len(ip) + 1):])

    return perfiles


def procesarLinea(linea):

    campos = ['password', 'usuario', 'fechaHora', 'offset', 'metodo', 'pagina', 'protocolo', 'resultado', 'tam', 'url', 'cliente', 'ip2', 'responseTime']
    sep = linea.split('\"')
    parte1 = ''.join(sep[0:2])

    aux = parte1.replace('"', '').replace('[', '').replace(']', '').split(' ')
    aux.append(sep[3:])

    toRet = dict()
    for i in range(len(aux)):
        toRet[campos[i]] = aux[i]

    return toRet


def procesarPerfil(ip, perfiles):

    nuevaLista = list()

    for linea in perfiles[ip]['entradas']:
        nuevaLista.append(procesarLinea(linea))

    perfiles[ip]['entradas'] = nuevaLista


def procesarLog(fichero):

    with open(fichero, encoding='utf8') as f:
        cadena = f.read()

    toRet = definirPerfiles(cadena)

    for perfil in toRet.keys():
        procesarPerfil(perfil, toRet)

    return toRet
