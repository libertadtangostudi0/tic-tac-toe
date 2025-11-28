import pygame

from config import BASE_SIZE, GRID_SIZE, FPS
from logger_config import logger


class MenuState:
    """Holds menu configuration and selected options."""

    def __init__(self) -> None:
        logger.debug("MenuState: initializing")

        # theme-related
        self.player_x_image = None
        self.player_o_image = None
        self.selected_theme_id = "classic"
        self.selected_theme_name = "Classic X/O"

        # Animation (for animated themes)
        self.animation_frames_x = []
        self.animation_frames_o = []
        self.animation_frame_duration_ms = 0

        # game options
        self.board_size = GRID_SIZE
        self.win_length = GRID_SIZE
        self.fps = FPS

        # game mode flags
        self.vs_bot = None  # None = not chosen, False = vs player, True = vs bot

        self.font = pygame.font.SysFont(None, 36)

        button_width = int(BASE_SIZE * 0.7)
        button_height = 50
        gap = 20
        buttons_count = 4

        total_height = buttons_count * button_height + (buttons_count - 1) * gap
        top = (BASE_SIZE - total_height) // 2
        x = (BASE_SIZE - button_width) // 2

        self.buttons = {
            "vs_player": pygame.Rect(x, top, button_width, button_height),
            "vs_bot": pygame.Rect(
                x, top + (button_height + gap), button_width, button_height
            ),
            "options": pygame.Rect(
                x, top + 2 * (button_height + gap), button_width, button_height
            ),
            "themes": pygame.Rect(
                x, top + 3 * (button_height + gap), button_width, button_height
            ),
        }

        logger.debug("MenuState: buttons initialized")


def draw_button(surface: pygame.Surface, rect: pygame.Rect, text: str,
                font: pygame.font.Font, active: bool = False) -> None:
    """Draw a simple rounded button."""
    bg = (120, 120, 120) if active else (90, 90, 90)
    border = (230, 230, 230)
    text_color = (255, 255, 255)

    pygame.draw.rect(surface, bg, rect, border_radius=10)
    pygame.draw.rect(surface, border, rect, width=2, border_radius=10)

    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)


def draw_menu(surface: pygame.Surface, menu_state: MenuState) -> None:
    logger.trace("Menu: drawing menu frame")

    surface.fill((20, 20, 20))

    draw_button(surface, menu_state.buttons["vs_player"], "Play vs Player", menu_state.font)
    draw_button(surface, menu_state.buttons["vs_bot"], "Play vs Bot", menu_state.font)
    draw_button(surface, menu_state.buttons["options"], "Options", menu_state.font)
    draw_button(surface, menu_state.buttons["themes"], "Themes", menu_state.font)

    # info block under last button
    info_font = pygame.font.SysFont(None, 24)
    info_lines = [
        f"Board: {menu_state.board_size}x{menu_state.board_size}",
        f"Win length: {menu_state.win_length}",
        f"FPS: {menu_state.fps}",
        f"Theme: {menu_state.selected_theme_name}",
    ]

    last_rect = menu_state.buttons["themes"]
    y = last_rect.bottom + 10
    for line in info_lines:
        label = info_font.render(line, True, (230, 230, 230))
        rect = label.get_rect(center=(BASE_SIZE // 2, y))
        surface.blit(label, rect)
        y += label.get_height() + 2


def handle_menu_event(event, win, menu_state: MenuState, mode: str, state) -> str:
    """Process input in main menu. Returns new mode."""
    import pygame as _pg

    if event.type == _pg.QUIT:
        logger.info("Menu: QUIT event")
        state.running = False
        return mode

    if event.type != _pg.MOUSEBUTTONDOWN:
        return mode

    inside, bx, by = win.map_window_to_board(event.pos)
    if not inside:
        logger.debug("Menu: click outside board")
        return mode

    point = (bx, by)

    if menu_state.buttons["vs_player"].collidepoint(point):
        logger.info("Menu: switching to 'Player vs Player' mode")
        menu_state.vs_bot = False
        return "game"

    if menu_state.buttons["vs_bot"].collidepoint(point):
        logger.info("Menu: switching to 'Player vs Bot' mode")
        menu_state.vs_bot = True
        return "game"

    if menu_state.buttons["options"].collidepoint(point):
        logger.info("Menu: switching to 'Options' screen")
        return "options"

    if menu_state.buttons["themes"].collidepoint(point):
        logger.info("Menu: switching to 'Themes' screen")
        return "themes"

    logger.debug("Menu: click on empty area")
    return mode
