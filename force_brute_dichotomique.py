class SudokuOptimise:
    def __init__(self, grille_gui):
        self.grille = [[0] * 9 for _ in range(9)]
        self.rows  = [set() for _ in range(9)]
        self.cols  = [set() for _ in range(9)]
        self.boxes = [set() for _ in range(9)]
        
        for r in range(9):
            for c in range(9):
                val = grille_gui[r][c]
                if val != ' ':
                    self._placer(r, c, int(val))

    def _box(self, r, c):
        return (r // 3) * 3 + (c // 3)

    def _placer(self, r, c, val):
        self.rows[r].add(val)
        self.cols[c].add(val)
        self.boxes[self._box(r, c)].add(val)
        self.grille[r][c] = val

    def _retirer(self, r, c, val):
        self.rows[r].discard(val)
        self.cols[c].discard(val)
        self.boxes[self._box(r, c)].discard(val)
        self.grille[r][c] = 0

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

                    # CORRECTION ICI : On renvoie la case, mais avec 0 candidat
                    if n == 0: 
                        return r, c, set() 

                    if n < min_options:
                        min_options = n
                        meilleur = (r, c)
                        meilleurs_can = candidats
                        if n == 1: 
                            return r, c, meilleurs_can

        # S'il n'y a vraiment plus de 0 dans toute la grille, c'est la victoire
        if meilleur is None: 
            return None, None, None
            
        return meilleur[0], meilleur[1], meilleurs_can

    def solve(self):
        r, c, candidats = self._mrv()

        # Fin de la grille
        if candidats is None and r is None: 
            return True
            
        # Impasse détectée (grâce à notre correction)
        if candidats is not None and len(candidats) == 0: 
            return False

        for num in candidats:
            self._placer(r, c, num)
            if self.solve(): 
                return True
            self._retirer(r, c, num)
            
        return False

def resoudre_optimise(grille):
    optimiseur = SudokuOptimise(grille)
    if optimiseur.solve():
        for r in range(9):
            for c in range(9):
                grille[r][c] = optimiseur.grille[r][c]
        return True
    return False