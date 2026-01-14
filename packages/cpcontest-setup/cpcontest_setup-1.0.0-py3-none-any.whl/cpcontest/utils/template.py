import os
from datetime import datetime
from cpcontest.constants import AUTOR_DEFAULT, EQUIPO_RPC_DEFAULT


def procesar_plantilla(ruta_plantilla, datos_reemplazo):
    """
    Lee una plantilla y reemplaza los marcadores con datos reales

    Args:
        ruta_plantilla: Ruta al archivo de plantilla
        datos_reemplazo: Diccionario con los datos a reemplazar

    Returns:
        Lista de líneas procesadas
    """
    if not os.path.exists(ruta_plantilla):
        return None

    with open(ruta_plantilla, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    lineas_procesadas = []
    for linea in lineas:
        for clave, valor in datos_reemplazo.items():
            linea = linea.replace(clave, valor)
        lineas_procesadas.append(linea)

    return lineas_procesadas


def obtener_datos_fecha():
    """Obtiene los datos de fecha actual"""
    fecha_hora = datetime.now()
    return {
        "dia": fecha_hora.strftime("%d"),
        "mes": fecha_hora.strftime("%m"),
        "anio": fecha_hora.strftime("%Y"),
    }


def crear_datos_reemplazo_standard(nombre_archivo):
    """Crea diccionario de reemplazo para plantillas estándar"""
    fecha = obtener_datos_fecha()
    return {
        "$%U%$": AUTOR_DEFAULT,
        "$%D%$": fecha["dia"],
        "$%M%$": fecha["mes"],
        "$%Y%$": fecha["anio"],
        "$%file%$": nombre_archivo,
    }


def crear_datos_reemplazo_rpc(nombre_archivo, numero_ronda):
    """Crea diccionario de reemplazo para plantillas RPC"""
    fecha = obtener_datos_fecha()
    return {
        "$%U%$": EQUIPO_RPC_DEFAULT,
        "$%D%$": fecha["dia"],
        "$%M%$": fecha["mes"],
        "$%Y%$": fecha["anio"],
        "$%R%$": numero_ronda,
        "$%file%$": nombre_archivo,
    }
