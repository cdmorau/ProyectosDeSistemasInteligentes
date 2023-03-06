import sched
import time
import keyboard
import threading

# Definir la lista de movimientos
moves = ["down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right"]
moves3=["down","left","up","right"]
moves4=["down","right","up","right"]
moves5=["right","right","right","right","right","right","right","right","up","right","right","right","right"]
moves4=["right","up","right","up","right","up","right","up"]

# Definir la lista de movimientos
moves2 = ["down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right"]

import sched
import keyboard

# Definir la lista de movimientos
moves2 = ["down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right""down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right","down","left","up","right"]

# Definir el planificador
scheduler = sched.scheduler(time.time, time.sleep)

tiempo=0.135/2
# Definir la función para realizar los movimientos
def make_move(move):
    keyboard.press_and_release(move)

# Definir la función para agendar los movimientos
def schedulemove(move):
    scheduler.enter(tiempo, 1, make_move, argument=(move,))
    scheduler.run()
# Agendador de agendador
def schedule_shedule(move,time):
    scheduler.enter(time, 1, schedulemove, argument=(move,))
    scheduler.run()


def ejecMovs(movimientos):
    
    for i in range(len(movimientos)):
        schedule_shedule(movimientos[i],tiempo)




time.sleep(2)

ejecMovs(moves5)
# Crear un hilo para el agendamiento de movimientos
# moves_thread = threading.Thread(target=schedule_moves, args=(moves2,))
# moves_thread.start()



