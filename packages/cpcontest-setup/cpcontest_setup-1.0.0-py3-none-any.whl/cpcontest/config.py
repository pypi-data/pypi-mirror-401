import os
import platform
from datetime import datetime
from cpcontest.constants import CARPETAS_DESCARGAS


def detectar_sistema_operativo():
    """Detecta el sistema operativo actual"""
    return platform.system()


def obtener_anio_actual():
    """Obtiene el año actual"""
    return datetime.now().strftime("%Y")


def obtener_ruta_base(sistema, plataforma_abrev):
    """Construye la ruta base según el sistema operativo y plataforma"""
    anio = obtener_anio_actual()
    if sistema == "Windows":
        particion_del_disco = "D"
        ruta = f"{particion_del_disco}:\\Workspace\\Competitive-Programming\\Contests\\{plataforma_abrev}\\{anio}"
    elif sistema == "Linux":
        usuario = os.getenv("USER") or os.getenv("USERNAME") or "user"
        ruta = f"/home/{usuario}/Workspace/Competitive-Programming/Contests/{plataforma_abrev}/{anio}"
    elif sistema == "Darwin":
        usuario = os.getenv("USER") or os.getenv("USERNAME") or "user"
        ruta = f"/Users/{usuario}/Workspace/Competitive-Programming/Contests/{plataforma_abrev}/{anio}"
    return ruta


def obtener_ruta_plantillas(sistema):
    """Obtiene la ruta de las plantillas según el sistema operativo"""
    if sistema == "Windows":
        particion_del_disco = "D"
        return f"{particion_del_disco}:\\Workspace\\Competitive-Programming\\Templates"
    elif sistema == "Linux":
        usuario = os.getenv("USER") or os.getenv("USERNAME") or "user"
        return f"/home/{usuario}/Workspace/Competitive-Programming/Templates"
    elif sistema == "Darwin":
        usuario = os.getenv("USER") or os.getenv("USERNAME") or "user"
        return f"/Users/{usuario}/Workspace/Competitive-Programming/Templates"
    return None


def obtener_ruta_descargas(sistema):
    """Obtiene la ruta de la carpeta de descargas del usuario"""
    inicio_usuario = os.path.expanduser("~")
    for carpeta in CARPETAS_DESCARGAS:
        ruta = os.path.join(inicio_usuario, carpeta)
        if os.path.isdir(ruta):
            return ruta
    return inicio_usuario
