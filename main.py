#pgzero

# M8.L1 - Actividad #3: "Fin del juego"
# to-do: add reset

import random

WIDTH = 300
HEIGHT = 300

TITLE = "Ejemplo Fin de Juego" # Título de la ventana de juego
FPS = 30 # Fotogramas por segundo

fondo = Actor("bg")
personaje = Actor("spider")
personaje.velocidad = 5
personaje.puntos_salud_max = 100
personaje.puntos_salud_actuales = personaje.puntos_salud_max
personaje.ataque_min = 5
personaje.ataque_max = 7

partida_finalizada = False
resultado_partida = "jugando" # 3 estados: "jugando"/"victoria"/"derrota"

# Generación de enemigos
lista_enemigos = []


def spawnear_enemigo(tipo=""):
    
    if (tipo == ""):
        # Enemigo por defecto
        tipo = "block"
    
    # To-do: add logic to prevent enemies overlap
    # -> Step #1: crear función que devuelva un par random de coordenadas
    # -> Paso #2: Crear función que valide que esas coordenadas están libres
    #             -> tomamos el par de coord, y nos aseguramos que no haya un enemigo en ± width/2, ± height/2
    x = random.randint(20, 280)
    y = random.randint(20, 280)
    nvo_enemigo = Actor(tipo, (x, y))
    nvo_enemigo.puntos_salud_max = random.randint(15, 20)
    nvo_enemigo.puntos_salud_actuales = nvo_enemigo.puntos_salud_max
    # Seteamos la curación random
    
    nvo_enemigo.bonus = random.randint(1, 20)
    if (nvo_enemigo.bonus == 20):
        nvo_enemigo.bonus = 10 # curación crítica (5%)
    elif (nvo_enemigo.bonus <= 6 ):
        nvo_enemigo.bonus = 0 # no hay curación (30 %)
    else:
        nvo_enemigo.bonus = random.randint(3,5) # curación normal (65%)

    # Seteamos puntos ataque
    nvo_enemigo.ataque_min = 3
    nvo_enemigo.ataque_max = 6
    lista_enemigos.append(nvo_enemigo)

def simular_enfrentamiento(jugador, enemigo):

    global partida_finalizada, resultado_partida
    
    combate_finalizado = False #flag que determina si el combate continua
    ganador = ""
    
    # determinar quien ataca primero en combate
    tiene_ventaja = random.randint(0,1)

    if (tiene_ventaja == 0):
        tiene_ventaja = True
        atacante = jugador
        defensor = enemigo
    else:
        tiene_ventaja = False
        atacante = enemigo
        defensor = jugador

    # Simular combate
    # to-do agregar texto flotante
    while (not combate_finalizado):
        # 1er ataque: atacante ataca a defensor
        animate(defensor, tween='bounce_start_end', duration=0.5, x = defensor.x)
        defensor.puntos_salud_actuales -= random.randint(atacante.ataque_min, atacante.ataque_max)
        if (defensor.puntos_salud_actuales <= 0):
            combate_finalizado = True
            ganador = atacante

        # 2do ataque (respuesta): defensor ataca a atacante
        animate(atacante, tween='bounce_start_end', duration=0.5, x = atacante.x)
        atacante.puntos_salud_actuales -= random.randint(defensor.ataque_min, defensor.ataque_max)
        if (atacante.puntos_salud_actuales <= 0):
            combate_finalizado = True
            ganador = defensor

    # Combate finalizado.
    if (ganador == jugador):
        jugador.puntos_salud_actuales += enemigo.bonus
        if (jugador.puntos_salud_actuales > jugador.puntos_salud_max):
            jugador.puntos_salud_actuales = jugador.puntos_salud_max
        lista_enemigos.remove(enemigo)
        
    else:
        partida_finalizada = True
        resultado_partida = "derrota"

def mover_personaje():
    
    # izquierda y derecha
    
    if (personaje.x >= 0) and ((keyboard.left) or (keyboard.a)):
        personaje.x -= personaje.velocidad
    
    if (personaje.x < 0 ) and ((keyboard.left) or (keyboard.a)):
        personaje.x += WIDTH
      
    if (personaje.x <= WIDTH) and (keyboard.right) or (keyboard.d):
        personaje.x += personaje.velocidad
        
    if (personaje.x > WIDTH) and ((keyboard.right) or (keyboard.d)):
        personaje.x -= WIDTH
    
    # abajo y arriba
    
    if (personaje.y <= HEIGHT) and (keyboard.down) or (keyboard.s):
        personaje.y += personaje.velocidad
        
    if (personaje.y > HEIGHT) and ((keyboard.down) or (keyboard.s)):
        personaje.y -= HEIGHT
        
    if (personaje.y >= 0) and ((keyboard.up) or (keyboard.w)):
        personaje.y -= personaje.velocidad
        
    if (personaje.y < 0) and ((keyboard.up) or (keyboard.w)):
        personaje.y += HEIGHT

def draw():
  if not partida_finalizada:
    fondo.draw()
    
    for enemigo in lista_enemigos:
      enemigo.draw()

    personaje.draw()

    screen.draw.text(("Salud: " + str(personaje.puntos_salud_actuales) + "/" + str(personaje.puntos_salud_max) ),
                     midleft= (2, 270), color="black", background = "white", fontsize = 20)
      
  else:
    fondo.draw()

    if (resultado_partida == "victoria"):
        screen.draw.text("¡HAS GANADO!", center = (WIDTH/2, HEIGHT/2), color="white", background="black", fontsize = 32)
    else:
        screen.draw.text("¡HAS PERDIDO!", center = (WIDTH/2, HEIGHT/2), color="white", background="black", fontsize = 32)

for enemigo in range(random.randint(2, 7)): # Creamos enemigos
    spawnear_enemigo()

def update(dt):
    global partida_finalizada, resultado_partida
    mover_personaje()

    colision = personaje.collidelist(lista_enemigos)
  
    if colision != -1:
      # Si hay colisión con un enemigo:
      simular_enfrentamiento(personaje, lista_enemigos[colision])
      
    else:
      #if (len(lista_enemigos) == 0): <-- Otro método
      if lista_enemigos == []:
        partida_finalizada = True
        resultado_partida = "victoria"