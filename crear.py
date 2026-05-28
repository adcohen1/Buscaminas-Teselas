import math

def obtener_mejor_par(n):
	for i in range(int(math.sqrt(n)), 0, -1):
		if n % i == 0:
			j = n // i
            
			if j <= 1.7 * i and i <= 15 and j / i > 1:
				return [j, i]
                
		return None
	return None

num = 500
resultados = {}

# Un solo ciclo para procesar y filtrar
for i in range(16, num + 1):
    par = obtener_mejor_par(i)
    if par:
        resultados[i] = (par[0], par[1])

# Escritura eficiente
with open('list2.txt', 'w') as a:
    a.write('{\n')
    for n, par in resultados.items():
        a.write(f'\t\t\t\t{n}: {par},\n')
    a.write('}')

print('Escritura exitosa')

print(5 >= 0)

#conf = 'color_bg'
#valor = (60, 120, 180)

#with open('conf.txt', 'r') as a:
#	cont = a.read().split('\n')
#	new_cont = ''
#	for linea in cont:
#		if linea.split('=')[0] == conf:
#			new_cont += f'{conf}={valor}\n'
#			continue
#		new_cont += linea + '\n'

#print(new_cont)

#from adminConf import obtenerConf


#print(obtenerConf('dist'))
#admin = adminConf()
#admin.establecerConf('color_bg', (0, 0, 0))

#with open('conf.txt', 'r') as a:
#	print(a.read())
#			()
'''
import pygame
import random

# Inicialización básica
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

# 1. Definir la clase del objeto
class Particula(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Creamos una superficie pequeña
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))
        
        # OPTIMIZACIÓN CRUCIAL: Convertir el formato de píxeles
        self.image = self.image.convert()
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO)
        self.rect.y = random.randrange(ALTO)
        self.velocidad_y = random.randint(1, 5)

    def update(self):
        # Lógica de movimiento
        self.rect.y += self.velocidad_y
        if self.rect.y > ALTO:
            self.rect.y = -10
            self.rect.x = random.randrange(ANCHO)

# 2. Crear el GRUPO y llenarlo
grupo_particulas = pygame.sprite.Group()

for i in range(1000):
    nueva_particula = Particula()
    grupo_particulas.add(nueva_particula)

# Bucle principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # 3. Lógica y Dibujo eficiente
    grupo_particulas.update() # Actualiza todos los elementos
    
    pantalla.fill((30, 30, 30))
    
    # Dibuja todos los elementos del grupo en un solo paso
    grupo_particulas.draw(pantalla) 
    
    pygame.display.flip()
    reloj.tick(60) # Mantiene 60 FPS estables

pygame.quit()
'''
