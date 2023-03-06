import pyautogui
import mss
import numpy as np
import cv2

boardimage = pyautogui.locateOnScreen('images/board.png', confidence=0.9)
monitor = {"top": boardimage.top, "left": boardimage.left, "width": int(boardimage.height+boardimage.height*2/15), "height": boardimage.height}


def getScreen():
    global boardimage
    print(boardimage)

    # Inicializar mss
    with mss.mss() as sct:
        # Especificar la región de la pantalla a capturar

        # Tomar el screenshot
        screenshot = np.array(sct.grab(monitor))

    return screenshot

def getCabeza():
    img = getScreen()
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Cargar la imagen que se desea buscar
    template = cv2.imread('images/shape2.0.png', 0)
    
    # Crear una máscara para ignorar los pixeles blancos
    mask = cv2.inRange(img, np.array([255, 255, 255]), np.array([255, 255, 255]))
    mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    # Convertir la imagen con máscara a escala de grises
    gray_img = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
    
    
    # Buscar la imagen en la captura de pantalla
    res = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    # Obtener la posición de la imagen encontrada
    threshold = 0.8 # Se puede ajustar el umbral de detección
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        print("La imagen se encuentra en la posición:", pt)
    
    




getCabeza()
