from datetime import datetime
import os
import pickle
import dependencias.parseador as parseador

# Trabaja con los logs del directorio para realizar un preprocesamiento del mismo obteniendo los datos del mismo
def procesar(path):
    if not os.path.exists("Logs") or len(os.listdir("Logs")) == 0:
        print("Lanzar error")

    if not os.path.exists("Logs procesados"):
        os.mkdir("Logs procesados")

    procOriginal = parseador.procesarLog(path)
    proc = limitarExtensiones(procOriginal, ("html", "htm", "pdf", "asp", "exe", "txt", "doc", "ppt", "xls", "xml", ""))
    proc, bots = eliminarBots(proc)
    proc = definirTiempos(proc)
    proc = identificarUsuarios(proc)
    tiempoCorte = 1800
    proc = definirSesiones(proc, tiempoCorte)

    return proc, procOriginal, bots

def definirTiempos(log):
    content = log['contenido']
    minimaFecha = content[next(iter(content))][0]["fechaHora"]
    for host in content:
        for visita in range(len(content[host])):
            fecha1 = datetime.strptime(minimaFecha, '%d/%b/%Y:%H:%M:%S')
            fecha2 = datetime.strptime(content[host][visita]["fechaHora"], '%d/%b/%Y:%H:%M:%S')
            if fecha2 < fecha1:
                minimaFecha = content[host][visita]["fechaHora"]

    fecha1 = datetime.strptime(minimaFecha, '%d/%b/%Y:%H:%M:%S')

    for host in content:
        for visita in range(len(content[host])):
            content[host][visita]["Fecha"] = content[host][visita]["fechaHora"].split(":")[0]
            content[host][visita]["Hora"] = "" + content[host][visita]["fechaHora"].split(":")[1] + ":" + content[host][visita]["fechaHora"].split(":")[2] + ":" + content[host][visita]["fechaHora"].split(":")[3]
            fecha2 = datetime.strptime(content[host][visita]["fechaHora"], '%d/%b/%Y:%H:%M:%S')
            content[host][visita]["Timestamp"] = (fecha2 - fecha1).total_seconds()
    columnas = log['columnas']
    return {'contenido': content, 'columnas': columnas}


def eliminarBots(log):
    content = log['contenido']
    res = dict()
    bots = dict()
    for host in content:
        if "bot" in host or "crawler" in host or "spider" in host:
            bots[host] = content[host]
        else:
            res[host] = content[host]
    return {'contenido': res, 'columnas': log['columnas']}, bots


def definirSesiones(log, time):
    content = log['contenido']
    sesionesIP = dict()
    for host in content:
        sesionesIP[host] = dict()
        for usuario in content[host]:
            sesionesIP[host][usuario] = dict()
            sesionesIP[host][usuario]["sesion"] = dict()

    sesion = 1
    for host in content:
        for usuario in content[host]:
            for visita in range(len(content[host][usuario])):
                if len(sesionesIP[host][usuario]["sesion"]) > 0:
                    if (content[host][usuario][visita]["Timestamp"] - sesionesIP[host][usuario]["sesion"][sesion][0]["Timestamp"]) < time:
                        sesionesIP[host][usuario]["sesion"][sesion].append(content[host][usuario][visita])
                    else:
                        sesion += 1
                        sesionesIP[host][usuario]["sesion"][sesion] = list()
                        sesionesIP[host][usuario]["sesion"][sesion].append(content[host][usuario][visita])
                else:
                    sesionesIP[host][usuario]["sesion"][sesion] = list()
                    sesionesIP[host][usuario]["sesion"][sesion].append(content[host][usuario][visita])
            sesion += 1
    return {'contenido': sesionesIP, 'columnas': log['columnas']}


def identificarUsuarios(log):
    content = log['contenido']
    usuarios = dict()
    for host in content:
        usuarios[host] = dict()
        for visita in range(len(content[host])):
            if content[host][visita]["usuario"] == "-":
                usuarios[host][host] = list()
            else:
                usuarios[host][content[host][visita]["usuario"]] = list()
    for host in content:
        for visita in range(len(content[host])):
            for usuario in usuarios[host]:
                if usuario == content[host][visita]["usuario"] or usuario == host:
                    usuarios[host][usuario].append(content[host][visita])
    return {'contenido': usuarios, 'columnas': log['columnas']}


def limitarExtensiones(log, extensiones):
    content = log['contenido']
    res = dict()
    for host in content:
        res[host] = list()
        for visita in range(len(content[host])):
            pagina = content[host][visita]["pagina"]
            extension = pagina.split("/")[len(pagina.split("/")) - 1]
            extension = extension.split(".")[len(extension.split(".")) - 1]
            if extension in extensiones:
                res[host].append(content[host][visita])
    return {'contenido': res, 'columnas': log['columnas']}