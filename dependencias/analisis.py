from datetime import datetime
import os
import pickle

def paginasVisitadas(content):
    paginasVisitadas = dict()
    usuariosPaginas = dict()
    paginasHosts = dict()
    for host in content:
        for usuario in content[host]:
            for sesion in content[host][usuario]["sesion"]:
                for visita in range(len(content[host][usuario]["sesion"][sesion])):
                    if paginasVisitadas.keys().__contains__(content[host][usuario]["sesion"][sesion][visita]["pagina"]):
                        if paginasVisitadas[content[host][usuario]["sesion"][sesion][visita]["pagina"]].keys().__contains__(usuario):
                            paginasVisitadas[content[host][usuario]["sesion"][sesion][visita]["pagina"]][usuario] += 1
                        else:
                            paginasVisitadas[content[host][usuario]["sesion"][sesion][visita]["pagina"]][usuario] = 1
                    else:
                        paginasVisitadas[content[host][usuario]["sesion"][sesion][visita]["pagina"]] = dict()
                        paginasVisitadas[content[host][usuario]["sesion"][sesion][visita]["pagina"]][usuario] = 1

                    if paginasHosts.keys().__contains__(content[host][usuario]["sesion"][sesion][visita]["pagina"]):
                        if paginasHosts[content[host][usuario]["sesion"][sesion][visita]["pagina"]].keys().__contains__(host):
                            inicio = datetime.strptime(content[host][usuario]["sesion"][sesion][visita]["fechaHora"], '%d/%b/%Y:%H:%M:%S')
                            if (visita + 1) != len(content[host][usuario]["sesion"][sesion]):
                                fin = datetime.strptime(content[host][usuario]["sesion"][sesion][visita + 1]["fechaHora"], '%d/%b/%Y:%H:%M:%S')
                            else:
                                fin = inicio
                            tiempo = (fin - inicio).total_seconds()
                            paginasHosts[content[host][usuario]["sesion"][sesion][visita]["pagina"]][host]["tiempo"] += tiempo
                            paginasHosts[content[host][usuario]["sesion"][sesion][visita]["pagina"]][host]["visitas"] += 1
                        else:
                            inicio = datetime.strptime(content[host][usuario]["sesion"][sesion][visita]["fechaHora"],'%d/%b/%Y:%H:%M:%S')
                            if (visita + 1) != len(content[host][usuario]["sesion"][sesion]):
                                fin = datetime.strptime(
                                    content[host][usuario]["sesion"][sesion][visita + 1]["fechaHora"], '%d/%b/%Y:%H:%M:%S')
                            else:
                                fin = inicio
                            tiempo = (fin - inicio).total_seconds()
                            paginasHosts[content[host][usuario]["sesion"][sesion][visita]["pagina"]][host] = {"visitas": 1, "tiempo": tiempo}
                    else:
                        paginasHosts[content[host][usuario]["sesion"][sesion][visita]["pagina"]] = dict()
                        inicio = datetime.strptime(content[host][usuario]["sesion"][sesion][visita]["fechaHora"],'%d/%b/%Y:%H:%M:%S')
                        if (visita + 1) != len(content[host][usuario]["sesion"][sesion]):
                            fin = datetime.strptime(content[host][usuario]["sesion"][sesion][visita + 1]["fechaHora"],'%d/%b/%Y:%H:%M:%S')
                        else:
                            fin = inicio
                        tiempo = (fin - inicio).total_seconds()
                        paginasHosts[content[host][usuario]["sesion"][sesion][visita]["pagina"]][host] = {"visitas": 1, "tiempo": tiempo}

                    if usuariosPaginas.keys().__contains__(usuario):
                        if usuariosPaginas[usuario].keys().__contains__(content[host][usuario]["sesion"][sesion][visita]["pagina"]):
                            usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]]["visitas"] += 1
                            inicio = datetime.strptime(content[host][usuario]["sesion"][sesion][visita]["fechaHora"],'%d/%b/%Y:%H:%M:%S')
                            if (visita + 1) != len(content[host][usuario]["sesion"][sesion]):
                                fin = datetime.strptime(content[host][usuario]["sesion"][sesion][visita + 1]["fechaHora"], '%d/%b/%Y:%H:%M:%S')
                            else:
                                fin = inicio
                            tiempo = (fin - inicio).total_seconds()
                            usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]]["Tiempo"] += tiempo
                        else:
                            usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]] = dict()
                            usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]]["visitas"] = 1
                            inicio = datetime.strptime(content[host][usuario]["sesion"][sesion][visita]["fechaHora"],'%d/%b/%Y:%H:%M:%S')
                            if (visita + 1) != len(content[host][usuario]["sesion"][sesion]):
                                fin = datetime.strptime(content[host][usuario]["sesion"][sesion][visita + 1]["fechaHora"], '%d/%b/%Y:%H:%M:%S')
                            else:
                                fin = inicio
                            tiempo = (fin - inicio).total_seconds()
                            usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]]["Tiempo"] = tiempo
                    else:
                        usuariosPaginas[usuario] = dict()
                        usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]] = dict()
                        usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]]["visitas"] = 1
                        inicio = datetime.strptime(content[host][usuario]["sesion"][sesion][visita]["fechaHora"],'%d/%b/%Y:%H:%M:%S')
                        if (visita + 1) != len(content[host][usuario]["sesion"][sesion]):
                            fin = datetime.strptime(content[host][usuario]["sesion"][sesion][visita + 1]["fechaHora"],'%d/%b/%Y:%H:%M:%S')
                        else:
                            fin = inicio
                        tiempo = (fin - inicio).total_seconds()
                        usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]]["Tiempo"] = tiempo

    totalVisitas = dict()

    for usuario in usuariosPaginas:
        for pagina in usuariosPaginas[usuario]:
            usuariosPaginas[usuario][pagina]["Media"] = usuariosPaginas[usuario][pagina]["Tiempo"] / usuariosPaginas[usuario][pagina]["visitas"]

    for pagina in paginasVisitadas:
        totalVisitas[pagina] = {"visitas": 0, "tiempo": 0}
        for usuario in paginasVisitadas[pagina]:
            totalVisitas[pagina]["visitas"] += paginasVisitadas[pagina][usuario]
            totalVisitas[pagina]["tiempo"] += usuariosPaginas[usuario][pagina]["Tiempo"]

    res = dict()
    for usuario in usuariosPaginas:
        diccionario_ordenado = dict(sorted(usuariosPaginas[usuario].items(), key=lambda item: item[1]['visitas'], reverse=True))
        res[usuario] = diccionario_ordenado

    totalVisitas = dict(sorted(totalVisitas.items(), key=lambda item: item[1]['visitas'], reverse=True))
    for pagina, visitas in paginasHosts.items():
        paginasHosts[pagina] = list(sorted(visitas.items(), key=lambda item: item[1]["visitas"], reverse=True))
    return paginasVisitadas, totalVisitas, res, paginasHosts


