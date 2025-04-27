import random
from .mine import Mine


class ChampDeMines:
    def __init__(self, taille, nb_mines):
        self.taille = taille
        self.nb_mines = nb_mines
        self.mines = []

    def generer_mines(self, premier_clic):
        positions_possibles = [
            (x, y)
            for x in range(self.taille)
            for y in range(self.taille)
            # Éviter la case du premier clic et les cases adjacentes
            if not (x == premier_clic[0] and y == premier_clic[1]) and
            not (x == premier_clic[0] + 1 and y == premier_clic[1]) and
            not (x == premier_clic[0] and y == premier_clic[1] + 1) and
            not (x == premier_clic[0] + 1 and y == premier_clic[1] + 1) and
            not (x == premier_clic[0] - 1 and y == premier_clic[1] + 1) and
            not (x == premier_clic[0] - 1 and y == premier_clic[1] - 1) and
            not (x == premier_clic[0] and y == premier_clic[1] - 1) and
            not (x == premier_clic[0] -1 and y == premier_clic[1] ) and
            not (x == premier_clic[0] + 1 and y == premier_clic[1] -1 ) 
        ]
        positions = random.sample(positions_possibles, self.nb_mines)
        self.mines = [Mine(x, y) for (x, y) in positions]
        i=0
        for mine in self.mines:
            print(f"mine {i}: {mine.position()} ")
            i+=1

    def reveler(self, x, y):
        for mine in self.mines:
            if mine.x == x and mine.y == y:
                mine.reveler()
                return True  # Mine trouvée
        return False  # Pas de mine ici

    def marquer(self, x, y):
        for mine in self.mines:
            if mine.x == x and mine.y == y:
                mine.marquer()
                return True
