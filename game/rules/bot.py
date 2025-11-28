# rules/bot.py
import random


def bot_move(board, player):
    empty = []
    size = len(board.data)

    for r in range(size):
        for c in range(size):
            if board.data[r][c] == 0:
                empty.append((r, c))

    if not empty:
        return None

    return random.choice(empty)