import pygame
import random
import sys
import os

# --- INITIALIZE ---
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toothless: Night Fury Rescue") 
clock = pygame.time.Clock()

# --- COLORS ---
SKY = (5, 10, 24)
GOLD = (245, 158, 11)
RED = (239, 68, 68)
WHITE = (255, 255, 255)
CYAN = (0, 242, 255)

# --- ASSET LOADER ---
def load_img(name, size):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, name)
    try:
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        else:
            for file in os.listdir(script_dir):
                if name.lower() in file.lower():
                    new_path = os.path.join(script_dir, file)
                    img = pygame.image.load(new_path).convert_alpha()
                    return pygame.transform.scale(img, size)
            raise FileNotFoundError
    except:
        surf = pygame.Surface(size)
        if "toothless" in name: surf.fill(GOLD)
        elif "hunter" in name: surf.fill(RED)
        else: surf.fill(CYAN)
        return surf

# Load Assets
toothless_img = load_img('toothless.png', (80, 80))
hunter_img = load_img('hunter.png', (60, 60))
rescue_img = load_img('rescue.png', (50, 50))

# --- ENTITY CLASS ---
class Entity:
    def __init__(self, img, x, y, speed):
        self.img = img
        self.rect = self.img.get_rect(center=(x, y))
        self.vx, self.vy = random.uniform(-speed, speed), random.uniform(-speed, speed)
    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left < 0 or self.rect.right > WIDTH: self.vx *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT: self.vy *= -1

# --- INITIAL GAME STATE ---
player_rect = toothless_img.get_rect(center=(WIDTH//2, HEIGHT//2))
hunters = [Entity(hunter_img, random.randint(50,850), random.randint(50,650), 3) for _ in range(3)] # Start with 3
rescues = [Entity(rescue_img, random.randint(50,850), random.randint(50,650), 2) for _ in range(3)]
xp, active, total_rescues = 0, False, 0

# --- LOOP ---
while True:
    screen.fill(SKY)
    btn = pygame.Rect(WIDTH-170, 20, 150, 45)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn.collidepoint(event.pos): pygame.quit(); sys.exit()
            if not active: 
                active = True
                xp = 0
                total_rescues = 0
                # Reset hunters to 3 on new game
                hunters = [Entity(hunter_img, random.randint(50,850), random.randint(50,650), 3) for _ in range(3)]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not active: 
                active = True
                xp = 0
                total_rescues = 0
                hunters = [Entity(hunter_img, random.randint(50,850), random.randint(50,650), 3) for _ in range(3)]

    if not active:
        title_font = pygame.font.SysFont("Arial", 50, True)
        desc_font = pygame.font.SysFont("Arial", 22)
        screen.blit(title_font.render("NIGHT FURY: THE RESCUE", True, GOLD), (WIDTH//2 - 270, 120))
        lines = [
            "MISSION DESCRIPTION:",
            "- Rescue the BLUE DRAGONS to earn XP.",
            "- STAY AWAY from the RED HUNTER SHIPS.",
            "- WARNING: Every 5 rescues, a new Hunter joins the hunt!",
            "",
            "PRESS [SPACE] OR CLICK TO START"
        ]
        y_offset = 240
        for line in lines:
            color = CYAN if "START" in line else WHITE
            screen.blit(desc_font.render(line, True, color), (WIDTH//2 - 250, y_offset))
            y_offset += 40
            
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_rect.x -= 8
        if keys[pygame.K_RIGHT]: player_rect.x += 8
        if keys[pygame.K_UP]: player_rect.y -= 8
        if keys[pygame.K_DOWN]: player_rect.y += 8

        for h in hunters:
            h.move(); screen.blit(h.img, h.rect)
            if player_rect.colliderect(h.rect): active = False

        for r in rescues:
            r.move(); screen.blit(r.img, r.rect)
            if player_rect.colliderect(r.rect):
                xp += 150
                total_rescues += 1
                r.rect.center = (random.randint(50,850), random.randint(50,650))
                
                # --- LEVEL UP LOGIC ---
                if total_rescues % 5 == 0:
                    new_h = Entity(hunter_img, random.randint(50,850), random.randint(50,650), 3)
                    hunters.append(new_h)
                    print(f"⚠️ NEW HUNTER DETECTED! Total Rescues: {total_rescues}")

        screen.blit(toothless_img, player_rect)
        stat = pygame.font.SysFont("Arial", 24, True).render(f"XP: {xp} | Rescues: {total_rescues}", True, GOLD)
        screen.blit(stat, (20, 20))

    pygame.draw.rect(screen, RED, btn, border_radius=12)
    q_txt = pygame.font.SysFont("Arial", 20, True).render("LEAVE GAME", True, WHITE)
    screen.blit(q_txt, (WIDTH - 155, 28))
    
    pygame.display.flip()
    clock.tick(60)
