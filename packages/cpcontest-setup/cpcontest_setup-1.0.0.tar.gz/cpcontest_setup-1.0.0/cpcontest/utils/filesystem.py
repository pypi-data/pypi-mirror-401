import os
import re
import glob
import shutil


def buscar_documento_pdf(directorio_descargas):
    """Busca un PDF de problemas en la carpeta de descargas"""
    archivos_pdf = glob.glob(os.path.join(directorio_descargas, "*.pdf"))

    for archivo in archivos_pdf:
        nombre_archivo = os.path.basename(archivo)
        if re.search(r"(problem|set|rpc|rnd|round)", nombre_archivo, re.IGNORECASE):
            return archivo

    if archivos_pdf:
        archivos_pdf.sort(key=os.path.getmtime, reverse=True)
        return archivos_pdf[0]

    return None


def mover_pdf_a_concurso(ruta_concurso, ruta_descargas):
    """Mueve el PDF de problemas a la carpeta del concurso"""
    if not ruta_descargas or not os.path.exists(ruta_descargas):
        print("\033[93mNo se pudo acceder a la carpeta de descargas.\033[0m")
        return False

    archivo_pdf = buscar_documento_pdf(ruta_descargas)

    if archivo_pdf:
        nombre_pdf = os.path.basename(archivo_pdf)
        destino_pdf = os.path.join(ruta_concurso, nombre_pdf)

        try:
            shutil.move(archivo_pdf, destino_pdf)
            print(f"\033[92mPDF encontrado y movido: {nombre_pdf}\033[0m")
            return True
        except Exception as e:
            print(f"\033[91mError al mover el PDF: {str(e)}\033[0m")
            return False
    else:
        print("\033[93mNo se encontró PDF de problemas en Descargas.\033[0m")
        return False


def crear_archivo_entrada(ruta):
    """Crea un archivo de entrada vacío"""
    open(ruta, "w").close()
