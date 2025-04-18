import pygame_menu

def create_main_menu(screen):
    width, height = screen.get_size()
    menu = pygame_menu.Menu(
        height=height,
        width=width,
        theme=pygame_menu.themes.Theme(
            background_color=(0, 0, 0),  # Black background
            title=False,  # Disable title to remove blue bar
            title_background_color=(0, 0, 0),  # Just in case
        ),
        title=''  # Make sure title is empty
    )

    menu.add.button('Start Game', lambda: print("Start"))
    menu.add.button('Quit', pygame_menu.events.EXIT)

    return menu
