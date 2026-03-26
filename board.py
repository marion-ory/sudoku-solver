class SudokuGrid:
    def __init__(self):

        self.grille = []
        self.position = []

    # [ Charge fichier .TXT ]
    def load_files(self, file_name):
        self.grille = []
        self.position = []
        with open(file_name, "r") as f:
            all_lines = f.readlines()
            for r, line in enumerate(all_lines):
                ligne_propre = []
                line = line.strip()  # nettoie
                for j, char in enumerate(line):
                    if char == "_":
                        ligne_propre.append(0)
                    else:
                        valeur = int(char)
                        ligne_propre.append(valeur)
                        self.position.append((r, j))
                self.grille.append(ligne_propre)

    def find_empty(self):  # cherche les positions vides
        for r in range(9):
            for c in range(9):
                if self.grille[r][c] == 0:
                    return (r, c)
        return None

    def verifier_tout(self):
        # Vérification des Lignes
        for ligne in self.grille:  # set supprime les doublons
            if len(set(ligne)) != 9 or 0 in ligne:
                return False  # pas de case vide sudoku est rempli

        # Vérification des Colonnes
        for c in range(9):
            colonne = [self.grille[r][c] for r in range(9)]
            if (
                len(set(colonne)) != 9 or 0 in colonne
            ):  # svérifie si il y a 9 chiffres unique
                return False

        # Vérification des Blocs 3x3 (decoupage de la grille)
        for i in range(0, 9, 3):  # ligne 0,3 et 6 debut de carré sur chaque ligne
            for j in range(0, 9, 3):  # colone 0, 3,6 debut de carré sur chaque colone
                bloc = []
                for r in range(i, i + 3):  # les 3 ligne du bloc
                    for c in range(j, j + 3):  # les 3 colone du bloc
                        bloc.append(self.grille[r][c])  # retourne les positions
                if len(set(bloc)) != 9 or 0 in bloc:  # ajoute les valeurs dans le bloc
                    return False  # pas la peine de continuer la grille est pas valide
        return True  # grille ok

    def solve_brute_force(self):
        case = self.find_empty()

        # Check si il reste une case vide
        if case is None:
            return self.verifier_tout()

        ligne, col = case
        for num in range(1, 10):  #  test toutes les possibilités de 1  à 9
            self.grille[ligne][col] = num

            # Appel récursif, on recommence find empty, test
            if self.solve_brute_force():
                return True

            # Backtrack : on remet à zéro si ça ne marche pas
            self.grille[ligne][col] = 0
        return False  # grille impossible à finir IMPASSE


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