def tiemposSesion(content):

    for host in content:
        for usuario in content[host]:
            tiempoTotal = 0
            for sesion in content[host][usuario]["sesion"]:
                inicio = datetime.strptime(content[host][usuario]["sesion"][sesion][0]["fechaHora"], '%d/%b/%Y:%H:%M:%S')
                fin = datetime.strptime(content[host][usuario]["sesion"][sesion][len(content[host][usuario]["sesion"][sesion]) - 1]["fechaHora"], '%d/%b/%Y:%H:%M:%S')
                tiempo = (fin - inicio).total_seconds()
                tiempoTotal += tiempo
                content[host][usuario]["sesion"][sesion] = {"tiempoSesion": 0, "visitas": content[host][usuario]["sesion"][sesion]}
                content[host][usuario]["sesion"][sesion]["tiempoSesion"] = tiempo
            content[host][usuario]["TiempoMedioSesion"] = tiempoTotal / len(content[host][usuario]["sesion"])
    return content


def diario(content, tiempoCorte):
    visitasDiarias = dict()

    for host in content:
        for usuario in content[host]:
            for sesion in content[host][usuario]["sesion"]:
                for visita in range(len(content[host][usuario]["sesion"][sesion]["visitas"])):
                    pagina = content[host][usuario]["sesion"][sesion]["visitas"][visita]["pagina"]
                    fecha = content[host][usuario]["sesion"][sesion]["visitas"][visita]["Fecha"]
                    if visitasDiarias.keys().__contains__(pagina):
                        if visitasDiarias[pagina].keys().__contains__(fecha):
                            visitasDiarias[pagina][fecha]["visitas"].append(content[host][usuario]["sesion"][sesion]["visitas"][visita])
                        else:
                            visitasDiarias[pagina][fecha] = {"UsuariosUnicos": 0, "numeroVisitas": 0, "visitas": list()}
                            visitasDiarias[pagina][fecha]["visitas"].append(content[host][usuario]["sesion"][sesion]["visitas"][visita])
                    else:
                        visitasDiarias[pagina] = dict()
                        visitasDiarias[pagina][fecha] = {"UsuariosUnicos": 0, "numeroVisitas": 0, "visitas": list()}
                        visitasDiarias[pagina][fecha]["visitas"].append(content[host][usuario]["sesion"][sesion]["visitas"][visita])

    for pagina in visitasDiarias:
        for fecha in visitasDiarias[pagina]:
            usuarios = list()
            usuarioVez = dict()
            for visita in range(len(visitasDiarias[pagina][fecha]["visitas"])):
                if visitasDiarias[pagina][fecha]["visitas"][visita]["host"] not in usuarios:
                    visitasDiarias[pagina][fecha]["UsuariosUnicos"] += 1
                if not usuarioVez.keys().__contains__(visitasDiarias[pagina][fecha]["visitas"][visita]["host"]):
                    usuarioVez[visitasDiarias[pagina][fecha]["visitas"][visita]["host"]] = visita
                    visitasDiarias[pagina][fecha]["numeroVisitas"] += 1
                else:
                    if (visitasDiarias[pagina][fecha]["visitas"][visita]["Timestamp"] - visitasDiarias[pagina][fecha]["visitas"][usuarioVez[visitasDiarias[pagina][fecha]["visitas"][visita]["host"]]]["Timestamp"]) > tiempoCorte:
                        usuarioVez[visitasDiarias[pagina][fecha]["visitas"][visita]["host"]] = visita
                        visitasDiarias[pagina][fecha]["numeroVisitas"] += 1

    return visitasDiarias


