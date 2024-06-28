import random, os, time

#adding a class for colours
class Colors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class Introductions(self, char_class):
    def __init__ (self, char_class, intro)
        self.char_class = char_class
        self.into = intro
        

#character creation class
class Character:
    def __init__ (self, name, char_class, health_mod):
        self.name = name
        self.char_name = char_class
        #self.char_class = char_class.lower()
        self.health = int((random.randint(3,6) + random.randint(3,6)) * health_mod + 15)
        self.damage_bonus = 0
        self.attacks_number = 1
        self.range = 0
        self.magic_chance = 0
        self.armor = 0
        self.rage = 0
        self.crit_chance = 0
    

    # Magic burst
    def magic_burst(self):
        if random.random() <= self.magic_chance/100:
            magic_type = random.choice(["damage", "healing"])
            value = random.randint(1,4)+1
            return magic_type, value
        return None, 0
    

    #ATTACK LOGIC
    #first we trigger magic bursts
    def attack_enemy(self, enemy, distance):
        magic_type, value = self.magic_burst()
        if magic_type == "damage":
            enemy.health -= value
            print(f"{self.name} bursts with magic, dealing {Colors.OKCYAN}{value}{Colors.ENDC} additional damage!")
        elif magic_type == "healing":
            self.health += value
            print(f"{self.name} is surrounded with magic and is healed for {Colors.OKGREEN}{value}{Colors.ENDC} health!")
        #then we attack at range
        if distance > 0 and self.range >= distance:
            damage = max(0, random.randint(1,4) + self.damage_bonus - enemy.armor)
            enemy.health -= damage
            print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage from a far!")
            
        elif distance > 0 and self.range < distance:
            print(f"{self.name} is too far to attack {enemy.name}. They rush forward, eager for a fight!")
        #and then attack in melee
        elif distance == 0:
            damage = max(0, random.randint(1,4) + self.damage_bonus - enemy.armor)
            enemy.health -= damage
            print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage with a mighty strike!")
            
    #is alive
    def is_alive(self):
        return self.health > 0
    
    
#Creating separate subsclasses for each of the classes to make their abilities more unique
class Barbarian(Character):
    def __init__ (self, name):
        super().__init__ (name, "Barbarian", health_mod = 2.8)
        self.damage_bonus = 3
        self.rage = 1
    
    def is_alive(self):
        if self.rage > 0 and self.health <= 0:
            self.health = random.randint(5,15)
            print (f"{Colors.FAIL}{self.name} is too angry to die!{Colors.ENDC} They stand back up with {Colors.OKGREEN}{self.health}{Colors.ENDC} health.")
            self.rage -=1
        return self.health > 0

class Fighter(Character):
    def __init__ (self, name):
        super().__init__ (name, "Fighter", health_mod = 2.5)
        self.armor = 2
        self.damage_bonus = 3

class Mage(Character):
    def __init__ (self, name):
        super().__init__(name, "Mage",health_mod = 1)
        self.damage_bonus = 1
        self.range = 2
        self.magic_chance = random.randint(49,69)+30

class Monk(Character):
    def __init__ (self, name):
        super().__init__(name, "Monk",health_mod = 2)
        self.attacks_number = 4
        self.damage_bonus = 0
        
    def attack_enemy(self, enemy, distance):
        if distance > 0 and self.range >= distance:
            damage = max(0, random.randint(1,4) + self.damage_bonus - enemy.armor)
            enemy.health -= damage
            print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage from a far!")
            #print(f"{enemy.name} has {Colors.OKGREEN}{enemy.health}{Colors.ENDC} health left.")
            print()
        elif distance > 0 and self.range < distance:
            print(f"{self.name} is too far to attack {enemy.name}. They approach closer.")
        elif distance == 0:
            current_attacks = 1
            while current_attacks <= self.attacks_number:
                damage = max(0, random.randint(1,4) + self.damage_bonus - enemy.armor)
                print(f"{self.name} attacks {enemy.name} {self.attacks_number} times with lightning strikes {Colors.WARNING}{damage}{Colors.ENDC} damage!")
                enemy.health -= damage
                current_attacks += 1
            #print(f"{enemy.name} has {Colors.OKGREEN}{enemy.health}{Colors.ENDC} health left.")

class Ranger(Character):
    def __init__ (self, name):
        super().__init__ (name, "Ranger",health_mod = 1.5)
        #self.attacks_number = 1
        #self.armor = 0
        self.damage_bonus = 2
        self.range = 5
        self.magic_chance = random.randint(0,10)+2

