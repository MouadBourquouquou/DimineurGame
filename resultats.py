from mines.mine import Mine
from grille import *

def verifier_defaite(grille, ligne, colonne):
    cellule = grille.cells[ligne][colonne]

    # Vérifie si la cellule contient une mine et si elle est révélée
    if isinstance(cellule, Mine) and cellule.est_visible():  # est_visible() est une méthode de la classe Mine qui vérifie si une mine a été révélée.
        return True  # visible = True, cela signifie que la mine a été révélée.
    return False

def verifier_victoire(grille,grille_lignes,grille_colonnes):
    for lig in range(grille_lignes):
        for col in range(grille_colonnes):
            cellule = grille.cells[lig][col]
            # Si la cellule n'est pas une mine et n'est pas révélée
            if not cellule.has_mine and not cellule.revealed:
                return False
    grille.victoire = True
    return True

def fin_de_jeu(grille, ligne, colonne):
    if verifier_defaite(grille, ligne, colonne):
        if grille.game_over:
            print("Oups ! Tu as perdu.")
    elif verifier_victoire(grille):
        print("Félicitations ! Tu as gagné.")