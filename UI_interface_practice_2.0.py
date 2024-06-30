import pygame
import sys
import random
import time

#version
current_version = 3.1

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(f"DnD Combat Arena {current_version}")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)

# Fonts
font_small = pygame.font.Font(None, 24)
font_medium = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 48)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, color, self.rect)
        draw_text(self.text, font_medium, BLACK, self.rect.x + 10, self.rect.y + 10)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.action()
        return None


# Game states
INTRO = 0
CHARACTER_SELECTION = 1
COMBAT = 2
GAME_OVER = 3


def create_character(player_num, char_class):
    if char_class == "Barbarian":
        return Barbarian(f"Player {player_num}")
    elif char_class == "Duelist":
        return Duelist(f"Player {player_num}")
    elif char_class == "Fighter":
        return Fighter(f"Player {player_num}")
    elif char_class == "Mage":
        return Mage(f"Player {player_num}")
    elif char_class == "Monk":
        return Monk(f"Player {player_num}")
    elif char_class == "Ranger":
        return Ranger(f"Player {player_num}")
    elif char_class == "Rogue":
        return Rogue(f"Player {player_num}")
    elif char_class == "Shadow Blade":
        return ShadowBlade(f"Player {player_num}")
   
    
class Introductions:
    def __init__(self, player_name, player_class):
        self.player_class = player_class
        self.player_name = player_name

    def greet(self):
        greetings = {
            "Fighter": f"Welcome, {self.player_name} the armored {self.player_class}! May your skills bring you victory.",
            "Mage": f"Greetings, {self.player_name} the wise {self.player_class}! May your knowledge bring you enlightenment.",
            "Rogue": f"Hello, {self.player_name} the sneaky {self.player_class}! May your cunning bring you success.",
            "Barbarian": f"Hey, {self.player_name} the smashing {self.player_class}! May your power destroy your foes.",
            "Ranger": f"Good day, {self.player_name} the swift {self.player_class}! May your aim be true.",
            "Monk": f"Blessings, {self.player_name} the stoic {self.player_class}! May your calm mind aid you in this fight.",
            "Shadow Blade": f"{self.player_name} slowly manifests from the shadows. May your thirst for revenge be cooled with enemy blood!",
            "Duelist": f"En garde, {self.player_name} the agile {self.player_class}! May your precision and skill be unmatched.",
        }
        return greetings.get(self.player_class)

class Character:
    def __init__(self, name, char_class, health_mod):
        self.armor = 0
        self.attacks_number = 1
        self.char_class = char_class
        self.crit_chance = random.randint(5, 15)
        self.crit_mod = 2
        self.damage_bonus = 1
        self.dodge_chance = random.randint(1, 5)
        self.health = int((random.randint(10, 20)) * health_mod + 15)
        self.magic_chance = 0
        self.name = name
        self.parry_chance = 0
        self.parry_damage_mod = 1
        self.rage = 0
        self.range = 0

    def dodge(self):
        return random.random() < self.dodge_chance / 100

    def parry(self):
        return random.random() < self.parry_chance / 100

    def current_damage(self):
        is_crit = False
        current_damage = random.randint(1, 6) + self.damage_bonus
        if random.random() <= self.crit_chance / 100:
            current_damage *= self.crit_mod
            is_crit = True
        return is_crit, current_damage
    
    def ranged_attack(self, enemy, distance):
        log = []
        is_crit, damage = self.current_damage()
        damage = max(0, damage - enemy.armor)
        if distance > 0 and self.range >= distance:
            if not enemy.dodge():
                if not is_crit:
                    log.append(f"{self.name} uses the distance and shoots {enemy.name} for {damage} damage from afar!")
                    enemy.health -= damage
                else:
                    log.append(f"{self.name} hits {enemy.name}'s weak spot from the distance, critting for {damage} damage!")
                    enemy.health -= damage
            else:
                log.append(f"{enemy.name} dodges the attack! They take no damage.")
        return log
    
    def melee_attack(self, enemy, distance):
        log = []
        is_crit, damage = self.current_damage()
        damage = max(0, damage - enemy.armor)
        if not enemy.parry(): #check if  enemy didn't parry
            if not enemy.dodge(): #check if enemy didn't dodge
                if not is_crit: #check if self  didn't crit
                    log.append(f"{self.name} attacks {enemy.name} for {damage} damage with a mighty strike!")
                    enemy.health -= damage
                else:
                    log.append(f"{self.name} crits {enemy.name}! They deal an astonishing {damage} damage!")
                    enemy.health -= damage
            else:
                log.append(f"{enemy.name} dodges the attack from {self.name}!")
        else: #parry sequence
            _, enemy_damage = enemy.current_damage()
            counter_damage = max(0, enemy_damage - self.armor) * enemy.parry_damage_mod
            self.health -= counter_damage
            log.append(f"{enemy.name} parries the attack from {self.name} and counter-attacks for {counter_damage} damage!")
        return log
    
    def full_attack(self, enemy, distance):
        log = []
        if distance > 0 and self.range >= distance:
            log.extend(self.ranged_attack(enemy, distance))
        elif distance > 0 and self.range < distance:
            log.append(f"{self.name} is too far away to attack {enemy.name}. {self.name} rushes forward!")
        else:
            log.extend(self.melee_attack(enemy, distance))
        log.append(f"{enemy.name} has {enemy.health} health left.")
        return log
           
    def magic_burst(self):
        if random.random() < self.magic_chance / 100:
            magic_type = random.choice(["damage", "healing"])
            _, value = self.current_damage()
            return magic_type, value
        return None, 0

    def is_alive(self):
        return self.health > 0

    def print_health(self):
        print(f"{self.name} has {Colors.OKGREEN}{self.health}{Colors.ENDC} health left.")
    
    #this is a single combat round
    def combat_round(self, enemy, distance):
        log = []
        magic_type, magic_value = self.magic_burst()
        if magic_type == "damage":
            enemy.health -= magic_value
            log.append(f"{self.name} bursts with ethereal energy, dealing {magic_value} magic damage!")
        elif magic_type == "healing":
            self.health += magic_value
            log.append(f"{self.name} is surrounded with magic and is healed for {magic_value} health! They have {self.health} health now.")
        attacks_number = self.attacks_number
        while attacks_number > 0:
            log.extend(self.full_attack(enemy, distance))
            attacks_number -= 1
        return log
    

    #function to print character stats
    def print_stats(self):
        print(f"""{self.name}'s stats are:
{Colors.OKGREEN}Health: {self.health}{Colors.ENDC}
Range: {self.range}
Attack bonus: {self.damage_bonus}
Crit chance: {Colors.FAIL}{self.crit_chance}%{Colors.ENDC}
Armor: {self.armor}
Dodge chance: {self.dodge_chance}%
Parry chance: {self.parry_chance}%
Magic chance: {Colors.OKCYAN}{self.magic_chance}%{Colors.ENDC}
""")    

