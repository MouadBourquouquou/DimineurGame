import pygame
from constants import *
from grille import Grille

pygame.init() # Initialise tous les modules Pygame et Active les modules graphiques/audio/inputs
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#Crée la fenêtre de jeu avec les dimensions définies dans constants.py
pygame.display.set_caption("Démineur")#Définit le titre de la fenêtre

FLAG_IMG = pygame.image.load("d:\CI 3 ENSA\Modélisation de l'aide à la décision\Projet Démineur\DimineurGame\images/flag.png")#Charge l'image du drapeau
FLAG_IMG = pygame.transform.scale(FLAG_IMG, (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))  # Redimensionne l'image à 80% de la taille d'une cellule
Mine_IMG=  pygame.image.load("d:\CI 3 ENSA\Modélisation de l'aide à la décision\Projet Démineur\DimineurGame\images/mine.png")
Mine_IMG=  pygame.transform.scale(Mine_IMG, (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))

def dessiner_grille(screen, grille):
    for lig in range(grille_lignes):
        for col in range(grille_colonnes):
            cell = grille.cells[lig][col]
            rect = pygame.Rect(col*CELL_SIZE, lig*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            
            pygame.draw.rect(screen, GREY, rect)#Dessine un rectangle plein (sans bordure).
        
            if cell.flagged:
                # Centrer le drapeau dans la cellule
                flag_rect = FLAG_IMG.get_rect(center=rect.center) #Crée un rectangle de la taille de l'image et Centre ce rectangle sur le centre de la cellule
                screen.blit(FLAG_IMG, flag_rect)#blit() : Méthode PyGame pour copier une image sur une surface
            
            if cell.revealed:
                Mine_rect = Mine_IMG.get_rect(center=rect.center) #Crée un rectangle de la taille de l'image et Centre ce rectangle sur le centre de la cellule
                screen.blit(Mine_IMG, Mine_rect)
        

def main():
    grille = Grille()# Création de l'objet Grille
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#fermeture de fenêtre
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Clic droit
                x, y = pygame.mouse.get_pos()#une fonctionnalité essentielle de PyGame pour récupérer la position de la souris en pixel.
                col = x // CELL_SIZE
                lig = y // CELL_SIZE
                if 0 <= lig < grille_lignes and 0 <= col < grille_colonnes:
                    grille.put_flag(lig, col)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # clic gauche
            x, y = pygame.mouse.get_pos()
            col = x // CELL_SIZE
            lig = y // CELL_SIZE
            if 0 <= lig < grille_lignes and 0 <= col < grille_colonnes:
                grille.reveal_cell(lig, col)  # Appel à la méthode reveal_cell

        screen.fill(BG_COLOR)
        dessiner_grille(screen, grille)
        pygame.display.flip()#affiche tous ce u'on cree dans la grille sur l'écran,il est essentielle 

if __name__ == "__main__":
    main()
