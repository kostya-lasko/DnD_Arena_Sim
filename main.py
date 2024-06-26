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

#character creation class
class Character:
    def __init__ (self, name, char_class):
        self.name = name
        self.char_class = char_class.lower()
        self.health, self.damage, self.range, self.magic_chance, self.armor, self.rage, self.attacks_number = self.set_stats()
   #sets stats based on the character class 
    def set_stats(self):
        if self.char_class == "warrior":
            return (int((random.randint(2,6) + random.randint(2,6)) * 2 + 15), 3, 0, 0, 1, 0, 1)
        elif self.char_class == "ranger":
            return (int((random.randint(2,6) + random.randint(2,6)) * 1.2 + 15), 1, 6, random.randint(1,20)/100 + 0.02, 0, 0, 1)
        elif self.char_class == "mage":
            return (int((random.randint(2,6) + random.randint(2,6)) * 0.8 + 15), 0, 3, random.randint(1,20)/100 + 0.8, 0, 0, 1)
        #elif self.char_class == "barb":
        #    return (int((random.randint(2,6) + random.randint(2,6)) * 2.6 + 15), 4, 0, 0, 0, 1, 1)
        elif self.char_class == "monk":
            return (int((random.randint(2,6) + random.randint(2,6)) * 1.5 + 15), 1, 0, 0, 0, 0, 3)
        
    def display_stats(self):
        print(f"{Colors.OKCYAN}Name: {self.name}")
        print(f"Class: {self.char_class}")
        print(f"HP: {self.health}")
        print(f"Attack Bonus: {self.damage}")
        print(f"Attack range: {self.range}")
        print(f"Magic Chance: {self.magic_chance}{Colors.ENDC}")

#magic burst
def magic_burst(character):
    if random.random() <= character.magic_chance:
        magic_type = random.choice(["damage", "healing"])
        value = random.randint(1, 4)+1
        return magic_type, value
    return None, 0

#combat round
def combat_round(attacker, defender, distance):
    damage = random.randint(1,3) + attacker.damage
    armor = defender.armor
   #ranged attacks
    if distance > 0:
        if attacker.range > distance:
            print(f"{attacker.name} attacks at range dealing {Colors.WARNING}{damage-armor} damage.{Colors.ENDC}")
            defender.health = defender.health - (damage - armor)
            if armor > 0:
                print (f"{defender.name}'s armor blocked some incoming damage!")
    
    #melee attacks
    else:
        print(f"{attacker.name} strikes in melee dealing {Colors.WARNING}{damage-armor} damage.{Colors.ENDC}")
        defender.health = defender.health - (damage - armor)
        if armor > 0:
                print (f"{defender.name}'s armor blocked some incoming damage!")
        if attacker.attacks_number > 1:
            damage = random.randint(1,3) + attacker.damage  
            damage2 = random.randint(1,3) + attacker.damage  
            print(f"Fast as a lightning, {attacker.char_class} attacks {attacker.attacks_number-1} more times! They deal {Colors.WARNING}{damage-armor}{Colors.ENDC} damage and then {Colors.WARNING}{damage2-armor}{Colors.ENDC} more damage!")
            if armor > 0:
                print (f"{defender.name}'s armor blocked some incoming damage!")
            defender.health = defender.health - (damage - armor)
            defender.health = defender.health - (damage2 - armor)
    
   #magic burst calling
    magic_type, magic_value = magic_burst(attacker)
    if magic_type == "damage" and attacker.health > 0:
        print(f"{Colors.OKCYAN}{attacker.name} unleashes their magic {magic_value} damage!{Colors.ENDC}")
        defender.health -= magic_value
    elif magic_type == "healing" and attacker.health > 0:
        print(f"{Colors.OKCYAN}{attacker.name} is surrounded by healing energies, restoring {Colors.OKGREEN}{magic_value}{Colors.ENDC} health!{Colors.ENDC}")
        attacker.health += magic_value

#combat subroutine
def combat(char1, char2):
    print("The fight begins! Characters start at the opposite corners of the arena.")
    distance = 5
    round_num = 0
    if char1.range == 0 and char2.range == 0:
      distance -= 1
    #Removing everything related to Barbarian
    #def check_revival(character):
     #   if character.health <= 0 and character.rage > 0:
     #       print(f"Wait! {character.name}'s inner rage allows them to stand back!")
     #       character.health = 1
      #      character.rage -= 1
       #     return True
        #return False

    while char1.health > 0 and char2.health > 0:
      round_num += 1
      print(f"\n{Colors.BOLD}Round {round_num}{Colors.ENDC}")

      #I want both combatants to attack simultenously, not one by one. 
      combat_round(char1, char2, distance)
      combat_round(char2, char1, distance)
      
      if distance > 0:
          print("Fighters are getting closer to each other")
          distance -= 1

      print(f"{char1.name} has {Colors.OKGREEN}{char1.health}{Colors.ENDC} health left")
      print(f"{char2.name} has {Colors.OKGREEN}{char2.health}{Colors.ENDC} health left")
      
      if char1.health <= 0 and char2.health <= 0:
          print(f"{Colors.FAIL}Both combatants fall. It's a draw!{Colors.ENDC}")
      elif char1.health <= 0:
          print(f"{Colors.FAIL}{char1.name} falls. {char2.name} is victorious with {Colors.OKGREEN}{char2.health}{Colors.ENDC} health remaining!{Colors.ENDC}")
          
      elif char2.health <= 0:
          print(f"{Colors.FAIL}{char2.name} falls. {char1.name} is victorious with {Colors.OKGREEN}{char1.health}{Colors.ENDC} health remaining!{Colors.ENDC}")

      time.sleep(2)
   

#main program
def create_character(player_number):
    print(f"Player {player_number}, create your character!")
    name = input("Name your character: ")
    char_class = input("Select your character class (warrior, mage, ranger, barb, monk): ").lower().strip()
    return Character(name, char_class)

def main():
    char1 = create_character(1)
    print("\nCharacter 1 stats:")
    char1.display_stats()
    time.sleep(2)

    char2 = create_character(2)
    print("\nCharacter 2 stats:")
    char2.display_stats()
    time.sleep(2)

    #input("\nPress Enter to start the combat...")
    #clear()
    combat(char1, char2)

if __name__ == "__main__":
    main()