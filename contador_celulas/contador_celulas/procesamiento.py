# -*- coding: utf-8 -*-
"""
Created on Tue May  3 23:58:49 2026

@author: casil
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


# %% FUNCIONES

def rgb_a_gris(img):

    B = img[:, :, 0].astype(np.float32)
    G = img[:, :, 1].astype(np.float32)
    R = img[:, :, 2].astype(np.float32)

    gray = 0.299 * R + 0.587 * G + 0.114 * B
    return np.clip(gray, 0, 255).astype(np.uint8)


def transformacion_log(img):

    img_norm = img.astype(np.float32) / 255.0
    log_img  = np.log(1 + img_norm)
    resultado = (log_img / log_img.max()) * 255
    return np.round(resultado).astype(np.uint8)


def ajuste_lineal(img):

    a, b = img.min(), img.max()
    if b == a:
        return img.copy()
    resultado = ((255) / (b - a)) * (img.astype(np.float32) - a)
    return np.round(resultado).astype(np.uint8)


def filtro_pasa_bajas_fft(img, radio):

    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2

    mask = np.zeros((rows, cols))
    mask = cv2.circle(mask, (ccol, crow), radio, 1, -1)

    fft      = np.fft.fft2(img)
    fftsh    = np.fft.fftshift(fft)
    fft_filt = fftsh * mask

    reg      = np.fft.ifftshift(fft_filt)
    reg      = np.fft.ifft2(reg)
    img_filt = np.abs(reg)

    img_filt = cv2.normalize(img_filt, None, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(img_filt)


def sobel_propio(img):

    kernel_sx = np.array([[-1, 0, 1],
                           [-2, 0, 2],
                           [-1, 0, 1]], dtype=np.float32)

    kernel_sy = np.array([[ 1,  2,  1],
                           [ 0,  0,  0],
                           [-1, -2, -1]], dtype=np.float32)

    img_f    = img.astype(np.float32)
    edges_sx = signal.convolve2d(img_f, kernel_sx, mode='same')
    edges_sy = signal.convolve2d(img_f, kernel_sy, mode='same')
    magnitud = np.sqrt(edges_sx**2 + edges_sy**2)
    return magnitud


def contar_celulas(ruta_imagen, dist_thresh=0.4, area_min=600,
                   radio_fft=80, kernel_sep=5, verbose=True):

    # 1. Carga
    img = cv2.imread(ruta_imagen)
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: '{ruta_imagen}'")
    img_original = img.copy()

    # 2. Preprocesamiento
    gray       = rgb_a_gris(img)
    clahe      = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    gray_clahe = clahe.apply(gray)
    gray_log   = transformacion_log(gray_clahe)
    gray_fft   = filtro_pasa_bajas_fft(gray_log, radio=radio_fft)
    blur       = cv2.GaussianBlur(gray_fft, (7, 7), 1.5)

    plt.figure(1, figsize=(14, 4))
    plt.suptitle('Preprocesamiento', fontsize=13)
    plt.subplot(1, 4, 1), plt.imshow(gray,       cmap='gray'), plt.title('1. Grises')
    plt.subplot(1, 4, 2), plt.imshow(gray_clahe, cmap='gray'), plt.title('2. CLAHE')
    plt.subplot(1, 4, 3), plt.imshow(gray_log,   cmap='gray'), plt.title('3. Log')
    plt.subplot(1, 4, 4), plt.imshow(gray_fft,   cmap='gray'), plt.title('4. FFT + blur')
    plt.tight_layout()

    # 3. Bordes Sobel
    bordes_sobel = sobel_propio(blur)

    plt.figure(2)
    plt.subplot(1, 2, 1), plt.imshow(blur,         cmap='gray'), plt.title('Preprocesada')
    plt.subplot(1, 2, 2), plt.imshow(bordes_sobel, cmap='gray'), plt.title('Bordes Sobel (propio)')

    # 4. Umbralización
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    plt.figure(3)
    plt.subplot(1, 2, 1), plt.imshow(blur, cmap='gray'), plt.title('Antes de umbral')
    plt.subplot(1, 2, 2), plt.imshow(th,   cmap='gray'), plt.title('Umbral Otsu')

    # 5. Morfología
    kernel_close = np.ones((kernel_sep, kernel_sep), np.uint8)
    kernel_open  = np.ones((3, 3), np.uint8)
    closed  = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel_close, iterations=2)
    opening = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel_open, iterations=2)

    plt.figure(4)
    plt.subplot(1, 3, 1), plt.imshow(th,      cmap='gray'), plt.title('Umbral')
    plt.subplot(1, 3, 2), plt.imshow(closed,  cmap='gray'), plt.title('Cerrado')
    plt.subplot(1, 3, 3), plt.imshow(opening, cmap='gray'), plt.title('Limpio')

    # 6. Watershed
    sure_bg = cv2.dilate(opening, kernel_close, iterations=3)
    dist    = cv2.distanceTransform(opening, cv2.DIST_L2, 5)

    _, sure_fg = cv2.threshold(dist, dist_thresh * dist.max(), 255, 0)
    sure_fg    = np.uint8(sure_fg)
    unknown    = cv2.subtract(sure_bg, sure_fg)

    num_labels, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    img_ws  = img_original.copy()
    markers = cv2.watershed(img_ws, markers)

    plt.figure(5, figsize=(12, 4))
    plt.suptitle('Watershed', fontsize=13)
    plt.subplot(1, 3, 1), plt.imshow(dist,    cmap='jet'),           plt.title('Distance Transform'), plt.colorbar()
    plt.subplot(1, 3, 2), plt.imshow(sure_fg, cmap='gray'),          plt.title(f'Centros (thresh={dist_thresh})')
    plt.subplot(1, 3, 3), plt.imshow(markers, cmap='nipy_spectral'), plt.title('Marcadores watershed')

    # 7. Conteo
    img_resultado = img_original.copy()
    cell_count    = 0

    for label in np.unique(markers):
        if label <= 1:
            continue
        mask = np.uint8(markers == label)
        area = cv2.countNonZero(mask)

        if area > area_min:
            cell_count += 1
            M = cv2.moments(mask)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(img_resultado, (cx, cy), 4, (0, 255, 0), -1)

    img_resultado[markers == -1] = [0, 0, 255]

    if verbose:
        print(f"Células detectadas : {cell_count}")
        print(f"  dist_thresh      : {dist_thresh}")
        print(f"  area_min         : {area_min}")

    plt.figure(6, figsize=(14, 5))
    plt.suptitle(f'Resultado final — {cell_count} células detectadas', fontsize=14)
    plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(img_original,  cv2.COLOR_BGR2RGB)), plt.title('Original'),     plt.axis('off')
    plt.subplot(1, 3, 2), plt.imshow(opening, cmap='gray'),                           plt.title('Segmentada'),   plt.axis('off')
    plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(img_resultado, cv2.COLOR_BGR2RGB)), plt.title('Conteo final'), plt.axis('off')
    plt.tight_layout()
    plt.show()

    return {
        "conteo":        cell_count,
        "markers":       markers,
        "img_resultado": img_resultado,
        "img_original":  img_original,
        "segmentada":    opening,
        "parametros": {
            "dist_thresh": dist_thresh,
            "area_min":    area_min,
            "radio_fft":   radio_fft,
            "kernel_sep":  kernel_sep,
        }
    }
