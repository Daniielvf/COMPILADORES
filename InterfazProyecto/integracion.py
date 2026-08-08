import re
import subprocess
from collections import Counter


RUTA_ANALIZADOR = (
    "/home/claudiagod/Escritorio/COMPILADORES/Analizador/Analizador"
)


OPERADORES = {
    "+": "TK_SUMA",
    "-": "TK_RESTA",
    "*": "TK_MULTIPLICACION",
    "/": "TK_DIVISION",
    "%": "TK_MODULO",
    "=": "TK_ASIGNACION",
    "==": "TK_IGUALDAD",
    "!=": "TK_DIFERENTE",
    ">": "TK_MAYOR",
    "<": "TK_MENOR",
    ">=": "TK_MAYOR_IGUAL",
    "<=": "TK_MENOR_IGUAL",
    "&&": "TK_AND",
    "||": "TK_OR",
    "!": "TK_NOT"
}


def obtener_token(tipo, lexema):

    if tipo == "Palabra reservada":
        return "TK_" + lexema.upper()

    if tipo == "Identificador":
        return "TK_IDENTIFICADOR"

    if tipo == "Entero":
        return "TK_ENTERO"

    if tipo == "Flotante":
        return "TK_FLOTANTE"

    if tipo == "Booleano":

        if lexema == "true":
            return "TK_TRUE"

        return "TK_FALSE"

    if tipo == "Cadena":
        return "TK_CADENA"

    if tipo == "Operador":
        return OPERADORES.get(
            lexema,
            "TK_OPERADOR"
        )

    return "TK_DESCONOCIDO"


def ejecutar_analizador(ruta_archivo):

    with open(
        ruta_archivo,
        "r",
        encoding="utf-8"
    ) as archivo:

        resultado = subprocess.run(
            [RUTA_ANALIZADOR],
            stdin=archivo,
            capture_output=True,
            text=True
        )

    if resultado.returncode != 0:
        raise Exception(
            resultado.stderr
        )

    return resultado.stdout


def procesar_salida(salida):

    tokens = []

    patron = re.compile(
        r"Linea\s+(\d+):\s+(.+?)\s+->\s+(.*)"
    )

    for linea in salida.splitlines():

        coincidencia = patron.match(
            linea.strip()
        )

        if not coincidencia:
            continue

        numero_linea = int(
            coincidencia.group(1)
        )

        tipo = coincidencia.group(2).strip()

        lexema = coincidencia.group(3).strip()

        token = obtener_token(
            tipo,
            lexema
        )

        tokens.append({
            "token": token,
            "lexema": lexema,
            "tipo": tipo,
            "linea": numero_linea
        })

    return tokens


def generar_estadisticas(ruta_archivo, tokens):

    with open(
        ruta_archivo,
        "r",
        encoding="utf-8"
    ) as archivo:

        contenido = archivo.read()

    reservadas = []

    for token in tokens:

        if token["tipo"] == "Palabra reservada":
            reservadas.append(
                token["lexema"]
            )

    conteo_reservadas = Counter(
        reservadas
    )

    return {
        "lineas": len(contenido.splitlines()),
        "caracteres": len(contenido),

        "enteros": sum(
            1
            for token in tokens
            if token["tipo"] == "Entero"
        ),

        "flotantes": sum(
            1
            for token in tokens
            if token["tipo"] == "Flotante"
        ),

        "identificadores": sum(
            1
            for token in tokens
            if token["tipo"] == "Identificador"
        ),

        "booleanos": sum(
            1
            for token in tokens
            if token["tipo"] == "Booleano"
        ),

        "cadenas": sum(
            1
            for token in tokens
            if token["tipo"] == "Cadena"
        ),

        "operadores": sum(
            1
            for token in tokens
            if token["tipo"] == "Operador"
        ),

        "reservadas": dict(
            conteo_reservadas
        )
    }


def generar_tabla_simbolos(tokens):

    simbolos = []

    for token in tokens:

        if token["tipo"] == "Identificador":

            simbolos.append({
                "lexema": token["lexema"],
                "token": token["token"],
                "tipo": token["tipo"],
                "linea": token["linea"]
            })

    return simbolos


def analizar_archivo(ruta_archivo):

    salida = ejecutar_analizador(
        ruta_archivo
    )

    tokens = procesar_salida(
        salida
    )

    estadisticas = generar_estadisticas(
        ruta_archivo,
        tokens
    )

    simbolos = generar_tabla_simbolos(
        tokens
    )

    return {
        "tokens": tokens,
        "estadisticas": estadisticas,
        "simbolos": simbolos
    }