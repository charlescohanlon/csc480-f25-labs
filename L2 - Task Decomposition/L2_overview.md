# CSC 480 Lab 2: Task Decomposition, Multi‑Agent Design Patterns, and Communication Protocols

In this lab, you’ll practice breaking down a complex problem into smaller tasks, define specialized agents to tackle those tasks, choose a multi‑agent design pattern, and specify how agents will communicate. You’ll also outline and implement a simple three‑agent system with AutoGen to make these ideas concrete.

---

## Overview

Designing effective agentic systems starts with a good task decomposition, a clear mapping from tasks to agent roles, and a coordination style (design pattern) that fits the workflow. Communication protocols then provide the rules and message formats that let agents exchange information reliably and securely.

By the end of this lab, you will be able to:

- Decompose a complex problem into a comprehensive set of constituent tasks.
- Identify and define the roles, responsibilities, and abilities of individual agents.
- Select and justify an appropriate multi‑agent design pattern (Manager‑Worker, Sequential Pipeline, Collaborative Team).
- Explain and apply foundational agent communication protocols at a high level (MCP, A2A), and relate them to representative, real‑world standards.
- Start thinking about the architecture of your project (agents, tasks, design pattern, and interaction protocols)

---

## Communication protocols

Below are four protocol families commonly discussed when building multi‑agent systems.

1) [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP)
- What it is: A protocol for exposing tools, data sources, and structured context to models in a consistent, secure way so agents can discover and call tools reliably.
- Why it matters: Normalizes tool access, encourages strong typing and capability discovery, and supports safe, auditable tool use across agents.

2) [Agent‑to‑Agent](https://a2a-protocol.org/latest/) (A2A)
- What it is: Patterns and APIs that let agents converse directly with each other (peer‑to‑peer), exchange plans, critique outputs, and request help.
- Why it matters: Enables specialization and collaboration (e.g., Planner ↔ Solver ↔ Critic) with well‑defined message turns and termination criteria.

3) [Agent Communication Protocol](https://agentcommunicationprotocol.dev/introduction/welcome) (ACP, now apart of A2A under the Linux Foundation)
- What it is: A general umbrella for message schemas and performatives used by agents over standard transports (often REST/HTTP)
- Why it matters: Clear message intent (request, inform, propose) and structured, serializable payloads make it easy to integrate agents across services.

4) [Agent‑User Interaction](https://docs.ag-ui.com/introduction) (AG‑UI)
- What it is: Real‑time, event‑driven channels between agents and humans (text, audio, streaming tokens) that support interactive oversight and feedback.
- Why it matters: Enables human‑in‑the‑loop control, live streaming, and multimodal experiences.

---

## Lab activities

### Designing a simple agentic system for this lab

1) Problem & task decomposition
	- State the main problem your multi‑agent system will solve.
	- Brainstorm and list the steps and sub‑tasks needed to achieve the goal.

2) Agent definition
	- Identify your primary agents.
	- For each, define role, responsibilities, inputs/outputs, and success criteria.

3) Design pattern selection
	- Choose Manager‑Worker, Sequential Pipeline, or Collaborative Team.
	- Justify why this pattern fits your workflow and constraints.

4) Communication design
	- MCP: Describe the shared context and tools all agents need (schemas, access rules, at a high-level).
	- A2A: Specify at least two essential agent‑to‑agent interactions (sender, receiver, purpose, key fields, again at a high-level).

5) Interaction mapping
	- Create a diagram (flowchart/sequence diagram) showing agents, your chosen pattern, and MCP/A2A interactions.

6) Further exploration (optional)
	- Briefly discuss how ACP or AG‑UI could benefit your system and what you would adopt (e.g., DIDComm for secure messaging, Realtime API for UI streaming).

---

## Exercise: create a simple three‑agent system (AutoGen)

We’ll outline and implement a minimal, task‑decomposed system with three agents.

