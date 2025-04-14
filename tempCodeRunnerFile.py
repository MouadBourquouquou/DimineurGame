import pygame
from constants import *
from grille import Grille

pygame.init()
screen = pygame.display.set_mode((grille_colonnes * CELL_SIZE, grille_lignes * CELL_SIZE + 50))
pygame.display.set_caption("Démineur")

def dessiner_grille(screen, grille):
    for lig in range(grille_lignes):
        for col in range(grille_colonnes):
            x = col * CELL_SIZE
            y = lig * CELL_SIZE + 50
            cell = grille.cells[lig][col]
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            color = (160, 160, 160) if cell.revealed else (100, 100, 100)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

            if cell.revealed and not cell.has_mine:
                mines_voisines = grille.compter_mines_voisines(lig, col)
                if mines_voisines > 0:
                    font = pygame.font.SysFont(None, 24)
                    text = font.render(str(mines_voisines), True, (0, 0, 255))
                    screen.blit(text, (x + 10, y + 5))

            if cell.revealed and cell.has_mine:
                pygame.draw.circle(screen, (255, 0, 0), rect.center, CELL_SIZE // 4)

            if cell.flagged and not cell.revealed:
                pygame.draw.circle(screen, (0, 255, 0), rect.center, CELL_SIZE // 4)

def afficher_chrono(screen, temps):
    font = pygame.font.SysFont(None, 30)
    secondes = temps // 1000
    texte = font.render(f"Temps : {secondes}s", True, (0, 0, 0))
    screen.blit(texte, (10, 10))

def afficher_message(screen, message):
    font = pygame.font.SysFont(None, 40)
    text = font.render(message, True, (255, 0, 0))
    rect = text.get_rect(center=(screen.get_width() // 2, 25))
    screen.blit(text, rect)

def main():
    grille = Grille()
    running = True
    jeu_demarre = False
    temps_debut = 0

    while running:
        temps_ecoule = pygame.time.get_ticks() - temps_debut

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                x, y = pygame.mouse.get_pos()
                if y >= 50:
                    col = x // CELL_SIZE
                    lig = (y - 50) // CELL_SIZE

            if event.type == pygame.MOUSEBUTTONDOWN:
                if y >= 50 and 0 <= lig < grille_lignes and 0 <= col < grille_colonnes:
                    if not grille.game_over:
                        if event.button == 3:
                            grille.put_flag(lig, col)
                        elif event.button == 1:
                            if not jeu_demarre:
                                jeu_demarre = True
                                temps_debut = pygame.time.get_ticks()
                            grille.reveal_cell(lig, col)

        screen.fill(BG_COLOR)
        dessiner_grille(screen, grille)

        if jeu_demarre:
            afficher_chrono(screen, temps_ecoule)

        if grille.game_over:
            afficher_message(screen, "Perdu ! 😵")

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
