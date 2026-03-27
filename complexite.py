import time
import math
import statistics
import copy
from force_brute import resoudre_force_brute
from backtracking import resoudre_sudoku
from force_brute_dichotomique import resoudre_optimise

# 1. ══════════ CLASSES DE COMPLEXITÉ ══════════
_CLASSES = {
    "O(1)": lambda n: 1,
    "O(log n)": lambda n: math.log2(n) if n > 1 else 1,
    "O(n)": lambda n: n,
    "O(n log n)": lambda n: n * math.log2(n) if n > 1 else n,
    "O(n²)": lambda n: n**2,
    "O(n³)": lambda n: n**3,
    "O(2ⁿ)": lambda n: 2**n,
}

# 2. ══════════ FONCTIONS MOTEURS ══════════


def _mesurer(fonction, entree, repetitions=3):
    temps = []
    for _ in range(repetitions):
        debut = time.perf_counter()
        fonction(entree)
        temps.append(time.perf_counter() - debut)
    return statistics.median(temps)


def _normaliser(valeurs):
    mn, mx = min(valeurs), max(valeurs)
    if mx == mn:
        return [0.0] * len(valeurs)
    return [(v - mn) / (mx - mn) for v in valeurs]


def _score_erreur(mesures_norm, tailles, modele_fn):
    modele = [modele_fn(n) for n in tailles]
    modele_norm = _normaliser(modele)
    return sum((m - t) ** 2 for m, t in zip(mesures_norm, modele_norm)) / len(
        mesures_norm
    )


def calculer_complexite(fonction, generateur_entree, tailles=None, repetitions=3):
    if tailles is None:
        tailles = [10, 50, 100, 500, 1000]
    print("\n" + "═" * 52)
    print("  ANALYSE DE COMPLEXITÉ EMPIRIQUE")
    print("═" * 52)
    mesures = []
    for n in tailles:
        entree = generateur_entree(n)
        t = _mesurer(fonction, entree, repetitions)
        mesures.append(t)
        print(f"  n = {n:>6}  →  {t * 1000:.4f} ms")

    mesures_norm = _normaliser(mesures)
    scores = {}
    for nom, fn in _CLASSES.items():
        try:
            scores[nom] = _score_erreur(mesures_norm, tailles, fn)
        except:
            scores[nom] = float("inf")

    classes_triees = sorted(scores.items(), key=lambda x: x[1])
    for i, (nom, err) in enumerate(classes_triees):
        if err == float("inf"):
            continue
        barre = "█" * max(1, int((1 - err) * 20))
        etoile = "  ← MEILLEURE" if i == 0 else ""
        print(f"  {nom:<12}  {barre:<20}  (err={err:.4f}){etoile}")

    return classes_triees[0][0], dict(zip(tailles, mesures))


def comparer_fonctions(fonctions, generateur_entree, tailles=None, repetitions=3):
    if tailles is None:
        tailles = [10, 20, 30]
    resultats = {}
    print("\n" + "═" * 60)
    print("  COMPARAISON DE FONCTIONS")
    print("═" * 60)
    print(f"  {'n':>8}", end="")
    for nom in fonctions:
        print(f"  {nom:>14}", end="")
    print("\n  " + "─" * 56)

    for n in tailles:
        entree = generateur_entree(n)
        print(f"  {n:>8}", end="")
        for nom, fn in fonctions.items():
            # On passe une COPIE de la grille pour ne pas modifier l'originale
            t = _mesurer(fn, copy.deepcopy(entree), repetitions)
            resultats.setdefault(nom, []).append(t)
            print(f"  {t * 1000:>11.4f} ms", end="")
        print()
    return resultats


# 3. ══════════ BLOC D'EXÉCUTION ══════════

if __name__ == "__main__":
    # Définition du générateur (n = nombre de cases vides)
    def generer_grille_test(n):
        from sudoku_engine import init_game

        # On peut imaginer une fonction qui vide 'n' cases
        _, _, _, grid = init_game()
        return grid

    # Wrappers pour envoyer la grille sans l'app GUI
    algos = {
        "Force Brute": lambda g: resoudre_force_brute(g, app=None),
        "Backtracking": lambda g: resoudre_sudoku(g, app=None),
        "MRV Optimisé": lambda g: resoudre_optimise(g, app=None),
    }

    # Lancer la comparaison
    comparer_fonctions(
        fonctions=algos,
        generateur_entree=generer_grille_test,
        tailles=[5, 10, 15, 20],  # Tailles prudentes pour la force brute
        repetitions=2,
    )
