class Character:
    def __init__(self, name, health=100, attack=20, defense=10):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.inventory = []

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.health -= actual_damage
        return actual_damage

class Enemy(Character):
    pass

class Player(Character):
    def use_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"You used {item}.")
            return True
        else:
            print("You don'