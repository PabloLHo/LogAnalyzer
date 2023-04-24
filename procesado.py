from datetime import datetime


def definirTiempos(content):
    minimaFecha = content[next(iter(content))][next(iter(content[next(iter(content))]))]["fechaHora"]
    for host in content:
        for visita in content[host]:
            fecha1 = datetime.strptime(minimaFecha, '%Y-%m-%d:%H:%M:%S')
            fecha2 = datetime.strptime(content[host][visita]["fechaHora"], '%Y-%m-%d:%H:%M:%S')
            if fecha2 < fecha1:
                minimaFecha = content[host][visita]["fechaHora"]

    fecha1 = datetime.strptime(minimaFecha, '%Y-%m-%d:%H:%M:%S')

    for host in content:
        for visita in content[host]:
            content[host][visita]["Fecha"] = content[host][visita]["fechaHora"].split(":")[0]
            content[host][visita]["Hora"] = "" + content[host][visita]["fechaHora"].split(":")[1] + ":" + content[host][visita]["fechaHora"].split(":")[2] + ":" + content[host][visita]["fechaHora"].split(":")[3]
            fecha2 = datetime.strptime(content[host][visita]["fechaHora"], '%Y-%m-%d:%H:%M:%S')
            content[host][visita]["Timestamp"] = (fecha2 - fecha1).total_seconds()


def eliminarBots(content):
    res = dict()
    for host in content:
        if "bot" in host or "crawler" in host or "spider" in host:
            pass
        else:
            res[host] = content[host]
    return res


def definirSesiones(content, time):
    sesionesIP = dict()
    for host in content:
        sesionesIP[host] = dict()
        for usuario in content[host]:
            sesionesIP[host][usuario] = dict()

    sesion = 1
    for host in content:
        for usuario in content[host]:
            for visita in content[host][usuario]:
                if len(sesionesIP[host][usuario][sesion]) > 0:
                    if (content[host][usuario][visita]["Timestamp"] - sesionesIP[host][usuario][sesion][0]) < time:
                        sesionesIP[host][usuario][sesion].append(content[host][usuario][visita])
                    else:
                        sesion += 1
                        sesionesIP[host][usuario][sesion].append(content[host][usuario][visita])
                else:
                    sesionesIP[host][usuario][sesion].append(content[host][usuario][visita])
            sesion += 1
    return sesionesIP


def identificarUsuarios(content):
    usuarios = dict()
    for host in content:
        usuarios[host] = dict()
        for visita in content[host]:
            if content[host][visita]["usuario"] == "-":
                usuarios[host][host] = list()
            else:
                usuarios[host][content[host][visita]["usuario"]] = list()
    for host in content:
        for visita in content[host]:
            for usuario in usuarios[host]:
                if usuario == content[host][visita]["usuario"] or usuario == host:
                    usuarios[host][usuario].append(content[host][visita])
    return usuarios
