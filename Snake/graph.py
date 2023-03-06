#Sirve para ver el la posición del mouse en tiempo real

import pyautogui
import time
while True:
    x, y = pyautogui.position()
    color = pyautogui.screenshot().getpixel((x, y))
    print(f"Posición del mouse: ({x}, {y})")
    print(f"Valor RGB en la posición: {color}")
    time.sleep(1)
