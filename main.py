from pytmx.util_pygame import load_pygame
import ctypes
from additions import *
import pygame
import sys
import menus

pygame.init()

display_width = 32 * 20
display_height = 32 * 20


pygame.display.set_caption("Gardex")
icon = pygame.image.load('assets/icons/game_icon.png')
background_img = pygame.image.load("assets/backgrounds/background.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
screen_info = pygame.display.Info()
running = True

world_objects = []
render_objects = []
ui_objects = []
gameState = 0 #Відповідає за вибір сцени, потипу юі чи гра
past_gameState = 1

window_mode = 1

scene = menus.SettingsMenu(screen_info.current_w, screen_info.current_h)

def quit():
    pygame.quit()
    sys.exit()

def newGame():
    pass

def LoadGame():
    pass

def openSettingsMenu():
    global scene
    scene = menus.SettingsMenu(screen_info.current_w, screen_info.current_h)
    scene.visible = True
    print("opened")

def BackToMenu():
    pass
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
        if not (scene == None):
            scene.handle_event(e)
        for uiob in ui_objects:
            uiob.handle_event(e)
    screen_info = pygame.display.Info()
    # Load background image
    background = pygame.transform.scale(background_img, (screen_info.current_w, screen_info.current_h))
    screen.blit(background, (0, 0))
    if gameState == 0: #головне меню
        if not (scene == None):
            scene.draw(screen)
        if not(past_gameState == gameState):
            past_gameState = gameState
            ui_objects = [
                Button(300, 200, 200, 50, "New", WHITE, GRAY, DARK_GRAY, newGame),
                Button(300, 275, 200, 50, "Load", WHITE, GRAY, DARK_GRAY, LoadGame),
                Button(300, 350, 200, 50, "Settings", WHITE, GRAY, DARK_GRAY, openSettingsMenu),
                Button(300, 425, 200, 50, "Quit", WHITE, GRAY, DARK_GRAY, quit)
            ] #Need to Fix Dynamic rendering

        for uiob in ui_objects:
            uiob.check_hover(pygame.mouse.get_pos())
            uiob.draw(screen)
        #for ele in render_objects:
        #    ele.draw(screen)
    elif gameState == 1: #гра
        screen.fill((0, 0, 0))
        for obj in render_objects:
            obj.update(keys)
    else:
        gameState = 0

    pygame.display.flip()

pygame.quit()
