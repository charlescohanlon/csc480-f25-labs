import random
import time
from typing import List, Tuple, Dict, Optional
from itertools import permutations

LETTER_VALUES: Dict[str, int] = {
    "A": 1,
    "B": 3,
    "C": 3,
    "D": 2,
    "E": 1,
    "F": 4,
    "G": 2,
    "H": 4,
    "I": 1,
    "J": 8,
    "K": 5,
    "L": 1,
    "M": 3,
    "N": 1,
    "O": 1,
    "P": 3,
    "Q": 10,
    "R": 1,
    "S": 1,
    "T": 1,
    "U": 1,
    "V": 4,
    "W": 4,
    "X": 8,
    "Y": 4,
    "Z": 10,
    "_": 0,
}
BOARD_SIZE = 15
RACK_SIZE = 7

# Predefined setup for board premiums
# 0=empty, 2=Double Letter, 3=Triple Letter, 4=Double Word, 5=Triple Word
PREMIUM_BOARD = [
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    [2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 2],
    [0, 0, 4, 0, 0, 0, 2, 0, 2, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0],
    [0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 2, 0, 2, 0, 0, 0, 4, 0, 0],
    [2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 2],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
]

with open("./words.txt") as f:
    DICTIONARY = set(word.strip().upper() for word in f if len(word.strip()) >= 2)


def is_valid_word(word: str) -> bool:
    """Checks if a word is valid."""
    return word.upper() in DICTIONARY


class Move:
    """Represents a potential action taken by a player."""

    def __init__(
        self,
        tiles_placed: List[Tuple[int, int, str]],
        score: int,
        is_pass: bool = False,
    ):
        self.tiles_placed = tiles_placed  # List of (row, col, letter)
        self.score = score
        self.is_pass = is_pass

    def __repr__(self):
        if self.is_pass:
            return "Pass Move"
        # Extract the word formed (simplified, assuming linear placement for representation)
        word = "".join([letter for _, _, letter in self.tiles_placed])
        tile_positions = [(r, c) for r, c, _ in self.tiles_placed]
        return (
            f"Move(Word='{word}', Score={self.score}, Tile Positions={tile_positions})"
        )

    def __eq__(self, value: "Move"):
        # Two Move objects are equal if all fields are equal
        return (
            all(
                tile1 == tile2
                for tile1, tile2 in zip(self.tiles_placed, value.tiles_placed)
            )
            and self.score == value.score
            and self.is_pass == value.is_pass
        )

    def __hash__(self):
        return hash((tuple(self.tiles_placed), self.is_pass))


