"""Utility classes and helpers for the agentic Spelling Bee lab.

This module implements a ``SpellingBeeProblem`` class that models the New
York Times Spelling Bee puzzle as a search problem.  It is designed to be
consumed by the generalized search engine referenced in ``L3.ipynb`` and
exposes a minimal API for generating successor states, evaluating goal
states, and enumerating valid target words.

The implementation focuses on pedagogy: it keeps the surface area small and
easy to reason about while still being faithful to the official game rules:

* Words must contain only the provided letters.
* The required ("center") letter must appear at least once.
* Words must meet a configurable minimum length (default: 4).
* Repeated letters are allowed.

To keep the branching factor manageable for search, we pre-filter a word list
and retain only entries that are feasible under the given rules.  We also
precompute all valid prefixes so that the successor generator can prune branches
that can no longer lead to a valid solution.

Example
-------

>>> problem = SpellingBeeProblem.from_letters(
...     letters=["A", "D", "E", "L", "O", "P", "R"],
...     required_letter="O",
... )
>>> problem.successors("")[:3]
[("A", "A"), ("D", "D"), ("E", "E")]
>>> problem.is_goal("PAROLED")
True

The class will attempt to load a dictionary from one of several common
locations (``/usr/share/dict/words`` first) but also ships with a tiny fallback
list so the API remains usable out-of-the-box.  For serious experimentation,
point ``dictionary_path`` at a richer corpus.
"""

from __future__ import annotations

import asyncio
import heapq
import inspect
from dataclasses import dataclass, field
from itertools import count
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Union

__all__ = ["SpellingBeeProblem", "SearchResult", "generalized_search"]


# ---------------------------------------------------------------------------
# Dictionary helpers
# ---------------------------------------------------------------------------


_FALLBACK_WORDS: Set[str] = {
    # pangrams using common Spelling Bee letter sets
    "LEOPARD",
    "PAROLED",
    "PARADOLE",  # archaic but keeps prefixes alive
    "TRIANGLE",
    "ALTERING",
    "RELATING",
    "INTEGRAL",
    "DEALER",
    "LOADER",
    "PEDAL",
    "PAROLED",
    "PARLOR",
    "PALADIN",
    "RENOVATED",
    "RATIONED",
    "RATION",
    "RATIONING",
    "RATIONED",
    "RATIONER",
    "RATIONERS",
    # shorter words for generic coverage
    "ROAD",
    "READ",
    "LEAD",
    "PALE",
    "REAL",
    "DEAL",
    "RAIL",
    "TRAIL",
    "LATER",
    "ALERT",
    "ALTER",
    "TREAD",
    "TREADLE",
    "PETAL",
    "LEAPT",
    "LEAPT",
    "RENT",
    "TONE",
    "NOTE",
    "TREAT",
    "PLATE",
    "PLEAT",
    "LEAPT",
    "OPAL",
    "POET",
    "REAP",
    "ROPE",
    "LOOP",
    "LOOPS",
    "ROOT",
    "ROOTED",
}


def _load_word_list(
    dictionary: Optional[Iterable[str]] = None, dictionary_path: Optional[Path] = None
) -> Set[str]:
    """Load a candidate dictionary.

    Parameters
    ----------
    dictionary:
            Optional iterable of words supplied programmatically.
    dictionary_path:
            Optional file path containing one word per line.

    Returns
    -------
    set of uppercase words without surrounding whitespace.
    """

    if dictionary is not None:
        return {str(word).strip().upper() for word in dictionary if word}

    if dictionary_path is not None:
        path = Path(dictionary_path)
        if not path.is_file():
            raise FileNotFoundError(f"Dictionary path does not exist: {path}")
        with path.open("r", encoding="utf-8") as handle:
            return {line.strip().upper() for line in handle if line.strip()}

    default_candidates: Tuple[Path, ...] = (
        Path("/usr/share/dict/words"),
        Path("/usr/share/dict/web2"),
        Path(__file__).with_name("words.txt"),
    )

    for candidate in default_candidates:
        if candidate.is_file():
            with candidate.open("r", encoding="utf-8") as handle:
                return {line.strip().upper() for line in handle if line.strip()}

    # Nothing else available – fall back to the bundled miniature list.
    return set(_FALLBACK_WORDS)


# ---------------------------------------------------------------------------
# Core problem representation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SearchResultMetadata:
    """Small helper container for search-related metadata.

    The generalized search implementation provided to students may choose to
    stash additional metadata alongside each state (for example, whether the
    word is a pangram). Exposing a typed container keeps the interface tidy
    without committing us to a concrete implementation in this lab.  The
    ``SpellingBeeProblem`` currently sets this to ``None`` in successor tuples,
    but the attribute is defined for completeness and future extension.
    """

    is_pangram: bool = False
    score: int = 0


