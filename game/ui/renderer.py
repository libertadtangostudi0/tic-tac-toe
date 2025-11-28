import pygame

from config import (
    BASE_SIZE,
    BG_COLOR,
    LINE_COLOR,
    X_COLOR,
    O_COLOR,
    LINE_WIDTH,
    MARK_WIDTH,
)


def _cell_size_from_board(board) -> int:
    """Calculate cell size based on board size and base surface size."""
    size = len(board)
    if size <= 0:
        return BASE_SIZE
    return BASE_SIZE // size


def _scale_image_to_cell(image: pygame.Surface, cell_size: int) -> pygame.Surface:
    """
    Scale image to fit inside a single cell without overlapping grid lines.

    Keeps aspect ratio and leaves a small padding from the grid lines.
    """
    if image is None:
        return image

    # Safe inner area: remove grid line thickness from each side and add small padding.
    inner_size = cell_size - 2 * LINE_WIDTH
    inner_size = max(inner_size - 2, 1)

    src_w, src_h = image.get_size()
    if src_w <= 0 or src_h <= 0:
        return image

    scale = min(inner_size / src_w, inner_size / src_h)
    target_w = max(int(src_w * scale), 1)
    target_h = max(int(src_h * scale), 1)

    return pygame.transform.smoothscale(image, (target_w, target_h))


def draw_grid(surface: pygame.Surface, board) -> None:
    """Draw grid lines on the base surface for the given board."""
    size = len(board)
    cell_size = _cell_size_from_board(board)

    # vertical lines
    x = cell_size
    for _ in range(1, size):
        pygame.draw.line(surface, LINE_COLOR, (x, 0), (x, BASE_SIZE), LINE_WIDTH)
        x += cell_size

    # horizontal lines
    y = cell_size
    for _ in range(1, size):
        pygame.draw.line(surface, LINE_COLOR, (0, y), (BASE_SIZE, y), LINE_WIDTH)
        y += cell_size


def draw_marks(
    surface: pygame.Surface,
    board,
    player_x_image: pygame.Surface | None = None,
    player_o_image: pygame.Surface | None = None,
) -> None:
    """
    Draw marks on the board.

    If player_x_image / player_o_image are provided, they are scaled
    to fit current cell size for any board dimension.
    """
    size = len(board)
    cell_size = _cell_size_from_board(board)

    scaled_x: pygame.Surface | None = None
    scaled_o: pygame.Surface | None = None

    if player_x_image is not None:
        scaled_x = _scale_image_to_cell(player_x_image, cell_size)

    if player_o_image is not None:
        scaled_o = _scale_image_to_cell(player_o_image, cell_size)

    for row in range(size):
        for col in range(size):
            value = board[row][col]
            if value == 0:
                continue

            cx = col * cell_size + cell_size // 2
            cy = row * cell_size + cell_size // 2

            if value == 1:
                # Player X
                if scaled_x is not None:
                    rect = scaled_x.get_rect(center=(cx, cy))
                    surface.blit(scaled_x, rect)
                else:
                    offset = cell_size // 3
                    pygame.draw.line(
                        surface,
                        X_COLOR,
                        (cx - offset, cy - offset),
                        (cx + offset, cy + offset),
                        MARK_WIDTH,
                    )
                    pygame.draw.line(
                        surface,
                        X_COLOR,
                        (cx - offset, cy + offset),
                        (cx + offset, cy - offset),
                        MARK_WIDTH,
                    )
            elif value == -1:
                # Player O
                if scaled_o is not None:
                    rect = scaled_o.get_rect(center=(cx, cy))
                    surface.blit(scaled_o, rect)
                else:
                    radius = cell_size // 3
                    pygame.draw.circle(
                        surface,
                        O_COLOR,
                        (cx, cy),
                        radius,
                        MARK_WIDTH,
                    )


def draw_all(
    surface: pygame.Surface,
    board,
    player_x_image: pygame.Surface | None = None,
    player_o_image: pygame.Surface | None = None,
) -> None:
    """Draw full board: background, grid and marks."""
    surface.fill(BG_COLOR)
    draw_grid(surface, board)
    draw_marks(surface, board, player_x_image, player_o_image)
