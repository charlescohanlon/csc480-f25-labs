# Cal Poly SLO CSC 480-F25 Artificial Intelligence

**Prof. Franz J. Kurfess, Charles O'Hanlon**

# Lab 1: (Agentic) LLMs

> This lab has two parts. **Part 1** covers text-based generative AI tools. **Part 2** is a short, hands-on “hello world” with **LLMs as agents** using **AutoGen**.

## Part 1 - Text-based Generative AI

### Overview

While chatbots have been around for a long time[^1], over the last year or so the use of Large Language Models (LLMs) as foundations for generative AI tools has significantly enhanced their capabilities.

Large language models (LLMs) are a type of artificial intelligence (AI) that have been trained on massive datasets of text and code. This training allows LLMs to learn the statistical relationships between words and phrases, and to generate text that is similar to the text they were trained on.

Generative AI tools use LLMs to generate text, translate languages, write different kinds of creative content, and answer questions in an informative way. For example, an LLM could be used to generate a news article, translate a novel from one language to another, write a poem, or answer a question about a complex topic.

LLMs are still under development, but they have the potential to revolutionize the way we interact with computers. Generative AI tools that use LLMs can be used to automate tasks, create new forms of art and entertainment, and provide us with new insights into the world around us.

In this lab activity, you will explore and critically examine some of the most popular generative AI tools that use LLMs. You will evaluate the strengths and weaknesses of these tools, and identify the potential benefits and risks of using them.

#### Popular Generative AI Tools

| Chatbot | LLM Used | Market Share (%) | Comments/Uses |
|---------|----------|------------------|---------------|
| ChatGPT | GPT-4o, GPT-3.5/4/5 | 60.6 | General-purpose, largest user base, rapid integration |
| Microsoft Copilot | GPT-4 | 14.1 | Assistant in Windows, Office, and enterprise tools |
| Google Gemini | Gemini | 13.4 | Native to Google Search, Workspace, and Android |
| Perplexity | Mistral 7B, Llama 2 | 6.5 | Focused on accuracy and search |
| Claude AI | Claude 3 | 3.5 | Business-focused, fast-growing segment |
| Grok | Grok 2/3/5 | 0.8 | Platform-specific, fast conversational search |

This list is not comprehensive, and more tools and applications based on them become available on an ongoing basis. For this lab, you are free to select any such tool or model that interacts with a user through a text-based interface.

---

### Goals and Objectives

The goal of this exercise is to explore text-based chatbots, virtual assistants and similar tools based on Large Language Models (LLMs). It also contains a simple programming exercise to familiarize students with Jupyter Notebooks in the Google Colab environment.

This lab can be done individually or in a team. For each team member, a different tool needs to be evaluated. In a team, you can develop a common set of tasks, prompts, dialog flows or other structures and try it out with different tools. Each team member must submit their own answers. You can also create a common document for the team, point to it from the survey, and enter only short answers there.

---

### Assessment

The following aspects give you some guidance on the assessment of the generative AI tool that you are exploring. In one or two paragraphs, state your thoughts on the aspect for your selected too.

#### Description

How do you perceive the generative AI tool you selected? Why did you select it for this exercise? Do you have prior experience with it or similar ones? For full points, it is not sufficient to copy and paste a generic description of the tool (e.g., from its Web page or Wikipedia).

#### Truthfulness

Was the information provided factually correct? Did the tool hallucinate, make up random facts, or appear to generate incorrect information on purpose? Does it reveal the sources for its information? If you ask the same question in a slightly different formulation, do you get consistent answers? Would you trust the information you got to make important decision, such as about your health or your career? Feel free to address other factors that you find relevant here.

#### Creativity

Did the tool present the information in a novel, original way, or did it appear to reproduce existing content in a bland manner? Was the content or presentation surprising to you? See Koivisto, M., and Grassini, S. (2023) below for a recent examination.

#### Advantages

Based on your experiences, what advantages did you see? How were they evident in this particular tool? Are there actual or potential applications where you would consider using it?

#### Problems

What potential or actual problems to you see with your selected tool? Did you encounter any of them in your experiments? Are there circumstances where you would not use the tool?

---

### Deliverables, Submission, and Deadline

The deliverable consists of

