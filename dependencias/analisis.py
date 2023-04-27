from datetime import datetime
import os
import pickle

def paginasVisitadas(content):
    paginasVisitadas = dict()
    usuariosPaginas = dict()
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
    return paginasVisitadas, totalVisitas, res


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
                        else:
                            visitasDiarias[usuario][fecha] = {"numeroVisitas": 1, "visitas": list()}
                            visitasDiarias[usuario][fecha]["visitas"].append(content[host][usuario]["sesion"][sesion]["visitas"][visita])
                    else:
                        visitasDiarias[usuario] = dict()
                        visitasDiarias[usuario][fecha] = {"numeroVisitas": 1, "visitas": list()}
                        visitasDiarias[usuario][fecha]["visitas"].append(content[host][usuario]["sesion"][sesion]["visitas"][visita])

    for usuario in visitasDiarias:
        for fecha in visitasDiarias[usuario]:
            aux = 0
            for visita in range(len(visitasDiarias[usuario][fecha]["visitas"])):
                if (visitasDiarias[usuario][fecha]["visitas"][visita]["Timestamp"] - visitasDiarias[usuario][fecha]["visitas"][aux]["Timestamp"]) > tiempoCorte:
                    aux = visita
                    visitasDiarias[usuario][fecha]["numeroVisitas"] += 1
    return visitasDiarias


def numeroSesiones(content):
    sesiones = 0
    for host in content:
        for usuario in content[host]:
            for sesion in content[host][usuario]["sesion"]:
                if sesiones < sesion:
                    sesiones = sesion
    return sesiones


# Analiza el contenido extraido de los logs para extraer conocimiento de los mismos
def analizar(path):
    if not os.path.exists("Logs procesados") or len(os.listdir("Logs procesados")) == 0:
        print("Lanzar error")

    path = path.split("/")[len(path.split("/")) - 1]
    fichero_procesado = open("Logs procesados/" + path, "rb")
    tiempoCorte = 1800
    aux = pickle.load(fichero_procesado)
    procesados = aux['proc']
    visitasPagina, totalPaginas, usuariosPaginas = paginasVisitadas(procesados['contenido'])
    actualizadoSesiones = tiemposSesion(procesados['contenido'])
    visitasDiariasPaginas = diario(procesados['contenido'],tiempoCorte)
    visitasUsuarioDiarias = usuarioDiario(procesados['contenido'],tiempoCorte)
    sesionesTotales = numeroSesiones(procesados['contenido'])

    return {'procesado': aux['original'], 'visitasPagina': visitasPagina, 'totalPaginas': totalPaginas, 'usuariosPaginas': usuariosPaginas,
            'actualizadoSesiones': actualizadoSesiones, 'visitasDiariasPaginas': visitasDiariasPaginas, 'visitasUsuarioDiarias': visitasUsuarioDiarias,
            'numSesiones': sesionesTotales}