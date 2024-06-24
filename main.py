import random
import time
import os

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

def clear():
  os.system('clear')
  
#this subroutine changes the character stats based on their class
def charStatsMod(charClass):
  charClass = charClass.lower()
  if charClass in ["warrior"]:
    healthMod = 2
    attackBonus = 3
    range = 0
    magicChance = 0
  elif charClass in ["mage"]:
    healthMod = 0.8
    attackBonus = 0
    range = 2
    magicChance = random.randint(1,20)/100 + 0.6
  elif charClass in ["ranger"]:
    healthMod = 1
    attackBonus = 1
    range = 4
    magicChance = random.randint(0,10)/100 + 0.02
  else:
    print (Colors.WARNING + "This is an unknown class." + Colors.ENDC)
    return None, None, None, None
  return (healthMod, attackBonus, range, magicChance)


# this subroutine handles how magic works
def magicBurst(characterMagicChance):
  magicHappened = random.randint(1,100)
  if magicHappened <= characterMagicChance*100:  
    # print ("This character explodes with magic!")
    magicType = random.randint(1,2)
    if magicType == 1:
      magicDamage = random.randint(1,3) + 1
      magicHealing = 0
    if magicType == 2:
      magicDamage = 0
      magicHealing = random.randint(1,3) + 1
    return (magicDamage, magicHealing)
  else:
    return 0, 0 


#this subroutine lets your create your character     
def characterGenerator():
 # while True:
    characterName = input ("Name your character: ")
    time.sleep(0.1)
    characterClass = input ("Select your character class: (warrior, mage, ranger) ")
    time.sleep(0.2)
    healthMod, attackBonus, range, magicChance = charStatsMod(characterClass)
    
    # setting character stats: health, str, range and magic chance
    characterHealth = int(((random.randint(2,6) + random.randint(2,6))*healthMod + 20))
    characterStr = int((random.randint(1,3) + attackBonus))
    characterRange = int(range)
    #characterAttackBonus = int(attackBonus)
    characterMagicChance = float(magicChance)
    print ("Generating awesome stats for this amazing character... ")
    time.sleep(1)
    print (Colors.OKCYAN + "Your character's name is", characterName)
    time.sleep(0.33)
    print ("Your character's class is", characterClass)
    time.sleep(0.33)
    print ("HP: " + str(characterHealth))
    time.sleep(0.33)
    print ("STR: " + str(characterStr))
    time.sleep(0.33)
    print ("Attack range: " + str(characterRange))
    time.sleep(0.33)
    print ("Magic Chance: " + str(characterMagicChance) + Colors.ENDC)
    time.sleep(0.33)
    return characterName, characterClass, characterHealth, characterStr, characterRange, characterMagicChance


# subroutine that handles the combat system
def combat (char1Name, char1Health, char1Str, char1Range, char1MagicChance, char2Name, char2Health, char2Str, char2Range, char2MagicChance):
  print ("The fight begins! Characters start at the opposite corners of the arena.")
  distance = 5
  round = 0
  while True:
    char1Dmg = random.randint(1,3) + char1Str
    char2Dmg = random.randint(1,3) + char2Str
    if distance > 0:
      print ("Fighters are getting closer to each other")
      distance = distance - 1
    #check for ranged attacks
      if char1Range > distance:
        print (char1Name + " attacks at range dealing " + str(char1Str) + " damage")
        char2Health = char2Health - char1Dmg
        time.sleep(0.5)
      if char2Range > distance:
        print (char2Name + " attacks at range dealing " + str(char2Str) + " damage")
        char1Health = char1Health - char2Dmg
        time.sleep(0.5)
    
    # check for magic bursts
    char1MagicDamage, char1MagicHealing = magicBurst(char1MagicChance)
    if char1MagicDamage > 0:
      print (Colors.OKCYAN + char1Name + " magic surge goes wild dealing " + str(char1MagicDamage) + " damage" + Colors.ENDC)
      char2Health = char2Health - char1MagicDamage
      time.sleep(1)
    if char1MagicHealing > 0:
      print (Colors.OKCYAN+ "Magic energies gather around " + char1Name + " healing them for " + str(char1MagicHealing) + " health" + Colors.ENDC)
      char1Health = char1Health + char1MagicHealing
    char2MagicDamage, char2MagicHealing = magicBurst(char2MagicChance)
    if char2MagicDamage > 0:
      print (Colors.OKCYAN + char2Name + " explodes with magic dealing " + str(char2MagicDamage) + " damage" + Colors.ENDC)
      char1Health = char1Health - char2MagicDamage
    if char2MagicHealing > 0:
      print (Colors.OKCYAN + "Magic swirls around " + char2Name + " healing them for " + str(char2MagicHealing) + " health" + Colors.ENDC)
      char2Health = char2Health + char2MagicHealing
      time.sleep(1)

    
    # melee combat
    if distance == 0:
      print (Colors.BOLD  + "Both combatants clash in melee!" + Colors.ENDC)
      print (char1Name + " attacks dealing " + str(char1Dmg) + " damage")
      char2Health = char2Health - char1Dmg
      time.sleep(0.5)
      print (char2Name + " hits back dealing " + str(char2Dmg) + " damage")
      char1Health = char1Health - char2Dmg
      #print (char1Name + " has " + Colors.OKGREEN + str(char1Health) + Colors.ENDC + " health remaining")
      #print (char2Name + " has " + Colors.OKGREEN + str(char2Health) + Colors.ENDC + " health remaining")
      #print ()

    
    #check if anyone died or if both are dead
    if char1Health <= 0 and char2Health <= 0:
      print (Colors.FAIL + "Both combatants fall on the ground. It's a draw!" + Colors.ENDC)
      break
    if char1Health <= 0:
      print (Colors.FAIL + char1Name + " falls on the ground" + Colors.ENDC)
      if char2Health > 0:
        print (char2Name + " stands victorious!")
        print (char2Name + " has " + Colors.OKGREEN + str(char2Health) + Colors.ENDC + " health remaining")
        break
    elif char2Health <= 0:
      print (Colors.FAIL + char2Name + " falls on the ground" + Colors.ENDC)
      
      if char1Health > 0:
        print (char1Name + " wins this fight!")
        print (char1Name + " has " + Colors.OKGREEN + str(char1Health) + Colors.ENDC + " health remaining")
        break    
    
    round += 1   
    print (char1Name + " has " + Colors.OKGREEN + str(char1Health) + Colors.ENDC + " health left")
    print (char2Name + " has " + Colors.OKGREEN + str(char2Health)  + Colors.ENDC +  " health left" + Colors.ENDC)
    print ("End of round", round)
    print ()  
    time.sleep(3)

#calling the character generator subroutine
print ("Player 1, you will now create your character!")
print ()
char1Name, char1Class, char1Health, char1Str, char1Range, char1MagicChance= characterGenerator()
print (char1Name + " is getting ready for the fight...")
print()
time.sleep(2)
# clear()

print ("Player 2, you will now create your character!")
print ()
char2Name, char2Class, char2Health, char2Str, char2Range, char2MagicChance = characterGenerator()
print (char2Name + " is gathering their strength...")
print()
time.sleep(2)
# clear()

#let them fight!
combat(char1Name, char1Health, char1Str, char1Range, char1MagicChance, char2Name, char2Health, char2Str, char2Range, char2MagicChance)
