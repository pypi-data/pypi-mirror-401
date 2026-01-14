import os
from cpcontest.platforms.base import BaseContest
from cpcontest.utils.template import procesar_plantilla, crear_datos_reemplazo_rpc
from cpcontest.utils.filesystem import crear_archivo_entrada
from cpcontest.constants import PLANTILLAS_ARCHIVO, PLANTILLA_RPC_CPP


class RPCContest(BaseContest):
    """Maneja rondas de RPC"""

    def crear_archivos(self, lista_problemas, numero_concurso):
        """Crea los archivos para la ronda de RPC"""
        if self.extension == "cpp":
            nombre_plantilla = PLANTILLA_RPC_CPP
        else:
            nombre_plantilla = PLANTILLAS_ARCHIVO[self.extension]

        ruta_plantilla = os.path.join(self.ruta_plantillas, nombre_plantilla)
        plantilla_existe = self.verificar_plantilla_existe(ruta_plantilla)

        self.imprimir_encabezado()

        for problema_id in lista_problemas:
            ruta_problema = os.path.join(self.ruta_concurso, problema_id)
            os.makedirs(ruta_problema, exist_ok=True)

            archivo_base = os.path.join(
                ruta_problema, f"{problema_id}.{self.extension}"
            )

            if plantilla_existe:
                datos_reemplazo = crear_datos_reemplazo_rpc(
                    problema_id, numero_concurso
                )
                lineas = procesar_plantilla(ruta_plantilla, datos_reemplazo)
                self.escribir_archivo(archivo_base, lineas)
            else:
                self.escribir_archivo(archivo_base, f"// Problema {problema_id}\n")

            archivo_entrada = os.path.join(ruta_problema, "in1")
            crear_archivo_entrada(archivo_entrada)

            print(f"{problema_id}/{problema_id}.{self.extension}")
            print(f"{problema_id}/in1")

        self.imprimir_pie()
