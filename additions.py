import pygame
import sys

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
TRANSPARENT = (0, 0, 0, 128)

#Fonts
basic_font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, click_color, function):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.click_color = click_color
        self.hovered = False
        self.clicked = False
        self.click_time = 0
        self.function = function

    def draw(self, surface):
        if self.clicked and pygame.time.get_ticks() - self.click_time < 100:
            color = self.click_color
        elif self.hovered:
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
        global gameState
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.function()
            self.clicked = True
            self.click_time = pygame.time.get_ticks()
            print(f"{self.text} button clicked!")



class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)

        handle_pos = self.rect.x + int(
            (self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width)
        handle_rect = pygame.Rect(handle_pos - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(surface, WHITE, handle_rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, handle_rect, 2, border_radius=5)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.value = max(self.min_value, min(self.max_value,
                                                 (event.pos[0] - self.rect.x) / self.rect.width * (
                                                             self.max_value - self.min_value) + self.min_value))
