#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Project 3 (lab) - GameCharacter 
'''
Build a Game Character Stats Tracker
In this lab, you'll build a game character stats tracker. The program will allow you to create a character with specific attributes, update those attributes, and retrieve the current stats of the character.

Objective: Fulfill the user stories below and get all the tests to pass to complete the lab.

User Stories:

Create a class named GameCharacter that represents a game character and manages character stats.

When instantiated, a new GameCharacter object should have the following attributes:

_name set to the string given at the moment of the instantiation.
_health set to 100.
_mana set to 50.
_level set to 1.
Create a name property for read-only access to the character's name.

For the health property:

Define a getter that returns the current health.
Define a setter that prevents health from being set below 0, and caps the health at 100.
For the mana property:

Define a getter that returns the current mana.
Define a setter that prevents mana from being set below 0, and caps the mana at 50.
Create a getter for level to return the character's current level.

Define a method named level_up that:

Increases the character's level by 1.
Resets health to 100 and mana to 50 using their corresponding property setters.
Prints a message in the form of <name> leveled up to <level>! (where <name> and <level> should be replaced by the character's name and new level, respectively).
Define a __str__ method that returns a formatted string including:

The character's name.
The character's level.
The character's current health.
The character's current mana.
For example, a character named Kratos, right after the instantiation, should be represented as the following:

Name: Kratos
Level: 1
Health: 100
Mana: 50
Usage example
hero = GameCharacter('Kratos') # Creates a new character named Kratos
print(hero)  # Displays the character's stats

hero.health -= 30  # Decreases health by 30
hero.mana -= 10    # Decreases mana by 10
print(hero)  # Displays the updated stats

hero.level_up()  # Levels up the character
print(hero)  # Displays the stats after leveling up
'''

class GameCharacter:
    def __init__(self, name):
        self._name = name
        self._health = 100
        self._mana = 50
        self._level = 1
    
    def __str__(self):
        return f"\nName: {self.name}\nLevel: {self.level}\nHealth: {self.health}\nMana: {self.mana}"
    
    @property
    def name(self):
        return self._name
    
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_health):
        new_health = max(0, min(new_health, 100))
        if new_health < self._health:
            print(f"Decreases health by {self._health - new_health}")
        elif new_health > self._health:
            print(f"Increases health by {new_health - self._health}")
        self._health = new_health
    
    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, new_mana):
        new_mana = max(0, min(new_mana, 50))
        if new_mana < self.mana:
            print(f"Decrease mana by {self.mana - new_mana}")
        elif new_mana > self.mana:
            print(f"Increse mana by {new_mana - self.mana}")
        self._mana = new_mana
    
    @property
    def level(self):
        return self._level

    def level_up(self):
        self._level += 1
        self.health = 100
        self.mana = 50
        print(f"{self.name} leveled up to {self.level}!")
    
#hero = GameCharacter('Kratos') # Creates a new character named Kratos

#hero.health -= 30  # Decreases health by 30 
#hero.mana -= 10    # Decreases mana by 10

#hero.level_up()  # Levels up the character
#print(hero)
