
# Lab 4: Agentic Monte Carlo Search

## Overview/Background

This lab introduces **Monte Carlo Search**, a powerful technique for exploring large search spaces where exhaustive traversal is infeasible. Unlike the systematic search methods from Lab 3 (BFS, DFS, A*) which expand nodes based on a defined order or heuristic, Monte Carlo methods use **random sampling** to estimate the value of different moves or states. By running many random simulations (playouts or rollouts) from a given state, the algorithm can approximate which choices are most promising on average. This approach is particularly effective in domains with high branching factors or complex evaluation functions, such as games and planning problems.

This method is a foundational component of more advanced algorithms like Monte-Carlo Tree Search (MCTS), which was famously used in AlphaGo. For further reading, consult Russell & Norvig's _Artificial Intelligence: A Modern Approach_ (Fourth Edition) or Ertel's _Introduction to Artificial Intelligence_ on advanced search topics.

## Learning Objectives

By the end of this lab, you will be able to:

- Understand the principles of Monte Carlo Search and its trade-offs compared to systematic search algorithms.
- Implement a conventional Monte Carlo Search algorithm by adapting the generalized search framework from Lab 3.
- Design and implement an agentic system to perform and evaluate the random simulations (rollouts) that are central to the Monte Carlo method.
- Analyze how the number of simulations impacts solution quality and performance.
- Specify the communication patterns (MCP/A2A) required for agents to collaboratively execute and aggregate the results of Monte Carlo rollouts.

## Concepts and Principles

This lab focuses on the following key AI concepts and principles:

- **Monte Carlo Search**: Using random sampling and simulations to guide search.
- **Stochastic vs. Deterministic Search**: Comparing random exploration with the systematic methods from previous labs (BFS, DFS, A*).
- **Exploration vs. Exploitation**: The fundamental trade-off in balancing the discovery of new paths versus refining known good paths.
- **Agentic Simulation**: Decomposing the simulation process into roles for specialized agents (e.g., Simulator, Evaluator, Aggregator).
- **Multi-Agent Design Patterns**: Applying patterns like Manager-Worker or Collaborative Team to orchestrate the search process.

## Conventional Implementation Approach

A conventional implementation of Monte Carlo Search can be built upon the general search formulation from Lab 3. The core idea is to evaluate each possible successor state from the current state by running a number of random simulations.

1. **General Search Formulation**: From Lab 3, you have a `generalized_search` function that takes a problem, a cost function `g(n)`, and a heuristic function `h(n)`. For Monte Carlo Search, the "heuristic" is not a static estimate but a dynamically computed value based on simulation outcomes.
2. **Evaluating Successors**: For the current state, generate all possible successor states.
3. **Simulation Loop**: For each successor state, run _N_ random simulations (rollouts). A rollout is a sequence of random moves from that successor state until a terminal state is reached.
4. **Scoring**: Each simulation ends in a terminal state with a score (e.g., win/loss, puzzle score). The value of a successor state is the average score over all _N_ simulations.
5. **Selection**: The agent then chooses the successor state with the best average score to move to.

This process replaces the static `h(n)` from Best-First or A* search with a computationally empirical estimate based on random exploration.

## Agentic Design for Monte Carlo Search

While a single function can run the simulations, an **agentic approach** decomposes this process into specialized roles, making the system more modular, extensible, and capable of sophisticated reasoning.

Here is a possible agentic architecture for this lab:

1. **Orchestrator Agent**: This agent manages the overall search process. It receives the current state and invokes the search tool.
    
    - **Responsibilities**: Identify successor states, delegate simulation tasks for each successor, and select the best move based on aggregated results.
2. **Simulator Agent**: This agent is responsible for executing a random rollouts.
    
    - **Role**: Given a starting state, perform random actions until a terminal state is reached.
    - **Inputs**: A game state.
    - **Outputs**: The terminal state and its final score.

This design often fits a **Manager-Worker pattern**, where the Orchestrator is the manager delegating simulation tasks (the "work") to one or more Simulator agents.

### Communication Design (MCP and A2A)

---

- **Model Context Protocol (MCP)**: The Orchestrator would use a `run_monte_carlo_evaluation` tool. This tool's schema would define its parameters, such as the `current_state` and the `number_of_simulations`. The tool call would trigger the multi-agent workflow.
- **Agent-to-Agent (A2A)**:
    - **Orchestrator → Simulator**: A request to run one simulation for a specific successor state.
    - **Simulator → Orchestrator**: A message containing the outcome and score of a completed simulation.

