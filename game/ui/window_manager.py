import pygame
from config import BASE_SIZE, BG_COLOR


class WindowManager:

    def __init__(self):
        self.screen = pygame.display.set_mode(
            (BASE_SIZE, BASE_SIZE),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Adaptive Tic-Tac-Toe")

        self.base_surface = pygame.Surface((BASE_SIZE, BASE_SIZE))


    def get_window_size(self):
        return self.screen.get_size()


    def clear(self):
        self.screen.fill(BG_COLOR)


    def blit_scaled_centered(self):
        win_w, win_h = self.get_window_size()
        side = min(win_w, win_h)

        scaled = pygame.transform.smoothscale(
            self.base_surface, (side, side)
        )

        ox = (win_w - side) // 2
        oy = (win_h - side) // 2

        self.screen.blit(scaled, (ox, oy))


    def map_window_to_board(self, pos):
        wx, wy = pos
        win_w, win_h = self.get_window_size()

        side = min(win_w, win_h)
        ox = (win_w - side) // 2
        oy = (win_h - side) // 2

        if not (ox <= wx < ox + side and oy <= wy < oy + side):
            return False, 0, 0

        scale = float(BASE_SIZE) / float(side)

        bx = (wx - ox) * scale
        by = (wy - oy) * scale

        return True, bx, by