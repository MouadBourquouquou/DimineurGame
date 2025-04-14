import random
from constants import *
from mines.ChampMines import ChampDeMines
class Cellule:
    def __init__(self):
        self.flagged = False  # Seul attribut nécessaire
        self.revealed = False  # Si la cellule a été révélée
        self.has_mine = False # Si la cellule contient une mine

        
class Grille:
    def __init__(self):
        self.cells = [[Cellule() for _ in range(grille_colonnes)] for _ in range(grille_lignes)]
        self.champ = None  # ChampDeMines, initialisé après le premier clic
        self.first_click = True  # Pour s'assurer que les mines ne sont générées qu'une seule fois
        self.game_over = False 
    def put_flag(self, lig, col):
        if 0 <= lig < grille_lignes and 0 <= col < grille_colonnes:
            self.cells[lig][col].flagged = not self.cells[lig][col].flagged
    
    
                
    def reveal_cell(self, lig, col):
        #  Gestion du premier clic : Initialisation du champ de mines
        if self.first_click:
            # Création du champ de mines avec dimensions et nombre de mines
            self.champ = ChampDeMines(grille_lignes, NUM_MINES)
            # Génération des mines en évitant la cellule du premier clic (lig, col)
            self.champ.generer_mines((lig, col))
            # Marquage des cellules minées dans la grille
            for mine in self.champ.mines:
                self.cells[mine.x][mine.y].has_mine = True
            self.first_click = False # Le jeu est maintenant initialisé
        #  Vérifications préalables
        if self.cells[lig][col].revealed or self.cells[lig][col].flagged:
            return   # Ne rien faire si cellule déjà révélée ou marquée
        #  Gestion des cas après révélation
        if self.cells[lig][col].has_mine:
            # Case minée : fin du jeu
            self.cells[lig][col].revealed = True
            # Révélation de toutes les mines (affichage)
            self.game_over = True
            for mine in self.champ.mines:
                self.cells[mine.x][mine.y].revealed = True
        else:
            # Case vide : révélation récursive des cases adjacentes
            self._reveal_recursive(lig, col)

    def _reveal_recursive(self, lig, col):
        """Révèle récursivement les cellules vides."""
        # Vérifier les limites de la grille
        if not (0 <= lig < grille_lignes and 0 <= col < grille_colonnes):
            return

        cell = self.cells[lig][col]
        # Ne pas traiter les cellules déjà révélées, minées ou marquées
        if cell.revealed or cell.has_mine or cell.flagged:
            return

        cell.revealed = True
        # Si pas de mines voisines, continuer la récursion
        if self.compter_mines_voisines(lig, col) == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i != 0 or j != 0:  # Éviter la cellule actuelle
                        self._reveal_recursive(lig + i, col + j) 
    # Compte le nombre de mines voisines pour une cellule donnée
    # Cette méthode est appelée lorsque la cellule est révélée
    # et permet de savoir combien de mines sont autour d'elle     par Abdelghani Bensalih
    def compter_mines_voisines(self, lig, col):
        mines = 0
        for i in range(-1, 2):  # -1, 0, 1
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                voisin_lig = lig + i
                voisin_col = col + j
                if 0 <= voisin_lig < grille_lignes and 0 <= voisin_col < grille_colonnes:
                    if self.cells[voisin_lig][voisin_col].has_mine:
                        mines += 1
        return mines
