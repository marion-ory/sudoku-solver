import time


def find_empty(grille):
    for r in range(9):
        for c in range(9):
            # Harmonisation avec les types de ton app (0 ou " ")
            if grille[r][c] in [0, " ", "", None]:
                return (r, c)
    return None


def est_valide_simple(grille, ligne, col, num):
    # On utilise la même logique que le backtracking pour que ce soit jouable
    for j in range(9):
        if grille[ligne][j] == num:
            return False
    for i in range(9):
        if grille[i][col] == num:
            return False
    debut_l, debut_c = 3 * (ligne // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grille[debut_l + i][debut_c + j] == num:
                return False
    return True


def resoudre_force_brute(grille, app=None):
    case = find_empty(grille)

    # Si plus de cases vides, on a fini
    if case is None:
        return True

    ligne, col = case
    for num in range(1, 10):
        # Pour que la force brute soit "visible", on pose le chiffre
        grille[ligne][col] = num

        # --- VISUALISATION MAC-COMPATIBLE ---
        if app:
            try:
                app.cells[(ligne, col)].delete(0, "end")
                app.cells[(ligne, col)].insert(0, str(num))
                app.cells[(ligne, col)].configure(
                    text_color="#e05c6a"
                )  # Rouge pour montrer que c'est "brut"
                app.update_idletasks()
                app.update()
                # On met une pause très courte, sinon c'est interminable
                time.sleep(0.001)
            except:
                return False

        # Si le chiffre est valide, on continue
        if est_valide_simple(grille, ligne, col, num):
            if resoudre_force_brute(grille, app):
                return True

        # --- BACKTRACK ---
        grille[ligne][col] = 0
        if app:
            try:
                app.cells[(ligne, col)].delete(0, "end")
                app.update_idletasks()
                app.update()
            except:
                pass

    return False
