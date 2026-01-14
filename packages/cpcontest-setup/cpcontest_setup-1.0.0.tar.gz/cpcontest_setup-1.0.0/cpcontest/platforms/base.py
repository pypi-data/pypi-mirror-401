import os
from abc import ABC, abstractmethod
from cpcontest.config import obtener_ruta_plantillas
from cpcontest.utils.filesystem import crear_archivo_entrada


class BaseContest(ABC):
    """Clase base abstracta para concursos"""

    def __init__(self, ruta_concurso, extension, sistema):
        self.ruta_concurso = ruta_concurso
        self.extension = extension
        self.sistema = sistema
        self.ruta_plantillas = obtener_ruta_plantillas(sistema)

    @abstractmethod
    def crear_archivos(self, *args, **kwargs):
        """Método abstracto para crear archivos del concurso"""
        pass

    def verificar_plantilla_existe(self, ruta_plantilla):
        """Verifica si existe una plantilla"""
        if not os.path.exists(ruta_plantilla):
            print(
                f"\033[93mAdvertencia: No se encontró la plantilla para {self.extension}\033[0m"
            )
            print(f"\033[93mCreando archivos vacíos...\033[0m")
            return False
        return True

    def escribir_archivo(self, ruta_archivo, contenido):
        """Escribe contenido en un archivo"""
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            if isinstance(contenido, list):
                f.writelines(contenido)
            else:
                f.write(contenido)

    def imprimir_encabezado(self):
        """Imprime encabezado de archivos creados"""
        print("\033[94mArchivos creados:\n-----------------------------\033[0m")

    def imprimir_pie(self):
        """Imprime pie de archivos creados"""
        print("\033[94m-----------------------------\033[0m")
