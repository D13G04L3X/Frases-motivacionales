# -*- coding: utf-8 -*-
"""
Notificador de mensajes motivacionales - A&CM
Muestra una notificacion (toast) de Windows con una frase al azar
tomada de mensajes.json, evitando repetir la ultima que se mostro.
"""

import json
import random
from pathlib import Path
from datetime import datetime

from windows_toasts import WindowsToaster, Toast

# --- Configuracion ---------------------------------------------------------
# BASE = la carpeta donde vive este archivo. Asi funciona sin importar
# desde donde lo ejecute el Programador de tareas.
BASE = Path(__file__).resolve().parent
ARCHIVO_MENSAJES = BASE / "mensajes.json"
ARCHIVO_ESTADO = BASE / "estado.json"      # se crea solo
ARCHIVO_LOG = BASE / "registro.log"        # se crea solo

APP_NOMBRE = "A&CM"
TITULO = "A&CM \u00b7 Mensaje del d\u00eda"   # "A&CM · Mensaje del día"
# ---------------------------------------------------------------------------


def cargar_mensajes():
    with open(ARCHIVO_MENSAJES, "r", encoding="utf-8") as f:
        datos = json.load(f)
    return datos.get("mensajes", [])


def elegir_mensaje(mensajes):
    """Elige una frase al azar sin repetir la ultima mostrada."""
    ultimo = -1
    if ARCHIVO_ESTADO.exists():
        try:
            with open(ARCHIVO_ESTADO, "r", encoding="utf-8") as f:
                ultimo = json.load(f).get("ultimo_indice", -1)
        except Exception:
            ultimo = -1

    opciones = list(range(len(mensajes)))
    if len(opciones) > 1 and ultimo in opciones:
        opciones.remove(ultimo)

    indice = random.choice(opciones)

    with open(ARCHIVO_ESTADO, "w", encoding="utf-8") as f:
        json.dump({"ultimo_indice": indice}, f, ensure_ascii=False)

    return mensajes[indice]


def registrar(texto):
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write("{:%Y-%m-%d %H:%M:%S}  ->  {}\n".format(datetime.now(), texto))


def mostrar(texto):
    toaster = WindowsToaster(APP_NOMBRE)
    toast = Toast()
    toast.text_fields = [TITULO, texto]   # 1a linea = titulo, 2a = cuerpo
    toaster.show_toast(toast)


def main():
    try:
        mensajes = cargar_mensajes()
        if not mensajes:
            return
        texto = elegir_mensaje(mensajes)
        mostrar(texto)
        registrar(texto)
    except Exception as e:
        try:
            registrar("ERROR: {}".format(e))
        except Exception:
            pass


if __name__ == "__main__":
    main()
