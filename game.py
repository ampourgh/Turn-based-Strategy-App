import sys

from monster import Dragon, Goblin, Troll, Monster
from clear import clear_screen
from combat import Combat
import random


class Game:
  def setup(self):
    self.player = Character()
    self.monsters = [
      Goblin(),
      Troll(),
      Dragon()
    ]
    self.monster = self.get_next_monster()

  def get_next_monster(self):
    try:
      return self.monsters.pop(0)
    except IndexError:
      return None

  def monster_turn(self):
    clear_screen()
    if self.monster.attack():
      print("{} is attacking!".format(self.monster))

      if input("Dodge? Y/N ").lower() == 'y':
        if self.player.dodge():
          print("You dodged the attack!")
        else:
          print("You got hit anyway!")
          self.player.hit_points -= 1
      else:
        print("{} hit you for 1 point!".format(self.monster))
        self.player.hit_points -= 1
    else:
      print("{} isn't attacking this turn.".format(self.monster))

  def player_turn(self):
    player_choice = input("""\n[A]ttack | [R]est | [I]nventory
                           \n[Q]uit | Type in your choice: """).lower()
    if player_choice == 'a':
      print("You're attacking {}!".format(self.monster))

      if self.player.attack():
        if self.monster.dodge():
          print("{} dodged your attack!".format(self.monster))
        else:
          if self.player.leveled_up():
            self.monster.hit_points -= 2
          else:
            self.monster.hit_points -= 1

          print("You hit {} with your {}!".format(
              self.monster, self.player.weapon))
      else:
        print("You missed!")
    elif player_choice == 'r':
      self.player.rest()

    elif player_choice == 'i':
      self.player.inventory()

    elif player_choice == 'q':
      sys.exit()

    else:
      self.player_turn()

  def cleanup(self):
    if self.monster.hit_points <= 0:
      self.player.experience += self.monster.experience
      print("You killed {}!".format(self.monster))
      self.monster = self.get_next_monster()

      print("{} droped a {}!".format(self.monster, Monster.items[0]))
      self.player.items.append(Monster.items[random.randint(0, 4)])



  def __init__(self):
    self.setup()

    while self.player.hit_points and (self.monster or self.monsters):
      print('\n'+'='*20)
      print(self.player)
      self.monster_turn()
      print('-'*20)
      self.player_turn()
      self.cleanup()
      print('\n'+'='*20)

    if self.player.hit_points:
      print("You win!")
    elif self.monsters or self.monster:
      print("You lose!")
    sys.exit()

class Character(Combat, Game):
  attack_limit = 100
  experience = 0
  base_hit_points = 10

  def attack(self):
    roll = random.randint(1, self.attack_limit)
    if self.weapon == 'sword':
      roll += 1
    elif self.weapon == 'axe':
      roll += 2
    return roll > 4

  def get_weapon(self):

    weapon_choice = input("Weapon ([S]word, [A]xe, [B]ow): ").lower()

    if weapon_choice in 'sab':
      if weapon_choice == 's':
        return 'sword'
      elif weapon_choice == 'a':
        return 'axe'
      else:
        return 'bow'
    else:
      return self.get_weapon()

  def __init__(self, **kwargs):
    self.name = input("Name: ")
    self.weapon = self.get_weapon()
    self.hit_points = self.base_hit_points

    for key, value in kwargs.items():
      setattr(self, key, value)

  def __str__(self):
    return '{}, HP: {}, XP: {}'.format(self.name, self.hit_points, self.experience)

  def rest(self):
    if self.hit_points < self.base_hit_points:
      self.hit_points += 1

  def leveled_up(self):
    return self.experience >= 5

  items = ['potion', 'potion', 'bottle of dust']

  def inventory(self):

      self.show_inventory(self.items)

      player_choice = input("\nType in item number: ")

      if ((int(player_choice) - 1) < len(self.items)):
          if (self.items[(int(player_choice) - 1)] == 'potion'):
              self.rest()
              self.rest()
              print("You feel rejuvenated!")
              discard_choice = input("")
              emptyJug = input("\nDiscard the empty jug? [Y]es | [N]o | [O]ther Options ").lower()
              if emptyJug == 'y':
                  print("You drop the jug to the ground and it shatters to pieces.")
                  del self.items[(int(player_choice) - 1):(int(player_choice)):]
              elif emptyJug == 'o':
                  options = input("[T]hrow at Monster | [E]at jug | [W]ear as a hat").lower()
                  del self.items[(int(player_choice) - 1):(int(player_choice)):]
                  if options == 't':
                      print("You threw the jug at the monster, causing some damage.")
                  elif options == 'e':
                      print("You begin eating the jug, your health points drop.")
                  elif options == 'w':
                      print("The sorrounding monsters give you a puzzled stare.")
                  else:
                      print("You did nothing with the bottle.")
              else:
                  print("You tucked the jug back into your inventory.")
                  del self.items[(int(player_choice) - 1):(int(player_choice)):]
                  self.items.append('empty jug')

          else:
              print("The item you picked out did nothing and vanished!")
              del self.items[(int(player_choice) - 1):(int(player_choice)):]
      else:
          print("Your inventory does not go that deep, it seems...")

  def show_inventory(self, items):
    try:
      counter = 1
      print("\n")
      for i in items:
        print("[" + str(counter) + "] " + i)
        counter += 1
    except IndexError:
      return None


Game()
