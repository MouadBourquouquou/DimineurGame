import random
from constants import *
class Cellule:
    def __init__(self):
        self.flagged = False  # Seul attribut nécessaire

class Grille:
    def __init__(self):
        self.cells = [[Cellule() for _ in range(grille_colonnes)] for _ in range(grille_lignes)]
    
    def put_flag(self, lig, col):
        if 0 <= lig < grille_lignes and 0 <= col < grille_colonnes:
            self.cells[lig][col].flagged = not self.cells[lig][col].flagged