from pathlib import Path

from api import suelos
from ui import consola

RUTA_EXCEL = Path(__file__).parent / "data" / "resultado_laboratorio_suelo.xlsx"


def main():
    print("Cargando datos de suelos, un momento...")
    df = suelos.cargar_datos(RUTA_EXCEL)
    while True:
        depto, muni, cultivo, n = consola.pedir_consulta()
        filas, encontrados, usados = suelos.consultar(df, depto, muni, cultivo, n)
        if filas:
            consola.mostrar_resumen(encontrados, usados)
            consola.mostrar_tabla(filas)
        else:
            consola.mostrar_sin_resultados(suelos.listar_opciones(df, depto, muni))
        if not consola.preguntar_otra():
            break


if __name__ == "__main__":
    main()