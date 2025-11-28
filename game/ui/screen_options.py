import pygame

from config import BASE_SIZE
from logger_config import logger

MIN_BOARD_SIZE = 3
MAX_BOARD_SIZE = 10
MIN_WIN_LENGTH = 3

MIN_FPS = 30
MAX_FPS = 240
FPS_STEP = 10


def _build_controls():
    button_width = int(BASE_SIZE * 0.9)
    row_height = 50
    gap = 15

    rows = 4  # board, win, fps, back
    total_height = rows * row_height + (rows - 1) * gap
    top = (BASE_SIZE - total_height) // 2
    x = (BASE_SIZE - button_width) // 2

    controls = {}

    def three_part_row(row_index: int, key_prefix: str) -> None:
        y = top + row_index * (row_height + gap)
        minus_rect = pygame.Rect(x, y, row_height, row_height)
        plus_rect = pygame.Rect(x + button_width - row_height, y, row_height, row_height)
        label_rect = pygame.Rect(
            minus_rect.right + 10,
            y,
            button_width - 2 * row_height - 20,
            row_height,
        )
        controls[f"{key_prefix}_minus"] = minus_rect
        controls[f"{key_prefix}_plus"] = plus_rect
        controls[f"{key_prefix}_label"] = label_rect

    three_part_row(0, "board")
    three_part_row(1, "win")
    three_part_row(2, "fps")

    y_back = top + 3 * (row_height + gap)
    controls["back"] = pygame.Rect(x, y_back, button_width, row_height)

    return controls


def _ensure_limits(menu_state) -> None:
    if menu_state.board_size < MIN_BOARD_SIZE:
        menu_state.board_size = MIN_BOARD_SIZE
    if menu_state.board_size > MAX_BOARD_SIZE:
        menu_state.board_size = MAX_BOARD_SIZE

    if menu_state.win_length < MIN_WIN_LENGTH:
        menu_state.win_length = MIN_WIN_LENGTH
    if menu_state.win_length > menu_state.board_size:
        menu_state.win_length = menu_state.board_size

    if menu_state.fps < MIN_FPS:
        menu_state.fps = MIN_FPS
    if menu_state.fps > MAX_FPS:
        menu_state.fps = MAX_FPS


def draw_options(surface: pygame.Surface, menu_state) -> None:
    logger.trace("Options: drawing options screen")

    surface.fill((15, 15, 15))

    title_font = pygame.font.SysFont(None, 40)
    font = pygame.font.SysFont(None, 30)

    title = title_font.render("Settings", True, (230, 230, 230))
    title_rect = title.get_rect(center=(BASE_SIZE // 2, 40))
    surface.blit(title, title_rect)

    controls = _build_controls()

    minus_label = font.render("-", True, (230, 230, 230))
    plus_label = font.render("+", True, (230, 230, 230))

    # board size
    pygame.draw.rect(surface, (80, 80, 80), controls["board_minus"], border_radius=8)
    pygame.draw.rect(surface, (200, 200, 200), controls["board_minus"], width=2, border_radius=8)
    surface.blit(minus_label, minus_label.get_rect(center=controls["board_minus"].center))

    pygame.draw.rect(surface, (80, 80, 80), controls["board_plus"], border_radius=8)
    pygame.draw.rect(surface, (200, 200, 200), controls["board_plus"], width=2, border_radius=8)
    surface.blit(plus_label, plus_label.get_rect(center=controls["board_plus"].center))

    text = f"Board size: {menu_state.board_size}x{menu_state.board_size}"
    lbl = font.render(text, True, (230, 230, 230))
    surface.blit(lbl, lbl.get_rect(center=controls["board_label"].center))

    # win length
    pygame.draw.rect(surface, (80, 80, 80), controls["win_minus"], border_radius=8)
    pygame.draw.rect(surface, (200, 200, 200), controls["win_minus"], width=2, border_radius=8)
    surface.blit(minus_label, minus_label.get_rect(center=controls["win_minus"].center))

    pygame.draw.rect(surface, (80, 80, 80), controls["win_plus"], border_radius=8)
    pygame.draw.rect(surface, (200, 200, 200), controls["win_plus"], width=2, border_radius=8)
    surface.blit(plus_label, plus_label.get_rect(center=controls["win_plus"].center))

    text = f"Win length: {menu_state.win_length}"
    lbl = font.render(text, True, (230, 230, 230))
    surface.blit(lbl, lbl.get_rect(center=controls["win_label"].center))

    # fps
    pygame.draw.rect(surface, (80, 80, 80), controls["fps_minus"], border_radius=8)
    pygame.draw.rect(surface, (200, 200, 200), controls["fps_minus"], width=2, border_radius=8)
    surface.blit(minus_label, minus_label.get_rect(center=controls["fps_minus"].center))

    pygame.draw.rect(surface, (80, 80, 80), controls["fps_plus"], border_radius=8)
    pygame.draw.rect(surface, (200, 200, 200), controls["fps_plus"], width=2, border_radius=8)
    surface.blit(plus_label, plus_label.get_rect(center=controls["fps_plus"].center))

    text = f"FPS: {menu_state.fps}"
    lbl = font.render(text, True, (230, 230, 230))
    surface.blit(lbl, lbl.get_rect(center=controls["fps_label"].center))

    # back
    back_rect = controls["back"]
    pygame.draw.rect(surface, (90, 90, 90), back_rect, border_radius=8)
    pygame.draw.rect(surface, (220, 220, 220), back_rect, width=2, border_radius=8)
    back_label = font.render("Back", True, (230, 230, 230))
    surface.blit(back_label, back_label.get_rect(center=back_rect.center))


def handle_options_event(event, win, menu_state, mode: str, state) -> str:
    import pygame as _pg

    if event.type == _pg.QUIT:
        logger.info("Options: QUIT event")
        state.running = False
        return mode

    if event.type != _pg.MOUSEBUTTONDOWN:
        return mode

    inside, bx, by = win.map_window_to_board(event.pos)
    if not inside:
        return mode

    controls = _build_controls()
    point = (bx, by)

    if controls["board_minus"].collidepoint(point):
        menu_state.board_size -= 1
        _ensure_limits(menu_state)
        logger.debug(f"Options: board_size -> {menu_state.board_size}")
        return mode

    if controls["board_plus"].collidepoint(point):
        menu_state.board_size += 1
        _ensure_limits(menu_state)
        logger.debug(f"Options: board_size -> {menu_state.board_size}")
        return mode

    if controls["win_minus"].collidepoint(point):
        menu_state.win_length -= 1
        _ensure_limits(menu_state)
        logger.debug(f"Options: win_length -> {menu_state.win_length}")
        return mode

    if controls["win_plus"].collidepoint(point):
        menu_state.win_length += 1
        _ensure_limits(menu_state)
        logger.debug(f"Options: win_length -> {menu_state.win_length}")
        return mode

    if controls["fps_minus"].collidepoint(point):
        menu_state.fps -= FPS_STEP
        _ensure_limits(menu_state)
        logger.debug(f"Options: fps -> {menu_state.fps}")
        return mode

    if controls["fps_plus"].collidepoint(point):
        menu_state.fps += FPS_STEP
        _ensure_limits(menu_state)
        logger.debug(f"Options: fps -> {menu_state.fps}")
        return mode

    if controls["back"].collidepoint(point):
        logger.info("Options: back to main menu")
        return "menu"

    return mode
