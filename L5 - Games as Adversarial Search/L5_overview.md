# 2025-10-09 L5 Overview

## CSC 480 Lab 5: Games as Adversarial Search: From Minimax to Monte Carlo Scrabble Agent

### Overview/Background

This lab introduces **Adversarial Search** methods, a core topic in Artificial Intelligence (AI). Games offer a rich and varied domain for exploring AI techniques. These techniques range from classical perfect-information games to highly complex, partially observable, and multi-agent systems.

The classical search algorithms for optimal decision-making in turn-based adversarial games are **Minimax** and **Alpha-Beta Pruning**. Minimax works by maximizing the player's outcome while assuming a rational opponent seeks to minimize that score. **Alpha-Beta Pruning** is an optimization of Minimax that avoids exploring non-optimal branches of the search tree. Minimax and Alpha-Beta pruning are covered in Chapter 6 of Russell & Norvig’s _Artificial Intelligence: A Modern Approach_.

We will use **Scrabble** as a complex, real-world example. This serves as an **adversarial extension of the single-player word puzzle** concepts explored in earlier labs, such as the **NY Times Spelling Bee** (Labs 3 and 4). In Scrabble, players compete by strategically placing words to maximize their own score while limiting the opponent's opportunities.

#### Games Overview

Games provide various challenges for AI, including two-player turn-based structures, multiplayer asynchronous setups, and single-player puzzles. **Key challenges** include:

- **Game Structure:** How players interact (e.g., turn-based, asynchronous).
- **State Space Size:** The number of unique game states, which dictates search demands.
- **Game Complexity:** Factors like branching factors, hidden information, and non-determinism.
- **Perfect vs. Imperfect Information:** Whether all players know the entire game state (e.g., Chess has perfect information; Scrabble has partial information).
- **Adversarial vs. Cooperative:** The goal structure of the game (classical AI often targets zero-sum games).

Classical search algorithms like Minimax and Alpha-Beta pruning excel in deterministic, perfect information games with manageable state spaces but become impractical for games with very large or complex state spaces or imperfect information.



| Name         | Description                             | Game Structure                                  | State Space Size      | Complexity                 | Hidden Information | Suitable Methods                              | Notes                                                    |
| ------------ | --------------------------------------- | ----------------------------------------------- | --------------------- | -------------------------- | ------------------ | --------------------------------------------- | -------------------------------------------------------- |
| Tic-Tac-Toe  | Simple 3x3 alignment game               | Two-player, turn-based, perfect information     | Small (≈3^9)          | Low                        | No                 | Minimax, Alpha-Beta pruning                   | Classic introductory example                             |
| Connect 4    | Vertical disc drop game                 | Two-player, turn-based, perfect information     | Moderate (≈4.5×10^12) | Moderate                   | No                 | Minimax, Alpha-Beta pruning                   | Good balance of complexity and clarity                   |
| Mancala      | Stone sowing game                       | Two-player, turn-based, perfect information     | Moderate              | Moderate                   | No                 | Minimax, Alpha-Beta pruning                   | Strategic but manageable                                 |
| Breakthrough | Pawn race game                          | Two-player, turn-based, perfect information     | Moderate              | Moderate                   | No                 | Minimax, Alpha-Beta pruning                   | Simple mechanics, good teaching example                  |
| Checkers     | Classic board game                      | Two-player, turn-based, perfect information     | Large (>10^20)        | High                       | No                 | Minimax, Alpha-Beta pruning, heuristics       | Computationally demanding                                |
| Chess        | Classic strategic board game            | Two-player, turn-based, perfect information     | Extremely large       | Very High                  | No                 | Minimax, Alpha-Beta pruning, heuristics, ML   | Highly complex, advanced techniques needed               |
| **Scrabble** | Tile placement board word game          | Two-player, turn-based, imperfect information   | Very large            | Very High                  | Partial            | Monte Carlo, Minimax variants with heuristics | Complex spatial, partial info, strategic constraints     |
| Clue         | Detective deduction game                | Multi-player, turn-based, partial observation   | Huge                  | Complex and uncertain      | Yes                | Probabilistic reasoning, agent communication  | Not suited for classical Minimax                         |
| Mafia        | Social deduction and communication game | Multi-player, asynchronous, partial observation | Extremely large       | Complex, non-deterministic | Yes                | Agent communication, adaptive agents, NLP     | Requires sophisticated agentic models                    |
| Hangman      | Word guessing game                      | Asymmetric guesser vs chooser                   | Moderate to large     | Low with adaptations       | Yes (secret word)  | Probabilistic models, language models         | Not straightforward for Minimax; mainly prediction-based |

