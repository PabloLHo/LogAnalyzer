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
                            usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]] += 1
                        else:
                            usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]] = 1
                    else:
                        usuariosPaginas[usuario] = dict()
                        usuariosPaginas[usuario][content[host][usuario]["sesion"][sesion][visita]["pagina"]] = 1
    totalVisitas = dict()

    for pagina in paginasVisitadas:
        totalVisitas[pagina] = 0
        for usuario in paginasVisitadas[pagina]:
            totalVisitas[pagina] += paginasVisitadas[pagina][usuario]

    res = dict()
    for usuario in usuariosPaginas:
        diccionario_ordenado = dict(sorted(usuariosPaginas[usuario].items(), key=lambda item: item[1], reverse=True))
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