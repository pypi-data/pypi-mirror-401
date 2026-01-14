import subprocess


def abrir_editor(ruta_concurso, sistema):
    """Abre VSCode en la carpeta del concurso"""
    try:
        if sistema == "Windows":
            subprocess.run(f'code "{ruta_concurso}"', shell=True)
        else:
            subprocess.run(["code", ruta_concurso])

        print(f"\033[94mAbriendo VSCode en {ruta_concurso} 😁\033[0m")

    except FileNotFoundError:
        print(f"\033[93mVSCode no encontrado. Abre manualmente la carpeta:\033[0m")
        print(f"\033[93m{ruta_concurso}\033[0m")
    except Exception as e:
        print(f"\033[91mError al abrir VSCode: {str(e)}\033[0m")