class Rogue(Character):
    def __init__(self, name):
        super().__init__ (name, "Rogue", health_mod = 1.8)
        self.damage_bonus = 1
        self.crit_chance = 0.35
        self.crit_mod = 4
    
    #redefining attack_enemy to include the crit chance back
    def attack_enemy(self, enemy, distance):
        #we attack at range
        if distance > 0 and self.range >= distance:
            damage = max(0, random.randint(1,4) + self.damage_bonus - enemy.armor)
            enemy.health -= damage
            print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage from a far!")
        elif distance > 0 and self.range < distance:
            print(f"{self.name} is too far to attack {enemy.name}.")
        #and then attack in melee with a crit chance
        elif distance == 0:
            if random.random() <= self.crit_chance:
                damage = max(0, (random.randint(2,4) + self.damage_bonus)*self.crit_mod - enemy.armor)
                print(f"{self.name} {Colors.FAIL}crits{Colors.ENDC} with their attack! They deal {Colors.WARNING}{damage}{Colors.ENDC} damage!")
                enemy.health -= damage
            else:
                damage = max(0, random.randint(1,4) + self.damage_bonus - enemy.armor)
                print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage with a mighty strike!")
                enemy.health -= damage

#allowing players to choose their class
def choose_class(name):
    classes = {
        "1": Fighter,
        "2": Monk,
        "3": Mage,
        "4": Ranger,
        "5": Barbarian,
        "6": Rogue
    }
    class_names = {
        "1": "Fighter",
        "2": "Monk",
        "3": "Mage",
        "4": "Ranger",
        "5": "Barbarian",
        "6": "Rogue"
    }
    print("Choose your class:")
    print("1. Fighter")
    print("2. Monk")
    print("3. Mage")
    print("4. Ranger")
    print("5. Barbarian")
    print("6. Rogue")
    choice = input("Enter the number of your choice: ")
    return classes[choice](name), class_names[choice]

def main():
    player1_name = input("Player 1, choose your character name: ")
    print("Player 1, choose your character class: ")
    player1, player1_class = choose_class(player1_name)
    print(f"Welcome, {player1.name}, the {player1_class}")
    print(f"""Their stats are:
{Colors.OKGREEN}Health: {player1.health}{Colors.ENDC}
Attack bonus: {player1.damage_bonus}
Range: {player1.range}
Armor: {player1.armor}
{Colors.OKCYAN}Magic chance: {player1.magic_chance}%{Colors.ENDC}
Crit chance: {player1.crit_chance}
""")

    player2_name = input("Player 2, choose your character name: ")
    print("Player 2, choose your character class: ")
    player2, player2_class = choose_class(player2_name)
    print(f"Welcome, {player2.name}, the {player2_class}")
    print(f"""Their stats are:
{Colors.OKGREEN}Health: {player2.health}{Colors.ENDC}
Attack bonus: {player2.damage_bonus}
Range: {player2.range}
Armor: {player2.armor}
{Colors.OKCYAN}Magic chance: {player2.magic_chance}%{Colors.ENDC}
Crit chance: {player2.crit_chance}
""")
    time.sleep(3)
   
    print(f"{Colors.WARNING}Let the fight begin!{Colors.ENDC}")
    print()
    time.sleep(2)
    distance = 4
    round = 1
    while player1.is_alive() and player2.is_alive():
        print()
        print (f"Current round: {round}")
       
        player1.attack_enemy(player2, distance)
        player2.attack_enemy(player1, distance)
        if not player2.is_alive():
            print(f"{Colors.FAIL}{player2.name} has been defeated!{Colors.ENDC} {player1.name} wins!")
            if not player1.is_alive():
                print(f"But wait a second! {player1.name} {Colors.FAIL} slowly falls to the ground too!{Colors.ENDC} It's a draw!")
                break
            print(f"{player1.name} has {Colors.OKGREEN}{player1.health}{Colors.ENDC} health left.")
            break

        if not player1.is_alive():
            print(f"{Colors.FAIL}{player1.name} has been defeated!{Colors.ENDC} {player2.name} wins!")
            if not player2.is_alive():
                print(f"But wait a second! {player2.name}{Colors.FAIL} slowly falls to the ground too!{Colors.ENDC} It's a draw!")
                break
            print(f"{player2.name} has {Colors.OKGREEN}{player2.health}{Colors.ENDC} health left.")
            break
        if distance > 0:
            if player1.range == 0 and player2.range == 0:
                distance = max (0, distance - 2)
            else:
                distance = max (0, distance - 1)
        round +=1
        print(f"{player1.name} has {Colors.OKGREEN}{player1.health}{Colors.ENDC} health left.")
        print(f"{player2.name} has {Colors.OKGREEN}{player2.health}{Colors.ENDC} health left.")
        time.sleep(2)

if __name__ == "__main__":
    main()