class ScrabbleState:
    """Represents the current state of the Scrabble game."""

    def __init__(
        self,
        board: List[List[str]],
        tile_pool: List[str],
        racks: Dict[int, List[str]],
        current_player: int,
        scores: Dict[int, int],
    ):
        self.board = board
        self.tile_pool = tile_pool
        self.racks = racks
        self.current_player = current_player
        self.scores = scores
        self.passes_in_a_row = 0

    def __repr__(self) -> str:
        """Return a readable representation of the Scrabble game state."""

        # Helper function to display the board
        def format_board():
            lines = []
            lines.append("    " + " ".join(f"{i:2d}" for i in range(BOARD_SIZE)))
            lines.append("   +" + "---" * BOARD_SIZE + "+")
            for r in range(BOARD_SIZE):
                row_str = f"{r:2d} |"
                for c in range(BOARD_SIZE):
                    cell = self.board[r][c]
                    if cell == "":
                        # Show premium squares on empty cells
                        premium = PREMIUM_BOARD[r][c]
                        if premium == 2:
                            row_str += " ² "  # Double letter
                        elif premium == 3:
                            row_str += " ³ "  # Triple letter
                        elif premium == 4:
                            row_str += " * "  # Double word
                        elif premium == 5:
                            row_str += " # "  # Triple word
                        else:
                            row_str += " · "  # Empty
                    else:
                        row_str += f" {cell} "
                row_str += "|"
                lines.append(row_str)
            lines.append("   +" + "---" * BOARD_SIZE + "+")
            return "\n".join(lines)

        # Build the representation
        output = []
        output.append("=" * 60)
        output.append("SCRABBLE GAME STATE")
        output.append("=" * 60)

        # Current player and scores
        output.append(f"\nCurrent Player: Player {self.current_player}")
        output.append(f"Scores: Player 1: {self.scores[1]}, Player 2: {self.scores[2]}")
        output.append(f"Consecutive Passes: {self.passes_in_a_row}")

        # Player racks
        output.append(
            f"\nPlayer 1 Rack: {' '.join(self.racks[1])} ({len(self.racks[1])} tiles)"
        )
        output.append(
            f"Player 2 Rack: {' '.join(self.racks[2])} ({len(self.racks[2])} tiles)"
        )

        # Tile pool
        output.append(f"\nTiles Remaining in Pool: {len(self.tile_pool)}")

        # Board
        output.append("\nBoard:")
        output.append(
            "Legend: · = empty, ² = 2x letter, ³ = 3x letter, * = 2x word, # = 3x word"
        )
        output.append(format_board())

        # Terminal status
        if self.is_terminal():
            output.append("\n*** GAME OVER ***")
            winner = (
                1
                if self.scores[1] > self.scores[2]
                else (2 if self.scores[2] > self.scores[1] else None)
            )
            if winner:
                output.append(
                    f"Winner: Player {winner} with {self.scores[winner]} points!"
                )
            else:
                output.append("Game ended in a tie!")

        output.append("=" * 60)

        return "\n".join(output)

    @staticmethod
    def create_new_game() -> "ScrabbleState":
        """Factory function to create a new Scrabble game with initial setup."""
        # Initialize empty board
        board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Create tile pool with standard Scrabble distribution
        tile_distribution = {
            "A": 9,
            "B": 2,
            "C": 2,
            "D": 4,
            "E": 12,
            "F": 2,
            "G": 3,
            "H": 2,
            "I": 9,
            "J": 1,
            "K": 1,
            "L": 4,
            "M": 2,
            "N": 6,
            "O": 8,
            "P": 2,
            "Q": 1,
            "R": 6,
            "S": 4,
            "T": 6,
            "U": 4,
            "V": 2,
            "W": 2,
            "X": 1,
            "Y": 2,
            "Z": 1,
            "_": 2,  # '_' represents blank tiles
        }
        tile_pool = []
        for letter, count in tile_distribution.items():
            tile_pool.extend([letter] * count)
        random.shuffle(tile_pool)

        # Draw initial racks for both players
        racks = {}
        for player_id in [1, 2]:
            racks[player_id] = []
            for _ in range(RACK_SIZE):
                if tile_pool:
                    racks[player_id].append(tile_pool.pop())

        # Initialize scores
        scores = {1: 0, 2: 0}

        # Player 1 starts
        current_player = 1

        return ScrabbleState(
            board=board,
            tile_pool=tile_pool,
            racks=racks,
            current_player=current_player,
            scores=scores,
        )

    def get_legal_moves(self, player_id: int) -> List[Move]:
        if self.is_terminal():
            return []

        moves = []
        rack = self.racks[player_id]

        # Check if board is empty (first move)
        board_empty = all(
            self.board[r][c] == "" for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)
        )

        # If board is empty, only allow moves through center (7, 7)
        if board_empty:
            moves.extend(self._generate_first_move(rack))
        else:
            # Generate moves that connect to existing tiles
            moves.extend(self._generate_connected_moves(rack))

        # Always allow passing as a move
        moves.append(Move([], 0, is_pass=True))

        return moves

    # --- BEGIN Game Move Logic ---

    def _generate_first_move(self, rack: List[str]) -> List[Move]:
        """Generate all valid first moves (must go through center square)."""
        moves = []
        center = 7

        # Try all permutations of rack tiles for horizontal and vertical placements

        for length in range(2, len(rack) + 1):
            for perm in permutations(rack, length):
                word = "".join(perm)
                if not is_valid_word(word):
                    continue

                # Try horizontal placements through center
                for start_col in range(
                    max(0, center - length + 1),
                    min(center + 1, BOARD_SIZE - length + 1),
                ):
                    if start_col <= center < start_col + length:
                        tiles_placed = [
                            (center, start_col + i, perm[i]) for i in range(length)
                        ]
                        score = self._calculate_score(tiles_placed)
                        moves.append(Move(tiles_placed, score))

                # Try vertical placements through center
                for start_row in range(
                    max(0, center - length + 1),
                    min(center + 1, BOARD_SIZE - length + 1),
                ):
                    if start_row <= center < start_row + length:
                        tiles_placed = [
                            (start_row + i, center, perm[i]) for i in range(length)
                        ]
                        score = self._calculate_score(tiles_placed)
                        moves.append(Move(tiles_placed, score))

        return moves

    def _generate_connected_moves(self, rack: List[str]) -> List[Move]:
        """Generate all moves that connect to existing tiles on the board."""
        moves = []

        # Find all anchor points (empty squares adjacent to filled squares)
        anchors = self._find_anchors()

        for anchor_row, anchor_col in anchors:
            # Try building words horizontally
            moves.extend(
                self._build_words_at_anchor(
                    rack, anchor_row, anchor_col, horizontal=True
                )
            )
            # Try building words vertically
            moves.extend(
                self._build_words_at_anchor(
                    rack, anchor_row, anchor_col, horizontal=False
                )
            )

        return moves

    def _find_anchors(self) -> List[Tuple[int, int]]:
        """Find all empty squares adjacent to filled squares."""
        anchors = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == "":
                    # Check if adjacent to any filled square
                    adjacent_filled = False
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                            if self.board[nr][nc] != "":
                                adjacent_filled = True
                                break
                    if adjacent_filled:
                        anchors.append((r, c))
        return anchors

    def _build_words_at_anchor(
        self, rack: List[str], anchor_row: int, anchor_col: int, horizontal: bool
    ) -> List[Move]:
        """Build all valid words that include the anchor square."""
        moves = []

        # For each possible word length
        for word_len in range(2, len(rack) + 1):
            # For each permutation of tiles
            for perm in permutations(rack, word_len):
                word = "".join(perm)
                if not is_valid_word(word):
                    continue

                # Try different positions where the anchor is part of the word
                for anchor_pos_in_word in range(word_len):
                    if horizontal:
                        start_col = anchor_col - anchor_pos_in_word
                        if start_col < 0 or start_col + word_len > BOARD_SIZE:
                            continue

                        # Build the placement
                        tiles_placed = []
                        valid = True
                        tiles_used_from_rack = []

                        for i in range(word_len):
                            row, col = anchor_row, start_col + i
                            if self.board[row][col] == "":
                                # Need to place a tile here
                                tiles_placed.append((row, col, perm[i]))
                                tiles_used_from_rack.append(perm[i])
                            elif self.board[row][col] == perm[i]:
                                # Tile already on board matches
                                continue
                            else:
                                # Conflict with existing tile
                                valid = False
                                break

                        if not valid or len(tiles_placed) == 0:
                            continue

                        # Check if we have the tiles in our rack
                        rack_copy = rack[:]
                        can_place = True
                        for tile in tiles_used_from_rack:
                            if tile in rack_copy:
                                rack_copy.remove(tile)
                            else:
                                can_place = False
                                break

                        if not can_place:
                            continue

                        # Validate the complete main word formed (including existing tiles)
                        temp_board = [row[:] for row in self.board]
                        for r, c, letter in tiles_placed:
                            temp_board[r][c] = letter
                        main_word = self._get_word_at(
                            temp_board, anchor_row, anchor_col, horizontal=True
                        )
                        if not is_valid_word(main_word):
                            continue

                        # Validate all cross words formed
                        if self._validate_placement(tiles_placed, horizontal):
                            score = self._calculate_score(tiles_placed)
                            moves.append(Move(tiles_placed, score))

                    else:  # vertical
                        start_row = anchor_row - anchor_pos_in_word
                        if start_row < 0 or start_row + word_len > BOARD_SIZE:
                            continue

                        # Build the placement
                        tiles_placed = []
                        valid = True
                        tiles_used_from_rack = []

                        for i in range(word_len):
                            row, col = start_row + i, anchor_col
                            if self.board[row][col] == "":
                                # Need to place a tile here
                                tiles_placed.append((row, col, perm[i]))
                                tiles_used_from_rack.append(perm[i])
                            elif self.board[row][col] == perm[i]:
                                # Tile already on board matches
                                continue
                            else:
                                # Conflict with existing tile
                                valid = False
                                break

                        if not valid or len(tiles_placed) == 0:
                            continue

                        # Check if we have the tiles in our rack
                        rack_copy = rack[:]
                        can_place = True
                        for tile in tiles_used_from_rack:
                            if tile in rack_copy:
                                rack_copy.remove(tile)
                            else:
                                can_place = False
                                break

                        if not can_place:
                            continue

                        # Validate the complete main word formed (including existing tiles)
                        temp_board = [row[:] for row in self.board]
                        for r, c, letter in tiles_placed:
                            temp_board[r][c] = letter
                        main_word = self._get_word_at(
                            temp_board, anchor_row, anchor_col, horizontal=False
                        )
                        if not is_valid_word(main_word):
                            continue

                        # Validate all cross words formed
                        if self._validate_placement(tiles_placed, horizontal):
                            score = self._calculate_score(tiles_placed)
                            moves.append(Move(tiles_placed, score))

        return moves

    def _validate_placement(
        self, tiles_placed: List[Tuple[int, int, str]], horizontal: bool
    ) -> bool:
        """Validate that all cross-words formed by placement are valid."""
        # Create temporary board with new tiles
        temp_board = [row[:] for row in self.board]
        for row, col, letter in tiles_placed:
            temp_board[row][col] = letter

        # Check each placed tile for cross-words
        for row, col, letter in tiles_placed:
            if horizontal:
                # Check vertical cross-word at this position
                cross_word = self._get_word_at(temp_board, row, col, horizontal=False)
                if len(cross_word) > 1 and not is_valid_word(cross_word):
                    return False
            else:
                # Check horizontal cross-word at this position
                cross_word = self._get_word_at(temp_board, row, col, horizontal=True)
                if len(cross_word) > 1 and not is_valid_word(cross_word):
                    return False

        return True

    def _get_word_at(
        self, board: List[List[str]], row: int, col: int, horizontal: bool
    ) -> str:
        """Extract the complete word at the given position."""
        if horizontal:
            # Find start of word
            start_col = col
            while start_col > 0 and board[row][start_col - 1] != "":
                start_col -= 1
            # Find end of word
            end_col = col
            while end_col < BOARD_SIZE - 1 and board[row][end_col + 1] != "":
                end_col += 1
            # Extract word
            return "".join(board[row][c] for c in range(start_col, end_col + 1))
        else:
            # Find start of word
            start_row = row
            while start_row > 0 and board[start_row - 1][col] != "":
                start_row -= 1
            # Find end of word
            end_row = row
            while end_row < BOARD_SIZE - 1 and board[end_row + 1][col] != "":
                end_row += 1
            # Extract word
            return "".join(board[r][col] for r in range(start_row, end_row + 1))

    def _calculate_score(self, tiles_placed: List[Tuple[int, int, str]]) -> int:
        """Calculate the score for placing these tiles."""
        if not tiles_placed:
            return 0

        # Determine direction of main word
        if len(tiles_placed) == 1:
            row, col, letter = tiles_placed[0]
            # Check if forms horizontal or vertical word with existing tiles
            horizontal_word = self._get_word_at(self.board, row, col, horizontal=True)
            vertical_word = self._get_word_at(self.board, row, col, horizontal=False)
            # For single tile, we need to consider both directions
            pass

        # Assume horizontal if all same row, vertical if all same column
        rows = [r for r, c, l in tiles_placed]
        cols = [c for r, c, l in tiles_placed]
        horizontal = len(set(rows)) == 1

        total_score = 0
        word_multiplier = 1

        # Create temp board for scoring
        temp_board = [row[:] for row in self.board]
        for row, col, letter in tiles_placed:
            temp_board[row][col] = letter

        # Score main word
        if horizontal:
            row = rows[0]
            start_col = min(cols)
            end_col = max(cols)
            # Extend to include existing tiles
            while start_col > 0 and temp_board[row][start_col - 1] != "":
                start_col -= 1
            while end_col < BOARD_SIZE - 1 and temp_board[row][end_col + 1] != "":
                end_col += 1

            word_score = 0
            for c in range(start_col, end_col + 1):
                letter = temp_board[row][c]
                letter_score = LETTER_VALUES.get(letter, 0)
                # Apply premium if tile was just placed
                if any(r == row and col == c for r, col, l in tiles_placed):
                    premium = PREMIUM_BOARD[row][c]
                    if premium == 2:  # Double letter
                        letter_score *= 2
                    elif premium == 3:  # Triple letter
                        letter_score *= 3
                    elif premium == 4:  # Double word
                        word_multiplier *= 2
                    elif premium == 5:  # Triple word
                        word_multiplier *= 3
                word_score += letter_score
            total_score += word_score * word_multiplier
        else:
            col = cols[0]
            start_row = min(rows)
            end_row = max(rows)
            # Extend to include existing tiles
            while start_row > 0 and temp_board[start_row - 1][col] != "":
                start_row -= 1
            while end_row < BOARD_SIZE - 1 and temp_board[end_row + 1][col] != "":
                end_row += 1

            word_score = 0
            for r in range(start_row, end_row + 1):
                letter = temp_board[r][col]
                letter_score = LETTER_VALUES.get(letter, 0)
                # Apply premium if tile was just placed
                if any(row == r and c == col for row, c, l in tiles_placed):
                    premium = PREMIUM_BOARD[r][col]
                    if premium == 2:  # Double letter
                        letter_score *= 2
                    elif premium == 3:  # Triple letter
                        letter_score *= 3
                    elif premium == 4:  # Double word
                        word_multiplier *= 2
                    elif premium == 5:  # Triple word
                        word_multiplier *= 3
                word_score += letter_score
            total_score += word_score * word_multiplier

        # Score cross-words
        for row, col, letter in tiles_placed:
            if horizontal:
                cross_word = self._get_word_at(temp_board, row, col, horizontal=False)
                if len(cross_word) > 1:
                    # Score this cross-word
                    start_row = row
                    while start_row > 0 and temp_board[start_row - 1][col] != "":
                        start_row -= 1
                    cross_score = 0
                    cross_multiplier = 1
                    for r in range(start_row, start_row + len(cross_word)):
                        l = temp_board[r][col]
                        ls = LETTER_VALUES.get(l, 0)
                        if r == row:  # This is the newly placed tile
                            premium = PREMIUM_BOARD[r][col]
                            if premium == 2:
                                ls *= 2
                            elif premium == 3:
                                ls *= 3
                            elif premium == 4:
                                cross_multiplier *= 2
                            elif premium == 5:
                                cross_multiplier *= 3
                        cross_score += ls
                    total_score += cross_score * cross_multiplier
            else:
                cross_word = self._get_word_at(temp_board, row, col, horizontal=True)
                if len(cross_word) > 1:
                    # Score this cross-word
                    start_col = col
                    while start_col > 0 and temp_board[row][start_col - 1] != "":
                        start_col -= 1
                    cross_score = 0
                    cross_multiplier = 1
                    for c in range(start_col, start_col + len(cross_word)):
                        l = temp_board[row][c]
                        ls = LETTER_VALUES.get(l, 0)
                        if c == col:  # This is the newly placed tile
                            premium = PREMIUM_BOARD[row][c]
                            if premium == 2:
                                ls *= 2
                            elif premium == 3:
                                ls *= 3
                            elif premium == 4:
                                cross_multiplier *= 2
                            elif premium == 5:
                                cross_multiplier *= 3
                        cross_score += ls
                    total_score += cross_score * cross_multiplier

        # Bonus for using all 7 tiles
        if len(tiles_placed) == 7:
            total_score += 50

        return total_score

    # --- END Game Move Logic ---

    def apply_move(self, move: Move) -> "ScrabbleState":
        """Creates and returns the next state after the move is applied."""
        opponent_id = 3 - self.current_player
        next_state = ScrabbleState(
            board=[row[:] for row in self.board],
            tile_pool=self.tile_pool[:],
            racks={p: r[:] for p, r in self.racks.items()},
            current_player=opponent_id,  # Switch player
            scores=self.scores.copy(),
        )

        player_performing_move = self.current_player

        if not move.is_pass:
            # Place tiles on the board
            for row, col, letter in move.tiles_placed:
                next_state.board[row][col] = letter

            # Update score
            next_state.scores[player_performing_move] += move.score

            # Remove used tiles from rack
            tiles_to_remove = [letter for _, _, letter in move.tiles_placed]
            rack_copy = next_state.racks[player_performing_move][:]
            for tile in tiles_to_remove:
                if tile in rack_copy:
                    rack_copy.remove(tile)

            # Draw new tiles
            tiles_used = len(move.tiles_placed)
            new_tiles = next_state._draw_tiles(tiles_used)

            # Update rack with remaining tiles plus new tiles
            next_state.racks[player_performing_move] = rack_copy + new_tiles

            next_state.passes_in_a_row = 0
        else:
            next_state.passes_in_a_row = self.passes_in_a_row + 1

        return next_state

    def _draw_tiles(self, count: int) -> List[str]:
        """Draws tiles from the pool (handles stochasticity)."""
        drawn = []
        # Draw up to 'count' tiles, or until pool is empty
        actual_draw_count = min(count, len(self.tile_pool))
        for _ in range(actual_draw_count):
            tile = random.choice(self.tile_pool)
            self.tile_pool.remove(tile)
            drawn.append(tile)
        return drawn

    def is_terminal(self) -> bool:
        """Game ends if tile pool is empty or two consecutive passes occur."""
        return len(self.tile_pool) == 0 or self.passes_in_a_row >= 2

    def get_utility(self, maximizing_player_id: int) -> float:
        """Returns the utility (score differential) from the perspective of the maximizing player.
        This makes the game zero-sum.
        """
        opponent_id = 3 - maximizing_player_id
        return self.scores[maximizing_player_id] - self.scores[opponent_id]


