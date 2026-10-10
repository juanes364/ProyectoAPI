def pedir_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  ⚠ Este campo no puede estar vacío.")


def pedir_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor > 0:
                return valor
        except ValueError:
            pass
        print("  ⚠ Ingrese un número entero mayor que 0.")


def pedir_consulta():
    print("\n=== Consulta de propiedades edáficas ===")
    return (
        pedir_texto("Departamento: "),
        pedir_texto("Municipio: "),
        pedir_texto("Cultivo: "),
        pedir_entero("Número de registros a consultar: "),
    )


def mostrar_tabla(filas):
    if not filas:
        return
    columnas = list(filas[0].keys())
    celdas = [[("—" if f[c] is None else str(f[c])) for c in columnas] for f in filas]
    anchos = [max(len(c), *(len(r[i]) for r in celdas)) for i, c in enumerate(columnas)]
    linea = "+-" + "-+-".join("-" * a for a in anchos) + "-+"
    print(linea)
    print("| " + " | ".join(c.ljust(a) for c, a in zip(columnas, anchos)) + " |")
    print(linea)
    for r in celdas:
        print("| " + " | ".join(v.ljust(a) for v, a in zip(r, anchos)) + " |")
    print(linea)


def mostrar_resumen(encontrados, usados):
    print(f"\nRegistros encontrados: {encontrados} | usados en la consulta: {usados}")
    print("Medianas calculadas con los datos disponibles ('—' = sin dato medible).\n")


def mostrar_sin_resultados(opciones):
    print("\nNo se encontraron registros con esos criterios.")
    if opciones["municipios"]:
        print("Municipios disponibles en ese departamento:", ", ".join(opciones["municipios"]))
    if opciones["cultivos"]:
        print("Cultivos más frecuentes:", ", ".join(opciones["cultivos"][:10]))


def preguntar_otra():
    return input("\n¿Hacer otra consulta? (s/n): ").strip().lower() == "s"