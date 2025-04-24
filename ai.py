class AIPlayer:
    def __init__(self):
        # Historique des coups joués par l'IA et l'adversaire
        self.memory = []

        self.visited = set()


        self.safe_cells = set()

        self.dangerous_cells = set()

    def observe_player(self, move):
        """
        Observe le coup joué par le joueur humain.

        Args:
            move (tuple): La position jouée par le joueur, ex : (x, y)
        """
        pass  # À implémenter

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
