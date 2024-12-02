import pygame
import random
import sys

# Pygame inicializálása
pygame.init()

# Képernyő méretének beállítása
screen_width = 1366
screen_height = 688
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Akadály Kikerülős Játék")

# Színek
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Játékos paraméterek
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 10

# Akadály paraméterek
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 15
obstacles = []

# Események kezelése
clock = pygame.time.Clock()

# Játék változók
game_over = False
score = 0
high_score = 0  # Rekord kezdő értéke
current_skin = "Kék"  # Alapértelmezett skin
unlocked_skins = ["Kék", "Zöld", "Fekete", "Sárga"]  # Az összes skin elérhető

# Kezdőképernyő funkció
def show_start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    title_text = font.render("Akadály Kikerülős Játék", True, BLACK)
    start_text = font.render("Nyomj SPACE-t a kezdéshez!", True, BLUE)
    skin_text = font.render("Nyomj S-t a Skinekhez", True, BLUE)
    
    screen.blit(title_text, (screen_width // 4, screen_height // 3))
    screen.blit(start_text, (screen_width // 4, screen_height // 2 - 50))
    screen.blit(skin_text, (screen_width // 4, screen_height // 2 + 50))
    pygame.display.update()
    
    # Várakozás a kezdésre vagy skin menü megjelenítésére
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return "start"  # Kezdőképernyőn a játék indítása
        elif keys[pygame.K_s]:
            return "skins"  # Skin választás menü


# Skin választás menü
def show_skin_menu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    title_text = font.render("Válassz Skint!", True, BLACK)
    
    # Skin választás leírása a bal felső sarokba
    back_text = font.render("Nyomj ESC-t a visszalépéshez", True, BLUE)
    screen.blit(back_text, (10, 10))  # Bal felső sarokban

    screen.blit(title_text, (screen_width // 4, screen_height // 3))
    
    # Skinek megjelenítése
    skin_names = ["Kék", "Zöld", "Fekete", "Sárga"]
    skin_colors = [BLUE, GREEN, BLACK, YELLOW]  # A skin színek
    for i, skin in enumerate(skin_names):
        color = skin_colors[i]
        skin_text = font.render(f"{i+1}. {skin}", True, color)  # A skin számmal együtt
        screen.blit(skin_text, (screen_width // 4, screen_height // 2 + 50 * i))
    
    pygame.display.update()
    
    # Várakozás a skin választására vagy visszalépésre
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Visszalépés a főmenübe
            return "back"
        for i in range(4):
            if keys[pygame.K_1 + i]:  # Az 1, 2, 3, 4-es billentyűk a skin kiválasztásához
                return skin_names[i]  # Választott skin


# Játék kezdése a kezdőképernyővel
def start_game():
    global player_x, player_y, score, game_over
    score = 0
    game_over = False
    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height - player_height - 10

# Skin kiválasztása
def select_skin():
    global current_skin
    result = show_skin_menu()
    if result == "back":
        return "back"
    elif result in ["Kék", "Zöld", "Fekete", "Sárga"]:
        current_skin = result
        return result

# Kezdőképernyő megjelenítése és skin választás
while True:
    result = show_start_screen()
    if result == "start":
        start_game()
    elif result == "skins":
        skin = select_skin()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Játékos mozgása
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Akadály generálása
        if random.randint(1, 100) <= 16:  # Kb. minden 50ms-ban 16% esély egy új akadályra
            obstacle_x = random.randint(0, screen_width - obstacle_width)
            obstacles.append([obstacle_x, 0])

        # Akadályok mozgása
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed

        # Ütközés ellenőrzése
        for obstacle in obstacles:
            if (obstacle[0] < player_x + player_width and
                obstacle[0] + obstacle_width > player_x and
                obstacle[1] < player_y + player_height and
                obstacle[1] + obstacle_height > player_y):
                game_over = True
                break

        # Akadályok eltávolítása, ha kijutottak a képernyő aljára
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] < screen_height]

        # Pontszám frissítése
        score += 1

        # Képernyő törlése és frissítése
        screen.fill(WHITE)
        
        # Játékos és akadályok kirajzolása
        if current_skin == "Kék":
            pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
        elif current_skin == "Zöld":
            pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))
        elif current_skin == "Fekete":
            pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))
        elif current_skin == "Sárga":
            pygame.draw.rect(screen, YELLOW, (player_x, player_y, player_width, player_height))
        
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

        # Pontszám és rekord kirajzolása
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Pontszám: {score}", True, (0, 0, 0))
        high_score_text = font.render(f"Rekord: {high_score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))  # Pontszám bal felső sarokban
        screen.blit(high_score_text, (screen_width - 200, 10))  # Rekord jobb felső sarokban

        # Képernyő frissítése
        pygame.display.update()
        clock.tick(60)

    # Ha játék vége van, frissítjük a rekordot
    if score > high_score:
        high_score = score  # Rekord frissítése, ha az aktuális pontszám magasabb

    # Visszavisz a kezdőképernyőre
    game_over = False
    show_start_screen()