class AlphaBetaMinimax:
    """
    Implements a depth-limited Minimax search with Alpha-Beta Pruning.
    Crucial for demonstrating computational limits (high branching factor)
    and conceptual failures.
    """

    def __init__(self, max_depth: int):
        self.max_depth = max_depth
        self.nodes_explored = 0

    def find_best_move(self, state: ScrabbleState) -> Move:
        current_player = state.current_player
        self.nodes_explored = 0

        alpha = float("-inf")
        beta = float("inf")
        best_value = float("-inf")
        best_move = None

        moves = state.get_legal_moves(current_player)

        if not moves:
            return Move([], 0, is_pass=True)

        start_time = time.time()

        for move in moves:
            next_state = state.apply_move(move)
            # The subsequent layer is the Min player (opponent)
            value = self._minimax_value(
                next_state,
                self.max_depth - 1,
                alpha,
                beta,
                maximizing_player_id=current_player,
            )

            if value > best_value:
                best_value = value
                best_move = move

            # Update alpha at the root (Max level)
            alpha = max(alpha, best_value)

        duration = time.time() - start_time
        print(
            f"Minimax search completed in: {duration:.4f}s. Nodes explored: {self.nodes_explored}. Best move value: {best_value:.2f}"
        )

        return best_move

    def _minimax_value(
        self,
        state: ScrabbleState,
        depth: int,
        alpha: float,
        beta: float,
        maximizing_player_id: int,
    ) -> float:
        """Recursive Minimax function with Alpha-Beta pruning."""
        self.nodes_explored += 1

        if depth == 0 or state.is_terminal():
            # Return static evaluation (utility) at cutoff or terminal node
            return state.get_utility(maximizing_player_id)

        current_player_to_move = state.current_player
        is_max_player_turn = current_player_to_move == maximizing_player_id

        moves = state.get_legal_moves(current_player_to_move)

        if is_max_player_turn:
            value = float("-inf")
            for move in moves:
                next_state = state.apply_move(move)
                value = max(
                    value,
                    self._minimax_value(
                        next_state, depth - 1, alpha, beta, maximizing_player_id
                    ),
                )
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cutoff (Pruning)
            return value

        else:  # Min player turn (opponent)
            value = float("inf")
            for move in moves:
                next_state = state.apply_move(move)
                value = min(
                    value,
                    self._minimax_value(
                        next_state, depth - 1, alpha, beta, maximizing_player_id
                    ),
                )
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cutoff (Pruning)
            return value


