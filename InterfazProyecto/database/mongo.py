import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError


# =========================
# Ruta del archivo .env
# =========================
RUTA_ENV = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(
    dotenv_path=RUTA_ENV
)


MONGO_URI = os.getenv("MONGO_URI")

BASE_DATOS = "AnalizadorRuby"
COLECCION = "tabla_simbolos"


def guardar_tabla_simbolos(simbolos):

    if not MONGO_URI:
        raise Exception(
            "No se encontró MONGO_URI en el archivo .env"
        )

    cliente = None

    try:

        # =========================
        # Conectar con MongoDB Atlas
        # =========================
        cliente = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

        # =========================
        # Verificar conexion
        # =========================
        cliente.admin.command("ping")

        base_datos = cliente[
            BASE_DATOS
        ]

        coleccion = base_datos[
            COLECCION
        ]

        # =========================
        # Validar tabla de simbolos
        # =========================
        if not simbolos:
            return 0

        # =========================
        # Guardar tabla de simbolos
        # =========================
        resultado = coleccion.insert_many(
            simbolos
        )

        return len(
            resultado.inserted_ids
        )

    except PyMongoError as error:

        raise Exception(
            f"Error al conectar con MongoDB: {error}"
        )

    finally:

        if cliente is not None:
            cliente.close()