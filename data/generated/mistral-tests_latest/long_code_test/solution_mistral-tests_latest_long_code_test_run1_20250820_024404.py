import random

class Character:
    def __init__(self, name, class_, health, attack, defense):
        self.name = name
        self.class_ = class_
        self.health = health
        self.attack = attack
        self.defense = defense

    def display(self):
        print("Name:", self.name)
        print("Class:", self.class_)
        print("Health:", self.health)
        print("Attack:", self.attack)
        print("Defense:", self.defense)

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def display(self):
        print("Name:", self.name)
        print("Description:", self.description)

class Enemy:
    def __init