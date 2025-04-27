import pygame

class AIVisualizer:
    def __init__(self):
        self.debug_mode = False
        self.colors = {
            "danger": (255, 0, 0, 100),  # Rouge transparent
            "safe": (0, 255, 0, 100),    # Vert transparent
            "ai_move": (0, 0, 255, 150)   # Bleu transparent
        }

    def toggle_debug(self):
        """Active/désactive le mode debug visuel."""
        self.debug_mode = not self.debug_mode

    def draw_overlay(self, screen, ai_data, cell_size, y_offset=50):
        """Affiche les infos de l'IA sur la grille."""
        if not self.debug_mode:
            return

        # Cases dangereuses (rouge)
        for (x, y), danger in ai_data.get("danger_map", {}).items():
            alpha = min(int(danger * 50), 100)  # Opacité proportionnelle au danger
            s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            s.fill((255, 0, 0, alpha))
            screen.blit(s, (x * cell_size, y * cell_size + y_offset))

        # Cases sûres (vert)
        for (x, y) in ai_data.get("safe_cells", []):
            s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            s.fill((0, 255, 0, 100))
            screen.blit(s, (x * cell_size, y * cell_size + y_offset))

    def highlight_ai_move(self, screen, move, cell_size, y_offset=50):
        """Surligne le dernier coup de l'IA en bleu."""
        if move:
            x, y = move
            s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            s.fill((0, 0, 255, 150))
            screen.blit(s, (x * cell_size, y * cell_size + y_offset))
