import random

class AIPlayer:
    def __init__(self):
        # Historique des coups joués par l'IA et l'adversaire
        self.memory = []  # Liste de dictionnaires contenant l'historique complet des coups
        self.visited = set()  # Liste des cases déjà cliquées (sans doublons)
        self.safe_cells = set()  # Liste des cases sûres
        self.dangerous_cells = set()  # Liste des cases dangereuses (avec des drapeaux)
        self.danger_map = {}  # Dictionnaire des voisins des drapeaux avec un score de danger
        self.last_move = None  # Pour stocker le dernier coup de l'IA

    def mark_danger_around_flag(self, position):
        """
        Marque les cases autour d'un drapeau comme dangereuses.
        """
        x, y = position
        self.dangerous_cells.add((x, y))  # La case du drapeau est extrêmement dangereuse
        
        directions = [(-1, -1), (-1, 0), (-1, 1), 
                      (0, -1),          (0, 1), 
                      (1, -1), (1, 0),  (1, 1)]
        
        for dx, dy in directions:
            voisin = (x + dx, y + dy)

            if voisin in self.visited or voisin in self.dangerous_cells:
                continue

            if voisin in self.danger_map:
                self.danger_map[voisin] += 1  # Augmenter le score de danger si déjà marqué
            else:
                self.danger_map[voisin] = 1  # Initialiser le score à 1 si c'est un nouveau voisin

    def observe_player(self, move):
        """
        Observe et enregistre le coup joué par l'adversaire.
        """
        self.memory.append(move)
        pos = move['position']
        action = move['action']

        if action == 'click':
            self.visited.add(pos)
        elif action == 'flag':
            self.dangerous_cells.add(pos)
            self.mark_danger_around_flag(pos)
        elif action == 'number_revealed':
            self.visited.add(pos)

    def safe_zone(self, position):
        """
        Vérifie si la position donnée est dans une zone sûre.
        """
        for move in self.memory:
            if position == move['position']:
                if move['action'] == 'number_revealed':
                    self.safe_cells.add(position)

                if move['action'] == 'flag':
                    x, y = position
                    voisins = []
                    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                    for dx, dy in directions:
                        voisin_lig = x + dx
                        voisin_col = y + dy
                        voisins.append((voisin_lig, voisin_col))

                    nb_flag = sum(1 for nx, ny in voisins if (nx, ny) in self.dangerous_cells)
                    if nb_flag == move['value']:
                        for nx, ny in voisins:
                            if (nx, ny) not in self.dangerous_cells:
                                self.safe_cells.add((nx, ny))

    def update_knowledge(self, position, feedback):
        """
        Met à jour les connaissances de l'IA après avoir joué un coup.
        """
        # Cette fonction peut être utilisée pour traiter des feedbacks comme "safe", "danger", etc.
        pass  # À implémenter si nécessaire

    def play(self, grille):
        """
        Décide quel coup jouer (un seul).
        1. Si j'ai une case sûre, je la joue.
        2. Sinon, je joue une case aléatoire non révélée avec une préférence pour celles moins dangereuses.
        """
        
        # Mise à jour des cases sûres
        self.safe_cells = {pos for pos in self.safe_cells if not grille.cells[pos[0]][pos[1]].revealed}

        if self.safe_cells:
            move = self.safe_cells.pop()  # Choisir une case sûre disponible
            self.last_move = move
            return move  # Retourne la position à cliquer

        # Si aucune case sûre n'est disponible, chercher une case non révélée
        non_revealed = [(lig, col) for lig in range(grille.grille_lignes)
                        for col in range(grille.grille_colonnes)
                        if not grille.cells[lig][col].revealed and (lig, col) not in self.dangerous_cells]

        if non_revealed:
            # Ajouter un score de danger basé sur les voisins
            cell_scores = {}
            for (lig, col) in non_revealed:
                score = self.danger_map.get((lig, col), 0)
                cell_scores[(lig, col)] = score
                

            # Trier les cases par score (moins dangereux d'abord)
            least_dangerous_cells = sorted(cell_scores, key=cell_scores.get)

            move = least_dangerous_cells[0]  # Choisir la case la moins dangereuse
            self.last_move = move
            return move  # Retourne la position à cliquer

        # Si aucune case n'est trouvée, retourner None
        return None