* answering the **Lab 1 Questionnaire** about the selected tools
* Completing the **CSC 480-F25 Lab 1: Jupyter Basics and Python Refresher**

The deadline for this assignment is the end of the day (midnight) as listed on Canvas. In general, labs are due on Thursday the week after they were published.

---

### Grading Criteria

I’m planning to use the following scheme for the grading of this assignment. However, I reserve the right to modify it, after consultation with the students in the class.

| Aspect                     | Explanation                                                                                                                                             | Percent |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----: |
| Generative AI Descriptions | Brief description of the tool(s) you used.                                                                                                              |    20   |
| Truthfulness               | Was the information provided factually correct? Did the tool hallucinate, make up random facts, or appear to generate incorrect information on purpose? |    10   |
| Creativity                 | Did the tool present the information in a novel, original way, or did it appear to reproduce existing content in a bland manner?                        |    10   |
| Advantages                 | What advantages of generative AI tools do you see? How were they evident in this particular tool?                                                       |    20   |
| Problems                   | What problems do you see with generative AI tools? How were they evident in this particular tool?                                                       |    20   |
| Programming Exercise 1     | Simple array calculations.                                                                                                                              |    10   |
| Programming Exercise 2     | Using the numPy library.                                                                                                                                |    10   |

---

## Part 2 - LLMs as Agents (AutoGen “Simple Agent”)

### Brief introduction: LLMs as agents

Traditional chat use treats an LLM as a **single turn-by-turn responder**. In contrast, **LLM agents** are supposed to be software entities that:

* **Perceive** (read prompts, tool outputs, retrieved documents),
* **Reason/Plan** (decide what to do next, possibly break a task into steps or ask for clarification),
* **Act** (invoke tools/APIs, write and run code, query data sources, call other agents), and
* **Reflect** (evaluate intermediate results, revise plans, stop when goals are met).

Key ideas you’ll encounter w/ Agentic LLMs:

* **Tool use / function calling.** The model doesn’t just reply with text; it can call named functions (e.g., a calculator, database query, or web search) and incorporate the results into its next step.
* **State & memory.** Agents keep track of goals, partial results, and constraints across turns.
* **Planning & reflection.** Agents can draft a plan, execute it step-by-step, and critique their own outputs to improve reliability.
* **Multi-agent collaboration.** Multiple specialized agents (e.g., a “Planner,” a “Coder,” a “Reviewer”) can converse to solve a problem better than a single generalist.
* **Human-in-the-loop.** You can require confirmation before an agent takes certain actions, or ask it to explain/justify decisions.
* **Trade-offs.** Agents are powerful but introduce new challenges: cost/latency, non-determinism, coordination failures, tool security/permissions, and evaluation.

### The AutoGen framework (what it is and why it’s useful)

**AutoGen** is an open-source framework for building **multi-agent LLM applications**. It provides ready-made agent classes and a conversation engine so agents can **chat with each other (and with you)** to accomplish tasks.

At a glance:

* **Agent building blocks.** Define agents with roles (e.g., *assistant* vs. *user proxy*), goals, system prompts, and tool access.
* **Orchestrated conversations.** Use a **GroupChat** (plus a manager) to route messages among agents, enforce turn-taking, and detect when to stop.
* **Tools & code execution.** Register Python functions or external APIs as tools; agents can request tool calls, receive results (“observations”), and continue the dialogue.
* **Human oversight.** Keep a **UserProxy** in the loop to approve actions, provide hints, or inject data.
* **Extensibility.** Add specialized agents (retrieval, data analyst, tester), inject domain knowledge, or constrain behavior with guards and termination rules.
* **Logging & budgets.** Track token usage, set stop conditions, and record traces to help with grading/evaluation.

Typical patterns you may use in your project:

* **Planner-Solver.** One agent drafts steps; another executes them (with tools) and reports back.
* **Critic-Author.** An authoring agent writes; a critic reviews and suggests fixes until quality criteria are met.
* **Team of specialists.** A manager delegates subtasks to domain experts (e.g., retrieval, coding, analysis), then integrates results.

### What you’ll do in part 2 of this lab

1. **Install core packages**
   `autogen-core`, `autogen-agentchat`, `autogen-ext[openai]`, and `openai` (plus `python-dotenv` if you want to load a `.env` file).

