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

**Proceed with implementing `src/server/game_mechanics/` now.**📂 Engineering Handoff: Project "Infinite Echoes" (Revised)
===========================================================

**To:** Senior Full-Stack Software Engineer (LLM) **From:** Lead Software Architect **Date:** Current **Subject:** Implementation Phase 1 - Domain Logic & Mechanics

1.  Project Vision & Architecture

* * * * *

**"Infinite Echoes"** is a text-based, single-player RPG driven by a **Client-Server** architecture.

-   **Vision:** A reactive role-playing experience where the world evolves based on player actions, strictly adhering to **D&D 5e (SRD)** rules.

-   **Core Logic:** A "Reasoning Router" (LangGraph) dynamically switches between **Deterministic Mechanics** (D&D 5e Rules) and **Narrative Generation** (LLM).

### The Architectural Stack

-   **Language:** Python 3.11+ (Unified Client/Server).

-   **Orchestration:** LangGraph (Stateful, Cyclic Agents).

-   **Database:** PostgreSQL 16 + `pgvector` (Async SQLAlchemy).

-   **Data Model:** **Hybrid ECS**. Strict SQL columns are used for high-frequency indexing (HP, AC), while JSONB is used for flexible narrative/stat attributes.

1.  Current Status (The Foundation)

* * * * *

The architectural scaffolding is complete. The following files exist and establish the patterns you must follow.

### A. Infrastructure

-   **`docker-compose.yml`**: Runs Postgres with the `pgvector` image.

-   **`pyproject.toml`**: Defines dependencies (`fastapi`, `textual`, `langgraph`, `sqlalchemy`, `asyncpg`).

-   **`src/server/db/session.py`**: Async database session and engine setup.

### B. Critical Data Models (Reconciled)

-   **`src/server/db/models.py`**: Defines the `Entity` class.

    -   **Correction:** You must ensure the `Entity` model aligns with the **Implementation Blueprint**.

    -   **Strict Columns (SQL):** `hp_current`, `hp_max`, `ac`, `initiative`, `is_dead`. *These are indexed for query performance.*.

    -   **Flexible Attributes (JSONB):** `attributes` column. Stores Ability Scores (Str, Dex), Skills, and Inventory..

    -   **Vector Embedding:** `embedding` column exists for the "Dream Protocol" (future RAG tasks).

### C. AI Topology

-   **`src/server/ai_engine/graph.py`**: The StateGraph definition using LangGraph.

-   **`src/server/ai_engine/nodes.py`**: Async stubs for `router`, `mechanics`, and `narrator`.

1.  Your Mission (Immediate Next Steps)

* * * * *

You are starting **Phase 2: Domain Logic (The Mechanics)**.

**Goal:** Build the deterministic "Game Engine" that powers the simulation. This code must be pure Python, testable, and **completely independent of the AI/LLM**.

### Task Checklist

Implement the following in `src/server/game_mechanics/`:

1.  **`dice.py`**:

    -   Implement a standard dice roller (e.g., `roll("1d20+5")`).

    -   Should return structured results (total, individual die faces).

2.  **`rules.py`** (The Resolution Engine):

    -   Implement combat resolution logic.

    -   **Input:** Source Entity (dict), Target Entity (dict), Action Type.

    -   **Logic:**

        -   Extract modifiers from `attributes` (e.g., Str mod from Score).

        -   Compare Attack Roll vs `ac` (from Strict SQL field).

        -   Calculate Damage.

        -   **Check Death State:** If `hp_current` drops to 0, mark result as "Unconscious/Dead" (Supports SRS "Legacy System" requirement).

    -   **Output:** A structured result dictionary (Hit/Miss, Damage amount, Status effects).

3.  **Unit Tests**:

    -   Create `tests/unit/test_mechanics.py`.

    -   Verify math handles edge cases (Natural 20s, Negative modifiers).

### Critical Constraints

-   **Do NOT use AI calls here.** This layer is pure math.

-   **Do NOT access the database directly.** The functions should accept pure dictionaries (or Pydantic models) representing the combined state of the entity (SQL columns + JSON attributes merged).

-   **Compatibility:** Your output format must be consumable by the `mechanics_node` in `src/server/ai_engine/nodes.py`.

1.  Reference: The Data Shape

* * * * *

When writing `rules.py`, expect the input dictionaries to represent a **merged view** of the Entity (combining the SQL columns and the JSON attributes).

**Input `Entity` Dictionary Example:**

JSON

```
{
    "id": "uuid-...",
    "name": "Goblin Grunt",

    // STRICT SQL COLUMNS (Combat Vitals)
    "hp_current": 25,
    "hp_max": 25,
    "ac": 14,
    "initiative": 12,
    "is_dead": false,

    // JSONB ATTRIBUTES (Deep Stats & Inventory)
    "attributes": {
        "stats": {
            "str": 16, "dex": 12, "con": 14,
            "int": 10, "wis": 10, "cha": 8
        },
        "skills": {
            "stealth": 4
        },
        "inventory": ["rusty_sword", "potion"]
    }
}

```

**Proceed with implementing `src/server/game_mechanics/` now.**