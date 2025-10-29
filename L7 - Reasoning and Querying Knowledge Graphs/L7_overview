# Lab 7: Reasoning and Querying Knowledge Graph
### Overview/Background
This lab continues from Lab 6 by turning the case CSVs into a working graph and using Cypher to answer investigative questions. You will verify connectivity to a local Neo4j instance, prepare basic schema constraints and indexes, import entities and relationships, perform sanity checks, and then run queries that surface timelines, locations, and relationships. An optional agentic path lets you use an LLM-based assistant to propose and execute read-only queries. You’ll wrap up with a short reflection on trade-offs and lessons learned.

---

## Learning Objectives

By the end of this lab, you will be able to:

- Load entities and typed relationships from CSVs into a graph DB.
- Create and verify uniqueness constraints and useful indexes.
- Formulate Cypher queries that answer investigative questions and interpret results.
- Optionally use an agentic assistant to plan and execute read queries.
- Reflect on manual vs. agentic querying and identify next improvements.

---

## Concepts and Principles

- Node and relationship modeling with properties (e.g., dates, outcomes, relationshipType)
- Constraints (unique identifiers) and indexes for performance and quality
- Read-oriented Cypher patterns (MATCH/OPTIONAL MATCH, filtering, ordering, aggregation)
- Data validation via sanity checks and counts
- Agentic tool use for query planning and execution (optional)

---

## Lab Activities / Structure

- Setup and connectivity
	- Ensure the Python driver can connect to your local Neo4j instance.
- Data loading and preview
	- Read the provided case CSVs and inspect a few rows per file.
- Schema preparation
	- Create uniqueness constraints and helpful indexes for common lookups.
- Graph ingestion
	- Insert nodes for people, locations, events, evidence, and cases.
	- Insert typed relationships (person–person, person–location, evidence–location, person–case) with relevant properties.
- Sanity checks
	- Verify node totals and counts per relationship type.
- Investigative querying
	- Write Cypher to explore timelines, last-known locations, evidence provenance, and social/family ties.
- Optional agentic querying
	- Use an LLM-based assistant to propose and run read-only queries.
- Reflection
	- Compare manual and agentic approaches and outline follow‑ups.

---

## Deliverables and Submission

- Evidence of a successful connection check or a short diagnostic if it fails.
- Import outcomes (brief log or summary) and sanity‑check counts.
- A short reflection which includes comparing manual vs. agentic querying and listing next steps.

Submit your completed materials by the deadline via Canvas.

---

## Evaluation Criteria (guideline)

| Aspect | Explanation | Percent |
| :-- | :-- | :-- |
| Connectivity and Setup | Demonstrates working connection or reasoned troubleshooting. | 15 |
| Data Import & Schema | Applies constraints/indexes; ingests nodes/relationships correctly. | 25 |
| Querying & Analysis | Queries answer meaningful investigative questions with clear interpretation. | 35 |
| Reflection Quality | Specific, thoughtful observations and actionable next steps. | 25 |
