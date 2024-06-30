import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DnD Combat Arena")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Character classes with base stats
classes = {
    "Warrior": {"HP": 100, "Attack": 10, "Defense": 5},
    "Mage": {"HP": 80, "Attack": 15, "Defense": 3},
    "Archer": {"HP": 90, "Attack": 12, "Defense": 4}
}

# Character class
class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.hp = classes[char_class]["HP"]
        self.attack = classes[char_class]["Attack"]
        self.defense = classes[char_class]["Defense"]

    def attack_target(self, target):
        damage = self.attack - target.defense
        if damage < 0:
            damage = 0
        target.hp -= damage
        return damage

# Get player input for names and classes
def get_player_info(player_num):
    name = input(f"Player {player_num}, enter your character's name: ")
    char_class = input(f"Player {player_num}, choose your class (Warrior, Mage, Archer): ")
    while char_class not in classes:
        print("Invalid class. Please choose again.")
        char_class = input(f"Player {player_num}, choose your class (Warrior, Mage, Archer): ")
    return name, char_class

# Game loop
def main():
    player1_name, player1_class = get_player_info(1)
    player2_name, player2_class = get_player_info(2)

    player1 = Character(player1_name, player1_class)
    player2 = Character(player2_name, player2_class)

    players = [player1, player2]
    current_player = 0

    clock = pygame.time.Clock()
    running = True
    combat_log = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Combat logic
        if player1.hp > 0 and player2.hp > 0:
            attacker = players[current_player]
            defender = players[1 - current_player]
            damage = attacker.attack_target(defender)
            combat_log.append(f"{attacker.name} attacks {defender.name} for {damage} damage.")
            current_player = 1 - current_player
        else:
            running = False

        # Drawing
        screen.fill(WHITE)

        # Display player stats
        p1_text = font.render(f"{player1.name} (HP: {player1.hp})", True, RED)
        p2_text = font.render(f"{player2.name} (HP: {player2.hp})", True, BLUE)
        screen.blit(p1_text, (50, 50))
        screen.blit(p2_text, (50, 100))

        # Display combat log
        y_offset = 150
        for log_entry in combat_log[-10:]:  # Display last 10 log entries
            log_text = font.render(log_entry, True, BLACK)
            screen.blit(log_text, (50, y_offset))
            y_offset += 30

        pygame.display.flip()
        clock.tick(1)  # 1 tick per second for easy reading of the combat log

    # Display result
    screen.fill(WHITE)
    if player1.hp > 0:
        result_text = font.render(f"{player1.name} wins!", True, RED)
    elif player2.hp > 0:
        result_text = font.render(f"{player2.name} wins!", True, BLUE)
    else:
        result_text = font.render("It's a draw!", True, BLACK)
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()

if __name__ == "__main__":
    main()