def usuarioDiario(content, tiempoCorte):
    visitasDiarias = dict()

    for host in content:
        for usuario in content[host]:
            for sesion in content[host][usuario]["sesion"]:
                for visita in range(len(content[host][usuario]["sesion"][sesion]["visitas"])):
                    fecha = content[host][usuario]["sesion"][sesion]["visitas"][visita]["Fecha"]
                    if visitasDiarias.keys().__contains__(usuario):
                        if visitasDiarias[usuario].keys().__contains__(fecha):
                            visitasDiarias[usuario][fecha]["visitas"].append(content[host][usuario]["sesion"][sesion]["visitas"][visita])
                            visitasDiarias[usuario][fecha]["numeroVisitas"] += 1
                        else:
                            visitasDiarias[usuario][fecha] = {"numeroVisitas": 1, "visitas": list(), "tiempo": 0}
                            visitasDiarias[usuario][fecha]["visitas"].append(content[host][usuario]["sesion"][sesion]["visitas"][visita])
                    else:
                        visitasDiarias[usuario] = dict()
                        visitasDiarias[usuario][fecha] = {"numeroVisitas": 1, "visitas": list(), "tiempo": 0}
                        visitasDiarias[usuario][fecha]["visitas"].append(content[host][usuario]["sesion"][sesion]["visitas"][visita])
                    if (visita + 1) < len(content[host][usuario]["sesion"][sesion]["visitas"]):
                        if (content[host][usuario]["sesion"][sesion]["visitas"][visita + 1]["Timestamp"] - content[host][usuario]["sesion"][sesion]["visitas"][visita]["Timestamp"]) < tiempoCorte:
                            visitasDiarias[usuario][fecha]["tiempo"] += content[host][usuario]["sesion"][sesion]["visitas"][visita + 1]["Timestamp"] - content[host][usuario]["sesion"][sesion]["visitas"][visita]["Timestamp"]

    for usuario in visitasDiarias:
        for fecha in visitasDiarias[usuario]:
            aux = 0
            for visita in range(len(visitasDiarias[usuario][fecha]["visitas"])):
                if (visitasDiarias[usuario][fecha]["visitas"][visita]["Timestamp"] - visitasDiarias[usuario][fecha]["visitas"][aux]["Timestamp"]) > tiempoCorte:
                    aux = visita
                    visitasDiarias[usuario][fecha]["numeroVisitas"] += 1
                else:
                    visitasDiarias[usuario][fecha]["tiempo"] += visitasDiarias[usuario][fecha]["visitas"][visita]["Timestamp"] - visitasDiarias[usuario][fecha]["visitas"][aux]["Timestamp"]
    return visitasDiarias


