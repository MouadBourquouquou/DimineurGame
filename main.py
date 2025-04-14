import pygame
from constants import *
from grille import Grille

pygame.init() # Initialise tous les modules Pygame et Active les modules graphiques/audio/inputs
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#Crée la fenêtre de jeu avec les dimensions définies dans constants.py
pygame.display.set_caption("Démineur")#Définit le titre de la fenêtre

font = pygame.font.SysFont('Consolas', 20)


FLAG_IMG = pygame.image.load("images/flag.png")#Charge l'image du drapeau
FLAG_IMG = pygame.transform.scale(FLAG_IMG, (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))  # Redimensionne l'image à 80% de la taille d'une cellule
Mine_IMG=  pygame.image.load("images/mine.png")
Mine_IMG=  pygame.transform.scale(Mine_IMG, (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))

def dessiner_grille(screen, grille):
    for lig in range(grille_lignes):
        for col in range(grille_colonnes):
            cell = grille.cells[lig][col]
            rect = pygame.Rect(col*CELL_SIZE, lig*CELL_SIZE+50, CELL_SIZE-1, CELL_SIZE-1)
            
            pygame.draw.rect(screen, GREY, rect)#Dessine un rectangle plein (sans bordure).
        
            if cell.flagged:
                # Centrer le drapeau dans la cellule
                flag_rect = FLAG_IMG.get_rect(center=rect.center) #Crée un rectangle de la taille de l'image et Centre ce rectangle sur le centre de la cellule
                screen.blit(FLAG_IMG, flag_rect)#blit() : Méthode PyGame pour copier une image sur une surface
            
            if cell.revealed:
                Mine_rect = Mine_IMG.get_rect(center=rect.center) #Crée un rectangle de la taille de l'image et Centre ce rectangle sur le centre de la cellule
                screen.blit(Mine_IMG, Mine_rect)


def afficher_chrono(screen, temps_ms):
    temps_s = temps_ms // 1000
    sec = temps_s % 60
    min = temps_s // 60
    chrono_text = f"{min:02}:{sec:02}"
    chrono_surface = font.render(chrono_text, True, BLACK)

    # Fond pour le chrono
    pygame.draw.rect(screen, BG_COLOR, (SCREEN_WIDTH - 100, 10, 90, 30))
    screen.blit(chrono_surface, (SCREEN_WIDTH - 100, 10))
def afficher_flags(screen, flags_restants):
    color = RED if flags_restants <= 0 else BLACK  # Rouge si plus de flags disponibles
    text = font.render(f"Flags: {flags_restants}/{MAX_FLAGS}", True, color)
    pygame.draw.rect(screen, BG_COLOR, (10, 10, 120, 30))  # Agrandi pour accommoder le nouveau texte
    screen.blit(text, (15, 10))

def main():
    grille = Grille()# Création de l'objet Grille
    running = True
    jeu_demarre = False
    temps_debut = 0

    while running:
        temps_ecoule = pygame.time.get_ticks()-temps_debut


        for event in pygame.event.get():
            if event.type == pygame.QUIT:#fermeture de fenêtre
                running = False

            x, y = pygame.mouse.get_pos()  # une fonctionnalité essentielle de PyGame pour récupérer la position de la souris en pixel.
            if y >= 50:
                col = x // CELL_SIZE
                lig = (y - 50) // CELL_SIZE  # Ajustement pour la grille décalée

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Clic droit
                if 0 <= lig < grille_lignes and 0 <= col < grille_colonnes:
                    grille.put_flag(lig, col)
        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # clic gauche
                if 0 <= lig < grille_lignes and 0 <= col < grille_colonnes:
                    if not jeu_demarre:  # <-- Détection pour le chrono
                        jeu_demarre = True
                        temps_debut = pygame.time.get_ticks()
                    grille.reveal_cell(lig, col)  # Appel à la méthode reveal_cell

        screen.fill(BG_COLOR)
        dessiner_grille(screen, grille)
        afficher_flags(screen, MAX_FLAGS - grille.flags_places)

        # Afficher le chrono seulement s'il est actif
        if jeu_demarre:
            afficher_chrono(screen, temps_ecoule)

        pygame.display.flip()#affiche tous ce u'on cree dans la grille sur l'écran,il est essentielle 

if __name__ == "__main__":
    main()
