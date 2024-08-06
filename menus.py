from additions import *


def idle():
    pass
class SettingsMenu:
    def __init__(self, WIDTH, HEIGHT):
        self.visible = False
        self.volume_slider = Slider(350, 200, 200, 20, 0, 100, 50)
        self.fullscreen_button = Button(350, 250, 200, 50, "Fullscreen: Off", WHITE, GRAY, DARK_GRAY, idle)
        self.resolution_button = Button(350, 320, 200, 50, "Resolution", WHITE, GRAY, DARK_GRAY, idle)
        self.back_button = Button(350, 390, 200, 50, "Back", WHITE, GRAY, DARK_GRAY, idle)
        self.fullscreen = False
        self.resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
        self.current_resolution = 0
        self.ui_objects = [self.volume_slider, self.fullscreen_button, self.resolution_button, self.back_button]
        self.Width = WIDTH
        self.Height = HEIGHT

    def draw(self, surface):
        if not self.visible:
            return

        overlay = pygame.Surface((self.Width, self.Height), pygame.SRCALPHA)
        overlay.fill(TRANSPARENT)
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, WHITE, (250, 150, 400, 300), border_radius=10)
        pygame.draw.rect(surface, BLACK, (250, 150, 400, 300), 2, border_radius=10)

        volume_text = basic_font.render(f"Volume: {int(self.volume_slider.value)}%", True, BLACK)
        surface.blit(volume_text, (270, 170))
        self.volume_slider.draw(surface)
        self.fullscreen_button.draw(surface)
        self.resolution_button.draw(surface)
        self.back_button.draw(surface)

    def handle_event(self, event):
        if not self.visible:
            return False

        self.volume_slider.handle_event(event)

        if self.fullscreen_button.handle_event(event):
            self.fullscreen = not self.fullscreen
            self.fullscreen_button.text = f"Fullscreen: {'On' if self.fullscreen else 'Off'}"
            pygame.display.toggle_fullscreen()

        if self.resolution_button.handle_event(event):
            self.current_resolution = (self.current_resolution + 1) % len(self.resolutions)
            new_resolution = self.resolutions[self.current_resolution]
            pygame.display.set_mode(new_resolution, pygame.RESIZABLE)
            self.resolution_button.text = f"Resolution: {new_resolution[0]}x{new_resolution[1]}"

        if self.back_button.handle_event(event):
            self.visible = False
            return True

        for button in [self.fullscreen_button, self.resolution_button, self.back_button]:
            button.check_hover(pygame.mouse.get_pos())

        return True
