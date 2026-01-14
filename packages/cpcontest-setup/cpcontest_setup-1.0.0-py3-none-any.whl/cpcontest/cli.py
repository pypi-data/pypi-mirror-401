import os
from datetime import datetime
from cpcontest.config import (
    detectar_sistema_operativo,
    obtener_ruta_base,
    obtener_ruta_descargas,
)
from cpcontest.constants import PLATAFORMAS, EXTENSIONES_LENGUAJE, NOMBRE_LENGUAJES
from cpcontest.platforms import (
    CodeforcesContest,
    CodeChefContest,
    VJudgeContest,
    RPCContest,
    GenericContest,
)
from cpcontest.utils.filesystem import mover_pdf_a_concurso
from cpcontest.utils.editor import abrir_editor


def seleccionar_lenguaje():
    """Solicita al usuario que seleccione un lenguaje de programación"""
    while True:
        print("\033[93m¿En qué lenguaje resolverás?\033[0m")
        for key, nombre in NOMBRE_LENGUAJES.items():
            print(f"{key}. {nombre}")

        opcion = input("\033[93m->\033[0m ").strip()

        if opcion in EXTENSIONES_LENGUAJE:
            return EXTENSIONES_LENGUAJE[opcion]
        else:
            print("\033[91mOpción inválida. Intenta de nuevo.\033[0m")


def mostrar_banner(sistema):
    """Muestra el banner de bienvenida"""
    print(f"\033[96m╔════════════════════════════════════════════════════════╗\033[0m")
    print(f"\033[96m     Generador Universal de Concursos  |  SO: {sistema:8s}\033[0m")
    print(
        f"\033[96m╚════════════════════════════════════════════════════════╝\033[0m\n"
    )


def seleccionar_plataforma():
    """Solicita al usuario que seleccione una plataforma"""
    print("\033[93mSelecciona la plataforma:\033[0m")
    for key, value in PLATAFORMAS.items():
        print(f"{key}. {value['nombre']}")

    plataforma_id = input("\033[93m->\033[0m ").strip()

    if plataforma_id not in PLATAFORMAS:
        print("\033[91mPlataforma inválida.\033[0m")
        return None

    return PLATAFORMAS[plataforma_id]


def crear_directorio_concurso(ruta_concurso):
    """Crea el directorio del concurso y verifica si ya existe"""
    if os.path.exists(ruta_concurso):
        print(f"\033[91mEl concurso ya existe 😞\033[0m")
        print(f"Ruta: {ruta_concurso}")
        return False

    os.makedirs(ruta_concurso, exist_ok=True)
    return True


def procesar_codeforces(contest_id, ruta_concurso, extension, sistema):
    """Procesa un concurso de Codeforces"""
    print("\033[93mObteniendo información del concurso...\033[0m")
    nombres_problemas = CodeforcesContest.obtener_problemas(contest_id)

    if nombres_problemas is None:
        print("\033[91mNo se pudo obtener la información del concurso.\033[0m")
        return False

    print(f"\033[92mSe encontraron {len(nombres_problemas)} problemas.\033[0m")

    cantidad = input(
        f"\033[93m¿Cuántos problemas resolverás [max: {len(nombres_problemas)}]? ->\033[0m "
    ).strip()

    if not cantidad.isdigit():
        cantidad = len(nombres_problemas)
    else:
        cantidad = min(int(cantidad), len(nombres_problemas))

    contest = CodeforcesContest(ruta_concurso, extension, sistema)
    contest.crear_archivos(cantidad, nombres_problemas)
    return True


def procesar_codechef(contest_code, ruta_concurso, extension, sistema):
    """Procesa un concurso de CodeChef"""
    print("\033[93mObteniendo información del concurso...\033[0m")
    nombres_problemas = CodeChefContest.obtener_problemas(contest_code)

    if nombres_problemas is None:
        print("\033[91mNo se pudo obtener la información del concurso.\033[0m")
        return False

    print(f"\033[92mSe encontraron {len(nombres_problemas)} problemas.\033[0m")

    cantidad = input(
        f"\033[93m¿Cuántos problemas resolverás [max: {len(nombres_problemas)}]? ->\033[0m "
    ).strip()

    if not cantidad.isdigit():
        cantidad = len(nombres_problemas)
    else:
        cantidad = min(int(cantidad), len(nombres_problemas))

    contest = CodeChefContest(ruta_concurso, extension, sistema)
    contest.crear_archivos(cantidad, nombres_problemas)
    return True


