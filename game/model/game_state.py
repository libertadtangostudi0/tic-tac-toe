# model/game_state.py
from config import GRID_SIZE
from model.board import Board
from rules.check_winner import check_winner
from rules.turns import next_player
from logger_config import logger


class GameState:
    """Represents a single match of tic-tac-toe."""

    def __init__(self, board_size: int = GRID_SIZE, win_length: int | None = None):
        self.board_size = board_size
        self.win_length = win_length or board_size
        self.board = Board(board_size)
        self.current_player = 1
        self.winner = None
        self.running = True

    def apply_settings(self, board_size: int, win_length: int) -> None:
        """Apply new board settings and restart the game."""
        logger.debug(
            f"GameState: applying settings board_size={board_size}, win_length={win_length}"
        )
        self.board_size = board_size
        self.win_length = win_length
        self.restart()

    def apply_move(self, row: int, col: int) -> None:
        """Apply a single move for the current player."""
        if self.winner is not None:
            logger.debug("Move ignored: game already finished")
            return

        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            logger.debug(f"Move ignored: out of range row={row}, col={col}")
            return

        if not self.board.is_empty(row, col):
            logger.debug(f"Move ignored: cell not empty row={row}, col={col}")
            return

        logger.debug(f"Move: player={self.current_player}, row={row}, col={col}")
        self.board.set(row, col, self.current_player)

        self.winner = check_winner(self.board.data, self.win_length)

        if self.winner is None:
            self.current_player = next_player(self.current_player)
        else:
            if self.winner == 1:
                logger.info("Winner: X")
            elif self.winner == -1:
                logger.info("Winner: O")
            else:
                logger.info("Draw")

    def restart(self) -> None:
        logger.debug("Game restarted")
        self.board = Board(self.board_size)
        self.current_player = 1
        self.winner = None
        self.running = True