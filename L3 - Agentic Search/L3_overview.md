# CSC 480 Lab 3: Agentic Heuristic Search (NYT Spelling Bee)

In this lab, you’ll use a multi-agent system as a heuristic function to guide a provided generalized search engine through the state space of the New York Times Spelling Bee puzzle. You will integrate the generalized search function as a tool call, supply your own cost function, and design an agentic heuristic that the search engine will query while it maintains the frontier and priority queue. The Spelling Bee problem definition will also be provided.

---

## Overview

Agentic systems can complement classic search by providing adaptive heuristics that capture problem structure beyond static formulas. In this lab, you’ll connect a provided generalized search tool to an agentic heuristic you design. The search tool owns and maintains the search state (frontier, explored set, and priority queue), while your work focuses on:

- Using the provided Spelling Bee problem definition (letters, required center letter, validity rules)
- Implementing a cost function $g(n)$ for state transitions
- Building an agentic heuristic $h(n)$ that the search tool will query during search
- Integrating the tool and orchestrating interactions cleanly and safely

By the end of this lab, you will be able to:

- Integrate a provided generalized search function as a tool inside an agentic application.
- Design and implement an agentic heuristic that returns numeric estimates $h(n)$ for a given state.
- Provide and justify a cost function $g(n)$ appropriate for Spelling Bee.
- Explain and apply multi-agent communication patterns (MCP-style tool exposure and A2A interactions) to support heuristic computation.
- Run and compare search settings (e.g., Uniform Cost, A*) and reflect on outcomes and trade-offs.

---

## Generalized search tool (provided)

We provide a Python search function that you will call as a tool from your agentic system. It maintains the state of the search and will request heuristic estimates via a callback you supply.

Conceptual contract:

- Function: `generalized_search(problem, cost_fn, heuristic_fn, strategy="a_star" | "uniform_cost") -> SearchResult`
- Search state (owned internally by the tool):
  - frontier: set/queue of candidate nodes
  - explored_set: visited states
  - priority queue: orders nodes by $f(n) = g(n) + h(n)$ (A*) or $f(n) = g(n)$ (Uniform Cost)
- Your responsibilities:
  - `cost_fn`: a Python callable you implement: `cost_fn(parent_state, action, next_state) -> float`
  - `heuristic_fn`: a Python callable/async wrapper you implement that delegates to your agentic heuristic system: `heuristic_fn(state) -> float`
  - Spelling Bee problem: provided as a module/class with state representation, successors, goal checks, scoring helpers, and pangram metadata

Notes:

- The tool will invoke `heuristic_fn(state)` whenever it needs an $h(n)`. Inside the notebook scaffold, `run_agentic_search` defines an async `heuristic_fn` that must invoke your agents and return a numeric score; it is automatically wrapped into the synchronous callback the search function expects.
- The tool owns persistence of the frontier and priority queue; you will not mutate internal structures directly (feel free to read the implementation in `utils.py`).

---

## Communication protocols

At a high level, you’ll use:

1. Model Context Protocol (MCP-style) for tool exposure
	- Purpose: Expose the `generalized_search` function (and any utility tools) to your agents with typed inputs/outputs.
	- Why: Normalizes tool calls and makes `heuristic_fn` invocation auditable and testable.

2. Agent-to-Agent (A2A) interactions for heuristic computation
	- Purpose: Let specialized agents collaborate to estimate $h(n)$ for a state (e.g., feasibility analysis, letter coverage, word completion likelihood).
	- Why: Encapsulates reasoning steps and enables critique/aggregation before returning a single scalar.

---

## Lab activities

### Part 1: Agentic heuristic design and planning

1. Problem & heuristic decomposition
	- State the Spelling Bee goal and constraints.
	- Brainstorm factors that correlate with goal proximity (e.g., contains required letter, uses only allowed letters, dictionary viability, prefix extensibility).

2. Agent definition (heuristic team)
	- Identify your heuristic agents (e.g., Constraint Checker, Dictionary Feasibility Estimator, Completeness Scorer).
	- For each: role, responsibilities, inputs/outputs, and how its score contributes to $h(n)$.

3. Design pattern selection
	- Choose a coordination style (e.g., Manager-Worker or small Collaborative Team) to aggregate scores into one $h(n)$.
	- Justify your choice with respect to latency, reliability, and interpretability.

### Part 2: Tool integration and experimentation

4. Tool integration
	- Install AutoGen dependencies in the provided `%pip` cell and configure Azure/OpenAI credentials in the dedicated configuration cell.
	- Expose `generalized_search` as a tool callable from your orchestrator (or user) agent.
	- Implement `cost_fn` (pure Python) and the async `heuristic_fn` inside `run_agentic_search`. Ensure the heuristic delegates to your agents, aggregates their scores, and returns a numeric estimate.

5. Interaction mapping
	- Sketch a sequence/flow diagram showing tool call → heuristic_fn → agents → aggregated $h(n)$ → search tool.

6. Run the starter and custom puzzles in the notebook, paste or summarize the resulting metrics, and analyze how your heuristic impacted node expansions and cost.

7. Complete the reflection prompts to document successes, failure modes, communication insights, and next ideas.

---

## Exercise: integrate the tool and build a multi-agent heuristic

You’ll implement a minimal multi-agent heuristic system and wire it to the provided search function.

### Roles (example)

- Heuristic Orchestrator: Receives a state, coordinates sub-agents, aggregates a final $h(n)$.
- Feasibility Analyst: Scores whether the state can lead to a valid solution (dictionary/prefix viability, required letter present).
- Completeness Estimator: Scores distance to a likely complete/valid word under puzzle rules.

### Message flow

1. Search tool requests $h(n)$ by calling `heuristic_fn(state)`.
2. Orchestrator fans out to Feasibility Analyst and Completeness Estimator.
3. Sub-agents return partial scores and rationales.
4. Orchestrator normalizes/weights scores into a single $h(n)$ and returns it to `heuristic_fn` → search tool.

### Suggested acceptance criteria

- `heuristic_fn` returns a numeric $h(n)$ consistently; aggregation is documented and deterministic given the same inputs.
- `cost_fn` is defined and justified; units align with the heuristic so A* is meaningful.
- The integrated system finds valid Spelling Bee solutions on provided test puzzles within reasonable node expansions.
- Your diagram maps tool calls and agent interactions unambiguously.

---

## Deliverables and submission

Submit your filled-in notebook.

Include:

- Team members: Names and Cal Poly email addresses
- Heuristic design: Decomposition, agent roles, responsibilities, inputs/outputs
- Design pattern: Choice and justification
- Tool integration details: How `generalized_search`, `cost_fn`, and `heuristic_fn` are wired; expected inputs/outputs
- Interaction diagram: Flow of `heuristic_fn` calls across agents
- Results: Runs on sample puzzles with brief analysis (node expansions, solution quality/latency)
- Reflection: What worked, what didn’t, and ideas for improving $h(n)$

Submission method: Canvas.

---

## Evaluation criteria (20% each)

| Aspect | Explanation | Percent |
| :-- | :-- | :--: |
| Problem Description & Heuristic Decomposition | Goal and constraints are clear; heuristic is logically decomposed into sub-scores/agents. | 20 |
| Agent Design | Agents have clear roles and measurable outputs that map to $h(n)$; responsibilities are well-defined. | 20 |
| Tool Integration & Cost Function | `generalized_search` is correctly integrated; `cost_fn` is appropriate and consistent. | 20 |
| Heuristic Quality & Search Behavior | Heuristic is sound and helps the search tool find solutions efficiently. | 20 |
| Clarity & Coherence of Deliverables | Document is well-organized. | 20 |