def numeroSesiones(content):
    sesiones = 0
    for host in content:
        for usuario in content[host]:
            for sesion in content[host][usuario]["sesion"]:
                if sesiones < sesion:
                    sesiones = sesion
    return sesiones


def desliarSesiones(content):
    toRet = list()
    for host, resto in content.items():
        for usuario, resto2 in resto.items():
            for id, resto3 in resto2['sesion'].items():
                aux = resto3
                aux['id'] = id
                aux['host'] = host
                aux['usuario'] = usuario
                toRet.append(aux)
    return toRet


def extraccionExtensiones(content):
    extensiones = dict()
    for host in content:
        for usuario in content[host]:
            for sesion in content[host][usuario]["sesion"]:
                for i in range(len(content[host][usuario]["sesion"][sesion]["visitas"])):
                    pagina = content[host][usuario]["sesion"][sesion]["visitas"][i]["pagina"]
                    extension = pagina.split("/")[len(pagina.split("/")) - 1]
                    extension = extension.split(".")[len(extension.split(".")) - 1]
                    if extensiones.keys().__contains__(extension):
                        extensiones[extension] += 1
                    else:
                        extensiones[extension] = 1
    return extensiones


def obtenerBots(content, tiempoCorte):
    res = dict()
    paginasBots = dict()
    for host in content:
        for visita in range(len(content[host])):
            if "bot" in host:
                if not res.keys().__contains__("bot"):
                    res["bot"] = {"numeroVisitas": 0, "host": dict(), "visitas": list(), "tiempoUsado": 0}
                if not res["bot"]["host"].keys().__contains__(host):
                    res["bot"]["host"][host] = {"visitas": list(), "numeroVisitas": 0, "tiempoUsado": 0}
                res["bot"]["numeroVisitas"] += 1
                res["bot"]["visitas"].append(content[host][visita])
                if (visita + 1) < len(content[host]):
                    if (content[host][visita + 1]["Timestamp"] - content[host][visita]["Timestamp"]) < tiempoCorte:
                        res["bot"]["tiempoUsado"] += content[host][visita + 1]["Timestamp"] - content[host][visita]["Timestamp"]
                        res["bot"]["host"][host]["tiempoUsado"] += content[host][visita + 1]["Timestamp"] - content[host][visita]["Timestamp"]
                if not paginasBots.keys().__contains__(content[host][visita]["pagina"]):
                    paginasBots[content[host][visita]["pagina"]] = 0
                paginasBots[content[host][visita]["pagina"]] += 1
                res["bot"]["host"][host]["visitas"].append(content[host][visita])
                res["bot"]["host"][host]["numeroVisitas"] += 1
            elif "spider" in host:
                if not res.keys().__contains__("spider"):
                    res["spider"] = {"numeroVisitas": 0, "host": dict(), "visitas": list(), "tiempoUsado": 0}
                if not res["spider"]["host"].keys().__contains__(host):
                    res["spider"]["host"][host] = {"visitas": list(), "numeroVisitas": 0, "tiempoUsado": 0}
                res["spider"]["numeroVisitas"] += 1
                res["spider"]["visitas"].append(content[host][visita])
                if (visita + 1) < len(content[host]):
                    if (content[host][visita + 1]["Timestamp"] - content[host][visita]["Timestamp"]) < tiempoCorte:
                        res["spider"]["tiempoUsado"] += content[host][visita + 1]["Timestamp"] - content[host][visita][
                            "Timestamp"]
                        res["spider"]["host"][host]["tiempoUsado"] += content[host][visita + 1]["Timestamp"] - \
                                                                   content[host][visita]["Timestamp"]
                if not paginasBots.keys().__contains__(content[host][visita]["pagina"]):
                    paginasBots[content[host][visita]["pagina"]] = 0
                paginasBots[content[host][visita]["pagina"]] += 1
                res["spider"]["host"][host]["visitas"].append(content[host][visita])
                res["spider"]["host"][host]["numeroVisitas"] += 1
            else:
                if not res.keys().__contains__("crawler"):
                    res["crawler"] = {"numeroVisitas": 0, "host": dict(), "visitas": list(), "tiempoUsado": 0}
                if not res["crawler"]["host"].keys().__contains__(host):
                    res["crawler"]["host"][host] = {"visitas": list(), "numeroVisitas": 0, "tiempoUsado": 0}
                res["crawler"]["numeroVisitas"] += 1
                res["crawler"]["visitas"].append(content[host][visita])
                if (visita + 1) < len(content[host]):
                    if (content[host][visita + 1]["Timestamp"] - content[host][visita]["Timestamp"]) < tiempoCorte:
                        res["crawler"]["tiempoUsado"] += content[host][visita + 1]["Timestamp"] - content[host][visita][
                            "Timestamp"]
                        res["bot"]["host"][host]["tiempoUsado"] += content[host][visita + 1]["Timestamp"] - \
                                                                   content[host][visita]["Timestamp"]
                if not paginasBots.keys().__contains__(content[host][visita]["pagina"]):
                    paginasBots[content[host][visita]["pagina"]] = 0
                paginasBots[content[host][visita]["pagina"]] += 1
                res["crawler"]["host"][host]["visitas"].append(content[host][visita])
                res["crawler"]["host"][host]["numeroVisitas"] += 1

    return res, paginasBots


