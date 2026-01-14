import os
from cpcontest.platforms.base import BaseContest
from cpcontest.utils.template import procesar_plantilla, crear_datos_reemplazo_standard
from cpcontest.utils.filesystem import crear_archivo_entrada
from cpcontest.constants import PLANTILLAS_ARCHIVO


class GenericContest(BaseContest):
    """Maneja concursos de plataformas genéricas"""

    def crear_archivos(self, cantidad):
        """Crea archivos genéricos (A, B, C, etc.)"""
        ruta_plantilla = os.path.join(
            self.ruta_plantillas, PLANTILLAS_ARCHIVO[self.extension]
        )
        plantilla_existe = self.verificar_plantilla_existe(ruta_plantilla)

        self.imprimir_encabezado()

        for i in range(cantidad):
            nombre_archivo = chr(65 + i)
            ruta_salida = os.path.join(
                self.ruta_concurso, f"{nombre_archivo}.{self.extension}"
            )

            if plantilla_existe:
                datos_reemplazo = crear_datos_reemplazo_standard(nombre_archivo)
                lineas = procesar_plantilla(ruta_plantilla, datos_reemplazo)
                self.escribir_archivo(ruta_salida, lineas)
            else:
                self.escribir_archivo(ruta_salida, f"// Problema {nombre_archivo}\n")

            print(f"{nombre_archivo}.{self.extension}")

        crear_archivo_entrada(os.path.join(self.ruta_concurso, "in1"))
        print("in1")

        self.imprimir_pie()
