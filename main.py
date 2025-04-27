import pygame
from resultats import *
from grille import Grille
from ai import AIPlayer
from visualization import AIVisualizer
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
    font = pygame.font.SysFont('Consolas', 30)
    text = font.render(message, True, (255, 0, 0))
    rect = text.get_rect(center=(screen.get_width() // 2 , 500))
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

def draw_control_buttons():
    """Dessine les boutons de contrôle en bas de l'écran (texte seulement)"""
    # Bouton Quit (texte seulement)
    quit_text = font.render("Quit", True, WHITE)
    screen.blit(quit_text, (30, SCREEN_HEIGHT - 45))
    
    # Bouton Restart (texte seulement)
    restart_text = font.render("Restart", True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH//2 - 40, SCREEN_HEIGHT - 45))
    
    # Bouton Menu (texte seulement)
    menu_text = font.render("Menu", True, WHITE)
    screen.blit(menu_text, (SCREEN_WIDTH - 90, SCREEN_HEIGHT - 45))

def check_button_click(pos):
    """Vérifie quel bouton a été cliqué (zones approximatives autour du texte)"""
    x, y = pos
    
    # Zones cliquables approximatives (adaptez selon la taille de votre texte)
    if 10 <= x <= 110 and SCREEN_HEIGHT - 50 <= y <= SCREEN_HEIGHT - 10:  # Quit
        return "quit"
    if SCREEN_WIDTH//2 - 50 <= x <= SCREEN_WIDTH//2 + 50 and SCREEN_HEIGHT - 50 <= y <= SCREEN_HEIGHT - 10:  # Restart
        return "restart"
    if SCREEN_WIDTH - 110 <= x <= SCREEN_WIDTH - 10 and SCREEN_HEIGHT - 50 <= y <= SCREEN_HEIGHT - 10:  # Menu
        return "menu"
    
    return None
def handle_stats_screen(screen, grille, stats_data):
    screen.fill(BG_COLOR)
    dessiner_grille(screen, grille)
    afficher_flags(screen, grille.num_mines - grille.flags_places, grille.num_mines)
    afficher_chrono(screen, stats_data['time'])
    afficher_stats(screen, stats_data['time'], stats_data['clicks'], stats_data['efficiency'], stats_data['result'])
        
    draw_control_buttons()
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = check_button_click(event.pos)
                if action:
                    return action
    return None

def show_welcome_screen():
    show_welcome = True
    while show_welcome:
        screen.fill(BG_COLOR)
        welcome_font = pygame.font.SysFont('Consolas', 60)
        welcome_text = welcome_font.render("DÉMINEUR", True, BLACK)
        welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        screen.blit(welcome_text, welcome_rect)

        start_font = pygame.font.SysFont('Consolas', 30)
        start_text = start_font.render("START", True, BLACK)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH//2-70, SCREEN_HEIGHT//2-25, 140, 50))
        screen.blit(start_text, start_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    show_welcome = False

def choose_difficulty():
    while True:
        screen.fill(BG_COLOR)
        font = pygame.font.SysFont('Consolas', 50)
        title_text = font.render("Démineur", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)

        font = pygame.font.SysFont('Consolas', 30)
        easy_text = font.render("Facile", True, BLACK)
        medium_text = font.render("Moyen", True, BLACK)
        hard_text = font.render("Difficile", True, BLACK)

        easy_rect = easy_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        medium_rect = medium_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        hard_rect = hard_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if easy_rect.collidepoint(x, y):
                    return 9, 9, 10
                elif medium_rect.collidepoint(x, y):
                    return 14, 14, 30
                elif hard_rect.collidepoint(x, y):
                    return 16, 16, 50

def play_game(grille_lignes, grille_colonnes, num_mines):
    grille = Grille(grille_lignes, grille_colonnes, num_mines)
    ai_player = AIPlayer()
    ai_visualizer = AIVisualizer()

    jeu_demarre = False
    temps_debut = 0
    temps_ecoule = 0
    clicks = 1
    revealed = 0
    play = True
    AIturn = False  # Indique si c'est le tour de l'IA de jouer
    AI_thinking_time = 100  # Temps de réflexion de l'IA
    AI_thinking_time_max = 100  # Temps de réflexion maximum de l'IA
    
     
    move = {"position": None, "action": None, "position": None}

    while play:
        
        if jeu_demarre and not grille.game_over:
            temps_ecoule = pygame.time.get_ticks() - temps_debut

        screen.fill(BG_COLOR)
        dessiner_grille(screen, grille)
        afficher_flags(screen, grille.num_mines - grille.flags_places, grille.num_mines)
        #Ajouter un message visuel ou indicateur : “Tour du joueur / Tour de l’IA”.
        if AIturn:
            afficher_message(screen, "AI is thinking...")
            AI_thinking_time -= 1 
        else:
            
            afficher_message(screen, "Tour du joueur")
            
        

        if jeu_demarre:
            afficher_chrono(screen, temps_ecoule)

        draw_control_buttons()
        pygame.display.flip()
        
        # add a visual message for the player playing the game
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = check_button_click(event.pos)
                if action == "quit":
                    pygame.quit()
                    exit()
                elif action == "restart":
                    return "restart"
                elif action == "menu":
                    return "menu"

                x, y = event.pos
                if y >= 50:
                    col = x // CELL_SIZE
                    lig = (y - 50) // CELL_SIZE
                    if 0 <= lig < grille_lignes and 0 <= col < grille_colonnes and not grille.game_over:
                        if not jeu_demarre:
                            jeu_demarre = True
                            temps_debut = pygame.time.get_ticks()

                        if event.button == 3 and AI_thinking_time == AI_thinking_time_max:  # clic droit
                            AIturn = True
                            grille.put_flag(lig, col)
                            move = {"position": (lig, col), "action": "flag"}
                            clicks += 1
                             # Indique que c'est le tour de l'IA après un clic droit
                        elif event.button == 1 and AI_thinking_time == AI_thinking_time_max:  # clic gauche
                            AIturn = True
                            if not grille.cells[lig][col].flagged:
                                if grille.reveal_cell(lig, col):
                                    clicks += 1
                                    revealed += 1
                                    move = {"position": (lig, col), "action": "click"}
                                    if grille.cells[lig][col].has_mine:
                                        print("Vous avez cliqué sur une mine !")
                                        grille.game_over = True

        ai_player.observe_player(move)  # Observer le coup du joueur
        
        if not grille.game_over and jeu_demarre and AIturn == True and AI_thinking_time == 0:
            ai_move = ai_player.play(grille)
            print(f"IA a clické sur cette cellule : {ai_move}")
            
            AIturn = False  # Réinitialiser le tour de l'IA après son mouvement
            AI_thinking_time = AI_thinking_time_max # Réinitialiser le temps de réflexion de l'IA
            if ai_move:
                lig, col = ai_move
                if not grille.cells[lig][col].revealed and not grille.cells[lig][col].flagged:
                    if grille.reveal_cell(lig, col):
                        clicks += 1
                        revealed += 1
                        if grille.cells[lig][col].has_mine:
                            print("L'IA a cliqué sur une mine !")
                            grille.game_over = True
                            

        # Visualisation IA
        ai_data = {
            "danger_map": ai_player.danger_map,
            "safe_cells": list(ai_player.safe_cells),
            "last_move": ai_player.last_move
        }
        ai_visualizer.draw_overlay(screen, ai_data, CELL_SIZE)

        if grille.game_over or verifier_victoire(grille, grille_lignes, grille_colonnes):
            efficacite = (revealed / clicks) * 100 if clicks > 0 else 0
            stats_data = {
                'time': temps_ecoule,
                'clicks': clicks,
                'efficiency': efficacite,
                'result': "VICTOIRE !" if grille.victoire else "PERDU !",
                'grille': grille
            }
            action = handle_stats_screen(screen, grille, stats_data)
            if action == "quit":
                pygame.quit()
                exit()
            elif action == "restart":
                return "restart"
            elif action == "menu":
                return "menu"

def main():
    pygame.init()
    
    while True:
        show_welcome_screen()
        grille_lignes, grille_colonnes, num_mines = choose_difficulty()
        action = play_game(grille_lignes, grille_colonnes, num_mines)
        if action == "menu":
            continue
        elif action == "restart":
            continue
        else:
            break
    pygame.quit()

if __name__ == "__main__":
    main()
