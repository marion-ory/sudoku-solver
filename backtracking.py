import time  # <--- NE PAS OUBLIER L'IMPORT


def est_valide(grille, ligne, col, num):
    for j in range(9):
        if grille[ligne][j] == num:
            return False
    for i in range(9):
        if grille[i][col] == num:
            return False
    debut_ligne, debut_col = 3 * (ligne // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grille[debut_ligne + i][debut_col + j] == num:
                return False
    return True


def resoudre_sudoku(grille, app=None):
    for ligne in range(9):
        for col in range(9):
            if grille[ligne][col] in [0, " ", " "]:
                for num in range(1, 10):
                    if est_valide(grille, ligne, col, num):
                        grille[ligne][col] = num

                        # --- VISUALISATION (BIEN INDENTÉ ICI) ---
                        if app:
                            app.cells[(ligne, col)].configure(text_color="#4da6ff")
                            app.cells[(ligne, col)].delete(0, "end")
                            app.cells[(ligne, col)].insert(0, str(num))
                            app.update()
                            time.sleep(0.005)

                        # --- RÉCURSION (À L'INTÉRIEUR DU IF EST_VALIDE) ---
                        if resoudre_sudoku(grille, app):
                            return True

                        # Backtrack (Annulation)
                        grille[ligne][col] = " "

                        # --- NETTOYAGE ---
                        if app:
                            app.cells[(ligne, col)].delete(0, "end")
                            app.update()

                return False  # Retourne False si aucun des 9 chiffres ne marche
    return True
