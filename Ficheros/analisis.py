from datetime import datetime

def obtencionMedias(content):
    print("hola")


def metricasUsuarios(content):
    print("hola")


def tiemposNavegacion(content):
    print("hola")


def tiemposPagina(content):
    print("Hola")


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
        totalVisitas[pagina] = 0
        for usuario in paginasVisitadas[pagina]:
            totalVisitas[pagina] += paginasVisitadas[pagina][usuario]

    res = dict()
    for usuario in usuariosPaginas:
        diccionario_ordenado = dict(sorted(usuariosPaginas[usuario].items(), key=lambda item: item[1]['visitas'], reverse=True))
        res[usuario] = diccionario_ordenado

    totalVisitas = dict(sorted(totalVisitas.items(), key=lambda item: item[1], reverse=True))
    return paginasVisitadas,totalVisitas, res


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