📂 Engineering Handoff: Project "Infinite Echoes"
=================================================

**To:** Senior Full-Stack Software Engineer (LLM)

**From:** Lead Software Architect

**Date:** Current

**Subject:** Implementation Phase 1 - Domain Logic & Mechanics

1\. Project Vision & Architecture
---------------------------------

**"Infinite Echoes"** is a text-based, single-player RPG that uses a **Client-Server** architecture.

-   **Client:** A Python TUI (Textual) communicating via HTTP.

-   **Server:** A FastAPI backend that orchestrates a "Lazy Simulation" world.

-   **Core Logic:** A "Reasoning Router" (LangGraph) that dynamically switches between **Deterministic Mechanics** (D&D 5e Rules) and **Narrative Generation** (LLM).

### The Architectural Stack

-   **Language:** Python 3.11+

-   **Orchestration:** LangGraph (Stateful, Cyclic Agents)

-   **Database:** PostgreSQL 16 + `pgvector` (Async SQLAlchemy)

-   **Data Model:** "Hybrid ECS" (Strict SQL columns for indexing + JSONB `attributes` for flexible game stats).

2\. Current Status (What has been built)
----------------------------------------

The architectural scaffolding is complete. The following files exist and **must be respected**:

### A. Infrastructure

-   **`docker-compose.yml`**: Runs Postgres with the `pgvector` image.

-   **`pyproject.toml`**: Defines dependencies (`fastapi`, `textual`, `langgraph`, `sqlalchemy`, `asyncpg`).

-   **`src/server/config.py`**: Environment variable management.

-   **`src/server/db/session.py`**: Async database session and engine setup.

### B. Critical Data Models

-   **`src/server/db/models.py`**: Defines the **Entity** class.

    -   *Note:* Mechanics (Str, Dex, HP, AC) are stored in the `attributes` JSONB column. Do not create new SQL tables for stats.

    -   *Note:* The `embedding` column exists for the "Dream Protocol" (future task).

### C. AI Topology

-   **`src/server/ai_engine/state.py`**: Defines `AgentState` (TypedDict). This is the shared brain passed between graph nodes.

-   **`src/server/ai_engine/graph.py`**: The StateGraph definition.

-   **`src/server/ai_engine/nodes.py`**: Async stubs for `router`, `mechanics`, and `narrator`.

3\. Your Mission (Immediate Next Steps)
---------------------------------------

You are starting **Phase 2: Domain Logic (The Mechanics)** of the Implementation Blueprint.

**Goal:** Build the deterministic "Game Engine" that powers the simulation. This code must be pure Python, testable, and **completely independent of the AI/LLM**.

### Task Checklist

Please implement the following in `src/server/game_mechanics/`:

1.  **`dice.py`**:

    -   Implement a standard dice roller (e.g., `roll("1d20+5")`).

    -   Should return structured results (total, individual die faces).

2.  **`rules.py`** (The Resolution Engine):

    -   Implement combat resolution logic.

    -   **Input:** Source Entity (dict), Target Entity (dict), Action Type.

    -   **Logic:** * Extract stats from `Entity.attributes`.

        -   Compare Attack Roll vs AC.

        -   Calculate Damage.

    -   **Output:** A structured result dictionary (Hit/Miss, Damage amount, Status effects).

3.  **Unit Tests**:

    -   Create `tests/unit/test_mechanics.py`.

    -   Verify the math handles edge cases (Natural 20s, Negative modifiers).

### Critical Constraints

-   **Do NOT use AI calls here.** This layer is pure math.

-   **Do NOT access the database directly.** The functions should accept pure dictionaries (or Pydantic models) representing the entities, not DB sessions.

-   **Compatibility:** Your output format must be consumable by the `mechanics_node` in `src/server/ai_engine/nodes.py`.

4\. Reference: The Data Shape
-----------------------------

When writing `rules.py`, assume the `Entity.attributes` dictionary looks like this:

```
{
    "stats": {
        "str": 16, "dex": 12, "con": 14,
        "int": 10, "wis": 10, "cha": 8
    },
    "combat": {
        "hp": 25,
        "ac": 14,
        "initiative_bonus": 1
    },
    "inventory": ["rusty_sword", "potion"]
}

```

**Proceed with implementing `src/server/game_mechanics/` now.**