#Creating separate subsclasses for each of the classes to make their abilities more unique
class Barbarian(Character): #refuses to die once per combat and gets some healing
    def __init__ (self, name):
        super().__init__ (name, "Barbarian", health_mod = 2.45)
        self.damage_bonus = 3
        self.rage = 1
    
    def is_alive(self):
        if self.rage > 0 and self.health <= 0:
            self.health = random.randint(5, 18)
            return [f"{self.name} is too angry to die! They stand back up with {self.health} health."]
        return self.health > 0

class Duelist(Character): #has a chance to parry and strike back 
    def __init__(self, name):
        super().__init__(name, "Duelist", health_mod = 1.8)
        self.damage_bonus = 1
        self.parry_chance = 25  # 33% chance to parry
            
class Fighter(Character):
    def __init__ (self, name):
        super().__init__ (name, "Fighter", health_mod = 2.05)
        self.armor = 2
        self.damage_bonus = 3

class Mage(Character):
    def __init__ (self, name):
        super().__init__(name, "Mage",health_mod = 0.85)
        self.range = 2
        self.magic_chance = random.randint(49,69)+30

class Monk(Character):
    def __init__ (self, name):
        super().__init__(name, "Monk",health_mod = 2)
        self.attacks_number = 3
        self.damage_bonus = 0

class Ranger(Character):
    def __init__ (self, name):
        super().__init__ (name, "Ranger",health_mod = 1.5)
        self.damage_bonus = 2
        self.range = 5

class Rogue(Character): #crits often and extra hard
    def __init__(self, name):
        super().__init__ (name, "Rogue", health_mod = 2)
        self.damage_bonus = 1
        self.crit_chance = random.randint(50, 70)
        self.crit_mod = 4
    
class ShadowBlade(Character): #has a high crit and extra high dodge chance
    def __init__(self, name):
        super().__init__(name, "Shadow Blade", health_mod = 2)
        self.damage_bonus = 2
        self.crit_chance = random.randint(20,30)
        self.dodge_chance = random.randint(35,45) 
 
#allowing players to choose their class
def choose_class(name):
    classes = {
        "1": Fighter,
        "2": Monk,
        "3": Mage,
        "4": Ranger,
        "5": Barbarian,
        "6": Rogue,
        "7": ShadowBlade,
        "8": Duelist
    }
    class_names = {
        "1": "Fighter",
        "2": "Monk",
        "3": "Mage",
        "4": "Ranger",
        "5": "Barbarian",
        "6": "Rogue",
        "7": "Shadow Blade",
        "8": "Duelist"
    }
   #print("Choose your class:")
    print("1. Fighter")
    print("2. Monk")
    print("3. Mage")
    print("4. Ranger")
    print("5. Barbarian")
    print("6. Rogue")
    print("7. Shadow Blade")
    print("8. Duelist")
    choice = input("Enter the number of your choice: ")
    return classes[choice](name), class_names[choice]

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_character(character, x, y):
    # Placeholder for character drawing
    pygame.draw.rect(screen, RED if isinstance(character, Barbarian) else BLUE, (x, y, 50, 100))
    draw_text(character.name, font_small, WHITE, x, y + 110)
    draw_text(f"HP: {character.health}", font_small, GREEN, x, y + 130)

