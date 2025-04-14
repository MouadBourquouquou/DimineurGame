from mines.mine import Mine
from constants import grille_lignes, grille_colonnes
from grille import *


def verifier_defaite(grille, ligne, colonne):
    cellule = grille.cells[ligne][colonne]
    
    # Vérifie si la cellule contient une mine et si elle est révélée
    if isinstance(cellule, Mine) and cellule.est_visible():#est_visible() est une méthode de la classe Mine qui vérifie si une mine a été révélée.
        return True    ##visible = True, cela signifie que la mine a été révélée.
    return False

def verifier_victoire(grille):
    for lig in range(grille_lignes):
        for col in range(grille_colonnes):
            cellule = grille.cells[lig][col]
            # Si la cellule n'est pas une mine et n'est pas révélée
            if not isinstance(cellule, Mine) and not cellule.revealed: ##revealed est un attribut de la classe Cellule qui indique si une cellule a été révélée ou non.
                return False
    return True

def fin_de_jeu(grille, ligne, colonne):
    if grille.game_over:
        print("Oups ! Tu as perdu.")
    elif verifier_victoire(grille):
        print("Félicitations ! Tu as gagné.")