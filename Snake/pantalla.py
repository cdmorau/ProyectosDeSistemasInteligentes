import pyautogui
import cv2
import numpy as np
import pyautogui
import time
import mss
import sched
import sched
import keyboard

import heapq
from collections import deque


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

def get_image_pixels():
    global monitor
    global apple
    global cabezaActual
    # Load the image
    with mss.mss() as sct:
        screen_shot = sct.grab(monitor)
    img = np.array(screen_shot)

    if len(img.shape) == 3 and img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
    # Resize the image to 255 x 255 pixels
    img = cv2.resize(img, (255, 255))

    # Define the size of the grid
    rows = 15
    cols = 17

    # Define the size of each cell
    cell_width = img.shape[1] // cols
    cell_height = img.shape[0] // rows

    # Initialize the array to store the pixel values
    pixel_array = np.zeros((rows, cols))

    # Iterate over each cell
    for i in range(rows):
        for j in range(cols):
            # Compute the indices of the central pixel in the cell
            x = j * cell_width + cell_width // 2
            y = i * cell_height + cell_height // 2

            # Get the pixel value at the center of the cell
            pixel_value = img[y, x]
            
            # Store the pixel value in the array
            # Dar manzana a pple
            if pixel_value[0] <90:
                pixel_array[i,j] = 1
            if pixel_value[0]<50:
                apple= (i,j)
                pixel_array[i,j] = 0
            if pixel_value[0] >90:
                pixel_array[i,j] = pixel_value[0]
            

            
            # if pixel_value[0] >200:
            #     pixel_array[i,j] = 999

            if pixel_value[0]>100:
                sum = img[y, x - cell_width//2][0]+img[y, x + cell_width//2][0]+img[y - cell_height//2, x][0]+img[y + cell_height//2, x][0]
                if sum>400 and sum <550:
                    pixel_array[i, j] = 666
                    cabezaActual= (i,j) 
                else:
                    pixel_array[i, j] = pixel_value[0]
                    

    return pixel_array

def head(i,j,vec):
    vector= [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
    
    for pos in vector:
        if vec[i][j]<vec[pos[0]][pos[1]]:
            return pos
        
    pos= [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
    
    def find_second_largest(positions, vector):
        largest = max(vector[i][j] for i, j in positions)
        second_largest = max(vector[i][j] for i, j in positions if vector[i][j] != largest)
        for i, j in positions:
            if vector[i][j] == second_largest:
                return i, j
    
    return find_second_largest(pos, vec)





def encontrarManzana(m):
    global apple

    coordenadas = np.unravel_index(np.argmin(m), np.shape(m))
    apple=coordenadas
    return coordenadas

def encontrarByColor(m):
    global cabezaActual
    global cabezaPasada
    cabezaPasada= cabezaActual
    opciones = [181, 157, 148]
    mascara = np.isin(m, opciones) # Crea una máscara booleana
    if np.any(mascara):             # Si al menos un valor coincide con las opciones
        indices = np.argwhere(mascara)   # Encuentra los índices donde se cumple la condición
        indice = indices[0]          # Tomar el primer índice
        cabezaActual=tuple(indice)
        return tuple(indice)         # Retorna la tupla de las coordenadas
    else:                            # Si no hay valores que coinciden con las opciones
        indice = np.unravel_index(np.argmax(m), np.shape(m))
        cabezaActual=tuple(indice)
        return tuple(indice)  



def direccion():
    global cabezaActual
    global cabezaPasada
    
    if(cabezaPasada[1]<cabezaActual[1]):
        return ("right")
    elif(cabezaPasada[1]>cabezaActual[1]):
        return ("left")
    elif(cabezaPasada[0]<cabezaActual[0]):
        return ("down")
    elif(cabezaPasada[0]>cabezaActual[0]):
        return ("up")



def nochocar():
    global cabezaActual
    global apple
    global ar
    
    dir =direccion()
    if cabezaActual[1]==16 and dir=="right":
        pyautogui.press("down")
    elif cabezaActual[0]==14 and dir=="down":
        pyautogui.press("left")
    elif cabezaActual[1]==0 and dir=="left":
        pyautogui.press("up")
    elif cabezaActual[0]==0 and dir=="up":
        pyautogui.press("right")
    
    # elif (dir=="right" or dir=="left"):
    #     if apple[0]>cabezaActual[0]:
    #         pyautogui.press("down")
    #     elif apple[0]<cabezaActual[0]:
    #         pyautogui.press("up")
    # elif (dir=="up" or dir=="down"):
    #     if apple[1]>cabezaActual[1]:
    #         pyautogui.press("right")
    #     elif apple[1]<cabezaActual[1]:
    #         pyautogui.press("left")
    # if apple==cabezaActual:
    #     encontrarManzana(ar)


def find_shortest_path(maze, start, end):
    maze = maze.tolist()
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = [[start]]
    
    # marcamos el inicio como visitado
    visited[start[0]][start[1]] = True
    
    while queue:
        path = queue.pop(0)
        x, y = path[-1]
        
        # si hemos llegado al final, devolvemos la lista de movimientos
        if (x, y) == end:
            moves = []
            for i in range(1, len(path)):
                x1, y1 = path[i-1]
                x2, y2 = path[i]
                
                if x2 == x1 - 1:
                    moves.append("up")
                elif x2 == x1 + 1:
                    moves.append("down")
                elif y2 == y1 - 1:
                    moves.append("left")
                elif y2 == y1 + 1:
                    moves.append("right")
            return moves
        
        # buscamos los vecinos no visitados y válidos
        for (x2, y2) in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if (0 <= x2 < rows and 0 <= y2 < cols and not visited[x2][y2]
                    and maze[x2][y2] < 100):
                visited[x2][y2] = True
                queue.append(path + [(x2, y2)])
    
    # si no se encontró un camino, devolvemos None
    return nochocar()

def get_valid_neighbors(matrix, row, col, num_rows, num_cols):
    matrix = matrix.tolist()
    neighbors = []
    if row > 0 and matrix[row-1][col] < 100:
        neighbors.append((row-1, col))
    if row < num_rows-1 and matrix[row+1][col] < 100:
        neighbors.append((row+1, col))
    if col > 0 and matrix[row][col-1] < 100:
        neighbors.append((row, col-1))
    if col < num_cols-1 and matrix[row][col+1] < 100:
        neighbors.append((row, col+1))

    return neighbors



# Definir la función para realizar los movimientos
def make_move(move):
    global cabezaActual
    keyboard.press_and_release(move)

    if(move=="right"):
        cabezaActual=(cabezaActual[0],cabezaActual[1]+1)
    if(move=="up"):
        cabezaActual=(cabezaActual[0]-1,cabezaActual[1])
    if(move=="down"):
        cabezaActual=(cabezaActual[0]+1,cabezaActual[0])
    if(move=="left"):
        cabezaActual=(cabezaActual[0],cabezaActual[1]-1)
    print(cabezaActual)
    print(move)


# Definir la función para agendar los movimientos
def schedulemove(move):
    scheduler.enter(tiempo, 1, make_move, argument=(move,))
    scheduler.run()
# Agendador de agendador
def schedule_shedule(move,time):
    scheduler.enter(time, 1, schedulemove, argument=(move,))
    scheduler.run()


def ejecMovs(movimientos):
    global apple
    
    for i in range(len(movimientos)):
        schedule_shedule(movimientos[i],tiempo)

# Definir el planificador
scheduler = sched.scheduler(time.time, time.sleep)


inicio=find_image_center("images/snake2.png")

left = inicio[0]-145
top = inicio[1]-301
monitor = {"top": top, "left": left, "width": 680, "height": 600}
# Definir la lista de movimientos
moves2 = ["down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right""down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right"]

apple=(7,12)
cabezaActual= (7,3)
cabezaPasada= (7,2)
tiempo=0.135/2
ar=get_image_pixels()



time.sleep(2)

while True:
    print(get_image_pixels())
    print(cabezaActual)