def draw_combat_scene(player1, player2, distance, combat_log):
    screen.fill(BLACK)
    draw_character(player1, 100, 50)
    draw_character(player2, width - 150, 50)
    
    # Draw distance
    pygame.draw.line(screen, WHITE, (200, 130), (width - 200, 130), 2)
    draw_text(f"Distance: {distance}", font_small, WHITE, width // 2 - 50, 150)



def game_loop():
    game_state = INTRO
    player1 = None
    player2 = None
    current_player = 1
    round_num = 1
    distance = 4
    combat_log = []
    player_dead = False
    log_start_index = 0

    # Create buttons for character selection
    button_width, button_height = 200, 50
    button_x = (width - button_width) // 2
    buttons = [
        Button(button_x, 200, button_width, button_height, "Barbarian", GRAY, LIGHT_GRAY, lambda: create_character(current_player, "Barbarian")),
        Button(button_x, 260, button_width, button_height, "Duelist", GRAY, LIGHT_GRAY, lambda: create_character(current_player, "Duelist")),
        Button(button_x, 320, button_width, button_height, "Fighter", GRAY, LIGHT_GRAY, lambda: create_character(current_player, "Fighter")),
        Button(button_x, 380, button_width, button_height, "Mage", GRAY, LIGHT_GRAY, lambda: create_character(current_player, "Mage")),
        Button(button_x, 440, button_width, button_height, "Monk", GRAY, LIGHT_GRAY, lambda: create_character(current_player, "Monk")),
        Button(button_x, 500, button_width, button_height, "Ranger", GRAY, LIGHT_GRAY, lambda: create_character(current_player, "Ranger")),
        Button(button_x, 560, button_width, button_height, "Rogue", GRAY, LIGHT_GRAY, lambda: create_character(current_player, "Rogue")),
        Button(button_x, 620, button_width, button_height, "Shadow Blade", GRAY, LIGHT_GRAY, lambda: create_character(current_player, "Shadow Blade")),
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_state == INTRO and event.key == pygame.K_RETURN:
                    game_state = CHARACTER_SELECTION
                elif game_state == COMBAT and player_dead and event.key == pygame.K_RETURN:
                    game_state = GAME_OVER
                elif game_state == GAME_OVER and event.key == pygame.K_RETURN:
                        game_state = INTRO
                        player1 = None
                        player2 = None
                        current_player = 1
                        round_num = 1
                        distance = 4
                        combat_log = []
                        player_dead = False
                        log_start_index = 0  # Reset log start index

                # Scroll log with up/down arrow keys
                elif game_state == COMBAT and event.key == pygame.K_UP:
                    log_start_index = max(0, log_start_index - 1)
                elif game_state == COMBAT and event.key == pygame.K_DOWN:
                    log_start_index = min(len(combat_log) - 1, log_start_index + 1)

            if game_state == CHARACTER_SELECTION:
                for button in buttons:
                    character = button.handle_event(event)
                    if character:
                        if current_player == 1:
                            player1 = character
                            current_player = 2
                        else:
                            player2 = character
                            game_state = COMBAT

        screen.fill(BLACK)

        if game_state == INTRO:
            draw_text(f"DnD Combat Arena {current_version}", font_large, CYAN, width // 2 - 200, height // 2 - 50)
            draw_text("Press Enter to start", font_medium, WHITE, width // 2 - 100, height // 2 + 50)

        elif game_state == CHARACTER_SELECTION:
            draw_text(f"Player {current_player}, choose your character:", font_large, WHITE, width // 2 - 250, 100)
            for button in buttons:
                button.draw(screen)

        elif game_state == COMBAT:
            draw_combat_scene(player1, player2, distance, combat_log)

            if not player_dead:
                # Simulate combat rounds
                log1 = player1.combat_round(player2, distance)
                log2 = player2.combat_round(player1, distance)
                combat_log.append(f"Round {round_num}")
                combat_log.extend(log1)
                pygame.time.wait(300) 
                combat_log.extend(log2)
                pygame.time.wait(300)
                
                # Limit the combat log to the last 30 messages
                combat_log = combat_log[-40:]
                
                # Update distance
                if distance > 0:
                    if player1.range == 0 and player2.range == 0:
                        distance = max(0, distance - 2)
                    else:
                        distance = max(0, distance - 1)

                if not player1.is_alive() or not player2.is_alive():
                    player_dead = True

                round_num += 1

            # Draw combat log with scrolling
            log_x = 50 
            log_y_start = 210 
            log_display_limit = 20  # Number of log entries to display
            for i in range(log_display_limit):
                log_index = log_start_index + i
                if log_index < len(combat_log):
                    draw_text(combat_log[log_index], font_small, WHITE, log_x + 20, log_y_start + 20 + i * 20)

        elif game_state == GAME_OVER:
            winner = player1 if player1.is_alive() else player2
            draw_text(f"{winner.name} wins!", font_large, GREEN, width // 2 - 100, height // 2 - 50)
            draw_text("Press Enter to play again", font_medium, WHITE, width // 2 - 150, height // 2 + 50)

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # 60 FPS

if __name__ == "__main__":
    game_loop()