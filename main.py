import pygame
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Menu System")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)

# Fonts
title_font = pygame.font.SysFont('Arial', 64, bold=True)
menu_font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)


class Button:
    def __init__(self, text, x, y, width, height, inactive_color, active_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.action = action
        self.hover = False
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        # Check if mouse is over button
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

        # Draw button with appropriate color
        color = self.active_color if self.hover else self.inactive_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Border

        # Draw text
        text_surface = menu_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover and self.action:
                return self.action
        return None


class Menu:
    def __init__(self):
        self.running = True
        self.current_screen = "main_menu"

        # Create buttons for main menu
        button_width, button_height = 250, 60
        button_x = WIDTH // 2 - button_width // 2

        self.main_menu_buttons = [
            Button("Play", button_x, 200, button_width, button_height, LIGHT_BLUE, DARK_BLUE, "play_menu"),
            Button("Settings", button_x, 280, button_width, button_height, LIGHT_BLUE, DARK_BLUE, "settings"),
            Button("Credits", button_x, 360, button_width, button_height, LIGHT_BLUE, DARK_BLUE, "credits"),
            Button("Quit", button_x, 440, button_width, button_height, LIGHT_BLUE, RED, "quit")
        ]

        # Create buttons for play mode selection
        self.play_menu_buttons = [
            Button("Single Player", button_x, 200, button_width, button_height, LIGHT_BLUE, GREEN, "single_player"),
            Button("Two Player", button_x, 280, button_width, button_height, LIGHT_BLUE, PURPLE, "two_player"),
            Button("Story Mode", button_x, 360, button_width, button_height, LIGHT_BLUE, DARK_BLUE, "story_mode"),
            Button("Back", button_x, 440, button_width, button_height, LIGHT_BLUE, DARK_BLUE, "main_menu")
        ]

        # Create buttons for settings menu
        self.settings_buttons = [
            Button("Sound: ON", button_x, 200, button_width, button_height, LIGHT_BLUE, DARK_BLUE, "toggle_sound"),
            Button("Music: ON", button_x, 280, button_width, button_height, LIGHT_BLUE, DARK_BLUE, "toggle_music"),
            Button("Difficulty: Normal", button_x, 360, button_width, button_height, LIGHT_BLUE, DARK_BLUE,
                   "toggle_difficulty"),
            Button("Back", button_x, 440, button_width, button_height, LIGHT_BLUE, DARK_BLUE, "main_menu")
        ]

        # Create buttons for story chapters selection
        self.story_chapters_buttons = [
            Button("Chapter 1: Beginning", button_x, 200, button_width, button_height, LIGHT_BLUE, DARK_BLUE,
                   "chapter_1"),
            Button("Chapter 2: Journey", button_x, 280, button_width, button_height, LIGHT_BLUE, DARK_BLUE,
                   "chapter_2"),
            Button("Chapter 3: Climax", button_x, 360, button_width, button_height, LIGHT_BLUE, DARK_BLUE, "chapter_3"),
            Button("Back", button_x, 440, button_width, button_height, LIGHT_BLUE, DARK_BLUE, "play_menu")
        ]

        # Settings state
        self.sound_on = True
        self.music_on = True
        self.difficulty = "Normal"  # Easy, Normal, Hard
        self.game_mode = "single_player"  # single_player, two_player, story_mode (and chapter if applicable)
        self.story_chapter = None

        # Credits scroll variables
        self.credits_offset = HEIGHT
        self.credits_text = [
            "Game Credits",
            "",
            "Game Design",
            "Your Name",
            "",
            "Programming",
            "Your Name",
            "",
            "Art",
            "Your Name",
            "",
            "Sound",
            "Your Name",
            "",
            "Special Thanks",
            "Your Family",
            "Your Friends",
            "",
            "Press ESC to return to Main Menu"
        ]

        # Story introduction text
        self.story_text = {
            "chapter_1": [
                "Chapter 1: The Beginning",
                "",
                "Our hero awakens in a strange land,",
                "with no memory of how they arrived.",
                "",
                "A mysterious figure approaches and",
                "explains that the world is in danger.",
                "",
                "You must embark on a journey to",
                "recover the lost artifacts and",
                "restore balance to the realm.",
                "",
                "Press SPACE to begin your adventure..."
            ],
            "chapter_2": [
                "Chapter 2: The Journey",
                "",
                "After retrieving the first artifact,",
                "our hero discovers a hidden map.",
                "",
                "The map reveals the location of the",
                "second artifact, deep within the",
                "treacherous Crystal Caverns.",
                "",
                "New allies join your quest, but",
                "dangerous enemies lurk in the shadows.",
                "",
                "Press SPACE to continue your journey..."
            ],
            "chapter_3": [
                "Chapter 3: The Climax",
                "",
                "With two artifacts in hand, only one remains.",
                "",
                "The final artifact is held by the Dark Lord",
                "in their fortress atop the Forbidden Mountain.",
                "",
                "Your allies prepare for the final battle,",
                "knowing that the fate of the world",
                "hangs in the balance.",
                "",
                "Press SPACE to face your destiny..."
            ]
        }

        # Selected button index for keyboard navigation
        self.selected_button_index = 0
        self.active_buttons = self.main_menu_buttons

        # Story mode screen offset
        self.story_offset = 0

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle keyboard navigation
                if event.type == pygame.KEYDOWN:
                    if self.current_screen in ["main_menu", "settings", "play_menu", "story_chapters"]:
                        if event.key == pygame.K_UP:
                            self.selected_button_index = (self.selected_button_index - 1) % len(self.active_buttons)
                        elif event.key == pygame.K_DOWN:
                            self.selected_button_index = (self.selected_button_index + 1) % len(self.active_buttons)
                        elif event.key == pygame.K_RETURN:
                            action = self.active_buttons[self.selected_button_index].action
                            self.handle_action(action)

                    if event.key == pygame.K_ESCAPE:
                        if self.current_screen == "main_menu":
                            self.running = False
                        elif self.current_screen == "play_menu":
                            self.current_screen = "main_menu"
                            self.active_buttons = self.main_menu_buttons
                            self.selected_button_index = 0
                        elif self.current_screen == "story_chapters":
                            self.current_screen = "play_menu"
                            self.active_buttons = self.play_menu_buttons
                            self.selected_button_index = 0
                        elif self.current_screen in ["settings", "credits", "game", "story_intro"]:
                            self.current_screen = "main_menu"
                            self.active_buttons = self.main_menu_buttons
                            self.selected_button_index = 0

                    if self.current_screen == "story_intro" and event.key == pygame.K_SPACE:
                        self.current_screen = "game"

                # Handle button clicks
                if self.current_screen in ["main_menu", "settings", "play_menu", "story_chapters"]:
                    for button in self.active_buttons:
                        action = button.handle_event(event)
                        if action:
                            self.handle_action(action)

            # Update
            if self.current_screen == "credits":
                self.credits_offset -= 1
                if self.credits_offset < -len(self.credits_text) * 40:  # Reset scroll when it's off-screen
                    self.credits_offset = HEIGHT

            # Draw
            screen.fill(WHITE)

            if self.current_screen == "main_menu":
                self.draw_main_menu()
            elif self.current_screen == "play_menu":
                self.draw_play_menu()
            elif self.current_screen == "story_chapters":
                self.draw_story_chapters()
            elif self.current_screen == "settings":
                self.draw_settings_menu()
            elif self.current_screen == "credits":
                self.draw_credits()
            elif self.current_screen == "game":
                self.draw_game()
            elif self.current_screen == "story_intro":
                self.draw_story_intro()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def draw_main_menu(self):
        # Draw title
        title_text = title_font.render("Game Title", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw buttons
        for i, button in enumerate(self.main_menu_buttons):
            # Highlight selected button for keyboard navigation
            if i == self.selected_button_index:
                pygame.draw.rect(screen, DARK_BLUE, button.rect, 4)
            button.draw(screen)

    def draw_play_menu(self):
        # Draw title
        title_text = title_font.render("Play Mode", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw buttons
        for i, button in enumerate(self.play_menu_buttons):
            # Highlight selected button for keyboard navigation
            if i == self.selected_button_index:
                pygame.draw.rect(screen, DARK_BLUE, button.rect, 4)
            button.draw(screen)

    def draw_story_chapters(self):
        # Draw title
        title_text = title_font.render("Story Mode", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw buttons
        for i, button in enumerate(self.story_chapters_buttons):
            # Highlight selected button for keyboard navigation
            if i == self.selected_button_index:
                pygame.draw.rect(screen, DARK_BLUE, button.rect, 4)
            button.draw(screen)

    def draw_settings_menu(self):
        # Update button text based on settings
        self.settings_buttons[0].text = f"Sound: {'ON' if self.sound_on else 'OFF'}"
        self.settings_buttons[1].text = f"Music: {'ON' if self.music_on else 'OFF'}"
        self.settings_buttons[2].text = f"Difficulty: {self.difficulty}"

        # Draw title
        title_text = title_font.render("Settings", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw buttons
        for i, button in enumerate(self.settings_buttons):
            # Highlight selected button for keyboard navigation
            if i == self.selected_button_index:
                pygame.draw.rect(screen, DARK_BLUE, button.rect, 4)
            button.draw(screen)

    def draw_story_intro(self):
        # Draw story text for selected chapter
        if self.story_chapter in self.story_text:
            text_lines = self.story_text[self.story_chapter]

            # Draw a semi-transparent background
            bg_surface = pygame.Surface((WIDTH, HEIGHT))
            bg_surface.set_alpha(200)
            bg_surface.fill(BLACK)
            screen.blit(bg_surface, (0, 0))

            # Draw story text
            for i, line in enumerate(text_lines):
                if i == 0:  # Title line
                    text = menu_font.render(line, True, WHITE)
                else:
                    text = small_font.render(line, True, WHITE)

                text_rect = text.get_rect(center=(WIDTH // 2, 100 + i * 30))
                screen.blit(text, text_rect)

            # Draw prompt
            prompt_text = small_font.render("Press SPACE to continue or ESC to return to menu", True, WHITE)
            prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(prompt_text, prompt_rect)

    def draw_credits(self):
        # Draw scrolling credits
        for i, line in enumerate(self.credits_text):
            if i == 0:
                text = title_font.render(line, True, BLACK)
            else:
                text = small_font.render(line, True, BLACK)

            text_rect = text.get_rect(center=(WIDTH // 2, self.credits_offset + i * 40))
            screen.blit(text, text_rect)

        # Draw back instruction
        back_text = small_font.render("Press ESC to return to Main Menu", True, BLACK)
        back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(back_text, back_rect)

    def draw_game(self):
        # This is just a placeholder for the game screen
        mode_text = ""
        if self.game_mode == "single_player":
            mode_text = "Single Player Mode"
        elif self.game_mode == "two_player":
            mode_text = "Two Player Mode"
        elif self.game_mode == "story_mode":
            mode_text = f"Story Mode - {self.story_chapter.replace('_', ' ').title()}"

        game_text = title_font.render("Game Running", True, BLACK)
        mode_display = menu_font.render(mode_text, True, BLACK)
        instructions = small_font.render("Press ESC to return to Main Menu", True, BLACK)

        game_rect = game_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        mode_rect = mode_display.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))

        screen.blit(game_text, game_rect)
        screen.blit(mode_display, mode_rect)
        screen.blit(instructions, instructions_rect)

    def handle_action(self, action):
        if action == "play_menu":
            self.current_screen = "play_menu"
            self.active_buttons = self.play_menu_buttons
            self.selected_button_index = 0
        elif action == "single_player":
            self.game_mode = "single_player"
            self.current_screen = "game"
        elif action == "two_player":
            self.game_mode = "two_player"
            self.current_screen = "game"
        elif action == "story_mode":
            self.current_screen = "story_chapters"
            self.active_buttons = self.story_chapters_buttons
            self.selected_button_index = 0
        elif action == "chapter_1" or action == "chapter_2" or action == "chapter_3":
            self.game_mode = "story_mode"
            self.story_chapter = action
            self.current_screen = "story_intro"
        elif action == "settings":
            self.current_screen = "settings"
            self.active_buttons = self.settings_buttons
            self.selected_button_index = 0
        elif action == "credits":
            self.current_screen = "credits"
            self.credits_offset = HEIGHT
        elif action == "main_menu":
            self.current_screen = "main_menu"
            self.active_buttons = self.main_menu_buttons
            self.selected_button_index = 0
        elif action == "quit":
            self.running = False
        elif action == "toggle_sound":
            self.sound_on = not self.sound_on
        elif action == "toggle_music":
            self.music_on = not self.music_on
        elif action == "toggle_difficulty":
            difficulties = ["Easy", "Normal", "Hard"]
            current_index = difficulties.index(self.difficulty)
            self.difficulty = difficulties[(current_index + 1) % len(difficulties)]


# Function to integrate with your game
def run_menu():
    menu = Menu()
    menu.run()
    # When menu.run() ends, the user has either:
    # 1. Closed the game entirely (self.running = False)
    # 2. Selected a game mode (game_mode set accordingly)

    # You can return settings to your main game
    return {
        "running": menu.running,
        "sound_on": menu.sound_on,
        "music_on": menu.music_on,
        "difficulty": menu.difficulty,
        "game_mode": menu.game_mode,
        "story_chapter": menu.story_chapter
    }


# Example of how to use this menu:
if __name__ == "__main__":
    game_settings = run_menu()
    print("Game settings:", game_settings)

    # If the user selected a game mode, you would start your game here
    if game_settings["running"]:
        print("Starting game with settings:")
        print(f"Sound: {'ON' if game_settings['sound_on'] else 'OFF'}")
        print(f"Music: {'ON' if game_settings['music_on'] else 'OFF'}")
        print(f"Difficulty: {game_settings['difficulty']}")
        print(f"Game Mode: {game_settings['game_mode']}")

        if game_settings["game_mode"] == "story_mode":
            print(f"Story Chapter: {game_settings['story_chapter']}")

        # Here you would call your game's main function
        # main_game(game_settings)