import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import pygame
from logger_config import logger
from config import BASE_SIZE, GRID_SIZE


ThemeDict = Dict[str, Any]


def _themes_json_path() -> Path:
    """Return path to themes.json."""
    return Path(__file__).with_name("themes.json")


def load_themes() -> List[ThemeDict]:
    """Load themes description from themes.json.

    Returns list of dicts. If file is missing or invalid, returns builtin only.
    """
    path = _themes_json_path()

    if not path.exists():
        logger.error(f"themes.json not found at: {path}")
        return [
            {"id": "classic", "name": "Classic X/O", "type": "builtin"},
        ]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.error(f"Failed to read themes.json: {exc}")
        return [
            {"id": "classic", "name": "Classic X/O", "type": "builtin"},
        ]

    themes = data.get("themes")
    if not isinstance(themes, list) or not themes:
        logger.error("themes.json has no valid 'themes' list")
        return [
            {"id": "classic", "name": "Classic X/O", "type": "builtin"},
        ]

    # ensure builtin classic exists
    if not any(t.get("id") == "classic" for t in themes):
        themes.insert(0, {"id": "classic", "name": "Classic X/O", "type": "builtin"})

    return themes


def _load_image_from_theme(base_dir: Path, rel_path: str) -> Optional[pygame.Surface]:
    """Load image for mark from theme folder."""
    full_path = base_dir / rel_path
    if not full_path.exists():
        logger.error(f"Theme image not found: {full_path}")
        return None

    try:
        image = pygame.image.load(str(full_path)).convert_alpha()
    except Exception as exc:
        logger.error(f"Failed to load theme image {full_path}: {exc}")
        return None

    return image


def _split_strip_to_frames(strip: pygame.Surface, frames: int) -> List[pygame.Surface]:
    """Split horizontal strip into a list of frame surfaces."""
    if frames <= 0:
        return []

    width = strip.get_width()
    height = strip.get_height()
    frame_width = width // frames

    result: List[pygame.Surface] = []
    for i in range(frames):
        rect = pygame.Rect(i * frame_width, 0, frame_width, height)
        frame = strip.subsurface(rect).copy()
        result.append(frame)
    return result


def apply_theme(menu_state, theme: ThemeDict) -> None:
    """Apply selected theme to menu_state (set images and metadata)."""
    theme_id = theme.get("id", "classic")
    theme_name = theme.get("name", theme_id)
    theme_type = theme.get("type", "builtin")

    menu_state.selected_theme_id = theme_id
    menu_state.selected_theme_name = theme_name

    # reset animation by default
    menu_state.animation_frames_x = []
    menu_state.animation_frames_o = []
    menu_state.animation_frame_duration_ms = 0

    # 1) builtin: standart X/O
    if theme_type == "builtin":
        menu_state.player_x_image = None
        menu_state.player_o_image = None
        return

    base_dir = _themes_json_path().parent

    # 2) static images
    if theme_type == "image":
        x_rel = theme.get("x_image")
        o_rel = theme.get("o_image")

        if not x_rel or not o_rel:
            logger.error("Image theme must have 'x_image' and 'o_image'")
            menu_state.player_x_image = None
            menu_state.player_o_image = None
            return

        x_img = _load_image_from_theme(base_dir, x_rel)
        o_img = _load_image_from_theme(base_dir, o_rel)

        if x_img is None or o_img is None:
            logger.error("Failed to load theme images, keeping previous")
            return

        from config import BASE_SIZE, GRID_SIZE  # локальный импорт, чтобы избежать циклов

        cell_size = BASE_SIZE // GRID_SIZE
        target_size = int(cell_size * 0.8)

        menu_state.player_x_image = pygame.transform.smoothscale(
            x_img, (target_size, target_size)
        )
        menu_state.player_o_image = pygame.transform.smoothscale(
            o_img, (target_size, target_size)
        )
        return

    # 3) animated theme
    if theme_type == "animated":
        x_strip_rel = theme.get("x_strip")
        o_strip_rel = theme.get("o_strip")
        frames = int(theme.get("frames", 1))
        frame_duration = int(theme.get("frame_duration_ms", 80))

        if not x_strip_rel or not o_strip_rel or frames <= 0:
            logger.error("Animated theme needs 'x_strip', 'o_strip' and positive 'frames'")
            return

        x_strip = _load_image_from_theme(base_dir, x_strip_rel)
        o_strip = _load_image_from_theme(base_dir, o_strip_rel)

        if x_strip is None or o_strip is None:
            logger.error("Failed to load animated strips, keeping previous")
            return

        cell_size = BASE_SIZE // GRID_SIZE
        target_size = int(cell_size * 0.8)

        x_frames = _split_strip_to_frames(x_strip, frames)
        o_frames = _split_strip_to_frames(o_strip, frames)

        if not x_frames or not o_frames:
            logger.error("Animated theme produced no frames")
            return

        scaled_x_frames: list[pygame.Surface] = []
        scaled_o_frames: list[pygame.Surface] = []

        for f in x_frames:
            scaled_x_frames.append(
                pygame.transform.smoothscale(f, (target_size, target_size))
            )
        for f in o_frames:
            scaled_o_frames.append(
                pygame.transform.smoothscale(f, (target_size, target_size))
            )

        menu_state.animation_frames_x = scaled_x_frames
        menu_state.animation_frames_o = scaled_o_frames
        menu_state.animation_frame_duration_ms = frame_duration

        
        menu_state.player_x_image = scaled_x_frames[0]
        menu_state.player_o_image = scaled_o_frames[0]

        logger.info(
            f"Animated theme applied: {theme_id}, frames={frames}, duration={frame_duration}ms"
        )
        return

    # unknown type
    logger.error(f"Unknown theme type: {theme_type}")
