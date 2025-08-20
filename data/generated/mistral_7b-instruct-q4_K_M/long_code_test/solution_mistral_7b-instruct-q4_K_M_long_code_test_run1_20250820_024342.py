import random

class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        
    def take_damage(self, damage):
        self.health -= damage
        
    def is_alive(self):
        return self.health > 0
    
class Enemy:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        
    def take_damage(self, damage):
        self.health -= damage
        
    def is_alive(self):
        return self.health > 0

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

def display_menu():
    print("Welcome to the adventure!")
    print("Please choose an option:")
    print("1 - Create a character")
    print("2 - Load a character")
    print("3 - Start game")
    print("4 - Quit")
    
def create_character(name, health, attack, defense):
    char = Character(name, health, attack, defense)
    return char

def load_character(filename):
    with open(filename, 'r') as file:
        data = file.read()
        name, health, attack, defense = map(str.strip, data.split(','))
        char = Character(name, int(health), int(attack), int(defense))
        return char

def start_game(player, enemy):
    while player.is_alive() and enemy.is_alive():
        player_attack = random.randint(1, player.attack)
        enemy_attack = random.randint(1, enemy.attack)
        player_health -= enemy_attack
        enemy_health -= player_attack
        
def main():
    while True:
        display_menu()
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            name = input("Enter the character's name: ")
            health = int(input("Enter the character's health: "))
            attack = int(input("Enter the character's attack: "))
            defense = int(input("Enter the character's defense: "))
            player = create_character(name, health, attack, defense)
            save_character(player.name, f"{player.name}.txt")
            
        elif choice == 2:
            filename = input("Enter the character's name to load: ")
            char = load_character(filename)
            if char is not None:
                player = char
                
        elif choice == 3:
            name = input("Enter the enemy's name: ")
            health = int(input("Enter the enemy's health: "))
            attack = int(input("Enter the enemy's attack: "))
            defense = int(input("Enter the enemy's defense: "))
            enemy = Enemy(name, health, attack, defense)
            player = Character("Player", 100, 20, 10)
            start_game(player, enemy)
            
        elif choice == 4:
            print("Thanks for playing!")
            break
        
        else:
            print("Invalid choice. Please try again.")

def save_character(name, data):
    with open(name, 'w') as file:
        file.write(data)

if __name__ == "__main__":
    main()