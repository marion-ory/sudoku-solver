import random

SIZE = 9
SPACE = 50

# Fonction pour afficher le sudoku de manière lisible
def show_result(matrix):
    print("\n--- Voici votre sudoku ---")
    for r_index, row in enumerate(matrix):
        string = ""
        for c_index, col in enumerate(row):
            # On affiche un point ou un espace si la case est vide pour la lisibilité
            display_val = col if col != ' ' else "."
            string += " {} ".format(display_val)
            
            # Ajout des barres verticales tous les 3 chiffres
            if (c_index + 1) % 3 == 0 and (c_index + 1) != SIZE:
                string += "|"
        print(string)
        
        # Ajout des barres horizontales toutes les 3 lignes
        if (r_index + 1) % 3 == 0 and (r_index + 1) != SIZE:
            print("-" * (SIZE * 3 + 2))

def check_neighboring_cells(row, number, x, delta_x1, delta_x2):
    return row[x + delta_x1] == number or row[x + delta_x2] == number

def number_in_row(matrix, number, y, x):
    checking_row = matrix[y]
    # Calcul dynamique des voisins selon la position dans le bloc 3x3
    delta_x1 = 0
    delta_x2 = 0

    # Détermine quelles colonnes voisines vérifier dans le bloc 3x3
    if x % 3 == 0: # Colonne de gauche du bloc
        delta_x1, delta_x2 = 1, 2
    elif x % 3 == 1: # Colonne du milieu du bloc
        delta_x1, delta_x2 = -1, 1
    else: # Colonne de droite du bloc
        delta_x1, delta_x2 = -1, -2

    return check_neighboring_cells(checking_row, number, x, delta_x1, delta_x2)

# Fonction pour la validation des chiffres (Ligne, Colonne, Bloc)
def is_number_valid(matrix, new_line, number):
    # 1. Vérification de la ligne actuelle
    if number in new_line:
        return False
    
    # 2. Vérification de la colonne (parmi les lignes déjà créées)
    current_col = len(new_line)
    for row in matrix:
        if row[current_col] == number:
            return False
            
    # 3. Vérification du bloc 3x3 (lignes du dessus dans le même bloc)
    # Si on est à la 2ème ligne du bloc (indice 1, 4, 7...)
    if len(matrix) % 3 == 1:
        return not number_in_row(matrix, number, -1, current_col)
    
    # Si on est à la 3ème ligne du bloc (indice 2, 5, 8...)
    if len(matrix) % 3 == 2:
        return not (number_in_row(matrix, number, -1, current_col) or 
                    number_in_row(matrix, number, -2, current_col))
    
    return True

def generate_coordinates():
    result = []
    for y in range(SIZE):
        for x in range(SIZE):
            result.append([y, x])
    return result

# Fonction pour créer les trous dans la grille
def make_spaces(matrix):
    coords = generate_coordinates()
    random.shuffle(coords) # On mélange une seule fois pour l'efficacité
    
    spaces_placed = 0
    for i in range(SPACE):
        y, x = coords[i]
        matrix[y][x] = ' ' # On remplace par un espace vide

# Fonction principale de création
def make_sudoku():
    matrix = []
    for i in range(SIZE):
        new_row = []
        numbers = list(range(1, SIZE + 1))
        
        while len(new_row) != SIZE:
            random.shuffle(numbers) # On mélange les chiffres possibles
            found = False
            
            for number in numbers:
                if is_number_valid(matrix, new_row, number):
                    new_row.append(number)
                    found = True
                    break
            
            # Si aucun chiffre n'est valide pour cette case, on reset la ligne
            if not found:
                new_row = []
        
        matrix.append(new_row)
    
    make_spaces(matrix)
    show_result(matrix)

make_sudoku()