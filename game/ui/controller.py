import pygame

from config import BASE_SIZE
from logger_config import logger


def handle_event(event, win, state) -> None:
    """Handle single pygame event."""
    if event.type == pygame.QUIT:
        logger.info("Quit event received")
        state.running = False
        return

    if event.type == pygame.MOUSEBUTTONDOWN:
        handle_mouse_click(event.pos, win, state)


def handle_mouse_click(pos, win, state) -> None:
    """Handle mouse click based on current game state."""
    logger.debug(f"Mouse click at pos={pos}")

    # If game has finished, any click inside board restarts the game
    if state.winner is not None:
        inside, _, _ = win.map_window_to_board(pos)
        if inside:
            logger.debug("Click inside board after game end -> restart")
            state.restart()
        else:
            logger.debug("Click outside board after game end -> ignored")
        return

    inside, bx, by = win.map_window_to_board(pos)
    if not inside:
        logger.debug("Click outside board -> ignored")
        return

    size = state.board_size
    if size <= 0:
        logger.debug("Invalid board size -> ignored click")
        return

    cell_size = BASE_SIZE // size

    col = int(bx // cell_size)
    row = int(by // cell_size)

    if not (0 <= col < size and 0 <= row < size):
        logger.debug(f"Click mapped out of range (row={row}, col={col}) -> ignored")
        return

    state.apply_move(row, col)