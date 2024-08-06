import pygame
from screeninfo import get_monitors
from pytmx.util_pygame import load_pygame
import ctypes
import sys
import time

pygame.init()

display_width = 32 * 20
display_height = 32 * 20


pygame.display.set_caption("Gardex")
#screen = pygame.display.set_mode((display_width, display_height))
icon = pygame.image.load('assets/icons/game_icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
screen_info = pygame.display.Info()
running = True

world_objects = []
render_objects = []
ui_objects = []
gameState = 0 #Відповідає за вибір сцени, потипу меню і тд

window_mode = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)


#Fonts
basic_font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, click_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.click_color = click_color
        self.hovered = False
        self.clicked = False

    def draw(self, surface):
        if(self.clicked):
            print("Clicked")
            color = self.click_color
        elif(self.hovered):
            print("hovered")
            color = self.hover_color
        else:
            color = self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)

        text_surface = basic_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            print(f"{self.text} button clicked!")
            self.clicked = True
            if self.text == "Quit":
                pygame.quit()
                sys.exit()

def window_init():
    global screen
    if(window_mode == 0):
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    elif(window_mode == 1):
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.SCALED + pygame.NOFRAME)
        ctypes.windll.user32.SetProcessDPIAware()
        environ = pygame.display.get_wm_info()["window"]
        ctypes.windll.user32.MoveWindow(ctypes.c_long(environ), 0, 0, ctypes.c_int(screen_width), ctypes.c_int(screen_height), ctypes.c_int(True), )

    else:
        screen = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)

def load_world(level_path):
    world = load_pygame(level_path)
    #Finish World Loading
    return world

window_init()



while running:
    global screen
    clock.tick(60)
    keys = pygame.key.get_pressed()
    event = pygame.event.get()

    for e in event:
        if e.type == pygame.QUIT:
            running = False

        for uiob in ui_objects:
            uiob.handle_event(e)

    if gameState == 0: #головне меню
        screen_info = pygame.display.Info()
        # Load background image
        background = pygame.image.load("assets/backgrounds/background.png")
        background = pygame.transform.scale(background, (screen_info.current_w, screen_info.current_h))
        ui_objects = [
            Button(300, 200, 200, 50, "New", WHITE, GRAY, DARK_GRAY),
            Button(300, 275, 200, 50, "Load", WHITE, GRAY, DARK_GRAY),
            Button(300, 350, 200, 50, "Settings", WHITE, GRAY, DARK_GRAY),
            Button(300, 425, 200, 50, "Quit", WHITE, GRAY, DARK_GRAY)
        ] #Need to Fix Dynamic rendering
        screen.blit(background, (0, 0))
        for uiob in ui_objects:
            uiob.check_hover(pygame.mouse.get_pos())
            uiob.draw(screen)
        #for ele in render_objects:
        #    ele.draw(screen)
    elif gameState == 1: #налаштування
        pass
    elif gameState == 2: #вибір світу
        pass
    elif gameState == 3: #створення світу
        pass
    elif gameState == 4: #завантаження світу
        pass
    elif gameState == 5: #гра
        screen.fill((0, 0, 0))
        for obj in render_objects:
            obj.update(keys)
    else:
        gameState = 0

    pygame.display.flip()

pygame.quit()
