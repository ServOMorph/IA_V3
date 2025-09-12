def is_prime(n):
  """Fonction pour vérifier si un nombre est premier."""
  if n <= 1:
    return False
  for i in range(2, int(n**0.5) + 1):
    if n % i == 0:
      return False
  return True

# Exemple d'utilisation
number = 17
if is_prime(number):
  print(f"{number} est un nombre premier.")
else:
  print(f"{number} n'est pas un nombre premier.")
