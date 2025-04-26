from grille import *
class AIPlayer:
    def __init__(self):
        # Historique des coups joués par l'IA et l'adversaire
        self.memory = [] #liste de dictionnaire contenant l'historique complet et détaillé des coups du joueur(peut contenir des doublons)

        self.visited = set() #liste des cases déjà cliquées (sans doublons)


        self.safe_cells = set() #liste des cases sûres (sans doublons)

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
            """if move['value'] == 0:
                self.safe_cells.add(pos)
                x, y = pos
                directions = [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1), (1, 0), (1, 1)]
                for dx, dy in directions:
                    neighbor = (x + dx, y + dy)
                    self.safe_cells.add(neighbor)""" #cela fait partie de la tache 4.
                     

    def choose_move(self):#Choisit la prochaine case que l'IA va jouer

        #  Chercher une case  sûre (c-a-d sans mine)
        for pos in self.safe_cells:
            if pos not in self.visited:
                # Retourner la  case sûre trouvée et non  visitée
                return pos

        # Si aucune case sûre, chercher une case aléatoire qui n'est pas  dangereuse
        for x in range(self.width):
            for y in range(self.height):
                pos = (x, y)
                if pos not in self.visited and pos not in self.dangerous_cells:
                    # Retourner la première case non visitée et non dangereuse 
                    return pos

        # Si toujours rien, choisir n'importe quelle case non visitée (risque possible)
        for x in range(self.width):
            for y in range(self.height):
                pos = (x, y)
                if pos not in self.visited:
                    # Retourner la première case libre trouvée
                    return pos

        #  Si toutes les cases ont été visitées, plus aucun coup à jouer
        return None


    def update_knowledge(self, position, feedback):
        """
        Met à jour les connaissances de l'IA après avoir joué un coup.

        Args:
            position (tuple): La position jouée par l'IA, ex : (x, y)
            feedback (str): Le résultat du coup (ex: "safe", "danger", etc.)
        """
        pass  # À implémenter
    

    def safe_zone(self, position): #Vérifie si la position donnée est dans une zone sûre.
        #avant de l'introduire au main faut d'abord s'assurer que 
        for move in self.memory:
            if position == move['position'] : #Parcourir toutes les actions dans self.memory
                if move['action'] == 'number_revealed':
                    self.safe_cells.add(position)
                if move['action'] == 'flag':
                    x,y=position
                    # Vérifier les voisins de la cellule actuelle
                    voisins = []
                    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                    for dx, dy in directions:
                        voisin_lig = x + dx
                        voisin_col = y + dy
                        voisins.append((voisin_lig, voisin_col))

                    #nbre de drapeaux dans les voisins
                    nb_flag = sum(1 for nx, ny in voisins if (nx, ny) in self.dangerous_cells)
                    if nb_flag == move['value']:
                        # Si le nombre de drapeaux correspond à la valeur révélée, on peut marquer les voisins comme sûrs
                        for nx, ny in voisins:
                            if (nx, ny) not in self.dangerous_cells:
                                self.safe_cells.add((nx, ny))
                    
