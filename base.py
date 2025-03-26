import pygame
import random
import os
import sys
from pygame.locals import *

pygame.init()
pygame.font.init()



'''
VARIABLES
'''

# DISPLAY
FPS = 60
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(">> CAT YOUR PAYCHECK <<")

# COLORS
YELLOW = (254, 236, 55)
PURPLE = (183,104,162)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 51, 153)
GRAY = (100, 100, 100)
DARK_GREEN = (26, 26, 25)

# CHARACTER
CHARACTER_COLOR = CYAN
CHARACTER_SIZE = 100
PLAYER_SPEED = 12
PLAYER_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
HP = 5
POINTS = 0
hp = pygame.image.load("textures/hp.png")
hp = pygame.transform.scale(hp, (32, 32))
nohp = pygame.image.load("textures/nohp.png")
nohp = pygame.transform.scale(nohp, (32, 32))
RESTRICTED_AREA = pygame.Rect(105, 0, 420, 70)
RESTRICTED_AREA_2 = pygame.Rect(322, 547, 5, 5)
RESTRICTED_AREA_3 = pygame.Rect(762, 0, 120, 80)
RESTRICTED_AREA_4 = pygame.Rect(510, 559, 420, 200)
RESTRICTED_AREA_5 = pygame.Rect(1052, 0, 250, 170)

# COLLECTIBLES
COIN_COLOR = YELLOW
COIN_SIZE = 40
CASH_COLOR = DARK_GREEN

# MENU
THEMES = [
    {"bg": (162, 178, 159), "text": (248, 237, 227), "button": (121, 135, 119)},  # SVETLO ZELENA
    {"bg": (96, 153, 102), "text": (237, 241, 214), "button": (64, 81, 59)},  # TMAVO ZELENA
    {"bg": (232, 184, 109), "text": (245, 247, 248), "button": (250, 188, 63)},  # SVETLO ZLTA
    {"bg": (96, 139, 193), "text": (243, 243, 224), "button": (19, 62, 135)},  # TMAVO MODRA
    {"bg": (255, 180, 194), "text": (253, 255, 210), "button": (102, 123, 198)} # SVETLO RUZOVA
    ]
theme_index = 0
current_theme = THEMES[theme_index]
icon = pygame.image.load("textures/icon1.png")
pygame.display.set_icon(icon)
rip_image = pygame.image.load("textures/player_rip.png")  
rip_image = pygame.transform.scale(rip_image, (50, 50))  
falling_rip = []
money_image = pygame.image.load("textures/cash.png")
money_image = pygame.transform.scale(money_image, (50, 50))
falling_money = []

font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 40)

cat_image = pygame.image.load("textures/player_d1.png") 
cat_image = pygame.transform.scale(cat_image, (125, 145))
corner_x = SCREEN_WIDTH - cat_image.get_width() - 30
corner_y = SCREEN_HEIGHT - cat_image.get_height() - 10

