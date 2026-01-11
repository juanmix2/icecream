import pygame
import random
import os
import time

pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lluvia Espacial Personalizada")

# Cargar recursos
background_img = pygame.image.load("background.jpg")  # assets/background.jpg
player_img = pygame.image.load("nave.png")          # assets/nave.png
meteor_img = pygame.image.load("meteorito.png")     # assets/meteorito.png
image_img = pygame.image.load("image.png").convert_alpha()

# Jugador
player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT-50))
player_speed = 5

# Meteoritos
meteors = []
meteor_rect = meteor_img.get_rect()
spawn_timer = 0

# Puntuación
score = 0
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Sistema de dificultad
base_speed = 3
current_level = 0
#fin running
tiempo=0
running = True
while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += player_speed

    # Generar meteoritos
    spawn_timer += 1
    if spawn_timer >= 30 and len(meteors) < 10:
        meteors.append({
            "rect": meteor_img.get_rect(center=(random.randint(50, WIDTH-50), -50)),
            "speed": base_speed + current_level
        })
        spawn_timer = 0

    # Actualizar dificultad
    current_level = score // 20

    # Dibujado
    screen.blit(background_img, (0, 0))
    screen.blit(player_img, player_rect)
    screen.blit(image_img,(0, 0))
    
    # Actualizar y dibujar meteoritos
    for meteor in meteors[:]:
        meteor["rect"].y += meteor["speed"]
        screen.blit(meteor_img, meteor["rect"])
        
        # Colisiones
        if player_rect.colliderect(meteor["rect"]):
             #sacar esta seccion
             screen.fill((0, 0, 0))
             text = font.render("GAME OVER", True, (25,0,0))
             text_rect = text.get_rect(center=(WIDTH // 18, HEIGHT // 18))
             screen.blit(text, text_rect)
            
             #para punto de restauracion
             running = False
            
            
        # Eliminar meteoritos fuera de pantalla
        if meteor["rect"].top > HEIGHT:
            meteors.remove(meteor)
            score += 1

    # Mostrar UI
    score_text = font.render(f"__Score: {score} | Level: {current_level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()