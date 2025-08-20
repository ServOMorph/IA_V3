class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.inventory = {}

    def take_damage(self, damage):
        damage -= self.defense
        if damage > 0:
            self.health -= damage

class Enemy(Character):
    pass

class Player(Character):
    def attack_enemy(self, enemy):
        enemy.take_damage(self.attack)

    def add_item(self, item):
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1

def main():
    player = Player("Hero", 100, 10, 5)
    enemy = Enemy("Ogre", 50, 5, 3)

    while True:
        print("\nPlayer stats:")
        print(f"Name: {player.name}, Health: {player.health}, Attack: {player.attack}, Defense: {player.defense}")
        print("Inventory:")
        for item, count in player.inventory.items():
            print(f"{item}: {count}")

        print("\nEnemy stats:")
        print(f"Name: {enemy.name}, Health: {enemy.health}, Attack: {enemy.attack}, Defense: {enemy.defense}")

        action = input("\nChoose an action (a - attack, i - inventory): ")
        if action == 'a':
            player.attack_enemy(enemy)
            enemy.attack_enemy(player)

            if enemy.health <= 0:
                print("You defeated the enemy!")
                item = "Sword"  # Temporary, should be random
                player.add_item(item)
                print(f"You gained a {item} from the battle.")
        elif action == 'i':
            print("Your inventory:")
            for item, count in player.inventory.items():
                print(f"{item}: {count}")

if __name__ == "__main__":
    main()