@dataclass
class SearchNode:
    """Represents a node in the search frontier."""

    state: str
    parent: Optional["SearchNode"]
    action: Optional[str]
    path_cost: float
    heuristic: float = 0.0
    metadata: Optional[SearchResultMetadata] = None

    def total_cost(self) -> float:
        return self.path_cost + self.heuristic


@dataclass
class SearchResult:
    """Return object produced by ``generalized_search``."""

    success: bool
    goal_state: Optional[str]
    actions: List[str]
    cost: float
    expansions: int
    explored: int
    frontier_size: int


class SpellingBeeProblem:
    """Represents a single instance of the NYT Spelling Bee puzzle.

    Parameters
    ----------
    letters:
            An iterable containing the seven permitted letters.
    required_letter:
            The mandatory letter that must appear in every valid solution.
    dictionary:
            Optional iterable of candidate words.  If provided, overrides
            ``dictionary_path`` and the default loaders.
    dictionary_path:
            Optional path to a newline-delimited word list.
    min_word_length:
            Minimum allowed word length. The official Spelling Bee uses 4.
    """

    DEFAULT_MIN_WORD_LENGTH = 4

    def __init__(
        self,
        letters: Iterable[str],
        required_letter: str,
        *,
        dictionary: Optional[Iterable[str]] = None,
        dictionary_path: Optional[Path | str] = None,
        min_word_length: int = DEFAULT_MIN_WORD_LENGTH,
    ) -> None:
        normalized_letters = tuple(self._normalize_letter(letter) for letter in letters)
        if len(normalized_letters) == 0:
            raise ValueError("At least one letter must be provided")

        if len(set(normalized_letters)) != len(normalized_letters):
            # Duplicates are technically allowed in the daily puzzle, but we keep
            # the canonical set unique to simplify reasoning.
            normalized_letters = tuple(dict.fromkeys(normalized_letters))

        normalized_required = self._normalize_letter(required_letter)
        if normalized_required not in normalized_letters:
            raise ValueError(
                "Required letter must be included in the provided letter set"
            )

        if min_word_length < 1:
            raise ValueError("Minimum word length must be positive")

        self._letters: Tuple[str, ...] = normalized_letters
        self._letter_set: Set[str] = set(normalized_letters)
        self._required_letter: str = normalized_required
        self._min_word_length: int = min_word_length

        if isinstance(dictionary_path, str):
            dictionary_path = Path(dictionary_path)

        raw_dictionary = _load_word_list(
            dictionary=dictionary, dictionary_path=dictionary_path
        )
        if not raw_dictionary:
            raise ValueError("Dictionary must contain at least one word")

        self._valid_words: Set[str] = {
            word for word in raw_dictionary if self._is_candidate_word(word)
        }

        if not self._valid_words:
            raise ValueError(
                "No valid words remain after filtering, consider supplying a larger dictionary"
            )

        self._max_word_length: int = max(len(word) for word in self._valid_words)
        self._prefixes: Set[str] = self._build_prefix_set(self._valid_words)
        self._pangrams: Set[str] = {
            word for word in self._valid_words if self.is_pangram(word)
        }

        # Include the empty string so the very first expansion is permitted.
        self._prefixes.add("")

    # ------------------------------------------------------------------
    # Public constructor helpers
    # ------------------------------------------------------------------

    @classmethod
    def from_letters(
        cls,
        letters: Sequence[str],
        required_letter: str,
        *,
        dictionary: Optional[Iterable[str]] = None,
        dictionary_path: Optional[Path | str] = None,
        min_word_length: int = DEFAULT_MIN_WORD_LENGTH,
    ) -> "SpellingBeeProblem":
        """Factory matching the usage pattern in the lab notebook."""

        return cls(
            letters=letters,
            required_letter=required_letter,
            dictionary=dictionary,
            dictionary_path=dictionary_path,
            min_word_length=min_word_length,
        )

    # ------------------------------------------------------------------
    # Search interface expected by the generalized search tool
    # ------------------------------------------------------------------

    @property
    def letters(self) -> Tuple[str, ...]:
        """Return the tuple of allowed letters (ordered as supplied)."""

        return self._letters

    @property
    def required_letter(self) -> str:
        """Return the mandatory letter for all valid words."""

        return self._required_letter

    @property
    def min_word_length(self) -> int:
        return self._min_word_length

    @property
    def valid_words(self) -> Set[str]:
        return set(self._valid_words)

    @property
    def pangrams(self) -> Set[str]:
        return set(self._pangrams)

    @property
    def max_word_length(self) -> int:
        return self._max_word_length

    def initial_state(self) -> str:
        """Return the initial (empty) state for search."""

        return ""

    def successors(
        self, state: str
    ) -> List[Tuple[str, str, Optional[SearchResultMetadata]]]:
        """Expand the given state by appending each feasible letter.

        Returns a list of ``(action, next_state, metadata)`` tuples, mirroring
        the pattern often used in search textbooks.  The metadata element is
        optional - we currently return ``None`` to keep things simple - but the
        slot is present so students can extend it without modifying the search
        engine.
        """

        normalized_state = self._normalize_word(state)
        if len(normalized_state) >= self._max_word_length:
            return []

        successors: List[Tuple[str, str, Optional[SearchResultMetadata]]] = []
        for letter in self._letters:
            next_state = normalized_state + letter
            if next_state in self._prefixes:
                successors.append((letter, next_state, None))
        return successors

    def is_goal(self, state: str) -> bool:
        """Check whether ``state`` constitutes a goal word under puzzle rules."""

        normalized_state = self._normalize_word(state)
        return normalized_state in self._valid_words

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def contains_only_allowed_letters(self, word: str) -> bool:
        """Return ``True`` if *word* is comprised solely of permitted letters."""

        normalized = self._normalize_word(word)
        return bool(normalized) and set(normalized).issubset(self._letter_set)

    def contains_required_letter(self, word: str) -> bool:
        """Return ``True`` if *word* includes the required letter."""

        return self._required_letter in self._normalize_word(word)

    def is_valid_word(self, word: str) -> bool:
        """Return ``True`` if *word* satisfies all puzzle constraints."""

        normalized = self._normalize_word(word)
        if len(normalized) < self._min_word_length:
            return False
        if not self.contains_only_allowed_letters(normalized):
            return False
        if self._required_letter not in normalized:
            return False
        return normalized in self._valid_words

    def is_pangram(self, word: str) -> bool:
        """Return ``True`` if *word* uses every provided letter at least once."""

        normalized = self._normalize_word(word)
        return self._letter_set.issubset(set(normalized))

    def score_word(self, word: str) -> int:
        """Compute the official Spelling Bee score for *word*.

        Rules (as of 2025):
                * 4-letter words are worth 1 point.
                * Words with length > 4 are worth their length.
                * Pangrams receive a 7-point bonus on top of their length score.
        """

        normalized = self._normalize_word(word)
        if not self.is_valid_word(normalized):
            raise ValueError(f"Word is not valid in this puzzle: {word}")

        base = 1 if len(normalized) == 4 else len(normalized)
        return base + (7 if self.is_pangram(normalized) else 0)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _is_candidate_word(self, word: str) -> bool:
        normalized = self._normalize_word(word)
        if len(normalized) < self._min_word_length:
            return False
        if not normalized.isalpha():
            return False
        if self._required_letter not in normalized:
            return False
        if not set(normalized).issubset(self._letter_set):
            return False
        return True

    @staticmethod
    def _normalize_letter(letter: str) -> str:
        if not letter or len(letter) != 1 or not letter.isalpha():
            raise ValueError(f"Invalid letter: {letter!r}")
        return letter.upper()

    @staticmethod
    def _normalize_word(word: str) -> str:
        return str(word or "").strip().upper()

    @staticmethod
    def _build_prefix_set(words: Iterable[str]) -> Set[str]:
        prefixes: Set[str] = set()
        for word in words:
            for end in range(1, len(word) + 1):
                prefixes.add(word[:end])
        return prefixes

    # ------------------------------------------------------------------
    # Representations
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover - human-friendly representation
        letters = "".join(self._letters)
        return (
            f"SpellingBeeProblem(letters='{letters}', required='{self._required_letter}', "
            f"words={len(self._valid_words)})"
        )


