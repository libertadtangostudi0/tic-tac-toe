import pygame

from config import BASE_SIZE
from logger_config import logger
from themes.theme_loader import apply_theme, ThemeDict


def _theme_rects(themes: list[ThemeDict]):
    button_width = int(BASE_SIZE * 0.8)
    button_height = 40
    gap = 10

    total_height = len(themes) * button_height + (len(themes) - 1) * gap + 60
    top = (BASE_SIZE - total_height) // 2 + 40
    x = (BASE_SIZE - button_width) // 2

    rects = []
    for idx, _ in enumerate(themes):
        y = top + idx * (button_height + gap)
        rects.append(pygame.Rect(x, y, button_width, button_height))

    # back button
    back_y = top + len(themes) * (button_height + gap) + 10
    back_rect = pygame.Rect(x, back_y, button_width, button_height)

    return rects, back_rect


def draw_themes(surface: pygame.Surface, menu_state, themes: list[ThemeDict]) -> None:
    logger.trace("Themes: drawing themes screen")

    surface.fill((15, 15, 15))

    title_font = pygame.font.SysFont(None, 40)
    font = pygame.font.SysFont(None, 28)

    title = title_font.render("Themes", True, (230, 230, 230))
    title_rect = title.get_rect(center=(BASE_SIZE // 2, 40))
    surface.blit(title, title_rect)

    rects, back_rect = _theme_rects(themes)

    for rect, theme in zip(rects, themes):
        is_active = theme.get("id") == getattr(menu_state, "selected_theme_id", "classic")
        bg = (110, 110, 110) if is_active else (70, 70, 70)
        border = (230, 230, 230) if is_active else (150, 150, 150)

        pygame.draw.rect(surface, bg, rect, border_radius=8)
        pygame.draw.rect(surface, border, rect, width=2, border_radius=8)

        name = theme.get("name", theme.get("id", "theme"))
        label = font.render(name, True, (230, 230, 230))
        surface.blit(label, label.get_rect(center=rect.center))

    # back button
    pygame.draw.rect(surface, (90, 90, 90), back_rect, border_radius=8)
    pygame.draw.rect(surface, (220, 220, 220), back_rect, width=2, border_radius=8)
    back_label = font.render("Back", True, (230, 230, 230))
    surface.blit(back_label, back_label.get_rect(center=back_rect.center))


def handle_themes_event(event, win, menu_state, mode: str, state,
                        themes: list[ThemeDict]) -> str:
    import pygame as _pg

    if event.type == _pg.QUIT:
        logger.info("Themes: QUIT event")
        state.running = False
        return mode

    if event.type != _pg.MOUSEBUTTONDOWN:
        return mode

    inside, bx, by = win.map_window_to_board(event.pos)
    if not inside:
        return mode

    rects, back_rect = _theme_rects(themes)
    point = (bx, by)

    for rect, theme in zip(rects, themes):
        if rect.collidepoint(point):
            apply_theme(menu_state, theme)
            logger.info(f"Themes: selected theme -> {menu_state.selected_theme_id}")
            return "menu"

    if back_rect.collidepoint(point):
        logger.info("Themes: back to main menu")
        return "menu"

    return mode
