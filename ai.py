class AIPlayer:
    def __init__(self):
        # Historique des coups joués par l'IA et l'adversaire
        self.memory = []

        self.visited = set()


        self.safe_cells = set()

        self.dangerous_cells = set()

    def observe_player(self, move):
        """
        Observe et enregistre le coup joué par le joueur humain.

        Args:
            move (dict): Un dictionnaire contenant l'action du joueur, ex :
                        {
                            'action': 'click',
                            'position': (x, y),
                            'value': None  # ou un chiffre pour number_revealed
                        }

            les action comme vous voyez dans la methode on a click,flag,number_revealed
        """
        self.memory.append(move)

        pos = move['position']
        action = move['action']

        if action == 'click':
            self.visited.add(pos)
        elif action == 'flag':
            self.dangerous_cells.add(pos)
        elif action == 'number_revealed':
            self.visited.add(pos)
            if move['value'] == 0:
                self.safe_cells.add(pos)
                x, y = pos
                directions = [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1), (1, 0), (1, 1)]
                for dx, dy in directions:
                    neighbor = (x + dx, y + dy)
                    self.safe_cells.add(neighbor)

    def choose_move(self):
        """
        Choisit le prochain coup à jouer par l'IA.

        Returns:
            tuple: La position choisie par l'IA, ex : (x, y)
        """
        pass  # À implémenter

    def update_knowledge(self, position, feedback):
        """
        Met à jour les connaissances de l'IA après avoir joué un coup.

        Args:
            position (tuple): La position jouée par l'IA, ex : (x, y)
            feedback (str): Le résultat du coup (ex: "safe", "danger", etc.)
        """
        pass  # À implémenter
