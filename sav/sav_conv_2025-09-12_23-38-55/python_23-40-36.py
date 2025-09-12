def somme(a, b):
  """Calcule la somme de deux nombres."""
  return a + b

# Obtenir les nombres de l'utilisateur
nombre1 = float(input("Entrez le premier nombre: "))
nombre2 = float(input("Entrez le deuxième nombre: "))

# Calculer la somme
somme_nombres = somme(nombre1, nombre2)

# Afficher la somme
print("La somme de", nombre1, "et", nombre2, "est:", somme_nombres)