2. **Set your OpenAI API key**
   Either export `OPENAI_API_KEY` as an environment variable, or uncomment the placeholder in the notebook to set it directly. (`dotenv` is optional: create a `.env` file and call `load_dotenv()`.)

3. **Note on asyncio**
   AutoGen uses Python **asyncio**; you’ll run an `async` function that spins up the agent and awaits an interactive chat loop.

4. **Run the simple agent**
   The notebook creates an `OpenAIChatCompletionClient`, instantiates an `AssistantAgent` (e.g., name: `"SimpleAgent"` with a brief `system_message`), and starts an interactive console with a seed task such as **“Hello world.”**

### Mini-exercises (exactly what to try)

* **Run the final cell** to start the console chat (`await setup_simple_chat()` in the notebook). Say hi and ask a couple of questions.
* **Edit the system message** (e.g., change tone or add a constraint) and re-run to see the effect.
* **Change the seed task** (replace “Hello world” with a question you choose) and observe the first response.
* *(Optional)* **Swap models or settings** in the client to compare behavior.

> **Learning outcome:** understand the smallest working example of an **LLM-as-agent** in AutoGen: configure client → create `AssistantAgent` → start an interactive chat loop. This sets up later labs where you’ll add tools and multi-agent coordination.

---

### Acknowledgments

This document was created with the assistance of two generative AI tools, Google Bard and ChatGPT. Below are the disclosure statements suggested by the respective tool.

#### Google Bard

**Disclosure:** Some of the content in this lab activity was generated using a large language model (LLM) called Google Bard or ChatGPT. LLMs are machine learning models that can generate text, translate languages, write different kinds of creative content, and answer your questions in an informative way.

#### ChatGPT

**Disclosure Statement: Use of AI Models in Lab Activities**

In this lab activity, we employ artificial intelligence (AI) models, specifically ChatGPT and Google Bard, to enhance the learning experience and explore AI applications. It is essential to understand the role and implications of these AI tools in our activities.

**ChatGPT:**
ChatGPT is a language model developed by OpenAI. It is designed to generate human-like text based on the input it receives.

Please note that ChatGPT's responses are generated algorithmically and may not always reflect factual or unbiased information. Students are encouraged to critically evaluate the responses for accuracy and ethical considerations.

We use ChatGPT to facilitate text-based interactions and generate responses to questions or prompts.

**Google Bard:**
Google Bard is a generative AI tool developed by Google. It is used for creative text generation and storytelling.

Similar to ChatGPT, Google Bard's responses are generated algorithmically and should be assessed for accuracy and appropriateness.

We utilize Google Bard to encourage creative exploration and generate imaginative content in our lab activities.

**Ethical Considerations:**
AI models like ChatGPT and Google Bard have the potential to generate content that may include biased or inappropriate information. It is essential to exercise responsible use of these tools.

Students are encouraged to consider ethical implications, potential biases, and reliability when using the AI-generated content in their lab work.

In cases where AI-generated content may impact sensitive or critical topics, it is advisable to cross-verify information with reputable sources.

**Feedback and Reporting:**
We welcome your feedback regarding the use of AI models in our lab activities. If you encounter any concerns related to the generated content or believe that it violates ethical guidelines, please report it to the instructor.

**Conclusion:**
By acknowledging the use of ChatGPT and Google Bard and understanding the ethical considerations associated with these AI tools, we aim to foster responsible and informed use of AI technology in our educational activities. These tools are employed to enhance creativity and exploration but should be used thoughtfully and in alignment with ethical principles.

If you have any questions or require further clarification regarding the use of AI models in this lab, please feel free to reach out to the instructor or teaching assistant.

---

### References

* Koivisto, M., and Grassini, S. (2023). Best humans still outperform artificial intelligence in a creative divergent thinking task | Scientific Reports. *Scientific Reports* 13, 13601. doi: 10.1038/s41598-023-40858-3
* Weizenbaum, Joseph. (1966). ELIZA—a computer program for the study of natural language communication between man and machine. *Communications of the ACM*, 9(1), 36-45. [https://doi.org/10.1145/365153.365168](https://doi.org/10.1145/365153.365168)

---