# HUDBA V MENU 
pygame.mixer.music.load("sounds/Meow.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)
volume_level = 50 
sound_on = True

# MINIGAME 1
result = None
TILE_SIZE = 200
BLANK = None
Last_click = False
PRINCESS_PINK = (255, 177, 207)
TILE_COLOR = PRINCESS_PINK
TEXT_COLOR = WHITE
BASIC_FONT_SIZE = 20
MESSAGE_COLOR = WHITE
cash_img = pygame.image.load("textures/cash.png")
FONT = pygame.font.Font(None, 55)

# MINIGAME 2
LINE_WIDTH = 10
CIRCLE_RADIUS = 60
CROSS_WIDTH = 15
font2 = pygame.font.Font(None, 74)
message_font2 = pygame.font.Font(None, 54)
board = [[None] * 3 for _ in range(3)]
current_player = "player"



'''
CLASSES
'''

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.left_sprites = [
            pygame.image.load("textures/player_still_l.png").convert_alpha(),
            pygame.image.load("textures/player_l1.png").convert_alpha(),
            pygame.image.load("textures/player_l2.png").convert_alpha(),
            pygame.image.load("textures/player_l3.png").convert_alpha()]
        self.right_sprites = [
            pygame.image.load("textures/player_still_r.png").convert_alpha(),
            pygame.image.load("textures/player_r1.png").convert_alpha(),
            pygame.image.load("textures/player_r2.png").convert_alpha(),
            pygame.image.load("textures/player_r3.png").convert_alpha()]
        self.left_sprites = [pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE)) for img in self.left_sprites]
        self.right_sprites = [pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE)) for img in self.right_sprites]
        self.up_sprites = [
            pygame.image.load("textures/player_u1.png").convert_alpha(),
            pygame.image.load("textures/player_u2.png").convert_alpha(),
            pygame.image.load("textures/player_u1.png").convert_alpha(),
            pygame.image.load("textures/player_u3.png").convert_alpha()]
        self.down_sprites = [
            pygame.image.load("textures/player_d1.png").convert_alpha(),
            pygame.image.load("textures/player_d2.png").convert_alpha(),
            pygame.image.load("textures/player_d1.png").convert_alpha(),
            pygame.image.load("textures/player_d3.png").convert_alpha()]
        self.up_sprites = [pygame.transform.scale(img, (CHARACTER_SIZE-(CHARACTER_SIZE//4), CHARACTER_SIZE)) for img in self.up_sprites]
        self.down_sprites = [pygame.transform.scale(img, (CHARACTER_SIZE-(CHARACTER_SIZE//4), CHARACTER_SIZE)) for img in self.down_sprites]

        self.image = self.right_sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 60
        self.direction = "right"

    def move(self, keys, screen_rect):
        old_rect = self.rect.copy()
        moved = False

        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= PLAYER_SPEED
            self.direction = "left"
            moved = True
        elif keys[K_RIGHT] or keys[K_d]:
            self.rect.x += PLAYER_SPEED
            self.direction = "right"
            moved = True
        elif keys[K_UP] or keys[K_w]:
            self.rect.y -= PLAYER_SPEED
            self.direction = "up"
            moved = True
        elif keys[K_DOWN] or keys[K_s]:
            self.rect.y += PLAYER_SPEED
            self.direction = "down"
            moved = True

        self.rect.clamp_ip(screen_rect)
        if self.rect.colliderect(RESTRICTED_AREA) or self.rect.colliderect(RESTRICTED_AREA_2) or self.rect.colliderect(RESTRICTED_AREA_3) or self.rect.colliderect(RESTRICTED_AREA_4) or self.rect.colliderect(RESTRICTED_AREA_5):
            self.rect = old_rect
        if moved:
            self.update_animation()

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.animation_timer > self.animation_speed:
            self.animation_timer = now
            self.frame_index = (self.frame_index + 1) % 4

            if self.direction == "left":
                self.image = self.left_sprites[self.frame_index]
            elif self.direction == "right":
                self.image = self.right_sprites[self.frame_index]
            if self.direction == "up":
                self.image = self.up_sprites[self.frame_index]
            elif self.direction == "down":
                self.image = self.down_sprites[self.frame_index]

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("textures/coin.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, ((COIN_SIZE*(2/3)), (COIN_SIZE*(2/3))))
        except pygame.error:
            self.image = pygame.Surface(((COIN_SIZE*(2/3)), (COIN_SIZE*(2/3))))
            self.image.fill(COIN_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.special = False

    def toggle_special(self):
        self.special = random.choice([True, False, False])
        if self.special == True:
            try:
                self.image = pygame.image.load("textures/cash.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (COIN_SIZE+((COIN_SIZE//2)-(COIN_SIZE//8)), COIN_SIZE))
            except pygame.error:
                self.image = pygame.Surface(COIN_SIZE+((COIN_SIZE//2)-(COIN_SIZE//8)), COIN_SIZE)
                self.image.fill(COIN_COLOR)
        else:
            try:
                self.image = pygame.image.load("textures/coin.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, ((COIN_SIZE*(2/3)), (COIN_SIZE*(2/3))))
            except pygame.error:
                self.image = pygame.Surface(((COIN_SIZE*(2/3)), (COIN_SIZE*(2/3))))
                self.image.fill(COIN_COLOR)


    def update_image(self):
        if self.special:
            self.image.fill(CASH_COLOR)
        else:
            self.image.fill(COIN_COLOR)



'''
MENU & SETTINGS
'''

def draw_text_menu(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def spawn_money():
    x_pos = random.randint(0, SCREEN_WIDTH - 50)
    y_pos = -50
    speed = random.uniform(0.5, 0.8)
    falling_money.append({"x": x_pos, "y": y_pos, "speed": speed})
def update_money():
    for money in falling_money:
        money["y"] += money["speed"]
    falling_money[:] = [m for m in falling_money if m["y"] < SCREEN_HEIGHT]

def spawn_rip():
    x_pos = random.randint(0, SCREEN_WIDTH - 50)
    y_pos = -50
    speed = random.uniform(0.5, 0.8)
    falling_rip.append({"x": x_pos, "y": y_pos, "speed": speed})
def update_rip():
    for rip in falling_rip:
        rip["y"] += rip["speed"]
    falling_rip[:] = [m for m in falling_rip if m["y"] < SCREEN_HEIGHT]

def main_menu():
    while True:
        global SCREEN
        # FARBA POZADIA
        SCREEN.fill(current_theme["bg"])

        draw_text_menu(">> CAT YOUR PAYCHECK <<", font, YELLOW, SCREEN, SCREEN_WIDTH // 2, 195)

        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
        settings_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 50)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 550, 200, 50)

        pygame.draw.rect(SCREEN, DARK_GREEN, start_button)
        pygame.draw.rect(SCREEN, DARK_GREEN, settings_button)
        pygame.draw.rect(SCREEN, DARK_GREEN, exit_button)

        draw_text_menu("Start", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 375)
        draw_text_menu("Settings", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 475)
        draw_text_menu("Exit", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 575)

        SCREEN.blit(cat_image, (corner_x, corner_y))

        if pygame.time.get_ticks() % 100 == 0:
            spawn_money()

        update_money()
        for money in falling_money:
            SCREEN.blit(money_image, (money["x"], money["y"]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    main()
                if settings_button.collidepoint(event.pos):
                    settings_menu()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()  
                    sys.exit()  

        pygame.display.flip()

def start_open():
    os.execlp("python", "python", "game.py")

def settings_menu():
    global theme_index, current_theme, sound_on, volume_level, SCREEN
    volume_slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 440, 200, 20)
    volume_slider = pygame.Rect(SCREEN_WIDTH // 2 - 100 + (volume_level * 2), 440, 10, 20)
    
    while True:
        SCREEN.fill(current_theme["bg"])

        draw_text_menu("SETTINGS", font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 150)

        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 50)
        theme_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 50)
        sound_toggle_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)

        pygame.draw.rect(SCREEN, current_theme["button"], back_button)
        pygame.draw.rect(SCREEN, current_theme["button"], theme_button)
        pygame.draw.rect(SCREEN, current_theme["button"], sound_toggle_button)
        pygame.draw.rect(SCREEN, YELLOW, volume_slider_rect)

        draw_text_menu("Back", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 525)
        draw_text_menu("Theme", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 275)
        draw_text_menu("Sound: ON" if sound_on else "Sound: OFF", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 375)
        draw_text_menu(f"Volume: {volume_level}%", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 475)

        pygame.draw.rect(SCREEN, WHITE, volume_slider_rect)
        pygame.draw.rect(SCREEN, YELLOW, volume_slider)

        SCREEN.blit(cat_image, (corner_x, corner_y))

        if pygame.time.get_ticks() % 150 == 0:
            spawn_rip()

        update_rip()
        for rip in falling_rip:
            SCREEN.blit(rip_image, (rip["x"], rip["y"]))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
                if theme_button.collidepoint(event.pos):
                    theme_index = (theme_index + 1) % len(THEMES)
                    current_theme = THEMES[theme_index]
                if sound_toggle_button.collidepoint(event.pos):
                    sound_on = not sound_on 
                    if not sound_on:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(volume_level / 100)
                        
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] and volume_slider_rect.collidepoint(event.pos):
                    volume_level = (event.pos[0] - volume_slider_rect.left) // 2
                    volume_level = max(0, min(volume_level, 100))
                    volume_slider.x = volume_slider_rect.left + (volume_level * 2)
                    pygame.mixer.music.set_volume(volume_level / 100)

        pygame.display.flip()



'''
MAIN GAME
'''

def get_new_character():
    return Player(PLAYER_POSITION[0], PLAYER_POSITION[1])

def random_coin_pos():
    while True:
        x = random.randint(10, SCREEN_WIDTH - COIN_SIZE)
        y = random.randint(10, SCREEN_HEIGHT - COIN_SIZE)
        coin_rect = pygame.Rect(x, y, COIN_SIZE, COIN_SIZE)
        if not (coin_rect.colliderect(RESTRICTED_AREA) or coin_rect.colliderect(RESTRICTED_AREA_2) or coin_rect.colliderect(RESTRICTED_AREA_3) or coin_rect.colliderect(RESTRICTED_AREA_4) or coin_rect.colliderect(RESTRICTED_AREA_5)):
            return [x, y]

def draw_hud():
    hp_x = 600
    hp_y = 20
    for i in range(0, HP):
        SCREEN.blit(hp, (hp_x, hp_y))
        hp_x += 45
    for i in range(0, 5-HP):
        SCREEN.blit(nohp, (hp_x, hp_y))
        hp_x += 45
    font = pygame.font.Font(None, 27)
    points_text = font.render(f"{POINTS} $", True, BLACK)
    pygame.draw.rect(SCREEN, GRAY, (923, 12, 46, 46))
    pygame.draw.rect(SCREEN, WHITE, (925, 15, 40, 40))
    SCREEN.blit(points_text, (927, 25))



'''
MINIGAME 1
'''

def scissors_tile(square_x, square_y):
    pygame.draw.rect(SCREEN, current_theme["button"], (square_x, square_y, 1.5*TILE_SIZE, TILE_SIZE))
    scaled_image = pygame.transform.scale(cash_img, (1.5*TILE_SIZE, TILE_SIZE))
    SCREEN.blit(scaled_image, (square_x, square_y))

def rock_tile(square_x, square_y):
    square_x = (SCREEN_WIDTH - TILE_SIZE) / 2 - TILE_SIZE - 150
    pygame.draw.rect(SCREEN, current_theme["button"], (square_x, square_y, 1.5*TILE_SIZE, TILE_SIZE))
    scaled_image = pygame.transform.scale(cash_img, (1.5*TILE_SIZE, TILE_SIZE))
    SCREEN.blit(scaled_image, (square_x, square_y))

def paper_tile(square_x, square_y):
    square_x = (SCREEN_WIDTH - TILE_SIZE) / 2 + TILE_SIZE + 150
    pygame.draw.rect(SCREEN, current_theme["button"], (square_x, square_y, 1.5*TILE_SIZE, TILE_SIZE))
    scaled_image = pygame.transform.scale(cash_img, (1.5*TILE_SIZE, TILE_SIZE))
    SCREEN.blit(scaled_image, (square_x, square_y))

def game(square_x, square_y):
    message = "> ONE OF THEM IS FAKE <"
    text_obj = FONT.render(message, True, current_theme["text"])
    text_rect = text_obj.get_rect(center=(SCREEN_HEIGHT//2, SCREEN_HEIGHT/2-(SCREEN_HEIGHT//3)))
    SCREEN.blit(text_obj, text_rect)
    scissors_tile(square_x, square_y)
    rock_tile(square_x, square_y)
    paper_tile(square_x, square_y)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def mouse_click(square_x, square_y):
    global Last_click, result
    if pygame.mouse.get_pressed()[0] and Last_click == False:
        pos = pygame.mouse.get_pos()
        pick = check_boxes(pos[0], pos[1], square_x, square_y)
        if pick != None:
            enemy_pick = ["Rock", "Scissors", "Paper"][random.randint(1, 3) - 1]
            SCREEN.fill(current_theme["bg"])
            if pick == enemy_pick:
                message = "YOU FOUND THE REAL CASH."
                text_obj = FONT.render(message, True, current_theme["text"])
                text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
                SCREEN.blit(text_obj, text_rect)
                pygame.display.update()
                pygame.time.delay(1000)
                result = True
                return result
            elif (pick == "Rock" and enemy_pick == "Paper") or (pick == "Paper" and enemy_pick == "Scissors") or (pick == "Scissors" and enemy_pick ==  "Rock"):
                message = "YOU FOUND THE REAL CASH."
                text_obj = FONT.render(message, True, current_theme["text"])
                text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
                SCREEN.blit(text_obj, text_rect)
                pygame.display.update()
                pygame.time.delay(1000)
                result = True
                return result
            elif (pick == "Rock" and enemy_pick == "Scissors") or (pick == "Paper" and enemy_pick == "Rock") or (pick == "Scissors" and enemy_pick ==  "Paper"):
                message = "OH NO. YOU FOUND FAKE MONEY!"
                text_obj = FONT.render(message, True, current_theme["text"])
                text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
                SCREEN.blit(text_obj, text_rect)
                pygame.display.update()
                pygame.time.delay(1000)
                result = False
                return result
    Last_click = pygame.mouse.get_pressed()[0]

def check_boxes(mouse_x, mouse_y, square_x, square_y):
    global TILE_SIZE
    rock_left = (SCREEN_WIDTH - TILE_SIZE) / 2 - TILE_SIZE - 150
    rock_right = (SCREEN_WIDTH - TILE_SIZE) / 2 - 150
    scissors_left = (SCREEN_WIDTH - TILE_SIZE) / 2
    scissors_right = (SCREEN_WIDTH - TILE_SIZE) / 2 + TILE_SIZE
    paper_left = (SCREEN_WIDTH - TILE_SIZE) / 2 + TILE_SIZE + 150
    paper_right = (SCREEN_WIDTH - TILE_SIZE) / 2 + 2*TILE_SIZE + 150
    tile_top = (SCREEN_HEIGHT - TILE_SIZE) / 2
    tile_bottom = (SCREEN_HEIGHT - TILE_SIZE) / 2 + TILE_SIZE

    if rock_left <= mouse_x <= rock_right and tile_top <= mouse_y <= tile_bottom:
        return "Rock"
    if scissors_left <= mouse_x <= scissors_right and tile_top <= mouse_y <= tile_bottom:
        return "Scissors"
    if paper_left <= mouse_x <= paper_right and tile_top <= mouse_y <= tile_bottom:
        return "Paper"
    return None

def mini_game_1():
    global SCREEN, BASIC_FONT, result, clock
    clock = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('>> CAT YOUR PAYCHECK <<')

    square_x = (SCREEN_WIDTH - TILE_SIZE) / 2
    square_y = (SCREEN_HEIGHT - TILE_SIZE) / 2
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()
                
        SCREEN.fill(current_theme["bg"])
        game(square_x, square_y) 
        mouse_click(square_x, square_y)
        if result is not None:
            running = False
        pygame.display.update()
    return result



'''
MINIGAME 2
'''

def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(SCREEN, current_theme["button"], (0, SCREEN_HEIGHT // 3 * i), (SCREEN_WIDTH, SCREEN_HEIGHT // 3 * i), LINE_WIDTH)
        pygame.draw.line(SCREEN, current_theme["button"], (SCREEN_WIDTH // 3 * i, 0), (SCREEN_WIDTH // 3 * i, SCREEN_HEIGHT), LINE_WIDTH)

def draw_mark(row, col, player):
    x = col * (SCREEN_WIDTH // 3) + (SCREEN_WIDTH // 6)
    y = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 6)
    if player == "player":  # X
        pygame.draw.line(SCREEN, current_theme["text"], (x - 40, y - 40), (x + 40, y + 40), CROSS_WIDTH)
        pygame.draw.line(SCREEN, current_theme["text"], (x - 40, y + 40), (x + 40, y - 40), CROSS_WIDTH)
    else:  # O
        pygame.draw.circle(SCREEN, current_theme["text"], (x, y), CIRCLE_RADIUS, LINE_WIDTH)

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    if all(cell is not None for row in board for cell in row):  
        return "draw"
    return None

def pc_move():
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = "pc"
                if check_winner() == "pc":
                    return row, col
                board[row][col] = "player"
                if check_winner() == "player":
                    board[row][col] = "pc"
                    return row, col
                board[row][col] = None
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = "pc"
                return row, col

def display_message(text):
    message = message_font2.render(text, True, current_theme["text"])
    SCREEN.fill(current_theme["bg"])
    SCREEN.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - message.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(1000)

def mini_game_2():
    global current_player, THEMES, board, result
    running = True
    SCREEN.fill(current_theme["bg"])
    draw_grid()
    current_player = "player"
    board = [[None] * 3 for _ in range(3)]
    pygame.display.set_caption('>> CAT YOUR PAYCHECK <<')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONDOWN and current_player == "player":
                x, y = event.pos
                row, col = y // (SCREEN_HEIGHT // 3), x // (SCREEN_WIDTH // 3)
                if board[row][col] is None:
                    board[row][col] = "player"
                    draw_mark(row, col, "player")
                    winner = check_winner()
                    if winner:
                        if winner == "draw":
                            display_message("IT'S A TIE.")
                            result = "Tie"
                            return result 
                        elif winner == "player":
                            display_message("YOU WON!")
                            result = True
                            return result
                        elif winner == "pc":
                            display_message("YOU LOST!")
                            result = False
                            return result
                    else:
                        current_player = "pc"

            if current_player == "pc" and running:
                row, col = pc_move()
                draw_mark(row, col, "pc")
                winner = check_winner()
                if winner:
                    if winner == "draw":
                        display_message("IT'S A TIE.")
                        result = "Tie"
                        return result
                    elif winner == "player":
                        display_message("YOU WON!")
                        result = True
                        return result
                    elif winner == "pc":
                        display_message("YOU LOST!")
                        result = False
                        return result
                else:
                    current_player = "player"

        pygame.display.update()
        pygame.display.flip()



'''
GAME LOOP
'''

def main():
    global FPS_CLOCK, SCREEN, BASIC_FONT, POINTS
    FPS_CLOCK = pygame.time.Clock()
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('>> CAT YOUR PAYCHECK <<')

    POINTS = 0
    while True:
        run_game()

def end_game():
    pygame.quit()
    sys.exit()

def game_over_screen():
    global POINTS, HP, nohp
    clock = pygame.time.Clock()

    running = True
    while running:
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 125, 250, 250, 50)
        points = pygame.Rect(SCREEN_WIDTH // 2 - 125, 320, 250, 50)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                end_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    HP = 5
                    main_menu()
        
        background = pygame.image.load("textures/backgroundnew.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        dead = pygame.image.load("textures/player_rip.png")
        dead = pygame.transform.scale(dead, (140, 140))
        background_dim = pygame.image.load("textures/gameoverbc.png")
        background_dim = pygame.transform.scale(background_dim, (SCREEN_WIDTH, SCREEN_HEIGHT))
        SCREEN.fill(current_theme["bg"])
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(background_dim, (0, 0))
        draw_text_menu("GAME OVER", font, WHITE, SCREEN, SCREEN_WIDTH // 2, 150)
        window = pygame.Rect(SCREEN_WIDTH // 2 - 250, 200, 500, 400)
        pygame.draw.rect(SCREEN, current_theme["bg"], window)

        SCREEN.blit(dead, (SCREEN_WIDTH // 2 - 70, 400))
        pygame.draw.rect(SCREEN, current_theme["button"], points)
        pygame.draw.rect(SCREEN, current_theme["button"], back_button)
        draw_text_menu("Back to menu", button_font, WHITE, SCREEN, SCREEN_WIDTH // 2, 270)
        draw_text_menu(f"Score: {POINTS}$", button_font, WHITE, SCREEN, SCREEN_WIDTH // 2, 340)

        pygame.display.flip()
        clock.tick(FPS)

    end_game()

def run_game():
    global POINTS, HP, result, hp, nohp
    clock = pygame.time.Clock()
    player = Player(PLAYER_POSITION[0], PLAYER_POSITION[1])
    coin = Coin(*random_coin_pos())

    all_sprites = pygame.sprite.Group(player, coin)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                end_game()
        keys = pygame.key.get_pressed()
        player.move(keys, SCREEN.get_rect())

        if pygame.sprite.collide_rect(player, coin):
            pygame.mixer.music.load("sounds/coin_sound.mp3")
            pygame.mixer.music.play(1)
            pygame.mixer.music.set_volume(0.5)

            if coin.special:
                minigame = random.randint(1, 2)
                if minigame == 1:
                    mini_game_1()
                elif minigame == 2:
                    mini_game_2()
                if result == True:
                    POINTS += 5
                elif result == False:
                    HP -= 1
                    if HP == 0:
                        game_over_screen()
                else:
                    pass
                result = None
            else:
                POINTS += 1
            coin.rect.topleft = random_coin_pos()
            coin.toggle_special()
        background = pygame.image.load("textures/backgroundnew.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        SCREEN.fill(current_theme["bg"])
        SCREEN.blit(background, (0, 0))
        draw_hud()
        all_sprites.draw(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)

    end_game()



if __name__ == "__main__":
    main_menu()