#### Scrabble as an Adversarial Extension of Spelling Bee

Scrabble is a classic two-player board game played on a 15x15 grid where players place letter tiles to form valid words. Players start with seven tiles drawn randomly and replenish their rack after each turn. Scoring is based on letter values and premium board squares.

The **NY Times Spelling Bee** (Lab 3/4) is a single-player puzzle focused on forming words from a fixed set of letters. Scrabble extends this linguistic challenge into an adversarial setting, adding the board layout, tile management, and strategic adversarial play.

|Criterion|NYT Spelling Bee|Scrabble|
|:--|:--|:--|
|**Description**|Single-player word puzzle. Form words from 7 letters arranged in a honeycomb.|Two-player adversarial board game placing tiles to form words on a 15x15 grid.|
|**Game Structure**|Single-player, puzzle|Two-player, turn-based, adversarial|
|**Constraints**|Words ≥4 letters, must include center letter, letters can repeat.|Tile rack of max 7 tiles drawn randomly; placed words must be valid and connected.|
|**Suitable Methods**|Dictionary lookup, backtracking, pruning.|Minimax, Alpha-Beta pruning, **Monte Carlo Tree Search with heuristics**.|
|**Notes**|Letters reusable; no adversarial play.|**Partial information** (unknown opponent tiles), spatial and strategic constraints.|

---

### Learning Objectives

By the end of this lab, you will be able to:

- **Review and analyze** the Minimax algorithm and Alpha-Beta pruning for zero-sum games.
- **Identify and justify** the limitations of conventional adversarial search methods (Minimax, Alpha-Beta) when applied to complex, imperfect-information games like Scrabble.
- **Explain and apply** advanced adversarial search techniques, specifically **Monte Carlo methods**, to handle large, uncertain game states.
- **Design and evaluate** sophisticated heuristics to guide adversarial Monte Carlo playouts and improve agent strength.
- **Conceptualize** how an **agentic design approach** (building on Labs 1 and 2) can be used to construct a sophisticated Scrabble agent.

---

### Concepts and Principles

- Minimax Algorithm
- Alpha-Beta Pruning
- Adversarial Search
- Game Complexity (State Space Size, Branching Factor, Hidden Information)
- Imperfect Information Games (e.g., Scrabble)
- Monte Carlo Tree Search (MCTS)
- Heuristic Functions
- Agentic Design and Communication Protocols (Planner, Critic, Tool Use, MCP, A2A)

---

### Tools and Resources

- Jupyter Notebook / Google Colab
- AutoGen framework (for implementing agent collaboration and heuristics)

---

### Conventional Adversarial Search: Minimax and Alpha-Beta Pruning

**Overall Method (Part 1):** Minimax determines the optimal move assuming the opponent is rational. Alpha-Beta Pruning is an optimization to speed up this process by pruning sections of the search tree.

A conventional implementation for a simple game like Tic-Tac-Toe often involves:

1. Reviewing the Minimax algorithm structure.
2. Implementing a simplified Minimax + Alpha-Beta pruning algorithm.

#### Limitations for a Complex Game like Scrabble (Part 2)

Minimax and Alpha-Beta Pruning rely on searching the game tree deeply, but this is impractical for Scrabble:

1. **Very High Complexity and State Space:** Scrabble has a vast state space and an enormous branching factor (number of possible moves per turn), making deep conventional search computationally impossible.
2. **Imperfect/Partial Information:** Players do not know their opponent's tiles. Minimax assumes perfect knowledge of the state, making naive application invalid.
3. **Non-Determinism:** The random replenishment of tiles introduces stochasticity, further complicating deterministic tree search.

A lab task will demonstrate these limits by running a provided naive Minimax snippet on simplified Scrabble states to observe severe performance limitations.

---

### Agentic Design and Advanced Search: Monte-Carlo

