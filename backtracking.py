# backtracking.py

def est_valide(grille, ligne, col, num):
    # Vérifier la ligne
    for j in range(9):
        if grille[ligne][j] == num:
            return False
            
    # Vérifier la colonne
    for i in range(9):
        if grille[i][col] == num:
            return False
            
    # Vérifier le carré 3x3
    debut_ligne, debut_col = 3 * (ligne // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grille[debut_ligne + i][debut_col + j] == num:
                return False
    return True

def resoudre_sudoku(grille):
    for ligne in range(9):
        for col in range(9):
            # On cherche une case vide (compatible avec 0 ou ' ' de notre GUI)
            if grille[ligne][col] in [0, ' ']:  
                for num in range(1, 10):
                    if est_valide(grille, ligne, col, num):
                        grille[ligne][col] = num # Action
                        
                        if resoudre_sudoku(grille): # Récursion
                            return True
                        
                        # Backtrack (Annulation) - On remet un espace pour la compatibilité GUI
                        grille[ligne][col] = ' ' 
                return False # Aucun chiffre ne marche, on déclenche le backtrack parent
    return True # Toutes les cases sont remplies