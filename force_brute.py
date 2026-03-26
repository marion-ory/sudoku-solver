
def verifier_tout(grille):
    # Vérification des Lignes
    for ligne in grille:
        # On vérifie qu'il y a 9 chiffres uniques et aucune case vide
        if len(set(ligne)) != 9 or ' ' in ligne:
            return False

    # Vérification des Colonnes
    for c in range(9):
        colonne = [grille[r][c] for r in range(9)]
        if len(set(colonne)) != 9 or ' ' in colonne:
            return False

    # Vérification des Blocs 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            bloc = []
            for r in range(i, i + 3):
                for c in range(j, j + 3):
                    bloc.append(grille[r][c])
            if len(set(bloc)) != 9 or ' ' in bloc:
                return False
                
    return True # La grille est pleine ET valide

def find_empty(grille):
    # Cherche la première position vide (' ')
    for r in range(9):
        for c in range(9):
            if grille[r][c] == ' ':
                return (r, c)
    return None

def resoudre_force_brute(grille):
    case = find_empty(grille)

    # S'il ne reste plus de case vide, on lance la grande vérification finale
    if case is None:
        return verifier_tout(grille)

    ligne, col = case
    
    # Test toutes les possibilités de 1 à 9
    for num in range(1, 10):
        grille[ligne][col] = num

        # Appel récursif
        if resoudre_force_brute(grille):
            return True

        # Backtrack : on remet un espace si ça mène à une impasse
        grille[ligne][col] = ' '
        
    return False