def desliarHosts(actualizadoSesiones, visitasUsuarioDiarias):
    visitasDiarias = dict()
    host = dict()
    for clave, contenido in actualizadoSesiones.items():
        host[clave] = dict()
        host[clave]['sesiones'] = dict()
        usuarios = list(contenido.keys())
        host[clave]['numSesiones'] = 0
        host[clave]['numVisitas'] = 0
        visitasDiarias[clave] = dict()
        for usuario in usuarios:
            host[clave]['sesiones'][usuario] = contenido[usuario]['sesion']
            host[clave]['numSesiones'] += len(contenido[usuario]['sesion'])
            for clave2, sesion in contenido[usuario]['sesion'].items():
                host[clave]['numVisitas'] += len(sesion)
            visitasDiarias[clave][usuario] = visitasUsuarioDiarias[usuario]
    return host, visitasDiarias


def obtenerSeguidas(sesiones):
    paginasSeguidas = dict()
    sinFin = dict()
    fin = dict()
    inicio = dict()
    for sesion in sesiones:
        if ('inicio', sesion['visitas'][0]['pagina']) in paginasSeguidas:
            paginasSeguidas[('inicio', sesion['visitas'][0]['pagina'])] += 1
            inicio[('inicio', sesion['visitas'][0]['pagina'])] += 1
        else:
            paginasSeguidas[('inicio', sesion['visitas'][0]['pagina'])] = 1
            inicio[('inicio', sesion['visitas'][0]['pagina'])] = 1
        for i in range(len(sesion['visitas'])-1):
            actual = sesion['visitas'][i]['pagina']
            siguiente = sesion['visitas'][i+1]['pagina']
            if (actual,siguiente) in paginasSeguidas:
                paginasSeguidas[(actual,siguiente)] += 1
                sinFin[(actual, siguiente)] += 1
            else:
                paginasSeguidas[(actual, siguiente)] = 1
                sinFin[(actual, siguiente)] = 1
        if (sesion['visitas'][-1]['pagina'],'fin') in paginasSeguidas:
            paginasSeguidas[(sesion['visitas'][-1]['pagina'],'fin')] += 1
            fin[(sesion['visitas'][-1]['pagina'],'fin')] += 1
        else:
            paginasSeguidas[(sesion['visitas'][-1]['pagina'],'fin')] = 1
            fin[(sesion['visitas'][-1]['pagina'], 'fin')] = 1
    ordenado = sorted(paginasSeguidas.items(), key=lambda kv: kv[1], reverse=True)
    sinFinOrdenado = sorted(sinFin.items(), key=lambda kv: kv[1], reverse=True)
    finOrdenado = sorted(fin.items(), key=lambda kv: kv[1], reverse=True)
    inicioOrdenado = sorted(inicio.items(), key=lambda kv: kv[1], reverse=True)
    return paginasSeguidas, ordenado, sinFinOrdenado, finOrdenado, inicioOrdenado


