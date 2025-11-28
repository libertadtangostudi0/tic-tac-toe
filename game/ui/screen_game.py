# game/ui/screen_game.py

from ui.renderer import draw_all


def draw_game(surface, state, menu_state) -> None:
    """
    Draw the main game screen using current game and menu state.

    surface    - pygame Surface to render on
    state      - GameState instance
    menu_state - MenuState instance (contains selected images)
    """
    board_matrix = state.board.data
    draw_all(
        surface,
        board_matrix,
        menu_state.player_x_image,
        menu_state.player_o_image,
    )