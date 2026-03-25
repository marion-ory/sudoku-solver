class SudokuGrid:
    def __init__(self):
        self.grille = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]

    def load_files(self, file_name):
        self.grille = []
        self.position = []

        with open(file_name, "r") as f:
            all_lines = f.readlines()

            for r, line in enumerate(all_lines):
                # passe de ligne en ligne et nettoie
                ligne_propre = []
                line = line.strip()

                # defini les caractères a remplacé
                for j, char in enumerate(line):
                    if char == "_":
                        ligne_propre.append(0)
                    else:
                        valeur = int(char)
                        ligne_propre.append(valeur)
                        # recupere les positions des nouvelles valeurs
                        self.position.append((r, j))
                self.grille.append(ligne_propre)


mon_sudoku = SudokuGrid()
mon_sudoku.load_files("grille/sudoku.txt")
for ligne in mon_sudoku.grille:
    print(ligne)
