import pygame
import sys

# Initialize pygame
pygame.init()

# Set screen size and create a window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

# Load button images
def load_btn_image(image_name):
    return pygame.image.load(image_name).convert_alpha()

# Button class to handle button creation and interaction
class Btn:
<<<<<<< HEAD
    def _init_(self, image, x, y, width, height, action=None, hover_image=None):
=======
    def __init__(self, image, x, y, width, height, action=None, hover_image=None):
>>>>>>> 51adfe3a64bfd5de554da0758a83383cc34046d3
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
<<<<<<< HEAD
    def _init_(self, screen):
=======
    def __init__(self, screen):
>>>>>>> 51adfe3a64bfd5de554da0758a83383cc34046d3
        self.screen = screen
        self.state = "main"
        self.main_menu_btns = []
        self.story_menu_btns = []
        self.options_menu_btns = []
        self.credits_menu_btns = []
        self.current_menu_btns = []

        # Load background image
        self.bg = pygame.image.load("assets/menu_background.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (screen_width, screen_height))

        # Load main menu buttons
        start_img = load_btn_image("assets/start_btn.png")
        start_hover = load_btn_image("assets/start_btn_hover.png")
        options_img = load_btn_image("assets/options_btn.png")
        options_hover = load_btn_image("assets/options_btn_hover.png")
        exit_img = load_btn_image("assets/exit_btn.png")
        exit_hover = load_btn_image("assets/exit_btn_hover.png")
        credits_img = load_btn_image("assets/credits_btn.png")  # no hover
        # Credits intentionally has no hover image

        self.start_btn = Btn(start_img, 400, 200, 300, 100, self.open_story_menu, start_hover)
        self.options_btn = Btn(options_img, 400, 300, 300, 100, self.open_options_menu, options_hover)
        self.credits_btn = Btn(credits_img, 400, 400, 300, 100, self.open_credits_menu)
        self.exit_btn = Btn(exit_img, 400, 500, 300, 100, self.quit_game, exit_hover)

        self.main_menu_btns = [self.start_btn, self.options_btn, self.credits_btn, self.exit_btn]

        # Load story menu buttons
        story_mode_img = load_btn_image("assets/story_mode_btn.png")
        story_mode_hover = load_btn_image("assets/story_mode_btn_hover.png")
        single_player_img = load_btn_image("assets/single_player_btn.png")
        single_player_hover = load_btn_image("assets/single_player_btn_hover.png")
        multiplayer_img = load_btn_image("assets/multiplayer_btn.png")
        multiplayer_hover = load_btn_image("assets/multiplayer_btn_hover.png")

        self.story_mode_btn = Btn(story_mode_img, 400, 200, 300, 100, self.start_story_mode, story_mode_hover)
        self.single_player_btn = Btn(single_player_img, 400, 300, 300, 100, self.start_single_player, single_player_hover)
        self.multiplayer_btn = Btn(multiplayer_img, 400, 400, 300, 100, self.start_multiplayer, multiplayer_hover)

        self.story_menu_btns = [self.story_mode_btn, self.single_player_btn, self.multiplayer_btn]

        # Load options menu buttons
        sound_on_img = load_btn_image("assets/sound_on_btn.png")
        sound_off_img = load_btn_image("assets/sound_off_btn.png")
        music_on_img = load_btn_image("assets/music_on_btn.png")
        music_off_img = load_btn_image("assets/music_off_btn.png")

        self.sound_on_btn = Btn(sound_on_img, 400, 200, 300, 100, self.toggle_sound)
        self.sound_off_btn = Btn(sound_off_img, 400, 200, 300, 100, self.toggle_sound)
        self.music_on_btn = Btn(music_on_img, 400, 300, 300, 100, self.toggle_music)
        self.music_off_btn = Btn(music_off_img, 400, 300, 300, 100, self.toggle_music)

        self.sound_on = True
        self.music_on = True

        # Load back button
        back_img = load_btn_image("assets/back_btn.png")
        back_hover = load_btn_image("assets/back_btn_hover.png")
        self.back_btn = Btn(back_img, 50, 50, 100, 40, self.return_to_main_menu, back_hover)

        # Credits scroll setup
        self.credits_scroll_y = screen_height

        self.current_menu_btns = self.main_menu_btns

    def open_story_menu(self):
        self.state = "story"
        self.current_menu_btns = self.story_menu_btns + [self.back_btn]

    def open_options_menu(self):
        self.state = "options"
        if self.sound_on:
            self.current_menu_btns = [self.sound_on_btn, self.music_on_btn, self.back_btn]
        else:
            self.current_menu_btns = [self.sound_off_btn, self.music_on_btn, self.back_btn]
        if not self.music_on:
            self.current_menu_btns[1] = self.music_off_btn

    def open_credits_menu(self):
        self.state = "credits"
        self.current_menu_btns = []  # No buttons except back
        self.credits_scroll_y = screen_height  # Reset scroll

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        print(f"Sound {'On' if self.sound_on else 'Off'}")
        self.open_options_menu()

    def toggle_music(self):
        self.music_on = not self.music_on
        print(f"Music {'On' if self.music_on else 'Off'}")
        self.open_options_menu()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def start_story_mode(self):
        print("Starting Story Mode...")

    def start_single_player(self):
        print("Starting Single Player Mode...")

    def start_multiplayer(self):
        print("Starting Multiplayer Mode...")

    def return_to_main_menu(self):
        self.state = "main"
        self.current_menu_btns = self.main_menu_btns

    def draw_credits(self):
        self.screen.fill((50, 50, 50))
        font = pygame.font.SysFont(None, 40)
        lines = [
            "Game Credits",
            "",
            "Game Design: Your Name",
            "Developer: Your Name",
            "Music: Composer Name",
            "Thanks for playing!"
        ]
        for i, line in enumerate(lines):
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width // 2, self.credits_scroll_y + i * 50))
            self.screen.blit(text, text_rect)
        self.credits_scroll_y -= 1
        if self.credits_scroll_y + len(lines) * 50 < 0:
            self.credits_scroll_y = screen_height

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.state == "credits":
            self.draw_credits()
        else:
            self.screen.blit(self.bg, (0, 0))
            for btn in self.current_menu_btns:
                btn.draw(self.screen)

        if self.state in ["story", "options", "credits"]:
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
                    for btn in self.current_menu_btns + ([self.back_btn] if self.state in ["story", "options", "credits"] else []):
                        if btn.check_click(mouse_pos):
                            btn.is_pressed = True
                            btn.click()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for btn in self.current_menu_btns + [self.back_btn]:
                        btn.is_pressed = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.state == "credits":
                    self.return_to_main_menu()

def main():
    menu = Menu(screen)
    while True:
        menu.handle_events()
        menu.draw()
        pygame.time.Clock().tick(60)

<<<<<<< HEAD
main()
=======
main()
>>>>>>> 51adfe3a64bfd5de554da0758a83383cc34046d3
