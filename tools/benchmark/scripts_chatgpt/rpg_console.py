import random
import sys

class Personnage:
    def __init__(self, nom, classe, pv, attaque, defense):
        self.nom = nom
        self.classe = classe
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.inventaire = []

    def est_vivant(self):
        return self.pv > 0

    def subir_degats(self, degats):
        self.pv -= max(0, degats - self.defense)
        if self.pv < 0:
            self.pv = 0

    def attaquer(self, cible):
        degats = random.randint(1, self.attaque)
        cible.subir_degats(degats)
        return degats

    def ajouter_objet(self, objet):
        self.inventaire.append(objet)

    def afficher_inventaire(self):
        if not self.inventaire:
            print("Inventaire vide.")
        else:
            print("Inventaire :")
            for i, obj in enumerate(self.inventaire, 1):
                print(f"{i}. {obj.nom}")

class Objet:
    def __init__(self, nom, effet):
        self.nom = nom
        self.effet = effet

    def utiliser(self, personnage):
        if self.effet == "soin":
            soin = random.randint(10, 20)
            personnage.pv += soin
            print(f"{personnage.nom} récupère {soin} PV.")
        elif self.effet == "attaque+":
            boost = random.randint(1, 3)
            personnage.attaque += boost
            print(f"{personnage.nom} gagne +{boost} attaque.")
        elif self.effet == "defense+":
            boost = random.randint(1, 3)
            personnage.defense += boost
            print(f"{personnage.nom} gagne +{boost} défense.")

class Ennemi(Personnage):
    def __init__(self, nom, pv, attaque, defense):
        super().__init__(nom, "Ennemi", pv, attaque, defense)

def creer_personnage():
    print("Choisissez une classe :")
    print("1. Guerrier (PV élevés, attaque moyenne, défense élevée)")
    print("2. Mage (PV moyens, forte attaque, faible défense)")
    print("3. Voleur (PV faibles, attaque correcte, défense moyenne)")
    choix = input("> ")

    if choix == "1":
        return Personnage("Héros", "Guerrier", 100, 10, 8)
    elif choix == "2":
        return Personnage("Héros", "Mage", 70, 15, 4)
    elif choix == "3":
        return Personnage("Héros", "Voleur", 60, 12, 6)
    else:
        return Personnage("Héros", "Aventurier", 80, 8, 5)

def generer_ennemi():
    ennemis = [
        Ennemi("Gobelin", 40, 6, 2),
        Ennemi("Orc", 60, 8, 4),
        Ennemi("Troll", 80, 10, 6),
        Ennemi("Squelette", 50, 7, 3)
    ]
    return random.choice(ennemis)

def generer_objet():
    objets = [
        Objet("Potion de soin", "soin"),
        Objet("Pierre de force", "attaque+"),
        Objet("Bouclier magique", "defense+")
    ]
    return random.choice(objets)

def combat(joueur, ennemi):
    print(f"Un {ennemi.nom} apparaît !")
    while joueur.est_vivant() and ennemi.est_vivant():
        print(f"\n{joueur.nom} ({joueur.classe}) - PV: {joueur.pv}")
        print(f"{ennemi.nom} - PV: {ennemi.pv}")
        print("Actions :")
        print("1. Attaquer")
        print("2. Utiliser objet")
        print("3. Fuir")
        action = input("> ")

        if action == "1":
            degats = joueur.attaquer(ennemi)
            print(f"Vous infligez {degats} dégâts à {ennemi.nom}.")
        elif action == "2":
            joueur.afficher_inventaire()
            choix = input("Choisissez un objet (numéro) ou Entrée pour annuler : ")
            if choix.isdigit():
                idx = int(choix) - 1
                if 0 <= idx < len(joueur.inventaire):
                    objet = joueur.inventaire.pop(idx)
                    objet.utiliser(joueur)
        elif action == "3":
            if random.random() < 0.5:
                print("Vous réussissez à fuir.")
                return
            else:
                print("Échec de la fuite.")

        if ennemi.est_vivant():
            degats = ennemi.attaquer(joueur)
            print(f"{ennemi.nom} vous inflige {degats} dégâts.")

    if joueur.est_vivant():
        print(f"Vous avez vaincu {ennemi.nom} !")
        if random.random() < 0.5:
            objet = generer_objet()
            joueur.ajouter_objet(objet)
            print(f"Vous trouvez un objet : {objet.nom}.")
    else:
        print("Vous êtes mort...")

def boucle_principale():
    joueur = creer_personnage()
    print(f"Bienvenue, {joueur.nom} le {joueur.classe} !")

    while joueur.est_vivant():
        print("\nMenu principal :")
        print("1. Explorer")
        print("2. Inventaire")
        print("3. Statut")
        print("4. Quitter")
        choix = input("> ")

        if choix == "1":
            if random.random() < 0.7:
                ennemi = generer_ennemi()
                combat(joueur, ennemi)
            else:
                print("Vous explorez sans incident.")
        elif choix == "2":
            joueur.afficher_inventaire()
        elif choix == "3":
            print(f"{joueur.nom} ({joueur.classe}) - PV: {joueur.pv}, Attaque: {joueur.attaque}, Défense: {joueur.defense}")
        elif choix == "4":
            print("Fin du jeu.")
            sys.exit(0)

    print("Partie terminée.")

if __name__ == "__main__":
    boucle_principale()
