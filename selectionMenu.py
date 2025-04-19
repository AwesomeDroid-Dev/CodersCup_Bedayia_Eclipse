import pygame
import pygame_menu
import sys

# Initialize pygame
pygame.init()
pygame.display.set_caption('Gadget Selection Menu')
screen_width, screen_height = 800, 600
surface = pygame.display.set_mode((screen_width, screen_height))

# Game variables
num_players = 1  # Default to 1 player
players_data = [
    {
        'name': 'Player 1',
        'head': None,
        'armor': None,
        'hands': None,
        'feet': None
    },
    {
        'name': 'Player 2',
        'head': None,
        'armor': None,
        'hands': None,
        'feet': None
    }
]

# Available gadgets for each slot
gadgets = {
    'head': ['Targeting Visor', 'Night Vision', 'Sonic Scanner', 'Thermal Goggles', 'Mind Shield'],
    'armor': ['Energy Shield', 'Stealth Field', 'Shock Absorber', 'Health Regenerator', 'Reflector Plating'],
    'hands': ['Grappling Hook', 'Plasma Cannon', 'Freeze Ray', 'Force Gloves', 'Hacking Device'],
    'feet': ['Rocket Boots', 'Speed Enhancers', 'Jump Boosters', 'Gravity Clamps', 'Silent Steps']
}

# Color scheme
THEME_BLUE = (25, 75, 150)
THEME_LIGHT_BLUE = (50, 120, 220)

# Custom theme
my_theme = pygame_menu.Theme(
    background_color=THEME_BLUE,
    title_background_color=THEME_LIGHT_BLUE,
    title_font_shadow=True,
    widget_padding=15,
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
    widget_font_size=20
)

def create_player_menu(player_index):
    """Create a menu for a specific player to choose gadgets"""
    player = players_data[player_index]
    
    menu = pygame_menu.Menu(
        f"{player['name']} Gadget Selection",
        screen_width,
        screen_height,
        theme=my_theme
    )
    
    # Add selectors for each gadget type
    menu.add.selector(
        'Head Gadget: ',
        [(item, item) for item in gadgets['head']],
        onchange=lambda _, item: set_gadget(player_index, 'head', item)
    )
    
    menu.add.selector(
        'Armor Gadget: ',
        [(item, item) for item in gadgets['armor']],
        onchange=lambda _, item: set_gadget(player_index, 'armor', item)
    )
    
    menu.add.selector(
        'Hand Gadget: ',
        [(item, item) for item in gadgets['hands']],
        onchange=lambda _, item: set_gadget(player_index, 'hands', item)
    )
    
    menu.add.selector(
        'Feet Gadget: ',
        [(item, item) for item in gadgets['feet']],
        onchange=lambda _, item: set_gadget(player_index, 'feet', item)
    )
    
    # Add buttons for navigation
    menu.add.button('Confirm Selection', lambda: confirm_player_selection(player_index))
    menu.add.button('Back', pygame_menu.events.BACK)
    
    return menu

def set_gadget(player_index, slot, gadget):
    """Set a gadget for a specific player and slot"""
    players_data[player_index][slot] = gadget

def confirm_player_selection(player_index):
    """Confirm gadget selection for a player"""
    player = players_data[player_index]
    
    # Check if all gadgets are selected
    for slot in ['head', 'armor', 'hands', 'feet']:
        if player[slot] is None:
            return  # Not all gadgets selected
    
    # If it's the first player and we have 2 players, go to second player's menu
    if player_index == 0 and num_players == 2:
        player_2_menu.mainloop(surface)
    else:
        # All players have selected, start the game
        start_game()

def set_players(value, num):
    """Set the number of players"""
    global num_players
    num_players = num

def start_game():
    """Start the game with selected gadgets"""
    # Clear the screen
    surface.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    
    # Display the selected gadgets for each player
    y_pos = 50
    for i in range(num_players):
        player = players_data[i]
        text = font.render(f"{player['name']} Loadout:", True, (255, 255, 255))
        surface.blit(text, (100, y_pos))
        y_pos += 40
        
        for slot in ['head', 'armor', 'hands', 'feet']:
            text = font.render(f"{slot.capitalize()}: {player[slot]}", True, (200, 200, 200))
            surface.blit(text, (120, y_pos))
            y_pos += 30
        
        y_pos += 20
    
    # Add a "Back to Main Menu" button
    back_button = pygame.Rect(300, y_pos + 20, 200, 50)
    pygame.draw.rect(surface, THEME_LIGHT_BLUE, back_button)
    text = font.render("Back to Menu", True, (255, 255, 255))
    surface.blit(text, (325, y_pos + 35))
    
    pygame.display.flip()
    
    # Wait for user to click back or quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    waiting = False
                    main_menu.mainloop(surface)

# Create menus
main_menu = pygame_menu.Menu(
    'Gadget Selection',
    screen_width,
    screen_height,
    theme=my_theme
)

# Add selector for number of players
main_menu.add.selector(
    'Number of Players: ',
    [('1 Player', 1), ('2 Players', 2)],
    onchange=set_players
)

player_1_menu = create_player_menu(0)
player_2_menu = create_player_menu(1)

# Add buttons to main menu
main_menu.add.button('Start Selection', player_1_menu)
main_menu.add.button('Quit', pygame_menu.events.EXIT)

# Main game loop
if __name__ == '__main__':
    main_menu.mainloop(surface)