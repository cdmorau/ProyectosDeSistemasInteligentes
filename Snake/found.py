#app para encontrar la cabeza de la serpiente basada en una imagen

import cv2
import mss
import numpy as np 
import pyautogui
import time


def buscar2():

    with mss.mss() as sct:
        screen_shot = sct.grab(monitor)

    screen_shot = np.array(screen_shot)

    img_rgb = cv2.imread("images/nose.png", cv2.IMREAD_GRAYSCALE)
    # Obtener las dimensiones de la imagen
    height, width = img_rgb.shape
    
    
def find_image_center(image_path):
    # Cargar la imagen
    img_rgb = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Obtener las dimensiones de la imagen
    height, width = img_rgb.shape

    # Capturar una captura de pantalla
    screenshot = pyautogui.screenshot()

    # Convertir la captura de pantalla a una matriz numpy en escala de grises
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

    # Encontrar la ubicación de la imagen en la captura de pantalla
    result = cv2.matchTemplate(screenshot, img_rgb, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Calcular la posición central de la imagen en la pantalla
    center_x = int(max_loc[0] + width / 2)
    center_y = int(max_loc[1] + height / 2)

    # Devolver la posición central de la imagen
    return (center_x, center_y)




inicio=find_image_center("images/snake2.png")
left = inicio[0]-145
top = inicio[1]-301
monitor = {"top": top, "left": left, "width": 680, "height": 600}


def buscar():

    with mss.mss() as sct:
        screen_shot = sct.grab(monitor)

    img = np.array(screen_shot)

        # Cargamos las imágenes
    
    template = cv2.imread("images/nose.png")

    # Convertimos las imágenes a escala de grises
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Creamos un objeto ORB para detectar características clave en ambas imágenes
    orb = cv2.ORB_create()

    # Detectamos los puntos clave y descriptores en ambas imágenes
    kp1, des1 = orb.detectAndCompute(template_gray, None)
    kp2, des2 = orb.detectAndCompute(img_gray, None)

    # Creamos un objeto BFMatcher para emparejar los descriptores
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Encontramos los emparejamientos más cercanos entre los descriptores de las imágenes
    matches = bf.match(des1, des2)

    # Ordenamos los emparejamientos por distancia de menor a mayor
    matches = sorted(matches, key=lambda x:x.distance)

    # Obtenemos la ubicación del objeto de búsqueda (template)
    h, w = template_gray.shape[:2]
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED))
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Dibujamos un rectángulo alrededor del objeto de búsqueda (template)
    cv2.rectangle(img, top_left, bottom_right, (0,0,255), 2)

    # Obtenemos la posición central del objeto de búsqueda (template)
    x_center = int(((top_left[0] + bottom_right[0]) / 2)*4/162)
    y_center = int(((top_left[1] + bottom_right[1]) / 2)*4/162)

    # Dibujamos un círculo en la posición central del objeto de búsqueda
    cv2.circle(img, (x_center, y_center), 5, (0,255,0), -1)

    
    print((x_center, y_center))


while True:
    time.sleep(0.2)
    buscar()
