import random
 
SIZE = 9
SPACE = 50
 
# ─── Fonctions utilitaires de génération ─────────────────────────────────────
 
def check_neighboring_cells(row, number, x, delta_x1, delta_x2):
    return row[x + delta_x1] == number or row[x + delta_x2] == number
 
def number_in_row(matrix, number, y, x):
    checking_row = matrix[y]
    # Calcul dynamique des voisins selon la position dans le bloc 3x3
    delta_x1 = 0
    delta_x2 = 0
 
    # Détermine quelles colonnes voisines vérifier dans le bloc 3x3
    if x % 3 == 0:       # Colonne de gauche du bloc
        delta_x1, delta_x2 = 1, 2
    elif x % 3 == 1:     # Colonne du milieu du bloc
        delta_x1, delta_x2 = -1, 1
    else:                # Colonne de droite du bloc
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
def make_spaces(matrix, fixed):
    coords = generate_coordinates()
    random.shuffle(coords) # On mélange une seule fois pour l'efficacité
    for i in range(SPACE):
        y, x = coords[i]
        matrix[y][x] = ' ' # On remplace par un espace vide
        fixed[y][x] = False # La case devient modifiable pour le joueur
 
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
    return matrix
 
# ─── Initialisation du jeu ───────────────────────────────────────────────────
 
def init_game():
    solution = make_sudoku()
    fixed = [[True] * 9 for _ in range(9)]       # Toutes les cases sont fixes au départ
    puzzle = [row.copy() for row in solution]     # Copie indépendante de la solution
    make_spaces(puzzle, fixed)                    # On perce les trous dans puzzle et fixed
    player_grid = [row.copy() for row in puzzle]  # Copie sur laquelle le joueur joue
    return solution, fixed, puzzle, player_grid
 
# ─── Détection des erreurs ───────────────────────────────────────────────────
 
def has_error(grid, y, x):
    # On convertit en string pour comparer les saisies joueur (str) avec les chiffres fixes (int)
    valeur = str(grid[y][x])
 
    # Pas d'erreur si la case est vide
    if valeur == ' ' or valeur == '':
        return False
 
    # Vérification de la ligne
    for x2 in range(9):
        if x2 != x and str(grid[y][x2]) == valeur:
            return True
 
    # Vérification de la colonne
    for y2 in range(9):
        if y2 != y and str(grid[y2][x]) == valeur:
            return True
 
    # Vérification du bloc 3x3
    bloc_y = (y // 3) * 3  # Coin supérieur gauche du bloc
    bloc_x = (x // 3) * 3
    for dy in range(3):
        for dx in range(3):
            if (bloc_y + dy != y or bloc_x + dx != x):
                if str(grid[bloc_y + dy][bloc_x + dx]) == valeur:
                    return True
 
    return False
 
# ─── Condition de victoire ───────────────────────────────────────────────────
 
def is_victory(grid, solution):
    # La grille est gagnée si toutes les cases correspondent à la solution
    for y in range(9):
        for x in range(9):
            if str(grid[y][x]) != str(solution[y][x]):
                return False
    return True
 
# ─── Comptage des erreurs actives ────────────────────────────────────────────
 
def count_errors(grid):
    # Retourne le nombre total de cases en erreur
    total = 0
    for y in range(9):
        for x in range(9):
            if has_error(grid, y, x):
                total += 1
    return total