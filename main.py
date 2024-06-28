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

#a class for different intros
class Introductions:
    def __init__ (self, player_name, player_class):
        self.player_class = player_class
        self.player_name = player_name
    def greet(self):
        greetings = {
            "Fighter": f"Welcome, {self.player_name} the armored {self.player_class}! May your skills bring you victory.",
            "Mage": f"Greetings, {self.player_name} the wise {self.player_class}! May your knowledge bring you enlightenment.",
            "Rogue": f"Hello, {self.player_name} the sneaky {self.player_class}! May your cunning bring you success.",
            "Barbarian": f"Hey, {self.player_name} the smashing {self.player_class}! May your power destroy your foes.",
            "Ranger": f"Good day, {self.player_name} the swift {self.player_class}! May your aim be true.",
            "Monk": f"Blessings, {self.player_name} the stoic {self.player_class}! May your calm mind aid you in this fight."
            }
        return greetings.get(self.player_class)

#character creation main class
class Character:
    def __init__ (self, name, char_class, health_mod):
        self.name = name
        self.char_name = char_class
        self.health = int((random.randint(10,20)) * health_mod + 15)
        self.damage_bonus = 1
        self.attacks_number = 1
        self.range = 0
        self.magic_chance = 0
        self.armor = 0
        self.rage = 0
        self.crit_chance = random.randint(5,15)
        self.crit_mode = 2
    
    #default damage for an attack
    def standard_damage(self):
        standard_damage = random.randint(1,6) + self.damage_bonus
        is_crit = False
        if random.random() <= self.crit_chance/100:
            is_crit = True
        return (standard_damage, is_crit)

    # Magic burst
    def magic_burst(self):
        if random.random() < self.magic_chance/100:
            magic_type = random.choice(["damage", "healing"])
            value, placeholder = self.standard_damage() 
            #value -= self.damage_bonus
            return magic_type, value
        return None, 0
    

    #ATTACK LOGIC
    #first we trigger magic bursts
    def attack_enemy(self, enemy, distance):
        magic_type, value = self.magic_burst()
        if magic_type == "damage":
            enemy.health -= value
            print(f"{self.name} bursts with etherial energy, dealing {Colors.OKCYAN}{value} magic damage{Colors.ENDC}!")
        elif magic_type == "healing":
            self.health += value
            print(f"{self.name} is surrounded with magic and is healed for {Colors.OKGREEN}{value}{Colors.ENDC} health!")
        #then we attack at range
        if distance > 0 and self.range >= distance:
            damage, is_crit = self.standard_damage()
            if is_crit:
                damage = max(0, damage*self.crit_mode - enemy.armor)
                print(f"{self.name} hits {enemy.name}'s weak spot from the distance, {Colors.FAIL}critting{Colors.ENDC} for {Colors.WARNING}{damage}{Colors.ENDC} damage!")
            else:
                damage = max(0, damage - enemy.armor)
                print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage from a far!")
            enemy.health -= damage
        elif distance > 0 and self.range < distance:
            print(f"{self.name} is too far to attack {enemy.name}. They rush forward, eager for a fight!")
        
        #and then attack in melee
        elif distance == 0:
            damage, is_crit = self.standard_damage()
            if is_crit:
                damage = max(0, damage*self.crit_mode - enemy.armor)
                print(f"{self.name} {Colors.FAIL}crits{Colors.ENDC} {enemy.name}! They deal an astonoshing {Colors.WARNING}{damage}{Colors.ENDC} damage!")
            else:
                damage = max(0, damage - enemy.armor)
                print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage with a mighty strike!")
            enemy.health -= damage
        print(f"{enemy.name} has {Colors.OKGREEN}{enemy.health}{Colors.ENDC} health left.")
    
    #function to print character stats
    def print_stats(self):
        print(f"""{self.name}'s stats are:
{Colors.OKGREEN}Health: {self.health}{Colors.ENDC}
Attack bonus: {self.damage_bonus}
Range: {self.range}
Armor: {self.armor}
Magic chance: {Colors.OKCYAN}{self.magic_chance}%{Colors.ENDC}
Crit chance: {Colors.FAIL}{self.crit_chance}%{Colors.ENDC}
""")    
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
            self.health = random.randint(5,18)
            print (f"{Colors.FAIL}{self.name} is too angry to die!{Colors.ENDC} They stand back up with {Colors.OKGREEN}{self.health}{Colors.ENDC} health.")
            self.rage -=1
        return self.health > 0

class Fighter(Character):
    def __init__ (self, name):
        super().__init__ (name, "Fighter", health_mod = 2.4)
        self.armor = 2
        self.damage_bonus = 3

