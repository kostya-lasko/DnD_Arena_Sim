import random, os, time

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
        self.name = name
        self.char_class = char_class
        self.health = int((random.randint(10, 20)) * health_mod + 15)
        self.damage_bonus = 1
        self.attacks_number = 1
        self.range = 0
        self.magic_chance = 0
        self.armor = 0
        self.rage = 0
        self.crit_chance = random.randint(5, 15)
        self.crit_mod = 2
        self.dodge_chance = random.randint(1, 5)
        self.parry_chance = 0
        self.parry_damage_mod = 1

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
        is_crit, damage = self.current_damage()
        damage = max(0, damage - enemy.armor)
        #check if they can attack at range
        if distance > 0 and self.range >= distance:
            if not enemy.dodge(): #if the enemy didn't dodge
                if not is_crit: #if I didn't crit
                    print(f"{self.name} uses the distance and shoots {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage from afar!")
                    enemy.health -= damage
                else:
                    print(f"{self.name} hits {enemy.name}'s weak spot from the distance, {Colors.FAIL}critting{Colors.ENDC} for {Colors.WARNING}{damage}{Colors.ENDC} damage!")
                    enemy.health -= damage
            else:
                print(f"{enemy.name} dodges the attack! They take no damage.")
    
    def melee_attack(self, enemy, distance): #start the Melee Attack sequence
        is_crit, damage = self.current_damage()
        damage = max(0, damage - enemy.armor)
        if not enemy.parry(): #if enemy didn't parry
            if not enemy.dodge(): #if the enemy didn't dodge
                if not is_crit: #if I didn't crit
                    print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage with a mighty strike!") #do regular damage
                    enemy.health -= damage
                else:
                    print(f"{self.name} {Colors.FAIL}crits{Colors.ENDC} {enemy.name}! They deal an astonishing {Colors.WARNING}{damage}{Colors.ENDC} damage!")
                    enemy.health -= damage
            else: #enemy dodged
                print(f"{enemy.name} dodges the attack from {self.name}!")
        else: #enemy does a parry counterattack                 
                _, enemy_damage = enemy.current_damage()
                counter_damage = max(0, enemy_damage - self.armor)*enemy.parry_damage_mod
                self.health -= counter_damage
                print(f"{enemy.name} parries the attack from {self.name} and counter-attacks for {Colors.WARNING}{counter_damage}{Colors.ENDC} damage!")
        #in any case, we need to print enemy health

    
    def full_attack(self, enemy, distance):
        is_crit, damage = self.current_damage()
        damage = max(0, damage - enemy.armor)
        if distance > 0 and self.range >= distance:
            self.ranged_attack(enemy, distance)
        elif distance > 0 and self.range < distance:
            print(f"{self.name} is too far away to attack {enemy.name}. {self.name} rushes forward!")
        else:
            self.melee_attack(enemy, distance)

        enemy.print_health()
           
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
        magic_type, magic_value = self.magic_burst()
        if magic_type == "damage":
            enemy.health -= magic_value
            print(f"{self.name} bursts with ethereal energy, dealing {Colors.OKCYAN}{magic_value} magic damage{Colors.ENDC}!")
        elif magic_type == "healing":
            self.health += magic_value
            print(f"{self.name} is surrounded with magic and is healed for {Colors.OKGREEN}{magic_value}{Colors.ENDC} health! They have {Colors.OKGREEN}{self.health}{Colors.ENDC} health now.")
        attacks_number = self.attacks_number
        while attacks_number > 0:
            self.full_attack(enemy, distance)
            attacks_number -= 1
    

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
class Barbarian(Character):
    def __init__ (self, name):
        super().__init__ (name, "Barbarian", health_mod = 2.45)
        self.damage_bonus = 3
        self.rage = 1
    
    def is_alive(self):
        if self.rage > 0 and self.health <= 0:
            self.health = random.randint(5,18)
            print (f"{Colors.FAIL}{self.name} is too angry to die!{Colors.ENDC} They stand back up with {Colors.OKGREEN}{self.health}{Colors.ENDC} health.")
            self.rage -=1
        return self.health > 0

class Duelist(Character):
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
        #self.magic_chance = random.randint(0,10)+2

class Rogue(Character):
    def __init__(self, name):
        super().__init__ (name, "Rogue", health_mod = 2)
        self.damage_bonus = 1
        self.crit_chance = random.randint(50, 70)
        self.crit_mod = 4
    
class ShadowBlade(Character):
    def __init__(self, name):
        super().__init__(name, "Shadow Blade", health_mod = 2)
        self.damage_bonus = 2
        self.crit_chance = random.randint(20,30)
        self.dodge_chance = random.randint(35,45)  #high dodge chance
 

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

def main():
    os.system("clear")
    print(f"""{Colors.OKCYAN}Welcome to the DnD Combat Arena 2.0. 
It allows 2 players to select their characters and watch how they fight to the death on our arena!{Colors.ENDC}""")
    player1_name = input("Player 1, choose your character name: ")
    print("Player 1, choose your character class: ")
    player1, player1_class = choose_class(player1_name)
    #os.system("clear")
    introduction = Introductions(player1_name, player1_class)
    print (introduction.greet())
    player1.print_stats()

    player2_name = input("Player 2, choose your character name: ")
    print("Player 2, choose your character class: ")
    player2, player2_class = choose_class(player2_name)
    introduction = Introductions(player2_name, player2_class)
    print (introduction.greet())
    player2.print_stats()
    time.sleep(3)
   
    print(f"{Colors.WARNING}Let the fight begin!{Colors.ENDC}")
    print()
    time.sleep(2)
    round = 1
    distance = 4
        
    while player1.is_alive() and player2.is_alive():
        print()
        print (f"{Colors.OKCYAN}Current round: {round}{Colors.ENDC}")
        player1.combat_round(player2, distance)
        print()
        player2.combat_round(player1, distance)
        if not player2.is_alive():
            print()
            print(f"{Colors.FAIL}{player2.name} has been defeated!{Colors.ENDC} {player1.name} wins! They have only {Colors.OKGREEN}{player1.health}{Colors.ENDC} health left.")
            if not player1.is_alive():
                print(f"But wait a second! {player1.name}{Colors.FAIL} slowly falls to the ground too!{Colors.ENDC} IT IS A DRA-A-A-A-A-A-A-W!")
                break
            break

        if not player1.is_alive():
            print()
            print(f"{Colors.FAIL}{player1.name} has been defeated! {Colors.ENDC}{player2.name} is left standing with {Colors.OKGREEN}{player2.health}{Colors.ENDC} health!")
            if not player2.is_alive():
                print(f"But wait a second! {player2.name} slowly {Colors.FAIL}falls to the ground too{Colors.ENDC}! IT IS A DRA-A-A-A-A-A-A-W!")
                break
            break
        print()
        time.sleep(2)
        round +=1
        if distance > 0:
            if player1.range == 0 and player2.range == 0:
                distance = max (0, distance - 2)
            else:
                distance = max (0, distance - 1)

if __name__ == "__main__":
    main()
