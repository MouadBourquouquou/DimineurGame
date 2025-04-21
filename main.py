'''import pygame
from resultats import *
from grille import Grille
# from resultats import fin_de_jeu
pygame.init()  # Initialise tous les modules Pygame et Active les modules graphiques/audio/inputs
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Crée la fenêtre de jeu avec les dimensions définies dans constants.py

pygame.display.set_caption("Démineur")  # Définit le titre de la fenêtre
pygame.display.set_icon(pygame.image.load("images/bombe.png"))
font = pygame.font.SysFont('Consolas', 30)

FLAG_IMG = pygame.image.load("images/flag.png")  # Charge l'image du drapeau
FLAG_IMG = pygame.transform.scale(FLAG_IMG, (
int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))  # Redimensionne l'image à 80% de la taille d'une cellule
Mine_IMG = pygame.image.load("images/mine.png")
Mine_IMG = pygame.transform.scale(Mine_IMG, (int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))

BG_COLOR = (10, 25, 47)  # Bleu nuit


def dessiner_grille(screen, grille):
    for lig in range(grille.grille_lignes):
        for col in range(grille.grille_colonnes):
            x = col * CELL_SIZE
            y = lig * CELL_SIZE + 50
            cell = grille.cells[lig][col]
            rect = pygame.Rect(col * CELL_SIZE, lig * CELL_SIZE + 50, CELL_SIZE - 1, CELL_SIZE - 1)

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
    screen.blit(chrono_surface, (SCREEN_WIDTH - 90, 10))


def afficher_message(screen, message):
    font = pygame.font.SysFont(None, 40)
    text = font.render(message, True, (255, 0, 0))
    rect = text.get_rect(center=(screen.get_width() // 2, 25))
    screen.blit(text, rect)


def afficher_flags(screen, flags_restants,total_flags):
    color = RED if flags_restants <= 0 else BLACK  # Rouge si plus de flags disponibles
    text = font.render(f"Flags: {flags_restants}/{total_flags}", True, color)
    pygame.draw.rect(screen, BG_COLOR, (10, 10, 120, 30))  # Agrandi pour accommoder le nouveau texte
    screen.blit(text, (5, 10))


def afficher_stats(screen, temps_ecoule, clicks, efficacite, resultat):
    panel_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
    pygame.draw.rect(screen, (20, 40, 70), panel_rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), panel_rect, 2, border_radius=10)

    stats_font = pygame.font.SysFont('Arial', 20)
    y = panel_rect.y + 10

    stats = [
        f"Temps: {temps_ecoule / 1000:.3f} sec",
        f"Clics: {clicks}",
        f"Efficacité: {efficacite:.0f}%"
    ]

    for stat in stats:
        text = stats_font.render(stat, True, (255, 255, 255))
        screen.blit(text, (panel_rect.x + 20, y))
        y += 25

    result_font = pygame.font.SysFont('Arial', 24, bold=True)
    result_color = (0, 255, 0) if "VICTOIRE" in resultat else (255, 0, 0)
    result_text = result_font.render(resultat, True, result_color)
    screen.blit(result_text, (panel_rect.centerx, panel_rect.y + 10))


def handle_stats_screen(screen, grille, stats_data):
    screen.fill(BG_COLOR)
    dessiner_grille(screen, grille)
    afficher_flags(screen, grille.num_mines - grille.flags_places, grille.num_mines)
    afficher_chrono(screen, stats_data['time'])
    afficher_stats(screen, stats_data['time'], stats_data['clicks'], stats_data['efficiency'], stats_data['result'])
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
    return False

def main():
    start = True
    play = False
    jeu_demarre = False
    temps_debut = 0
    temps_ecoule = 0
    grille_lignes, grille_colonnes, num_mines = 0,0,0
    clicks = 1
    revealed = 0
    start_time = 0
    show_stats = False

    while start:
        #dessiner la page d'accueil avec 3 niveaux de difficulté
        screen.fill(BG_COLOR)
        font = pygame.font.SysFont('Consolas', 50)
        title_text = font.render("Démineur", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)
        font = pygame.font.SysFont('Consolas', 30)
        easy_text = font.render("Facile", True, BLACK)
        easy_rect = easy_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(easy_text, easy_rect)
        medium_text = font.render("Moyen", True, BLACK)
        medium_rect = medium_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(medium_text, medium_rect)
        hard_text = font.render("Difficile", True, BLACK)
        hard_rect = hard_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(hard_text, hard_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if easy_rect.collidepoint(x, y): 
                    grille_lignes, grille_colonnes, num_mines = 9, 9, 10
                    play = True
                    start = False
                elif medium_rect.collidepoint(x, y):
                    grille_lignes, grille_colonnes, num_mines = 14, 14, 30
                    play = True
                    start = False
                elif hard_rect.collidepoint(x, y):
                    grille_lignes, grille_colonnes, num_mines = 16, 16, 50
                    play = True
                    start = False
            
    grille = Grille(grille_lignes,grille_colonnes,num_mines)  # Initialisation de la grille
    while play:
        if jeu_demarre and not grille.game_over:
            temps_ecoule = pygame.time.get_ticks() - temps_debut if jeu_demarre else 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

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
                        clicks += 1


                    # Clic gauche : révélation
                    elif event.button == 1:
                        grille.reveal_cell(lig, col)
                        clicks+=1
                        revealed +=1
                        if grille.cells[lig][col].has_mine:  # Vérification défaite
                            grille.game_over = True
                # Gestion de l'affichage
                if grille.game_over or verifier_victoire(grille,grille_lignes,grille_colonnes):

                    efficacite = (revealed / clicks) * 100 if clicks > 0 else 0
                    stats_data = {
                        'time': temps_ecoule,
                        'clicks': clicks,
                        'efficiency': efficacite,
                        'result': "VICTOIRE !" if grille.victoire else "PERDU !",
                        'grille': grille
                    }

                    show_stats = handle_stats_screen(screen, grille, stats_data)
                    if not show_stats:
                        play = False  # Retour au menu
                  
        # Affichage
        screen.fill(BG_COLOR)
        dessiner_grille(screen, grille)
        afficher_flags(screen, grille.num_mines - grille.flags_places,grille.num_mines)

        if jeu_demarre:
            afficher_chrono(screen, temps_ecoule)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()'''