class Mage(Character):
    def __init__ (self, name):
        super().__init__(name, "Mage",health_mod = 0.7)
        self.range = 2
        self.magic_chance = random.randint(49,69)+30

class Monk(Character):
    def __init__ (self, name):
        super().__init__(name, "Monk",health_mod = 2)
        self.attacks_number = 3
        self.damage_bonus = 0
        
    def attack_enemy(self, enemy, distance):
        if distance > 0 and self.range < distance:
            print(f"{self.name} is too far to attack {enemy.name}. They approach closer.")
        elif distance == 0:
            current_attacks = 1
            while current_attacks <= self.attacks_number:
                damage, is_crit = self.standard_damage()
                if is_crit:
                    damage = max(0, damage*self.crit_mode - enemy.armor)
                    print(f"{self.name} hits {enemy.name}'s weak spot with extreme precision and {Colors.FAIL}crits{Colors.ENDC} for {Colors.WARNING}{damage}{Colors.ENDC} damage!")
                else:
                    damage = max(0, damage - enemy.armor)
                    print(f"{self.name} attacks {enemy.name} {self.attacks_number} times with lightning fast strikes for {Colors.WARNING}{damage}{Colors.ENDC} damage!")
                enemy.health -= damage
                current_attacks += 1
        print(f"{enemy.name} has {Colors.OKGREEN}{enemy.health}{Colors.ENDC} health left.")
class Ranger(Character):
    def __init__ (self, name):
        super().__init__ (name, "Ranger",health_mod = 1.5)
        self.damage_bonus = 2
        self.range = 5
        #self.magic_chance = random.randint(0,10)+2

class Rogue(Character):
    def __init__(self, name):
        super().__init__ (name, "Rogue", health_mod = 1.8)
        self.damage_bonus = 1
        self.crit_chance = 0.60
        self.crit_mode = 4
    
    """#redefining attack_enemy to include the crit chance
    def attack_enemy(self, enemy, distance):
        #we attack at range
        if distance > 0 and self.range >= distance:
            damage = max(0, self.standard_damage - enemy.armor)
            enemy.health -= damage
            print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage from a far!")
        elif distance > 0 and self.range < distance:
            print(f"{self.name} is too far to attack {enemy.name}.")
        #and then attack in melee with a crit chance
        elif distance == 0:
            if random.random() <= self.crit_chance:
                damage = max(0, self.standard_damage() * self.crit_mod - enemy.armor)
                print(f"{self.name} {Colors.FAIL}crits{Colors.ENDC} with their attack! They deal {Colors.WARNING}{damage}{Colors.ENDC} damage!")
                enemy.health -= damage
            else:
                damage = max(0, self.standard_damage() - enemy.armor)
                print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage with a mighty strike!")
                enemy.health -= damage"""

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
   #print("Choose your class:")
    print(f"1. Fighter")
    print(f"2. Monk")
    print(f"3. Mage")
    print(f"4. Ranger")
    print(f"5. Barbarian")
    print(f"6. Rogue")
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
   # print(f"""Their stats are:
#Health: {Colors.OKGREEN}{player1.health}{Colors.ENDC}
#Attack bonus: {player1.damage_bonus}
#Range: {player1.range}
#Armor: {player1.armor}
#Magic chance: {Colors.OKCYAN}{player1.magic_chance}%{Colors.ENDC}
#Crit chance: {Colors.FAIL}{player1.crit_chance}%{Colors.ENDC}
#""")

    player2_name = input("Player 2, choose your character name: ")
    print("Player 2, choose your character class: ")
    player2, player2_class = choose_class(player2_name)
    introduction = Introductions(player2_name, player2_class)
    print (introduction.greet())
    player2.print_stats()
   # print(f"""Their stats are:
#Health: {Colors.OKGREEN}{player2.health}{Colors.ENDC}
#Attack bonus: {player2.damage_bonus}
#Range: {player2.range}
#Armor: {player2.armor}
#Magic chance: {Colors.OKCYAN}{player2.magic_chance}%{Colors.ENDC}
#Crit chance: {Colors.FAIL}{player2.crit_chance}%{Colors.ENDC}
#""")
    time.sleep(3)
   
    print(f"{Colors.WARNING}Let the fight begin!{Colors.ENDC}")
    print()
    time.sleep(2)
    distance = 4
    round = 1
    while player1.is_alive() and player2.is_alive():
        print()
        print (f"{Colors.OKCYAN}Current round: {round}{Colors.ENDC}")
       
        player1.attack_enemy(player2, distance)
        print()
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
        print()
        time.sleep(2)

if __name__ == "__main__":
    main()
