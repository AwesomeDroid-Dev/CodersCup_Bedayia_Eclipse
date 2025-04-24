import pygame
import json
import os
from Classes.Axe import Axe
from Classes.PeletLauncher import PelletLauncher
import sys

class Armory:
    def __init__(self, screen_width=1200, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Armory - Choose Your Equipment")
        
        # Load items data
        self.load_items()
        
        # Selected items
        self.selected_weapon = None
        self.selected_accessory = None
        
        # Load font
        try:
            self.title_font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 24)
            self.item_font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 16)
            self.desc_font = pygame.font.Font("./Resources/PressStart2P-Regular.ttf", 12)
        except:
            self.title_font = pygame.font.SysFont(None, 36)
            self.item_font = pygame.font.SysFont(None, 24)
            self.desc_font = pygame.font.SysFont(None, 18)
        
        # Item slots
        self.weapon_slots = []
        self.accessory_slots = []
        self.setup_slots()
        
        # Load background
        try:
            self.bg = pygame.image.load("Resources/bg_armory.png").convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (screen_width, screen_height))
        except:
            self.bg = None
        
        # Load item placeholder
        try:
            self.placeholder = pygame.image.load("Resources/item_placeholder.png").convert_alpha()
            self.placeholder = pygame.transform.scale(self.placeholder, (100, 100))
        except:
            self.placeholder = pygame.Surface((100, 100))
            self.placeholder.fill((50, 50, 50))
        
        # Try to load sound effects
        try:
            self.select_sound = pygame.mixer.Sound("./Resources/mouse.wav")
            self.confirm_sound = pygame.mixer.Sound("./Resources/confirm.wav")
        except:
            self.select_sound = None
            self.confirm_sound = None
        
        # Confirm button
        self.confirm_button = pygame.Rect(screen_width//2 - 100, screen_height - 80, 200, 50)
        self.confirm_hover = False

    def load_items(self):
        try:
            with open('items.json', 'r') as f:
                self.items_data = json.load(f)
            
            # Load weapon and accessory sprites
            for weapon in self.items_data['weapons']:
                try:
                    weapon['sprite_img'] = pygame.image.load(weapon['sprite']).convert_alpha()
                    weapon['sprite_img'] = pygame.transform.scale(weapon['sprite_img'], (100, 100))
                except:
                    weapon['sprite_img'] = None
            
            for accessory in self.items_data['accessories']:
                try:
                    accessory['sprite_img'] = pygame.image.load(accessory['sprite']).convert_alpha()
                    accessory['sprite_img'] = pygame.transform.scale(accessory['sprite_img'], (100, 100))
                except:
                    accessory['sprite_img'] = None
                    
        except Exception as e:
            print(f"Error loading items: {e}")
            self.items_data = {"weapons": [], "accessories": []}

    def setup_slots(self):
        # Set up weapon slots (top row)
        weapon_y = 150
        spacing = 150
        start_x = self.screen_width // 2 - (len(self.items_data['weapons']) * spacing // 2) + spacing // 2
        
        for i, weapon in enumerate(self.items_data['weapons']):
            slot_x = start_x + i * spacing
            self.weapon_slots.append({
                'rect': pygame.Rect(slot_x - 50, weapon_y - 50, 100, 100),
                'item': weapon,
                'selected': False
            })
        
        # Set up accessory slots (bottom row)
        accessory_y = 350
        start_x = self.screen_width // 2 - (len(self.items_data['accessories']) * spacing // 2) + spacing // 2
        
        for i, accessory in enumerate(self.items_data['accessories']):
            slot_x = start_x + i * spacing
            self.accessory_slots.append({
                'rect': pygame.Rect(slot_x - 50, accessory_y - 50, 100, 100),
                'item': accessory,
                'selected': False
            })

    def draw_item_slot(self, slot, highlighted=False):
        # Draw slot background
        border_color = (255, 215, 0) if highlighted else (128, 128, 128)
        border_width = 4 if highlighted else 2
        
        # Draw selection highlight if this item is selected
        if slot['selected']:
            select_rect = pygame.Rect(slot['rect'].x - 5, slot['rect'].y - 5,
                                    slot['rect'].width + 10, slot['rect'].height + 10)
            pygame.draw.rect(self.screen, (0, 255, 0), select_rect, 3, border_radius=8)
        
        # Draw slot border
        pygame.draw.rect(self.screen, border_color, slot['rect'], border_width, border_radius=5)
        
        # Draw item sprite if available, otherwise use placeholder
        if 'sprite_img' in slot['item'] and slot['item']['sprite_img']:
            self.screen.blit(slot['item']['sprite_img'], slot['rect'])
        else:
            self.screen.blit(self.placeholder, slot['rect'])

    def draw_item_details(self, item, x, y):
        # Draw item name
        name_text = self.item_font.render(item['name'], True, (255, 255, 255))
        self.screen.blit(name_text, (x, y))
        
        # Draw item description
        desc_text = self.desc_font.render(item['description'], True, (200, 200, 200))
        self.screen.blit(desc_text, (x, y + 30))
        
        # Draw item stats
        if 'damage' in item:  # Weapon stats
            damage_text = self.desc_font.render(f"Damage: {item['damage']}", True, (255, 100, 100))
            speed_text = self.desc_font.render(f"Speed: {item['speed']}", True, (100, 255, 100))
            range_text = self.desc_font.render(f"Range: {item['range']}", True, (100, 100, 255))
            
            self.screen.blit(damage_text, (x, y + 55))
            self.screen.blit(speed_text, (x, y + 75))
            self.screen.blit(range_text, (x, y + 95))
        
        elif 'effect' in item:  # Accessory stats
            effect_text = self.desc_font.render(f"Effect: {item['effect'].replace('_', ' ').title()}", True, (100, 255, 255))
            boost_text = self.desc_font.render(f"Boost: {item['boost']}", True, (255, 255, 100))
            
            self.screen.blit(effect_text, (x, y + 55))
            self.screen.blit(boost_text, (x, y + 75))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None, None  # User canceled selection
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check weapon slots
                    for slot in self.weapon_slots:
                        if slot['rect'].collidepoint(mouse_pos):
                            # Deselect all other weapon slots
                            for other_slot in self.weapon_slots:
                                other_slot['selected'] = False
                            
                            # Select this slot
                            slot['selected'] = True
                            self.selected_weapon = slot['item']
                            
                            if self.select_sound:
                                self.select_sound.play()
                    
                    # Check accessory slots
                    for slot in self.accessory_slots:
                        if slot['rect'].collidepoint(mouse_pos):
                            # Deselect all other accessory slots
                            for other_slot in self.accessory_slots:
                                other_slot['selected'] = False
                            
                            # Select this slot
                            slot['selected'] = True
                            self.selected_accessory = slot['item']
                            
                            if self.select_sound:
                                self.select_sound.play()
                    
                    # Check confirm button
                    if self.confirm_button.collidepoint(mouse_pos):
                        if self.selected_weapon and self.selected_accessory:
                            if self.confirm_sound:
                                self.confirm_sound.play()
                            return self.selected_weapon, self.selected_accessory
            
            # Check if mouse is hovering over confirm button
            self.confirm_hover = self.confirm_button.collidepoint(mouse_pos)
            
            # Draw screen
            self.draw()
            
            pygame.display.flip()
            clock.tick(60)
        
        return None, None  # Default return if loop exits

    def draw(self):
        # Draw background
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill((30, 30, 40))
        
        # Draw title
        title_text = self.title_font.render("ARMORY", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 50))
        
        # Draw section titles
        weapons_text = self.item_font.render("WEAPONS", True, (255, 200, 100))
        self.screen.blit(weapons_text, (self.screen_width // 2 - weapons_text.get_width() // 2, 100))
        
        accessories_text = self.item_font.render("ACCESSORIES", True, (100, 200, 255))
        self.screen.blit(accessories_text, (self.screen_width // 2 - accessories_text.get_width() // 2, 300))
        
        # Draw weapon slots
        hovered_item = None
        for slot in self.weapon_slots:
            is_hovered = slot['rect'].collidepoint(pygame.mouse.get_pos())
            self.draw_item_slot(slot, is_hovered)
            if is_hovered:
                hovered_item = slot['item']
        
        # Draw accessory slots
        for slot in self.accessory_slots:
            is_hovered = slot['rect'].collidepoint(pygame.mouse.get_pos())
            self.draw_item_slot(slot, is_hovered)
            if is_hovered:
                hovered_item = slot['item']
        
        # Draw item details if hovering
        if hovered_item:
            self.draw_item_details(hovered_item, 20, self.screen_height - 150)
        
        # Draw selected items summary
        summary_x = self.screen_width - 250
        summary_y = self.screen_height - 150
        
        pygame.draw.rect(self.screen, (50, 50, 60), (summary_x - 10, summary_y - 10, 240, 120), 0, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 120), (summary_x - 10, summary_y - 10, 240, 120), 2, border_radius=5)
        
        selected_text = self.item_font.render("SELECTED:", True, (255, 255, 255))
        self.screen.blit(selected_text, (summary_x, summary_y))
        
        weapon_text = self.desc_font.render(f"Weapon: {self.selected_weapon['name'] if self.selected_weapon else 'None'}", True, (255, 200, 100))
        self.screen.blit(weapon_text, (summary_x, summary_y + 30))
        
        accessory_text = self.desc_font.render(f"Accessory: {self.selected_accessory['name'] if self.selected_accessory else 'None'}", True, (100, 200, 255))
        self.screen.blit(accessory_text, (summary_x, summary_y + 60))
        
        # Draw confirm button
        button_color = (0, 200, 0) if self.confirm_hover else (0, 150, 0)
        disabled = not (self.selected_weapon and self.selected_accessory)
        
        if disabled:
            button_color = (100, 100, 100)
        
        pygame.draw.rect(self.screen, button_color, self.confirm_button, 0, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.confirm_button, 2, border_radius=10)
        
        confirm_text = self.item_font.render("CONFIRM", True, (255, 255, 255))
        self.screen.blit(confirm_text, (self.confirm_button.centerx - confirm_text.get_width() // 2, 
                                      self.confirm_button.centery - confirm_text.get_height() // 2))

def create_weapon_for_player(weapon_data, player):
    """Create a weapon instance based on weapon_data for the player"""
    if weapon_data['id'] == 'axe':
        return Axe(-10, -10, 50, 50, player)
    elif weapon_data['id'] == 'pellet_launcher':
        return PelletLauncher(player)
    # Add other weapon types as they're implemented
    else:
        # Default to axe if weapon type not recognized
        return Axe(-10, -10, 50, 50, player)

def apply_accessory_to_player(accessory_data, player):
    """Apply accessory effects to the player"""
    effect = accessory_data['effect']
    boost = accessory_data['boost']
    
    if effect == 'movement_speed':
        player.speed *= boost
    elif effect == 'damage_boost':
        player.damage_multiplier = boost
    elif effect == 'double_jump':
        player.has_double_jump = True
        player.jump_boost = boost
    elif effect == 'damage_reduction':
        player.damage_reduction = boost
    
    # Store the accessory data on the player
    player.accessory = accessory_data

def show_armory():
    """Show the armory and return selected items"""
    pygame.init()  # Ensure pygame is initialized
    armory = Armory()
    return armory.run()

if __name__ == "__main__":
    # Test the armory standalone
    pygame.init()
    weapon, accessory = show_armory()
    if weapon and accessory:
        print(f"Selected weapon: {weapon['name']}")
        print(f"Selected accessory: {accessory['name']}")
    else:
        print("Selection canceled")