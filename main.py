import pygame
from constants import *
from grille import Grille
from resultats import fin_de_jeu


pygame.init()  # Initialise tous les modules Pygame et Active les modules graphiques/audio/inputs
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Crée la fenêtre de jeu avec les dimensions définies dans constants.py
pygame.display.set_caption("Démineur")  # Définit le titre de la fenêtre

font = pygame.font.SysFont('Consolas', 30)


FLAG_IMG = pygame.image.load("images/flag.png")  # Charge l'image du drapeau
FLAG_IMG = pygame.transform.scale(FLAG_IMG, (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))  # Redimensionne l'image à 80% de la taille d'une cellule
Mine_IMG = pygame.image.load("images/mine.png")
Mine_IMG = pygame.transform.scale(Mine_IMG, (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))


def dessiner_grille(screen, grille):
    for lig in range(grille_lignes):
        for col in range(grille_colonnes):
            x = col * CELL_SIZE 
            y = lig * CELL_SIZE + 50  
            cell = grille.cells[lig][col]
            rect = pygame.Rect(col * CELL_SIZE, lig * CELL_SIZE + 50, CELL_SIZE - 1, CELL_SIZE - 1)
            color = (160, 160, 160) if cell.revealed else (100, 100, 100)
            pygame.draw.rect(screen, color, rect)  #  Dessine un rectangle plein (sans bordure)  //imane.
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            
            if cell.revealed and not cell.has_mine:
                mines_voisines = grille.compter_mines_voisines(lig, col)
                if mines_voisines > 0:
                    font = pygame.font.SysFont(None, 24)
                    text = font.render(str(mines_voisines), True, (0, 0, 255))
                    screen.blit(text, (x + 10, y + 5))

            if cell.revealed and cell.has_mine:
                screen.blit(pygame.transform.scale(Mine_IMG, (CELL_SIZE - 4, CELL_SIZE - 4)), (x + 2, y + 2))

            if cell.flagged and not cell.revealed:
                screen.blit(pygame.transform.scale(FLAG_IMG, (CELL_SIZE - 4, CELL_SIZE - 4)), (x + 2, y + 2))


def afficher_chrono(screen, temps_ms):
    temps_s = temps_ms // 1000
    sec = temps_s % 60
    min = temps_s // 60
    chrono_text = f"{min:02}:{sec:02}"
    chrono_surface = font.render(chrono_text, True, BLACK)

    # Fond pour le chrono
    pygame.draw.rect(screen, BG_COLOR, (SCREEN_WIDTH - 100, 10, 90, 30))
    screen.blit(chrono_surface, (SCREEN_WIDTH - 100, 10))
def afficher_message(screen, message):
    font = pygame.font.SysFont(None, 40)
    text = font.render(message, True, (255, 0, 0))
    rect = text.get_rect(center=(screen.get_width() // 2, 25))
    screen.blit(text, rect)  


def main():
    grille = Grille()  # Initialisation de la grille
    running = True
    jeu_demarre = False
    temps_debut = 0

    while running:
        temps_ecoule = pygame.time.get_ticks() - temps_debut if jeu_demarre else 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Gestion des événements souris
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                x, y = pygame.mouse.get_pos()
                if y >= 50:  # Zone de la grille (en dessous du chrono)
                    col = x // CELL_SIZE
                    lig = (y - 50) // CELL_SIZE  # Ajustement pour l'offset vertical

            # Actions sur clic
            if event.type == pygame.MOUSEBUTTONDOWN and y >= 50:
                if 0 <= lig < grille_lignes and 0 <= col < grille_colonnes and not grille.game_over:
                    # Démarrer le jeu au premier clic valide
                    if not jeu_demarre:
                        jeu_demarre = True
                        temps_debut = pygame.time.get_ticks()

                    # Clic droit : drapeau
                    if event.button == 3:  
                        grille.put_flag(lig, col)
                    
                    # Clic gauche : révélation
                    elif event.button == 1:  
                        grille.reveal_cell(lig, col)
                        if grille.cells[lig][col].has_mine:  # Vérification défaite
                            grille.game_over = True

        # Affichage
        screen.fill(BG_COLOR)
        dessiner_grille(screen, grille)
        
        # Chronomètre (si jeu démarré)
        if jeu_demarre:
            afficher_chrono(screen, temps_ecoule)
        
        # Message de fin (défaite)
        if grille.game_over:
            afficher_message(screen, "Perdu !")

        pygame.display.flip()

    pygame.quit()
if __name__ == "__main__":
    main()

