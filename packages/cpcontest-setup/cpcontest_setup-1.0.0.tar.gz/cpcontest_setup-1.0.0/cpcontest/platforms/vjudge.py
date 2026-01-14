import os
import json
import urllib.request
import urllib.error
from cpcontest.platforms.base import BaseContest
from cpcontest.utils.template import procesar_plantilla, crear_datos_reemplazo_standard
from cpcontest.utils.filesystem import crear_archivo_entrada
from cpcontest.constants import PLANTILLAS_ARCHIVO


class VJudgeContest(BaseContest):
    """Maneja concursos de VJudge"""

    @staticmethod
    def obtener_problemas(contest_id):
        """Obtiene la lista de problemas desde la API de VJudge"""
        url = f"https://vjudge.net/contest/data?contestId={contest_id}&dataType=rank"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": f"https://vjudge.net/contest/{contest_id}",
        }

        try:
            peticion = urllib.request.Request(url, headers=headers)
            respuesta = urllib.request.urlopen(peticion, timeout=10)
            datos = json.loads(respuesta.read().decode("utf-8"))

            problemas = datos.get("problems", [])

            if not problemas:
                print("\033[91mNo se encontraron problemas para este concurso.\033[0m")
                return None

            lista_problemas = []
            for problema in problemas:
                titulo = problema.get("title", "")
                numero = problema.get("num", 0)

                letra = chr(65 + numero) if numero < 26 else f"Problem_{numero}"

                if titulo:
                    nombre_formateado = f"{letra}_{titulo}"
                else:
                    nombre_formateado = letra

                nombre_archivo = nombre_formateado.replace(" ", "_")

                caracteres_invalidos = r'<>:"/\|?*!,;=+&%'
                for char in caracteres_invalidos:
                    nombre_archivo = nombre_archivo.replace(char, "")

                nombre_archivo = nombre_archivo[:100]

                lista_problemas.append(nombre_archivo)

            return lista_problemas

        except urllib.error.HTTPError as e:
            print(f"\033[91mError HTTP {e.code}: {e.reason}\033[0m")
            print(
                "\033[93mVerifica que el ID del concurso sea correcto (ej: 4559)\033[0m"
            )
            return None
        except urllib.error.URLError as e:
            print(f"\033[91mError de conexión: {e.reason}\033[0m")
            return None
        except json.JSONDecodeError:
            print("\033[91mError al decodificar la respuesta JSON\033[0m")
            return None
        except Exception as e:
            print(f"\033[91mError inesperado: {str(e)}\033[0m")
            return None

    def crear_archivos(self, cantidad, nombres_problemas):
        """Crea los archivos para el concurso de VJudge"""
        ruta_plantilla = os.path.join(
            self.ruta_plantillas, PLANTILLAS_ARCHIVO[self.extension]
        )
        plantilla_existe = self.verificar_plantilla_existe(ruta_plantilla)

        self.imprimir_encabezado()

        for i in range(cantidad):
            if i < len(nombres_problemas):
                nombre_archivo = nombres_problemas[i]
            else:
                nombre_archivo = f"Problema_{chr(65 + i)}"

            ruta_salida = os.path.join(
                self.ruta_concurso, f"{nombre_archivo}.{self.extension}"
            )

            if plantilla_existe:
                datos_reemplazo = crear_datos_reemplazo_standard(nombre_archivo)
                lineas = procesar_plantilla(ruta_plantilla, datos_reemplazo)
                self.escribir_archivo(ruta_salida, lineas)
            else:
                self.escribir_archivo(ruta_salida, f"// {nombre_archivo}\n")

            print(f"{nombre_archivo}.{self.extension}")

        crear_archivo_entrada(os.path.join(self.ruta_concurso, "in1"))
        print("in1")

        self.imprimir_pie()
