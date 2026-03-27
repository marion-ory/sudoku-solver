import time


class SudokuOptimise:
    def __init__(self, grille_gui, app=None):  # Ajout de app
        self.app = app
        self.grille = [[0] * 9 for _ in range(9)]
        self.rows = [set() for _ in range(9)]
        self.cols = [set() for _ in range(9)]
        self.boxes = [set() for _ in range(9)]

        for r in range(9):
            for c in range(9):
                val = grille_gui[r][c]
                if val != " " and val != 0:
                    self._placer(r, c, int(val), init=True)

    def _box(self, r, c):
        return (r // 3) * 3 + (c // 3)

    def _placer(self, r, c, val, init=False):
        self.rows[r].add(val)
        self.cols[c].add(val)
        self.boxes[self._box(r, c)].add(val)
        self.grille[r][c] = val

        # --- VISUALISATION ---
        if self.app and not init:
            self.app.cells[(r, c)].configure(
                text_color="#5cc98a"
            )  # Vert pour l'optimisé
            self.app.cells[(r, c)].delete(0, "end")
            self.app.cells[(r, c)].insert(0, str(val))
            self.app.update()
            time.sleep(0.01)  # On peut ajuster la vitesse ici

    def _retirer(self, r, c, val):
        self.rows[r].discard(val)
        self.cols[c].discard(val)
        self.boxes[self._box(r, c)].discard(val)
        self.grille[r][c] = 0

        # --- NETTOYAGE VISUEL ---
        if self.app:
            self.app.cells[(r, c)].delete(0, "end")
            self.app.update()

    def _candidats(self, r, c):
        utilises = self.rows[r] | self.cols[c] | self.boxes[self._box(r, c)]
        return set(range(1, 10)) - utilises

    def _mrv(self):
        meilleur = None
        meilleurs_can = None
        min_options = 10

        for r in range(9):
            for c in range(9):
                if self.grille[r][c] == 0:
                    candidats = self._candidats(r, c)
                    n = len(candidats)
                    if n == 0:
                        return r, c, set()
                    if n < min_options:
                        min_options = n
                        meilleur = (r, c)
                        meilleurs_can = candidats
                        if n == 1:
                            return r, c, meilleurs_can

        if meilleur is None:
            return None, None, None
        return meilleur[0], meilleur[1], meilleurs_can

    def solve(self):
        r, c, candidats = self._mrv()
        if candidats is None and r is None:
            return True
        if candidats is not None and len(candidats) == 0:
            return False

        for num in sorted(list(candidats)):  # Trier aide parfois à la stabilité
            self._placer(r, c, num)
            if self.solve():
                return True
            self._retirer(r, c, num)
        return False


# La fonction de pont que ton SudokuApp appelle :
def resoudre_optimise(grille, app=None):
    optimiseur = SudokuOptimise(grille, app)  # On passe l'app à l'objet
    if optimiseur.solve():
        for r in range(9):
            for c in range(9):
                grille[r][c] = optimiseur.grille[r][c]
        return True
    return False