import pygame
from resultats import *
from grille import Grille

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Démineur")
pygame.display.set_icon(pygame.image.load("images/bombe.png"))
font = pygame.font.SysFont('Consolas', 30)

# Couleurs
BG_COLOR = (10, 25, 47)  # Bleu nuit
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 150, 250)
BUTTON_HOVER_COLOR = (70, 170, 270)

def draw_welcome_screen():
    screen.fill(BG_COLOR)
    
    # Titre
    title_font = pygame.font.SysFont('Consolas', 60)
    title_text = title_font.render("DÉMINEUR", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title_text, title_rect)
    
    # Sous-titre
    subtitle_font = pygame.font.SysFont('Consolas', 20)
    subtitle_text = subtitle_font.render("Le classique jeu de stratégie et de chance", True, WHITE)
    subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60))
    screen.blit(subtitle_text, subtitle_rect)
    
    # Bouton Start
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=10)  # Bordure
    
    button_font = pygame.font.SysFont('Consolas', 30)
    button_text = button_font.render("COMMENCER", True, WHITE)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    pygame.display.flip()
    
    return button_rect

def draw_difficulty_screen():
    screen.fill(BG_COLOR)
    
    # Titre
    title_font = pygame.font.SysFont('Consolas', 50)
    title_text = title_font.render("Choisissez la difficulté", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)
    
    # Boutons de difficulté
    buttons = []
    difficulties = [
        ("Facile", 9, 9, 10),
        ("Moyen", 14, 14, 30),
        ("Difficile", 16, 16, 50)
    ]
    
    mouse_pos = pygame.mouse.get_pos()
    
    for i, (name, rows, cols, mines) in enumerate(difficulties):
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + i * 80, 200, 50)
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        button_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=10)
        
        button_font = pygame.font.SysFont('Consolas', 25)
        button_text = button_font.render(name, True, WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)
        
        buttons.append((button_rect, rows, cols, mines))
    
    pygame.display.flip()
    return buttons

def main():
    # État initial
    current_screen = "welcome"  # "welcome" ou "difficulty" ou "game"
    grille_lignes, grille_colonnes, num_mines = 0, 0, 0
    grille = None
    jeu_demarre = False
    temps_debut = 0
    temps_ecoule = 0
    clicks = 1
    revealed = 0
    
    running = True
    while running:
        if current_screen == "welcome":
            start_button = draw_welcome_screen()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button.collidepoint(event.pos):
                        current_screen = "difficulty"
        
        elif current_screen == "difficulty":
            difficulty_buttons = draw_difficulty_screen()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button_rect, rows, cols, mines in difficulty_buttons:
                        if button_rect.collidepoint(event.pos):
                            grille_lignes, grille_colonnes, num_mines = rows, cols, mines
                            grille = Grille(grille_lignes, grille_colonnes, num_mines)
                            current_screen = "game"
                            break
        
        elif current_screen == "game":
            # Votre logique de jeu existante ici
            if jeu_demarre and not grille.game_over:
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
                            clicks += 1

                        # Clic gauche : révélation
                        elif event.button == 1:
                            grille.reveal_cell(lig, col)
                            clicks += 1
                            revealed += 1
                            if grille.cells[lig][col].has_mine:  # Vérification défaite
                                grille.game_over = True
                    
                    # Gestion de l'affichage
                    if grille.game_over or verifier_victoire(grille, grille_lignes, grille_colonnes):
                        efficacite = (revealed / clicks) * 100 if clicks > 0 else 0
                        stats_data = {
                            'time': temps_ecoule,
                            'clicks': clicks,
                            'efficiency': efficacite,
                            'result': "VICTOIRE !" if grille.victoire else "PERDU !",
                            'grille': grille
                        }

                        if not handle_stats_screen(screen, grille, stats_data):
                            current_screen = "welcome"  # Retour à l'écran d'accueil
                            jeu_demarre = False
                            clicks = 1
                            revealed = 0

            # Affichage
            screen.fill(BG_COLOR)
            dessiner_grille(screen, grille)
            afficher_flags(screen, grille.num_mines - grille.flags_places, grille.num_mines)

            if jeu_demarre:
                afficher_chrono(screen, temps_ecoule)

            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
