import math
import unicodedata
from datetime import datetime

import pandas as pd

COL_DEPTO = "Departamento"
COL_MUNI = "Municipio"
COL_CULTIVO = "Cultivo"
COL_TOPO = "Topografia"
COL_VARIABLES = {
    "pH": "pH agua:suelo 2,5:1,0",
    "P (mg/kg)": "Fósforo (P) Bray II mg/kg",
    "K (cmol/kg)": "Potasio (K) intercambiable cmol(+)/kg",
}
MAXIMO_PLAUSIBLE = {"pH": 14.0, "P (mg/kg)": 1000.0, "K (cmol/kg)": 15.0}
VALOR_TIPICO = {"pH": 5.5, "P (mg/kg)": 20.0, "K (cmol/kg)": 0.4}


def normalizar(texto):
    texto = unicodedata.normalize("NFD", str(texto).strip().lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def _reconstruir_decimal(valor, tipico):
    digitos = str(int(round(valor))).lstrip("0")
    mejor, mejor_dist = None, None
    for k in range(0, 4):
        candidato = int(digitos) / 10 ** (len(digitos) - k)
        if candidato <= 0:
            continue
        dist = abs(math.log10(candidato) - math.log10(tipico))
        if mejor_dist is None or dist < mejor_dist:
            mejor, mejor_dist = candidato, dist
    return mejor


def a_numero(valor, variable):
    if valor is None or (isinstance(valor, float) and math.isnan(valor)):
        return None
    if isinstance(valor, datetime):
        return valor.day + valor.month / 100 if variable == "pH" else None
    if isinstance(valor, str):
        texto = valor.strip().replace(",", ".")
        if not texto or texto.startswith("<") or texto.upper() in ("ND", "NAN"):
            return None
        try:
            valor = float(texto)
        except ValueError:
            return None
    if valor > MAXIMO_PLAUSIBLE[variable]:
        return _reconstruir_decimal(valor, VALOR_TIPICO[variable])
    return float(valor)


def cargar_datos(ruta):
    df = pd.read_excel(ruta)
    for nombre, columna in COL_VARIABLES.items():
        df[nombre] = [a_numero(v, nombre) for v in df[columna]]
    for col in (COL_DEPTO, COL_MUNI, COL_CULTIVO, COL_TOPO):
        df[col] = df[col].astype(str).str.strip()
        df[col + "_norm"] = df[col].map(normalizar)
    return df


def listar_opciones(df, departamento=None, municipio=None):
    if departamento:
        df = df[df[COL_DEPTO + "_norm"] == normalizar(departamento)]
    if municipio:
        df = df[df[COL_MUNI + "_norm"] == normalizar(municipio)]
    return {
        "municipios": sorted(df[COL_MUNI].unique()),
        "cultivos": df[COL_CULTIVO].value_counts().index.tolist(),
    }


def consultar(df, departamento, municipio, cultivo, n_registros):
    filtro = (
        (df[COL_DEPTO + "_norm"] == normalizar(departamento))
        & (df[COL_MUNI + "_norm"] == normalizar(municipio))
        & (df[COL_CULTIVO + "_norm"].str.contains(normalizar(cultivo), regex=False))
    )
    encontrados = df[filtro]
    usados = encontrados.head(n_registros)
    filas = []
    for topo, grupo in usados.groupby(COL_TOPO, sort=True):
        fila = {
            "Departamento": grupo[COL_DEPTO].iloc[0],
            "Municipio": grupo[COL_MUNI].iloc[0],
            "Cultivo": grupo[COL_CULTIVO].iloc[0],
            "Topografía": topo,
            "Registros": len(grupo),
        }
        for nombre in COL_VARIABLES:
            mediana = grupo[nombre].median()
            fila[nombre] = None if pd.isna(mediana) else round(float(mediana), 2)
        filas.append(fila)
    return filas, len(encontrados), len(usados)