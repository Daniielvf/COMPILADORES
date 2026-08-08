from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generar_reporte_1(ruta, estadisticas):

    documento = SimpleDocTemplate(
        ruta,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elementos = []
    estilos = getSampleStyleSheet()

    titulo = estilos["Title"]
    titulo.alignment = TA_CENTER

    elementos.append(
        Paragraph(
            "REPORTE 1 - ESTADÍSTICAS DEL ANÁLISIS LÉXICO",
            titulo
        )
    )

    elementos.append(Spacer(1, 25))

    datos = [
        ["Descripción", "Cantidad"],
        ["Líneas de código", estadisticas["lineas"]],
        ["Caracteres encontrados", estadisticas["caracteres"]],
        ["Números enteros", estadisticas["enteros"]],
        ["Números flotantes", estadisticas["flotantes"]],
        ["Identificadores", estadisticas["identificadores"]],
        ["Valores booleanos", estadisticas["booleanos"]],
        ["Operadores", estadisticas["operadores"]]
    ]

    tabla = Table(
        datos,
        colWidths=[330, 120]
    )

    tabla.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0D6EFD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (1, 1), (1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
        ])
    )

    elementos.append(tabla)
    elementos.append(Spacer(1, 30))

    elementos.append(
        Paragraph(
            "PALABRAS RESERVADAS ENCONTRADAS",
            estilos["Heading2"]
        )
    )

    elementos.append(Spacer(1, 10))

    reservadas = sorted(
        estadisticas["reservadas"].items(),
        key=lambda elemento: elemento[1],
        reverse=True
    )

    datos_reservadas = [
        ["Palabra reservada", "Cantidad"]
    ]

    for palabra, cantidad in reservadas:
        datos_reservadas.append([
            palabra,
            cantidad
        ])

    tabla_reservadas = Table(
        datos_reservadas,
        colWidths=[330, 120]
    )

    tabla_reservadas.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0D6EFD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (1, 1), (1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
        ])
    )

    elementos.append(tabla_reservadas)

    documento.build(elementos)


def generar_reporte_2(ruta, tokens, simbolos):

    documento = SimpleDocTemplate(
        ruta,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=40,
        bottomMargin=40
    )

    elementos = []
    estilos = getSampleStyleSheet()

    titulo = estilos["Title"]
    titulo.alignment = TA_CENTER

    elementos.append(
        Paragraph(
            "REPORTE 2 - TOKENS Y TABLA DE SÍMBOLOS",
            titulo
        )
    )

    elementos.append(Spacer(1, 25))

    # =========================
    # Lexemas encontrados
    # =========================
    elementos.append(
        Paragraph(
            "LEXEMAS ENCONTRADOS",
            estilos["Heading2"]
        )
    )

    elementos.append(Spacer(1, 10))

    datos_tokens = [
        ["No.", "Lexema", "Token", "Línea"]
    ]

    for numero, token in enumerate(tokens, start=1):
        datos_tokens.append([
            numero,
            token["lexema"],
            token["token"],
            token["linea"]
        ])

    tabla_tokens = Table(
        datos_tokens,
        colWidths=[45, 170, 190, 60],
        repeatRows=1
    )

    tabla_tokens.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0D6EFD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (3, 0), (3, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
        ])
    )

    elementos.append(tabla_tokens)
    elementos.append(Spacer(1, 30))

    # =========================
    # Tabla de Simbolos
    # =========================
    elementos.append(
        Paragraph(
            "TABLA DE SÍMBOLOS",
            estilos["Heading2"]
        )
    )

    elementos.append(Spacer(1, 10))

    datos_simbolos = [
        ["No.", "Lexema", "Tipo", "Línea"]
    ]

    for numero, simbolo in enumerate(simbolos, start=1):
        datos_simbolos.append([
            numero,
            simbolo["lexema"],
            simbolo["tipo"],
            simbolo["linea"]
        ])

    tabla_simbolos = Table(
        datos_simbolos,
        colWidths=[45, 190, 170, 60],
        repeatRows=1
    )

    tabla_simbolos.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0D6EFD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (3, 0), (3, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
        ])
    )

    elementos.append(tabla_simbolos)

    documento.build(elementos)
