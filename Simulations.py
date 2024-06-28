import random
import time
import pandas as pd

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
            "Monk": f"Blessings, {self.player_name} the stoic {self.player_class}! May your calm mind aid you in this fight.",
            "Shadow Blade": f"{self.player_name} slowly manifests from the shadow. May your thirst for revenge be cooled with enemy blood!"
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
        self.dodge_chance = random.randint(1,5)

    def dodge(self):
        return random.random() < self.dodge_chance/100
    
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
            if enemy.dodge():
                print(f"{enemy.name} dodges the attack from {self.name}!")
            else:
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
            if enemy.dodge():
                print(f"{enemy.name} dodges the attack from {self.name}!")
            else:
                if is_crit:
                    damage = max(0, damage*self.crit_mode - enemy.armor)
                    print(f"{self.name} {Colors.FAIL}crits{Colors.ENDC} {enemy.name}! They deal an astonoshing {Colors.WARNING}{damage}{Colors.ENDC} damage!")
                else:
                    damage = max(0, damage - enemy.armor)
                    print(f"{self.name} attacks {enemy.name} for {Colors.WARNING}{damage}{Colors.ENDC} damage with a mighty strike!")
                enemy.health -= damage
        print(f"{enemy.name} has {Colors.OKGREEN}{enemy.health}{Colors.ENDC} health left.")
    
    #is alive
    def is_alive(self):
        return self.health > 0

# Same class definitions as provided (Colors, Introductions, Character, Barbarian, Fighter, Mage, Monk, Ranger, Rogue, Shadow_Blade)
class Barbarian(Character):
    def __init__ (self, name):
        super().__init__ (name, "Barbarian", health_mod = 2.4)
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
        super().__init__ (name, "Fighter", health_mod = 2)
        self.armor = 2
        self.damage_bonus = 3

class Mage(Character):
    def __init__ (self, name):
        super().__init__(name, "Mage",health_mod = 0.8)
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
                if enemy.dodge():
                    print(f"{enemy.name} dodges the attack from {self.name}!")
                else:
                    if is_crit:
                        damage = max(0, damage*self.crit_mode - enemy.armor)
                        print(f"{self.name} hits {enemy.name}'s weak spot with extreme precision and {Colors.FAIL}crits{Colors.ENDC} for {Colors.WARNING}{damage}{Colors.ENDC} damage!")
                    else:
                        damage = max(0, damage - enemy.armor)
                        print(f"{self.name} attacks {enemy.name} with lightning fast strikes for {Colors.WARNING}{damage}{Colors.ENDC} damage!")
                    enemy.health -= damage
                current_attacks += 1
        print(f"{enemy.name} has {Colors.OKGREEN}{enemy.health}{Colors.ENDC} health left.")

class Ranger(Character):
    def __init__ (self, name):
        super().__init__ (name, "Ranger",health_mod = 2)
        self.damage_bonus = 2
        self.range = 5
        #self.magic_chance = random.randint(0,10)+2

class Rogue(Character):
    def __init__(self, name):
        super().__init__ (name, "Rogue", health_mod = 1.8)
        self.damage_bonus = 1
        self.crit_chance = random.randint(50, 70)
        self.crit_mode = 4
    
class Shadow_Blade(Character):
    def __init__(self, name):
        super().__init__(name, "Shadow Blade", health_mod = 2)
        self.damage_bonus = 2
        self.crit_chance = random.randint(20,30)
        self.dodge_chance = random.randint(35,40)  #high dodge chance

    def attack_enemy(self, enemy, distance):
        super().attack_enemy(enemy, distance)  
#allowing players to choose their class automatically
def choose_class_auto(name, class_id):
    classes = {
        "1": Fighter,
        "2": Monk,
        "3": Mage,
        "4": Ranger,
        "5": Barbarian,
        "6": Rogue,
        "7": Shadow_Blade
    }
    class_names = {
        "1": "Fighter",
        "2": "Monk",
        "3": "Mage",
        "4": "Ranger",
        "5": "Barbarian",
        "6": "Rogue",
        "7": "Shadow Blade"
    }
    return classes[class_id](name), class_names[class_id]

def simulate_battle(player1_class_id, player2_class_id):
    player1_name = "Player1"
    player2_name = "Player2"
    player1, player1_class = choose_class_auto(player1_name, player1_class_id)
    player2, player2_class = choose_class_auto(player2_name, player2_class_id)

    distance = 4
    round = 1
    while player1.is_alive() and player2.is_alive():
        player1.attack_enemy(player2, distance)
        player2.attack_enemy(player1, distance)
        
        if not player2.is_alive() and not player1.is_alive():
            return "Draw", player1_class, player2_class
        elif not player2.is_alive():
            return player1_class, player1_class, player2_class
        elif not player1.is_alive():
            return player2_class, player1_class, player2_class
        
        if distance > 0:
            if player1.range == 0 and player2.range == 0:
                distance = max(0, distance - 2)
            else:
                distance = max(0, distance - 1)
        round += 1

def collect_statistics(num_simulations):
    results = []
    class_ids = ["1", "2", "3", "4", "5", "6", "7"]

    for _ in range(num_simulations):
        for class_id1 in class_ids:
            for class_id2 in class_ids:
                if class_id1 != class_id2:
                    winner, player1_class, player2_class = simulate_battle(class_id1, class_id2)
                    results.append((winner, player1_class, player2_class))

    return results

def main():
    num_simulations = 1000  # Number of simulations to run
    results = collect_statistics(num_simulations)
    df = pd.DataFrame(results, columns=["Winner", "Player1_Class", "Player2_Class"])
    
    # Save the results to a CSV file
    df.to_csv("combat_simulation_results.csv", index=False)
    print(df.value_counts().reset_index(name="Count"))

if __name__ == "__main__":
    main()