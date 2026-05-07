# contador_celulas 

Librería Python para el **conteo automático de células** en imágenes de microscopía.  

Desarrollada por estudiantes de Ingeniería Biomédica de la  **Universidad Autónoma de Aguascalientes**.

## Autores

| Nombre | 
|--------|
| Luis Casillas |
| Micaela Trujillo |
| César Girón |
| Uriel Villalobos |

## Instalación

```bash
pip install git+https://github.com/LuisCas3024/contador_celulas.git
```

> Requiere Python 3.11 o superior.


## Uso rápido

Elegir entre Celula1, Celula2, Celula3, Celula4

Elegir rango de dist (0.35 - 0.6)

Elegir area minima de eleccion de pixeles
"""

from contador_celulas import contar_celulas, ruta_imagen

resultado = contar_celulas(ruta_imagen("Celula1"), dist_thresh=0.4, area_min=600)

## Funciones disponibles

| Función | Descripción |

| `contar_celulas(ruta, ...)` | Pipeline completo: carga → procesamiento → conteo |
| `rgb_a_gris(img)` | Conversión BGR → grises (luminancia ITU-R BT.601) |
| `transformacion_log(img)` | Realce logarítmico de zonas oscuras |
| `ajuste_lineal(img)` | Estiramiento del histograma a [0, 255] |
| `filtro_pasa_bajas_fft(img, radio)` | Filtro pasa bajas circular en dominio FFT |
| `sobel_propio(img)` | Gradiente Sobel propio (convolución con scipy) |


## Parámetros de contar_celulas

| Parámetro | Tipo | Default | Descripción |

| `ruta_imagen` | str | — | Ruta a la imagen (JPEG, PNG, BMP, TIFF) |
| `dist_thresh` | float | 0.4 | Umbral Distance Transform. Rango: 0.4–0.7 |
| `area_min` | int | 600 | Área mínima en px para contar como célula |
| `radio_fft` | int | 80 | Radio del filtro pasa bajas (px) |
| `kernel_sep` | int | 5 | Tamaño del kernel morfológico |
| `verbose` | bool | True | Imprime el conteo en consola |

### Guía de ajuste rápido

| Situación | Parámetro a ajustar |

| Sobreconteo (divide una célula en dos) | Subir `dist_thresh` → 0.5–0.6 |
| Subconteo (agrupa dos células en una) | Bajar `dist_thresh` → 0.3–0.4 |
| Detecta ruido/fragmentos como células | Subir `area_min` → 800–1000 |
| Pierde células pequeñas | Bajar `area_min` → 300–400 |

---

## Dependencias

```
opencv-python >= 4.8
numpy         >= 1.24
scipy         >= 1.10
matplotlib    >= 3.7
```

---

## Pipeline interno

```
Imagen original
     
RGB → Grises  (luminancia ITU-R)
    
CLAHE  (ecualización adaptativa, clipLimit=2.5)
     
Transformación logarítmica
     
Filtro pasa bajas FFT  (máscara circular)
    
Desenfoque gaussiano  (7×7, σ=1.5)
    
Umbral Otsu inverso
     
Morfología: Cierre → Apertura
          
Distance Transform + Watershed
     
Conteo por área mínima  ──► Resultado
```

---

## Licencia

MIT License — libre para uso académico y personal.