For games where complexity and partial information prevent classical search, advanced methods are necessary.

#### Application of Agentic Design to Scrabble

The **agentic design approach** (practiced in Lab 2) involves decomposing complex problems into tasks and assigning roles to specialized agents. This can be applied to Scrabble decision-making (Part 4):

1. **Heuristic Collaboration (A2A):** Instead of one monolithic heuristic, specialized agents can collaborate (using **Agent-to-Agent (A2A) interactions**) to quickly evaluate board states or moves. Examples include:
    - **Score Estimator Agent:** Calculates immediate points.
    - **Tile Management Agent:** Assesses the quality of remaining tiles on the player's rack.
    - **Opponent Risk Agent:** Evaluates the risk created for the opponent based on the board setup.
2. **Tool Use (MCP):** Agents can expose structured capabilities like move generators or dictionary lookups as tools via the **Model Context Protocol (MCP)**.
3. **Coordination:** An orchestrator agent (Manager-Worker pattern) gathers and aggregates the analyses and numeric scores from the specialized heuristic agents to produce a final, composite heuristic value to guide the search.

#### Advanced Search: Adversarial Monte-Carlo (MCTS) (Part 3)

**Monte Carlo Tree Search (MCTS)** is effective for adversarial games with large, uncertain state spaces. MCTS explores the search space using randomized **playouts** (simulations) from a given state to the end of the game. These simulations estimate the value of different moves statistically, focusing effort on promising branches.

In Scrabble, MCTS is used to manage **partial information** by simulating games based on plausible distributions of hidden tiles (opponent's rack and the pool). The agentic heuristics designed in Part 4 are crucial here, as they guide the MCTS playouts to be strategically meaningful rather than purely random.

---

### Lab Activities Outline

|Part|Topic|Activity|
|:--|:--|:--|
|**Part 1**|**Classical Search Review**|Review Minimax + Alpha-Beta pruning on a simple game (e.g., provided framework code).|
|**Part 2**|**Minimax Limitations**|Discuss Scrabble’s complexity (large branching factor, partial information). Run provided naive Minimax snippet on simplified Scrabble states to observe performance and failure modes.|
|**Part 3**|**Adversarial Monte Carlo Agent**|Review a playable MCTS agent for Scrabble. Run matches and experiment with search parameters (e.g., number of playouts).|
|**Part 4**|**Agentic Heuristics and Impact**|Design and implement an **agentic heuristic system** (using specialized agents and A2A/MCP protocols) to provide sophisticated state evaluation for MCTS playouts. Modify and evaluate the composite heuristic, observing effects on agent strength.|
|**Reflection**|**Analysis**|Analyze the transition from classical search to MCTS, discussing trade-offs and how heuristic complexity impacts performance in complex, partially observable environments.|

---

### Deliverables, Submission, and Deadline

Submit your Jupyter notebook (.ipynb) via Canvas. The deadline for this assignment is the end of the day (midnight) as listed on Canvas/the course schedule.

---

### Evaluation Criteria

The lab will be graded based on the five criteria listed below, with each criterion accounting for 20% of the total score.

|Aspect|Explanation|Percent|
|:--|:--|:--|
|**1. Classical Search Principles & Limitations (Part 1 & 2)**|Clear analysis of Minimax/Alpha-Beta pruning principles and justification for why they fail when applied to complex, partial-information games like Scrabble.|**20**|
|**2. Monte Carlo Agent Implementation (Part 3)**|Correct implementation and functional demonstration of the Monte Carlo Tree Search (MCTS) agent for the Scrabble domain, including appropriate parameter experimentation.|**20**|
|**3. Agentic Heuristic System Design (Part 4)**|Well-defined design and documentation of the agent team used to generate the MCTS heuristic, including clear roles, responsibilities, and specification of MCP and A2A communication protocols.|**20**|
|**4. Heuristic Evaluation & Experimental Results (Part 4)**|Successful modification and evaluation of the sophisticated, agent-driven heuristic system, including observation and reporting on the effects of heuristic complexity on agent performance.|**20**|
|**5. Reflection and Comparative Analysis**|Insightful analysis of the transition from classical search (Minimax) to modern search (MCTS) and a critical discussion of heuristic effectiveness and performance trade-offs in complex, partially observable environments.|**20**|