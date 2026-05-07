# -*- coding: utf-8 -*-
"""
contador_celulas
================
Librería de procesamiento de imagen para conteo automático de células
mediante segmentación Watershed con Distance Transform.

Autores
-------
Luis Casillas, Micaela Trujillo, César Girón, Uriel Villalobos
Universidad Autónoma de Aguascalientes — 2026

Uso rápido
----------
>>> from contador_celulas import contar_celulas
>>> resultado = contar_celulas("ruta/a/imagen.jpeg", dist_thresh=0.4, area_min=600)
>>> print(resultado["conteo"])

Funciones disponibles
---------------------
contar_celulas        Pipeline completo: carga → procesamiento → conteo.
rgb_a_gris            Convierte BGR a escala de grises (luminancia ITU-R BT.601).
transformacion_log    Realce logarítmico de zonas oscuras.
ajuste_lineal         Estiramiento lineal del histograma a [0, 255].
filtro_pasa_bajas_fft Filtro pasa bajas circular en dominio FFT.
sobel_propio          Magnitud del gradiente Sobel (implementación propia con scipy).
"""

import os as _os

from contador_celulas.procesamiento import (
    contar_celulas,
    rgb_a_gris,
    transformacion_log,
    ajuste_lineal,
    filtro_pasa_bajas_fft,
    sobel_propio,
)

# ─── Imágenes de ejemplo incluidas en la librería ────────────────────────────

# Catálogo de imágenes disponibles
IMAGENES_DISPONIBLES = {
    "Celula1": "Celula1.jpeg",
    "Celula2": "Celula2.jpeg",
    "Celula3": "Celula3.jpeg",
    "Celula4": "Celula4.jpeg",
}

# Parámetros sugeridos por imagen (basados en las pruebas del equipo)
PARAMETROS_SUGERIDOS = {
    "Celula1": {"dist_thresh": 0.4, "area_min": 800},   # núcleos oscuros ~50px radio
    "Celula2": {"dist_thresh": 0.5, "area_min": 500},   # células grandes separadas
    "Celula3": {"dist_thresh": 0.5, "area_min": 400},   # núcleos medianos
    "Celula4": {"dist_thresh": 0.4, "area_min": 400},   # núcleos pequeños, densos
}

_IMG_DIR = _os.path.join(_os.path.dirname(__file__), "imagenes")


def ruta_imagen(nombre: str) -> str:
    """
    Devuelve la ruta absoluta a una imagen de ejemplo incluida en la librería.

    Parámetros
    ----------
    nombre : str
        Nombre de la imagen sin extensión.
        Opciones: "Celula1", "Celula2", "Celula3", "Celula4".

    Retorna
    -------
    str
        Ruta absoluta al archivo JPEG.

    Lanza
    -----
    ValueError
        Si el nombre no corresponde a ninguna imagen incluida.

    Ejemplo
    -------
    >>> from contador_celulas import ruta_imagen, contar_celulas
    >>> ruta = ruta_imagen("Celula1")
    >>> resultado = contar_celulas(ruta, dist_thresh=0.4, area_min=800)
    """
    if nombre not in IMAGENES_DISPONIBLES:
        disponibles = ", ".join(IMAGENES_DISPONIBLES.keys())
        raise ValueError(
            f"Imagen '{nombre}' no encontrada. "
            f"Imágenes disponibles: {disponibles}"
        )
    return _os.path.join(_IMG_DIR, IMAGENES_DISPONIBLES[nombre])


def listar_imagenes() -> list:
    """
    Retorna la lista de nombres de imágenes de ejemplo disponibles.

    Retorna
    -------
    list of str
        ["Celula1", "Celula2", "Celula3", "Celula4"]
    """
    return list(IMAGENES_DISPONIBLES.keys())


# ─────────────────────────────────────────────────────────────────────────────

__version__  = "0.1.0"
__authors__  = [
    "Luis Casillas",
    "Micaela Trujillo",
    "César Girón",
    "Uriel Villalobos",
]

__all__ = [
    "contar_celulas",
    "rgb_a_gris",
    "transformacion_log",
    "ajuste_lineal",
    "filtro_pasa_bajas_fft",
    "sobel_propio",
    "ruta_imagen",
    "listar_imagenes",
    "IMAGENES_DISPONIBLES",
    "PARAMETROS_SUGERIDOS",
]
