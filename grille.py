import random
from constants import *
from mines.ChampMines import ChampDeMines
class Cellule:
    def __init__(self):
        self.flagged = False  # Seul attribut nécessaire
        self.revealed = False  # Si la cellule a été révélée

        
class Grille:
    def __init__(self):
        self.cells = [[Cellule() for _ in range(grille_colonnes)] for _ in range(grille_lignes)]
        self.champ = None  # ChampDeMines, initialisé après le premier clic
        self.first_click = True  # Pour s'assurer que les mines ne sont générées qu'une seule fois
    
    def put_flag(self, lig, col):
        if 0 <= lig < grille_lignes and 0 <= col < grille_colonnes:
            self.cells[lig][col].flagged = not self.cells[lig][col].flagged
    
    def reveal_cell(self, lig, col):
        # Si c'est le premier clic, générer les mines
        if self.first_click:
            self.champ = ChampDeMines(grille_lignes, 10)  # Taille de la grille et nombre de mines
            self.champ.generer_mines((lig, col))  # Ne pas placer de mine sur le premier clic
            self.first_click = False

        # Vérifie si la cellule contient une mine
        mine_revealed = self.champ.reveler(lig, col)

        # Si c'est une mine, révéler toutes les mines
        if mine_revealed:
            self.cells[lig][col].revealed = True
            # Révèle toutes les mines
            for mine in self.champ.mines:
                self.cells[mine.x][mine.y].revealed = True