# Analiza el contenido extraido de los logs para extraer conocimiento de los mismos
def analizar(path,proc, procOriginal, bots, tiempoCorte):
    if not os.path.exists("Logs procesados"):
        print("Lanzar error")

    procesados = proc
    visitasPagina, totalPaginas, usuariosPaginas, paginasHosts = paginasVisitadas(procesados['contenido'])
    actualizadoSesiones = tiemposSesion(procesados['contenido'])
    sesiones = desliarSesiones(actualizadoSesiones)
    visitasDiariasPaginas = diario(procesados['contenido'],tiempoCorte)
    visitasUsuarioDiarias = usuarioDiario(procesados['contenido'],tiempoCorte)
    sesionesTotales = numeroSesiones(procesados['contenido'])
    extensiones = extraccionExtensiones(procesados["contenido"])
    host, visitasDiarias = desliarHosts(actualizadoSesiones, visitasUsuarioDiarias)
    datosBots, paginasBots = obtenerBots(bots, tiempoCorte)
    paginasSeguidas, paginasSeguidasOrdenado, ordenadoSinFin, ordenadoFin, inicioOrdenado = obtenerSeguidas(sesiones)

    megaDic = {'procesado': procOriginal, 'visitasPagina': visitasPagina, 'totalPaginas': totalPaginas, 'usuariosPaginas': usuariosPaginas,
            'actualizadoSesiones': actualizadoSesiones, 'visitasDiariasPaginas': visitasDiariasPaginas, 'visitasUsuarioDiarias': visitasUsuarioDiarias,
            'numSesiones': sesionesTotales, 'sesionesOrdenadas': sesiones, 'repeticionExtensiones': extensiones, 'visitasHostDiarias': visitasDiarias,
            'host': host, 'datosBots': datosBots, 'paginasSeguidas': paginasSeguidas, 'paginasSeguidasOrdenado': paginasSeguidasOrdenado, 'ordenadoSinFin': ordenadoSinFin,
            'ordenadoFin': ordenadoFin, "paginasBots": paginasBots, 'paginasHosts': paginasHosts, 'inicioOrdenado': inicioOrdenado}

    path = path.split("/")[len(path.split("/")) - 1]
    fichero_indice = open("Logs procesados/" + path, "wb")
    pickle.dump(megaDic, fichero_indice)