def procesar_vjudge(contest_id, ruta_concurso, extension, sistema):
    """Procesa un concurso de VJudge"""
    print("\033[93mObteniendo información del concurso...\033[0m")
    nombres_problemas = VJudgeContest.obtener_problemas(contest_id)

    if nombres_problemas is None:
        print("\033[91mNo se pudo obtener la información del concurso.\033[0m")
        return False

    print(f"\033[92mSe encontraron {len(nombres_problemas)} problemas.\033[0m")

    cantidad = input(
        f"\033[93m¿Cuántos problemas resolverás [max: {len(nombres_problemas)}]? ->\033[0m "
    ).strip()

    if not cantidad.isdigit():
        cantidad = len(nombres_problemas)
    else:
        cantidad = min(int(cantidad), len(nombres_problemas))

    contest = VJudgeContest(ruta_concurso, extension, sistema)
    contest.crear_archivos(cantidad, nombres_problemas)
    return True


def procesar_rpc(contest_id, ruta_concurso, extension, sistema):
    """Procesa una ronda de RPC"""
    ruta_descargas = obtener_ruta_descargas(sistema)
    mover_pdf_a_concurso(ruta_concurso, ruta_descargas)

    lista_problemas = (
        input("\033[93m¿Qué problemas resolverás? Ej: A B C ->\033[0m ").upper().split()
    )

    if not lista_problemas:
        print("\033[91mDebes ingresar al menos un problema.\033[0m")
        return False

    contest = RPCContest(ruta_concurso, extension, sistema)
    contest.crear_archivos(lista_problemas, contest_id)
    return True


def procesar_generico(ruta_concurso, extension, sistema):
    """Procesa un concurso genérico"""
    cantidad = input("\033[93m¿Cuántos problemas resolverás? ->\033[0m ").strip()

    if not cantidad.isdigit() or int(cantidad) < 1:
        print("\033[91mDebes ingresar un número válido de problemas.\033[0m")
        return False

    cantidad = int(cantidad)
    contest = GenericContest(ruta_concurso, extension, sistema)
    contest.crear_archivos(cantidad)
    return True


def main():
    """Función principal del CLI"""
    try:
        sistema = detectar_sistema_operativo()
        mostrar_banner(sistema)

        plataforma = seleccionar_plataforma()
        if not plataforma:
            return

        contest_id = input("\033[93mID del concurso ->\033[0m ").strip()

        if not contest_id:
            print("\033[91mDebes ingresar un ID de concurso válido.\033[0m")
            return

        ruta_base = obtener_ruta_base(sistema, plataforma["abrev"])

        if plataforma.get("especial"):
            ruta_concurso = os.path.join(ruta_base, f"Rnd{contest_id}")
        else:
            ruta_concurso = os.path.join(ruta_base, contest_id)

        os.makedirs(ruta_base, exist_ok=True)

        if not crear_directorio_concurso(ruta_concurso):
            return

        extension = seleccionar_lenguaje()

        exito = False
        tipo_plataforma = plataforma.get("tipo", "generic")

        if tipo_plataforma == "codeforces":
            exito = procesar_codeforces(contest_id, ruta_concurso, extension, sistema)
        elif tipo_plataforma == "rpc":
            exito = procesar_rpc(contest_id, ruta_concurso, extension, sistema)
        else:
            exito = procesar_generico(ruta_concurso, extension, sistema)

        if exito:
            abrir_editor(ruta_concurso, sistema)

    except KeyboardInterrupt:
        print("\n\033[91mEjecución cancelada!\033[0m")
    except Exception as e:
        print(f"\n\033[91mError inesperado: {str(e)}\033[0m")


if __name__ == "__main__":
    main()