### Roles
- Planner: Decomposes the user goal into a concise, ordered plan of steps with acceptance criteria.
- Implementer: Executes the steps (at first, just produces a textual draft/answer; later you can add tools).
- Critic/Integrator: Reviews the Implementer’s output against the plan and criteria; suggests fixes or declares “done.”

#### Message flow
1) User (or a UserProxy) posts the initial task.
2) Planner returns a step‑by‑step plan with success tests.
3) Implementer produces an initial solution/draft.
4) Critic reviews vs. the plan; if gaps exist, proposes corrections.
5) Loop Implementer ↔ Critic until pass, then return final result to User.

#### Minimal architecture outline
- Instantiate three AutoGen agents with distinct system prompts.
- Use a group chat (or manager/orchestrator) to route messages and enforce turn‑taking.
- Define stop conditions: e.g., Critic emits “APPROVED” or a max‑turn budget.
- Optional challenge: add simple tools (e.g., a calculator function) and expose them via an MCP‑like schema.

#### Suggested acceptance criteria
- Plan includes: numbered steps, each with inputs/outputs and a testable check.
- Implementer addresses every step.
- Critic verifies the checks; only then returns “APPROVED.”

### Setup steps

1) Environment
	- Install AutoGen packages (same as in L1, e.g., autogen‑core, autogen‑agentchat, autogen‑ext[openai or azure]).
	- Configure your API key(s) (Azure OpenAI for the course environment, see the Slack #labs channel for instructions if you've forgotten how).

2) Define agents (system prompts) e.g.,
	- Planner: “You decompose tasks into minimal steps with explicit acceptance criteria.”
	- Implementer: “You follow the plan step‑by‑step and produce the requested artifacts.”
	- Critic: “You verify against the plan; if not satisfied, request concrete fixes; otherwise say APPROVED.”

3) Wire up a group conversation
	- Create a group chat (with or without an explicit manager). Seed with the User task.
	- Route messages: User → Planner → Implementer → Critic → (loop) → final User.
	- Enforce termination on APPROVED or max turns.

4) Try two tasks
	- A small analytical task (e.g., outline pros/cons of two sorting algorithms with criteria).
	- A short creative task (e.g., write a 150‑word summary with specified constraints).

5) Reflection
	- Note where the pattern worked well or struggled.
	- Consider adding one tool (e.g., simple Python function) and observe the effect.

For API usage and examples of multi‑agent chat, see the AutoGen docs: https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat

---

## Deliverables and submission

Submit a single team document (PDF or Markdown) and a link to your code/notebook (if it's on GitHub make sure it's public)

For this lab, include your (to be filled in the notebook)...
- Team Members: Names and Cal Poly email addresses
- Task breakdown: A detailed, structured list of decomposed tasks.
- Agent profiles: Roles, responsibilities, inputs/outputs, and success criteria.
- Multi‑agent design pattern: Your choice and a brief justification.
- Communication design: MCP description and at least two A2A interactions (sender, receiver, purpose, fields).
- Interaction diagram: Visual diagram of the agent workflow.
- Hands‑on exercise (code or outline): Your three‑agent setup and a short reflection.

Submission method: GitHub repository or Canvas per Dr. Kurfess' guidance.

---

## Evaluation criteria (20% each)

| Aspect | Explanation | Percent |
| :-- | :-- | :--: |
| Problem Description & Task Decomposition | Goal is clear; problem is logically and comprehensively broken into sub‑tasks. | 20 |
| Agent Design | Agents have clear roles and abilities that map to the tasks; responsibilities are well‑defined. | 20 |
| Design Pattern Selection & Justification | Pattern fits the workflow; justification reflects thoughtful trade‑offs. | 20 |
| Communication Design | MCP and A2A interactions are clear, complete, and sufficient for collaboration. | 20 |
| Clarity & Coherence of Deliverables | Document is well‑organized; diagram accurately ties the architecture together. | 20 |