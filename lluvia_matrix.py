import pygame as pg
import random

# Inicializar Pygame
pg.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Matrix - Densidad Incremental")
pg.display.set_caption("Matrix - Regla de Simultaneidad y Mutación")

# --- COLORES ---
WHITE = (255, 255, 255)
@@ -19,81 +19,93 @@
font = pg.font.SysFont("ms gothic", FONT_SIZE, bold=True)
chars = [chr(int('0x30a0', 16) + i) for i in range(96)] + [str(x) for x in range(10)]

# --- LÓGICA DE DENSIDAD DINÁMICA ---
# --- LÓGICA DE DENSIDAD ---
MAX_COLUMNS = WIDTH // FONT_SIZE
# Lista de todas las columnas posibles desordenadas
all_slots = list(range(MAX_COLUMNS))
random.shuffle(all_slots)

active_columns = [] 
drops = {}          
history = {}        

# Variables de progresión
current_limit = 1.0  # Empezamos con capacidad para 1 gota
growth_speed = 0.1   # Qué tan rápido aumenta la densidad (más alto = más rápido)
current_limit = 1.0  
growth_speed = 0.1   

clock = pg.time.Clock()

def draw_aligned_char(char, col_idx, row_idx, color, clear_first=False):
    x_pos, y_pos = col_idx * FONT_SIZE, row_idx * FONT_SIZE
    if clear_first:
        pg.draw.rect(screen, BLACK, (x_pos, y_pos, FONT_SIZE, FONT_SIZE))
    char_surf = font.render(char, True, color)
    char_rect = char_surf.get_rect(center=(x_pos + FONT_SIZE // 2, y_pos + FONT_SIZE // 2))
    screen.blit(char_surf, char_rect)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False

    # Overlay (Rastro largo)
    # Fondo/Rastro
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(15) 
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # --- INCREMENTO DE DENSIDAD ---
    # El límite de gotas permitidas sube poco a poco en cada frame
    if current_limit < MAX_COLUMNS:
        current_limit += growth_speed

    # Si hay espacio bajo el nuevo límite y quedan columnas libres, activamos una
    if len(active_columns) < int(current_limit) and all_slots:
        new_col = all_slots.pop()
    # --- REGLA DE SIMULTANEIDAD ---
    just_started_now = set()

    # Activar nuevas gotas
    while len(active_columns) < int(current_limit) and all_slots:
        candidates = [s for s in all_slots if (s-1 not in just_started_now) and (s+1 not in just_started_now)]
        if not candidates: break
            
        new_col = random.choice(candidates)
        all_slots.remove(new_col)
        active_columns.append(new_col)
        drops[new_col] = 0 
        history[new_col] = [random.choice(chars) for _ in range(3)]
        just_started_now.add(new_col)

    # Procesar solo las gotas activas
    # --- PROCESAR GOTAS ---
    for i in active_columns:
        def draw_aligned_char(char, col_idx, row_idx, color, clear_first=False):
            x_pos, y_pos = col_idx * FONT_SIZE, row_idx * FONT_SIZE
            if clear_first:
                pg.draw.rect(screen, BLACK, (x_pos, y_pos, FONT_SIZE, FONT_SIZE))
            char_surf = font.render(char, True, color)
            char_rect = char_surf.get_rect(center=(x_pos + FONT_SIZE // 2, y_pos + FONT_SIZE // 2))
            screen.blit(char_surf, char_rect)

        # Mutación
        # 1. MUTACIÓN (Restaurada)
        if random.random() > 0.2:
            mut_offset = random.randint(4, 30)
            target_x, target_y = i * FONT_SIZE + FONT_SIZE // 2, (drops[i] - mut_offset) * FONT_SIZE + FONT_SIZE // 2
            target_y_idx = drops[i] - mut_offset
            target_x = i * FONT_SIZE + FONT_SIZE // 2
            target_y = target_y_idx * FONT_SIZE + FONT_SIZE // 2
            
            if 0 <= target_y < HEIGHT:
                curr_color = screen.get_at((int(target_x), int(target_y)))
                if curr_color != BLACK:
                    draw_aligned_char(random.choice(chars), i, drops[i] - mut_offset, curr_color, clear_first=True)
                # Si el color no es negro (hay un rastro ahí), mutamos el carácter
                if curr_color != (0, 0, 0, 255): 
                    draw_aligned_char(random.choice(chars), i, target_y_idx, curr_color, clear_first=True)

        # Dibujo (3 Blancos)
        draw_aligned_char(history[i][0], i, drops[i] - 3, GREEN)
        draw_aligned_char(history[i][1], i, drops[i] - 2, WHITE)
        draw_aligned_char(history[i][2], i, drops[i] - 1, WHITE)
        # 2. DIBUJO DE LA CABEZA (Efecto Matrix)
        if drops[i] >= 3: draw_aligned_char(history[i][0], i, drops[i] - 3, GREEN)
        if drops[i] >= 2: draw_aligned_char(history[i][1], i, drops[i] - 2, WHITE)
        if drops[i] >= 1: draw_aligned_char(history[i][2], i, drops[i] - 1, WHITE)

        new_char = random.choice(chars)
        history[i].pop(0)
        history[i].append(new_char)
        draw_aligned_char(new_char, i, drops[i], WHITE)

        # Movimiento
        # 3. MOVIMIENTO Y REINICIO
        drops[i] += 1
        if drops[i] * FONT_SIZE > HEIGHT:
            if random.random() > 0.95: 
                drops[i] = 0
                # Reinicio con chequeo de vecinos para no salir al mismo tiempo que otro
                if (i-1 not in just_started_now) and (i+1 not in just_started_now):
                    drops[i] = 0
                    just_started_now.add(i)

    pg.display.flip()
    clock.tick(10)
    clock.tick(15)

pg.quit()