class MonteCarlo:
    """
    Framework for Adversarial Monte Carlo Tree Search (MCTS) for Scrabble.
    This implementation focuses on the Monte Carlo aspect.
    """

    def __init__(self, num_playouts: int, heuristic_fn):
        self.num_playouts = num_playouts
        self.heuristic_fn = heuristic_fn

    async def find_best_move(self, state: ScrabbleState) -> Move:
        """Runs the Monte Carlo simulation to estimate move values."""

        moves = state.get_legal_moves(state.current_player)
        if not moves:
            return Move([], 0, is_pass=True)

        move_values = {}

        # Determine the number of playouts per move
        playouts_per_move = int(self.num_playouts // len(moves)) or 1

        print(
            f"Starting MCTS: {playouts_per_move} playouts per move (for {len(moves)} possible moves)..."
        )

        for move in moves:
            total_value = 0

            # Run simulations (rollouts)
            for _ in range(playouts_per_move):
                next_state = state.apply_move(move)

                # Use the agentic heuristic to evaluate the outcome of the simulation
                # NOTE: A real MCTS playout runs until terminal state, but here we
                # use the heuristic to evaluate the strategic value of the immediate successor
                # state resulting from the move, simulating guidance.
                value = await self.heuristic_fn(next_state, state.current_player)
                total_value += value

            avg_value = total_value / playouts_per_move
            move_values[move] = avg_value

        if move_values:
            best_move = max(move_values, key=move_values.get)
            return best_move

        return Move([], 0, is_pass=True)
