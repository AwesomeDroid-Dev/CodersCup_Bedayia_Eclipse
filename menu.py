import pygame
import sys
import os

import level_2

# Initialize pygame
pygame.init()

import level_1

# Initialize mixer if not already done
if not pygame.mixer.get_init():
    pygame.mixer.init()

# Play menu background music
MENU_MUSIC_PATH = os.path.join('Sounds', 'menu sound.wav')
if os.path.exists(MENU_MUSIC_PATH):
    pygame.mixer.music.load(MENU_MUSIC_PATH)
    pygame.mixer.music.play(-1)

# Load clicking sound for menu selection
CLICK_SOUND_PATH = os.path.join('Sounds', 'clicking sound.wav')
click_sound = pygame.mixer.Sound(CLICK_SOUND_PATH) if os.path.exists(CLICK_SOUND_PATH) else None

# Keep references to all sound effects for muting/unmuting
sound_effects = []
if click_sound:
    sound_effects.append(click_sound)

# Store music state
music_playing = True

# Load button images
def load_btn_image(image_name):
    return pygame.image.load(image_name).convert_alpha()

# Function to set sound effects volume
def set_sound_effects_volume(volume):
    for s in sound_effects:
        s.set_volume(volume)

# Button class to handle button creation and interaction
class Btn:
    def __init__(self, image, x, y, width, height, action=None, hover_image=None):
        self.image = pygame.transform.scale(image, (width, height))
        self.original_image = self.image
        self.hover_image = pygame.transform.scale(hover_image, (width, height)) if hover_image else None
        self.rect = self.image.get_rect(center=(x, y))
        self.action = action
        self.is_pressed = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self.hover_image:
            screen.blit(self.hover_image, self.rect)
        else:
            screen.blit(self.original_image, self.rect)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.action:
            self.action()

