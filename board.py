class SudokuGrid:
    def __init__(self):

        self.grille = []
        self.position = []

    def load_files(self, file_name):
        self.grille = []
        self.position = []
        with open(file_name, "r") as f:
            all_lines = f.readlines()
            for r, line in enumerate(all_lines):
                ligne_propre = []
                line = line.strip()
                for j, char in enumerate(line):
                    if char == "_":
                        ligne_propre.append(0)
                    else:
                        valeur = int(char)
                        ligne_propre.append(valeur)
                        self.position.append((r, j))
                self.grille.append(ligne_propre)

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.grille[r][c] == 0:
                    return (r, c)
        return None

    def verifier_tout(self):
        # Vérification des Lignes
        for ligne in self.grille:
            if len(set(ligne)) != 9 or 0 in ligne:
                return False

        # Vérification des Colonnes
        for c in range(9):
            colonne = [self.grille[r][c] for r in range(9)]
            if len(set(colonne)) != 9 or 0 in colonne:
                return False

        # Vérification des Blocs 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                bloc = []
                for r in range(i, i + 3):
                    for c in range(j, j + 3):
                        bloc.append(self.grille[r][c])
                if len(set(bloc)) != 9 or 0 in bloc:
                    return False
        return True

    def solve_brute_force(self):
        case = self.find_empty()

        # Si plus de case vide, on vérifie si la grille est valide
        if case is None:
            return self.verifier_tout()

        ligne, col = case
        for num in range(1, 10):
            self.grille[ligne][col] = num

            # Appel récursif
            if self.solve_brute_force():
                return True

            # Backtrack : on remet à zéro si ça ne marche pas
            self.grille[ligne][col] = 0
        return False


choix = input("Entrez le nom du fichier: ")
chemin_complet = "grille/" + choix

mon_sudoku = SudokuGrid()

try:
    mon_sudoku.load_files(chemin_complet)
    print("Grille chargée :")
    for l in mon_sudoku.grille:
        print(l)

    print("\nRésolution en cours...")
    if mon_sudoku.solve_brute_force():
        print("\nSUDOKU RÉSOLU :")
        for ligne in mon_sudoku.grille:
            print(ligne)
    else:
        print("Pas de solution trouvée.")
except FileNotFoundError:
    print(f"Erreur : le fichier {chemin_complet} n'existe pas.")
