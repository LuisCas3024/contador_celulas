# -*- coding: utf-8 -*-
"""
Created on Thu May  7 01:28:59 2026


Ejemplo de uso de la la libreria

Elegir entre Celula1, Celula2, Celula3, Celula4

Elegir rango de dist (0.35 - 0.6)

Elegir area minima de eleccion de pixeles
"""

from contador_celulas import contar_celulas, ruta_imagen

resultado = contar_celulas(ruta_imagen("Celula1"), dist_thresh=0.4, area_min=600)