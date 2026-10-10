# ProyectoAPI - Propiedades edáficas (Risaralda)

Aplicación de consola en Python que consulta las medianas de pH, Fósforo (P)
y Potasio (K) de análisis de suelos por departamento, municipio y cultivo.

## Estructura
- `main.py`: punto de entrada, coordina UI y API
- `api/suelos.py`: carga del Excel, limpieza y cálculo de medianas
- `ui/consola.py`: entrada de datos y tabla por consola
- `data/`: archivo Excel con los análisis de laboratorio

## Ejecución
pip install pandas openpyxl
python main.py

## Nota
En el Excel entregado varias celdas de P y K perdieron el punto decimal;
el módulo API las reconstruye con una heurística (ver `_reconstruir_decimal`).