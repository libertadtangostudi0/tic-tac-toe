# app.py
import sys
import pygame

from logger_config import logger
from ui.window_manager import WindowManager
from ui.menu.menu import MenuState, draw_menu, handle_menu_event
from ui.controller import handle_event
from ui.renderer import draw_all
from ui.screen_options import draw_options, handle_options_event
from ui.screen_themes import draw_themes, handle_themes_event
from model.game_state import GameState
from rules.check_winner import check_winner
from themes.theme_loader import load_themes


def run() -> None:
    pygame.init()
    logger.info("Game started")

    win = WindowManager()
    clock = pygame.time.Clock()

    state = GameState()
    menu_state = MenuState()

    themes = load_themes()

    mode = "menu"

    while state.running:
        for event in pygame.event.get():
            if mode == "menu":
                prev_mode = mode
                mode = handle_menu_event(event, win, menu_state, mode, state)
                if mode != prev_mode and mode == "game":
                    # apply board settings when starting game
                    state.board_size = menu_state.board_size
                    state.restart()
            elif mode == "options":
                mode = handle_options_event(event, win, menu_state, mode, state)
            elif mode == "themes":
                mode = handle_themes_event(event, win, menu_state, mode, state, themes)
            else:
                # game mode
                handle_event(event, win, state)

        if mode == "menu":
            draw_menu(win.base_surface, menu_state)
        elif mode == "options":
            draw_options(win.base_surface, menu_state)
        elif mode == "themes":
            draw_themes(win.base_surface, menu_state, themes)
        else:
            # game mode

            # if animated theme is active, choose current frame
            if menu_state.animation_frames_x and menu_state.animation_frame_duration_ms > 0:
                now = pygame.time.get_ticks()
                frame_count = len(menu_state.animation_frames_x)
                idx = (now // menu_state.animation_frame_duration_ms) % frame_count
                menu_state.player_x_image = menu_state.animation_frames_x[idx]

                if menu_state.animation_frames_o:
                    idx_o = (now // menu_state.animation_frame_duration_ms) % len(
                        menu_state.animation_frames_o
                    )
                    menu_state.player_o_image = menu_state.animation_frames_o[idx_o]

            draw_all(
                win.base_surface,
                state.board.data,
                menu_state.player_x_image,
                menu_state.player_o_image,
            )

        win.clear()
        win.blit_scaled_centered()
        pygame.display.flip()

        clock.tick(menu_state.fps)

    logger.info("Game terminated")
    pygame.quit()
    sys.exit()
