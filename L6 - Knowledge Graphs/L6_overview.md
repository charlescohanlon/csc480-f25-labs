# L6 Overview

## CSC 480 Lab 6: Knowledge Graphs

## Overview/Background

This lab introduces Knowledge Graphs in Neo4j with a hands-on focus on standing up a local database, verifying connectivity from Python, inspecting a small case dataset (CSV files), and creating a practical schema with constraints and indexes via Cypher. You’ll also have an optional path to try an agentic system (AutoGen + Azure OpenAI) that collaborates to propose and create the schema automatically. This lab sets the stage for reasoning and querying in Lab 7.

What you’ll actually do in the notebook:
- Install Python packages and confirm a live connection to a local Neo4j instance (via the Bolt driver).
- Unzip and preview the provided CSVs to understand entities and relationships at a glance.
- Use a helper function to execute Cypher that creates schema constraints and indexes (structure only; no data ingestion in this lab’s example schema cell).
- Optionally run an agentic system that plans and issues Cypher to create the schema (may be slow and requires Azure OpenAI configuration).
- Reflect on the trade-offs between manual Cypher and agentic schema creation, and capture lessons for Lab 7.

---

## Learning Objectives

By the end of this lab, you will be able to:

- Configure and connect to Neo4j Desktop from Python using the official driver.
- Inspect CSV-based case data and reason about potential node labels and relationship types.
- Create schema constraints and indexes in Neo4j using Cypher (and interpret execution counters).
- Understand the capabilities and limitations of an agentic approach to schema planning and creation.
- Articulate modeling and operational trade-offs you’ll consider when querying in Lab 7.

---

## Concepts and Principles

- Graph data modeling for knowledge graphs (nodes, relationships, properties)
- Identifiers, uniqueness constraints, and indexing for performance and data quality
- Cypher basics for schema management (constraints, indexes)
- Python–Neo4j connectivity (Bolt driver)
- Agentic orchestration (optional): collaborative planning and tool use to emit Cypher

---

## Tools and Resources

- Neo4j Desktop (a neo4j local instance)
- Python with packages: `neo4j`, `pandas` and `neomodel`
- Optional: AutoGen libraries and Azure OpenAI access for the agentic path

---

## Lab Activities / Notebook Structure

- Part 1 - Setup Neo4j and Connectivity
	- Install required Python packages.
	- Start a Neo4j Desktop DB and confirm the Bolt connection with a simple `RETURN 1` query using the Python driver.

- Part 1 (cont.) - Explore Provided Data
	- Unzip `L6-7_data.zip` and preview CSVs with `pandas` to understand the available entities and relations. The preview is also used as context for the optional agentic workflow.

- Part 2 - Example Schema via Cypher (Structure Only)
	- Use a provided `execute_cypher_query` helper to run a schema script that creates constraints and indexes for labels like `Case`, `Event`, `Evidence`, `Location`, and `Person`.
	- Observe the Neo4j summary counters (nodes/relationships created will remain 0 here; the script configures schema, not data import).
	- Be aware that some relationship property existence constraints require Enterprise and may not succeed in Community.

- Part 3 - Optional Agentic Schema Builder
	- Configure an Azure OpenAI client and instantiate two agents: a Schema Planner and a Schema Creator.
	- Run a round-robin group chat that proposes and executes Cypher using the helper tool, terminating when the creator reports completion.
	- This step is optional, may be slow, and requires proper Azure configuration.

- Part 4 - Reflection
	- Compare manual Cypher vs. agentic creation, discuss constraints/indexes impact, note modeling decisions and issues, and plan next steps for querying in Lab 7.

---

## Conventional (Manual) Path: Minimal Workflow

1) Verify connectivity
- Use the Python driver to connect to `bolt://127.0.0.1:7687` with your credentials and run `RETURN 1 as test`.

2) Inspect the data
- Unzip and preview the CSVs

3) Create schema
- Execute the provided Cypher script to set constraints and indexes. Review the counters and note any community vs. enterprise limitations.

---

## Optional Agentic Path: AutoGen-Assisted Schema Creation

- Configure Azure OpenAI (deployment, endpoint, and key) and install AutoGen packages.
- Run the agentic workflow that:
	- Plans a schema in context of the previewed data.
	- Calls the provided Cypher execution tool to materialize constraints/indexes.
- Expect longer runtimes and possible non-deterministic progress. Treat as exploratory; the manual path suffices for completion.

---

## Deliverables and Submission

- Your completed `L6.ipynb` with:
	- Connection check output (successful or diagnostic message with reasoning).
	- Schema creation attempt and output logs (execution counters and any errors noted).
	- Reflection answers in the final section.
	- (Optional) Evidence of attempting the agentic workflow, if configured.

Submit to Canvas by the posted deadline.

---

## Evaluation Criteria (guideline)

| Aspect | Explanation | Percent |
| :-- | :-- | :-- |
| Setup & Connectivity | Demonstrates a good-faith attempt to connect and diagnose issues (or shows success). | 20 |
| Schema Constraints/Indexes | Runs the schema Cypher, interprets counters, and recognizes community vs. enterprise limitations. | 25 |
| Data Inspection & Modeling Rationale | Shows meaningful inspection of CSVs and articulates how they inform labels/relationships. | 20 |
| Optional Agentic Attempt | If attempted, documents setup, outcome, and limitations clearly. | 10 |
| Reflection Quality | Clear, specific analysis of what worked, what struggled, and plans for Lab 7. | 25 |