# Menu class to manage different game screens
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.state = "main"
        self.main_menu_btns = []
        self.level_menu_btns = []
        self.options_menu_btns = []
        self.credits_menu_btns = []
        self.current_menu_btns = []

        # Load background image
        self.bg = pygame.image.load("assets/menu_background.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1200, 600))

        # Button dimensions
        button_width = 300
        button_height = 80

        # Level button dimensions - make them less wide but keep the same height
        level_button_width = 200
        level_button_height = 80

        # Offset all menus a little down
        vertical_offset = 60

        # Load images for all buttons
        def load_pair(base):
            return load_btn_image(f"assets/{base}_btn.png"), load_btn_image(f"assets/{base}_btn_hover.png")

        # Common function to space and center buttons vertically
        def create_buttons(images, actions, spacing=20, width=button_width, height=button_height):
            total_height = len(images) * height + (len(images) - 1) * spacing
            start_y = (600 - total_height) // 2 + vertical_offset
            buttons = []
            for i in range(len(images)):
                img, hover = images[i]
                action = actions[i]
                y = start_y + i * (height + spacing)
                buttons.append(Btn(img, 1200 // 2, y, width, height, action, hover))
            return buttons

        start_img = load_pair("start")
        options_img = load_pair("options")
        credits_img = load_pair("credits")
        exit_img = load_pair("exit")

        # Level buttons
        level1_img = load_pair("level1")
        level2_img = load_pair("level2")


        sound_on_img = load_btn_image("assets/sound_on_btn.png")
        sound_off_img = load_btn_image("assets/sound_off_btn.png")
        music_on_img = load_btn_image("assets/music_on_btn.png")
        music_off_img = load_btn_image("assets/music_off_btn.png")

        back_img, back_hover = load_pair("back")
        self.back_btn = Btn(back_img, 100, 50, 100, 40, self.return_to_main_menu, back_hover)

        # Main menu buttons (slightly less spacing)
        self.main_menu_btns = create_buttons(
            [start_img, options_img, credits_img, exit_img],
            [self.open_level_menu, self.open_options_menu, self.open_credits_menu, self.quit_game],
            spacing=15
        )

        # Level menu buttons - with narrower, less wide buttons
        self.level_menu_btns = create_buttons(
            [level1_img, level2_img],
            [self.start_level1, self.start_level2],
            spacing=15,
            width=level_button_width,
            height=level_button_height
        )

        # Options menu buttons with resized sound/music buttons
        small_btn_size = 64  # size for circular buttons like sound/music
        self.sound_on_btn = Btn(sound_on_img, 1200 // 2, 200 + vertical_offset, small_btn_size, small_btn_size, self.toggle_sound)
        self.sound_off_btn = Btn(sound_off_img, 1200 // 2, 200 + vertical_offset, small_btn_size, small_btn_size, self.toggle_sound)
        self.music_on_btn = Btn(music_on_img, 1200 // 2, 300 + vertical_offset, small_btn_size, small_btn_size, self.toggle_music)
        self.music_off_btn = Btn(music_off_img, 1200 // 2, 300 + vertical_offset, small_btn_size, small_btn_size, self.toggle_music)

        self.sound_on = True
        self.music_on = True

        self.credits_scroll_y = 600
        self.current_menu_btns = self.main_menu_btns

    def open_level_menu(self):
        if click_sound:
            click_sound.play()
        self.state = "level"
        self.current_menu_btns = self.level_menu_btns + [self.back_btn]

    def open_options_menu(self):
        if click_sound:
            click_sound.play()
        self.state = "options"
        if self.sound_on:
            sound_btn = self.sound_on_btn
        else:
            sound_btn = self.sound_off_btn
        music_btn = self.music_on_btn if self.music_on else self.music_off_btn
        self.current_menu_btns = [sound_btn, music_btn, self.back_btn]

    def open_credits_menu(self):
        if click_sound:
            click_sound.play()
        self.state = "credits"
        self.current_menu_btns = []
        self.credits_scroll_y = 600

    def toggle_sound(self):
        if click_sound:
            click_sound.play()
        self.sound_on = not self.sound_on
        print(f"Sound {'On' if self.sound_on else 'Off'}")
        set_sound_effects_volume(1.0 if self.sound_on else 0.0)
        self.open_options_menu()

    def toggle_music(self):
        global music_playing
        if click_sound:
            click_sound.play()
        self.music_on = not self.music_on
        print(f"Music {'On' if self.music_on else 'Off'}")
        if self.music_on:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            music_playing = True
        else:
            pygame.mixer.music.stop()
            music_playing = False
        self.open_options_menu()

    def quit_game(self):
        if click_sound:
            click_sound.play()
        pygame.quit()
        sys.exit()

    def start_level1(self):
        if click_sound:
            click_sound.play()
        running = False
        level_1.init_game()
        level_1.main()

    def start_level2(self):
        if click_sound:
            click_sound.play()
        level_2.init_game()
        level_2.main()

    def return_to_main_menu(self):
        if click_sound:
            click_sound.play()
        self.state = "main"
        self.current_menu_btns = self.main_menu_btns

    def draw_credits(self):
        self.screen.fill((50, 50, 50))
        font = pygame.font.SysFont(None, 40)
        lines = [
            "Game Credits",
            "",
            "Game Design:",
            "Ziyad Meligy",
            "Omar Samir",
            "Noureddin Elazab",
            "",
            "Developers:",
            "Noureddin Elazab",
            "Ziyad Meligy",
            "",
            "Music:",
            "Omar Samir",
            "",
            "Thanks for playing!"
        ]
        for i, line in enumerate(lines):
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(1200 // 2, self.credits_scroll_y + i * 50))
            self.screen.blit(text, text_rect)
        self.credits_scroll_y -= 1
        if self.credits_scroll_y + len(lines) * 50 < 0:
            self.credits_scroll_y = 600

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.state == "credits":
            self.draw_credits()
        else:
            self.screen.blit(self.bg, (0, 0))
            for btn in self.current_menu_btns:
                btn.draw(self.screen)

        if self.state in ["level", "options", "credits"]:
            self.back_btn.draw(self.screen)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for btn in self.current_menu_btns + ([self.back_btn] if self.state in ["level", "options", "credits"] else []):
                        if btn.check_click(mouse_pos):
                            btn.is_pressed = True
                            btn.click()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for btn in self.current_menu_btns + ([self.back_btn] if self.state in ["level", "options", "credits"] else []):
                        btn.is_pressed = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.state == "credits":
                    self.return_to_main_menu()

def main():
    # Initialize pygame
    pygame.init()

    # Set screen size and create a window
    screen_width = 1200
    screen_height = 600
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Menu")
        
    global running
    running = True
    menu = Menu(screen)
    while running:
        menu.handle_events()
        menu.draw()
        pygame.time.Clock().tick(60)

main()