### Lab Activities / Task

---

This lab consists of two main parts. You will be provided with a Jupyter Notebook containing a basic implementation of Monte Carlo Search for the NY Times Spelling Bee puzzle. Your task is to first improve the search heuristic and then re-implement the core logic using an agentic architecture with AutoGen. This assignment is intended to be completed individually, and any code you submit must be your own.

## Part 1: Improving the Monte Carlo Heuristic

In this part, you will work with the provided conventional implementation of Monte Carlo Search. The base code uses a simple heuristic for its random rollouts (e.g., selecting letters with uniform probability). Your task is to design and implement a more intelligent heuristic to guide the random simulations.

1. **Analyze the Base Implementation**: Familiarize yourself with the provided code for the NY Times Spelling Bee problem and the simple Monte Carlo search function.
2. **Design an Improved Heuristic**: Brainstorm ways to make the random rollouts "smarter." Your heuristic should guide the simulation toward more promising paths (i.e., finding valid, high-scoring words more quickly). Consider factors like:
    - Letter frequencies in the English language.
    - Common letter pairings or trigrams.
    - Prioritizing the use of unique letters to form pangrams.
3. **Implement and Test**: Modify the simulation function to incorporate your new heuristic. Run experiments comparing the performance of your improved heuristic against the baseline. You should evaluate based on metrics like the quality of the solution found, the number of simulations required, and the total runtime.

## Part 2: Agentic Implementation of Monte Carlo Search

In this part, you will refactor the Monte Carlo search process into a multi-agent system using the AutoGen framework, similar to the architecture from Lab 2 and 3. This involves decomposing the task into specialized agent roles.

1. **Decompose the Task**: Break down the Monte Carlo search process into distinct sub-tasks that can be assigned to specialized agents. A suggested architecture includes:
    - An **Orchestrator Agent** to manage the overall search from a given state.
    - A **Simulator Agent** to execute a single random rollout using your improved heuristic from Part 1.
2. **Define Agent Roles and Communication**:
    - For each agent, define its role, responsibilities, inputs, and outputs.
    - Select an appropriate multi-agent design pattern (e.g., Manager-Worker) and justify your choice.
    - Specify the communication protocols. Describe the tool schema for invoking the search (**MCP**) and define at least two key agent-to-agent (**A2A**) interactions, detailing the sender, receiver, and purpose of the communication.
3. **Implement the Agentic System**:
    - Instantiate the agents in AutoGen with appropriate system prompts that define their roles.
    - Use a group chat or a manager to orchestrate the conversation between the agents to perform the Monte Carlo evaluation for each successor state.
4. **Reflection**: In your report, analyze the effectiveness of your agentic implementation. Reflect on what worked well, what challenges you faced, and how the agentic design compares to the conventional implementation in terms of modularity, complexity, and extensibility.

## Deliverables, Submission, and Deadline

You are required to submit a single document:

- A **Jupyter Notebook** (`.ipynb`) containing your complete, runnable code for both Part 1 and Part 2. The notebook should also include your written reflections and analysis for each part.

The deadline for this assignment is the end of the day (midnight) as listed on Canvas.

## Grading Criteria

The lab will be graded based on the following criteria, with each aspect worth 20% of the total score. The instructor reserves the right to modify the grading scheme after consultation with the class.

| Aspect                                  | Explanation                                                                                                                                                                   | Percent |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| **Heuristic Function Implementation**   | The design, correctness, and effectiveness of the improved heuristic in Part 1. Your implementation should demonstrate a clear strategy beyond simple random choices.         | 20%     |
| **Agent Design and Task Decomposition** | The logical breakdown of the Monte Carlo search problem into agent roles. Agents must have clear, well-defined responsibilities that map effectively to the sub-tasks.        | 20%     |
| **Agentic System Implementation**       | A functional AutoGen implementation that correctly orchestrates the agents to perform the Monte Carlo search as designed in Part 2.                                           | 20%     |
| **Communication Design**                | The specification of the MCP tool schema for invoking the search and the A2A interactions are clear, sufficient for collaboration, and well-justified.                        | 20%     |
| **Analysis, Reflection, and Coherence** | The deliverable is well-organized and clearly written. The reflection thoughtfully analyzes the heuristic's performance and compares the agentic vs. conventional approaches. | 20%     |