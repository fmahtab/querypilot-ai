# QueryPilot AI

QueryPilot AI is an AI-powered retail analytics and knowledge assistant built with FastAPI, OpenAI, Google ADK, PostgreSQL, and pgvector.

> **Note:** RetailStar is a fictional retail company created for educational and demonstration purposes.

## Overview

QueryPilot AI allows users to ask RetailStar business and policy questions in natural language.

The project demonstrates several production-oriented AI engineering patterns, including:

- intent-based request routing
- Retrieval-Augmented Generation (RAG)
- semantic search with PostgreSQL and pgvector
- agentic tool use
- conversational context
- durable user memory
- structured evaluation and failure analysis

The system separates business knowledge from user memory: RetailStar documentation determines **what is true**, while user memory can influence **how information is explained**.

## Example Questions

Knowledge-base questions:

- What is BOPIS?
- What happens when inventory is low?
- How long are pickup orders held?
- What is the return policy?

Conversational follow-ups:

- What happens when inventory is low?
- What does that status mean?
- Who gets notified?

The application can also persist selected user context across sessions and use it to personalize future explanations.

## Architecture

QueryPilot uses a routing layer to determine how a question should be handled.

```text
User Question
     |
     v
Conversation Contextualization
     |
     v
Intent Classifier
     |
     +-------------------+--------------------+
     |                   |                    |
     v                   v                    v
 GENERAL          KNOWLEDGE_BASE          DATABASE
     |                   |                    |
   OpenAI           ADK Agent            Placeholder
                         |
                         v
               search_knowledge_base
                         |
                         v
                 PostgreSQL/pgvector
                         |
                         v
                 Grounded Response

```

The DATABASE route is currently a placeholder for future natural-language-to-SQL functionality.

## Retrieval-Augmented Generation (RAG)

RetailStar business documentation is stored as Markdown files and processed through a RAG pipeline.

The pipeline:

- Loads RetailStar documentation.
- Splits documents into heading-aware chunks.
- Generates embeddings for each chunk.
- Stores embeddings in PostgreSQL using pgvector.
- Performs semantic similarity search for relevant chunks.
- Uses retrieved content as the source of truth when answering RetailStar knowledge questions.

Examples of knowledge-base documents include:

- inventory policy
- returns policy
- business glossary
- company overview
- QueryPilot user guide

Responses also expose the retrieved source documents for transparency.

## Agentic Knowledge Retrieval

QueryPilot includes a Google ADK knowledge agent with access to a real retrieval tool:

`search_knowledge_base`

For RetailStar knowledge questions, the agent can decide to call the tool, retrieve relevant information from the pgvector knowledge base, observe the result, and generate a grounded response.

The agent is instructed not to rely on general model knowledge for RetailStar-specific policies because RetailStar is fictional.

This provides a clear agent workflow:

```text
Question
   |
   v
Agent Decision
   |
   v
search_knowledge_base()
   |
   v
Retrieve Relevant Chunks
   |
   v
Observe Tool Result
   |
   v
Grounded Answer
```

The standalone agent and tool invocation have been successfully tested. Integration of the agent runner into the main `/ask` knowledge-base route is currently in progress.

## Conversation Memory

QueryPilot supports conversational follow-up questions.

Recent messages are sent with each request and used to contextualize ambiguous follow-ups before routing and retrieval.

For example:

```
User: What happens when inventory is low?
User: What does that status mean?
User: Who gets notified?
```

QueryPilot rewrites follow-up questions into standalone questions before classification and retrieval.

Conversation history is intentionally temporary and represents the current interaction rather than long-term user information.  

## Durable Memory

QueryPilot also implements durable user memory using PostgreSQL.

Unlike conversation history, durable memory survives application restarts and new chat sessions.

### What is stored?

The current implementation stores a small set of explicit, stable user facts:

- `role`
- `experience_level`

### When is memory written?

A memory extraction step evaluates the user's message before saving anything.

Only explicit, stable, and potentially useful user information is eligible for durable storage. Ordinary questions, RetailStar policy information, and inferred user characteristics are not stored.

### Where is memory stored?

Durable memories are stored in the PostgreSQL `user_memories` table.

Each memory is associated with a user and memory key, with a uniqueness constraint preventing duplicate values for the same user/key combination.

### How is memory retrieved?

Relevant durable memory is loaded during `/ask` processing and supplied as personalization context.

Memory may affect the framing or level of detail of an answer, but it is not treated as a source of truth for RetailStar policies.

In other words:

**RAG determines what is true; memory helps determine how to explain it.**

### Forgetting / deletion

Explicit memory deletion is not implemented in the current capstone version.

This is intentionally left as future work so the capstone can focus on memory extraction, persistence, retrieval, and cross-session recall.

The current demo also uses a fixed demo user rather than production authentication. A production implementation would associate memories with authenticated user identities.

## Evaluation

QueryPilot includes an evaluation workflow for testing routing, retrieval, grounded responses, and refusal behavior.

A golden evaluation suite currently contains **11 test cases**, with the latest pre-agent-integration run passing:


**11 / 11 tests (100%)**


Manual TRACE analysis was also performed across 18 traces.

Observed failure modes were categorized into:

- Routing Failure
- Retrieval Failure
- Knowledge Base Gap
- Unsupported Answer Failure

The evaluation process has already been used to identify and correct issues in both the knowledge base and routing logic.

A final regression evaluation will be performed after the ADK agent is integrated into the main request flow.

## Tech Stack

- Python
- FastAPI
- OpenAI API
- Google Agent Development Kit (ADK)
- Gemini
- PostgreSQL
- pgvector
- SQLAlchemy
- Alembic
- Pydantic
- Streamlit
- Docker

## Project Status

QueryPilot AI is under active development as an AI Engineering Bootcamp capstone.

### Completed

- FastAPI `/ask` endpoint
- intent classification and routing
- RAG ingestion pipeline
- pgvector semantic retrieval
- grounded RetailStar knowledge responses
- source tracking
- conversational follow-up handling
- durable PostgreSQL memory
- memory extraction and update logic
- cross-session memory recall
- TRACE evaluation suite
- manual failure analysis
- Streamlit interface
- Google ADK knowledge agent
- real knowledge-base retrieval tool
- production PostgreSQL database and pgvector setup

### In Progress

- integrating the ADK agent into the main knowledge-base route
- graceful handling of model-provider failures
- public FastAPI deployment
- public Streamlit deployment
- final regression evaluation
- capstone demo preparation

## Planned Future Work

Potential extensions include:

- natural-language-to-SQL generation and execution
- SQL validation and self-correction
- authenticated user accounts
- per-user memory isolation
- explicit memory management and deletion
- additional agent tools
- richer observability and tracing
- production-grade retry and fallback strategies
- Next.js/TypeScript frontend

## Disclaimer

RetailStar is a fictional company created solely for educational and demonstration purposes. All business data, documentation, products, policies, and scenarios in this project are fictional and do not represent any real organization.