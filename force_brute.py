import time


def find_empty(grille):  # On remplace self par grille
    for r in range(9):
        for c in range(9):
            if grille[r][c] == 0 or grille[r][c] == " ":
                return (r, c)
    return None


def verifier_tout(grille):
    # Vérification des Lignes
    for ligne in grille:
        if len(set(ligne)) != 9 or 0 in ligne or " " in ligne:
            return False

    # Vérification des Colonnes
    for c in range(9):
        colonne = [grille[r][c] for r in range(9)]
        if len(set(colonne)) != 9 or 0 in colonne or " " in colonne:
            return False

    # Vérification des Blocs 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            bloc = []
            for r in range(i, i + 3):
                for c in range(j, j + 3):
                    bloc.append(grille[r][c])
            if len(set(bloc)) != 9 or 0 in bloc or " " in bloc:
                return False
    return True


def resoudre_force_brute(
    grille, app=None
):  # C'est cette fonction que SudokuApp appelle
    case = find_empty(grille)

    # Check s'il reste une case vide
    if case is None:
        return verifier_tout(grille)

    ligne, col = case
    for num in range(1, 10):
        grille[ligne][col] = num

        # --- VISUALISATION ---
        if app:
            # On met à jour la cellule dans l'interface
            app.cells[(ligne, col)].delete(0, "end")
            app.cells[(ligne, col)].insert(0, str(num))
            app.update()  # Force l'affichage à se rafraîchir
            time.sleep(0.01)  # Petite pause pour l'œil humain
        # ---------------------

        # Appel récursif
        if resoudre_force_brute(grille, app):
            return True

        # Backtrack
        grille[ligne][col] = 0

        # --- NETTOYAGE VISUEL  l'algorithme efface un chiffre de l'interface graphique ---
        if app:
            app.cells[(ligne, col)].delete(0, "end")
            app.update()
        # ------------------------
    return False