# ---------------------------------------------------------------------------
# Generalized search implementation
# ---------------------------------------------------------------------------


StrategyFn = Callable[[SearchNode], float]


async def generalized_search(
    *,
    problem: "SpellingBeeProblem",
    cost_fn: Callable[[str, str, str], float],
    heuristic_fn: Union[Callable[[str], float], Callable[[str], asyncio.coroutine]],
    strategy: str = "a_star",
    max_expansions: Optional[int] = None,
    verbose: bool = False,
) -> SearchResult:
    """Generic best-first search over ``SpellingBeeProblem`` states.

    Parameters
    ----------
    problem:
        Instance that provides ``initial_state()``, ``successors(state)`` and
        ``is_goal(state)``.
    cost_fn:
        Callable returning the incremental cost ``g(parent_state, action, child_state)``.
    heuristic_fn:
        Callable or async callable returning an admissible heuristic estimate ``h(state)``.
        Can be either a synchronous function or an async function.
    strategy:
        ``"a_star"`` (default) uses ``f = g + h``.  ``"uniform_cost"`` ignores the
        heuristic and behaves like UCS.
    max_expansions:
        Optional safety limit to prevent unbounded work.
    """

    strategy = strategy.lower()
    if strategy not in {"a_star", "uniform_cost"}:
        raise ValueError("strategy must be 'a_star' or 'uniform_cost'")

    initial_state = problem.initial_state()

    # Check if heuristic_fn is async
    is_async_heuristic = inspect.iscoroutinefunction(heuristic_fn)

    try:
        if strategy == "a_star":
            if is_async_heuristic:
                initial_heuristic = float(await heuristic_fn(initial_state))
            else:
                initial_heuristic = float(heuristic_fn(initial_state))
        else:
            initial_heuristic = 0.0
    except Exception as exc:  # pragma: no cover - propagate context
        raise RuntimeError(
            "heuristic_fn raised an exception for the initial state"
        ) from exc

    root = SearchNode(
        state=initial_state,
        parent=None,
        action=None,
        path_cost=0.0,
        heuristic=initial_heuristic,
        metadata=None,
    )

    frontier: List[Tuple[float, int, SearchNode]] = []
    counter = count()
    heapq.heappush(frontier, (root.total_cost(), next(counter), root))

    best_costs: Dict[str, float] = {initial_state: 0.0}
    explored: Set[str] = set()
    expansions = 0

    while frontier:
        if max_expansions is not None and expansions >= max_expansions:
            break

        _, _, node = heapq.heappop(frontier)

        if problem.is_goal(node.state):
            return _build_search_result(
                node,
                success=True,
                expansions=expansions,
                explored=len(explored),
                frontier_size=len(frontier),
            )

        if node.state in explored:
            continue

        explored.add(node.state)
        expansions += 1

        for action, next_state, _metadata in problem.successors(node.state):
            step_cost = float(cost_fn(node.state, action, next_state))
            if step_cost < 0:
                raise ValueError("cost_fn must return non-negative values")

            new_cost = node.path_cost + step_cost
            if next_state in best_costs and new_cost >= best_costs[next_state]:
                continue

            try:
                if strategy == "a_star":
                    if is_async_heuristic:
                        heuristic_value = float(await heuristic_fn(next_state))
                    else:
                        heuristic_value = float(heuristic_fn(next_state))
                else:
                    heuristic_value = 0.0
            except Exception as exc:
                raise RuntimeError(
                    f"heuristic_fn raised an exception for state {next_state!r}"
                ) from exc

            if verbose:
                if len(next_state) > 4:
                    print(f"Expanding: {node.state!r} + {action!r} -> {next_state!r}")
                    print(f"  Step cost: {step_cost}")
                    print(f"  New cost: {new_cost}")
                    print(f"  Heuristic score: {heuristic_value}")

            child = SearchNode(
                state=next_state,
                parent=node,
                action=action,
                path_cost=new_cost,
                heuristic=heuristic_value,
                metadata=_metadata,
            )

            best_costs[next_state] = new_cost
            heapq.heappush(frontier, (child.total_cost(), next(counter), child))

    return _build_search_result(
        node=None,
        success=False,
        expansions=expansions,
        explored=len(explored),
        frontier_size=len(frontier),
    )


def _build_search_result(
    node: Optional[SearchNode],
    *,
    success: bool,
    expansions: int,
    explored: int,
    frontier_size: int,
) -> SearchResult:
    if success and node is None:
        raise ValueError("Successful search must supply a goal node")

    actions: List[str] = []
    cost = float("inf")
    goal_state: Optional[str] = None

    if node is not None:
        cost = node.path_cost
        goal_state = node.state
        actions = _reconstruct_actions(node)

    return SearchResult(
        success=success,
        goal_state=goal_state,
        actions=actions,
        cost=cost if success else float("inf"),
        expansions=expansions,
        explored=explored,
        frontier_size=frontier_size,
    )


def _reconstruct_actions(node: SearchNode) -> List[str]:
    actions: List[str] = []
    cursor: Optional[SearchNode] = node
    while cursor and cursor.action is not None:
        actions.append(cursor.action)
        cursor = cursor.parent
    actions.reverse()
    return actions
