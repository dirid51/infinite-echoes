IMPLEMENTATION BLUEPRINT: Project "Infinite Echoes"
===================================================

System Objective:

Build a text-based, single-player RPG using a Client-Server architecture where a Python TUI (Textual) interacts with a FastAPI backend. The backend orchestrates a "Lazy Simulation" world using D&D 5e mechanics, Hybrid ECS data modeling, and a "Dream Protocol" for vector-based state persistence.

1\. Tech Stack Constraints
--------------------------

-   **Language:** Python 3.11+ (Unified Client/Server).

-   **Client Framework:** `textual` (TUI), `httpx` (Async API Client).

-   **Server Framework:** `fastapi`, `uvicorn`.

-   **Database:** PostgreSQL 16+ (Dockerized) with `pgvector` extension.

-   **ORM:** `sqlalchemy` (Async) with `alembic` for migrations.

-   **AI/LLM:** `langchain` (Orchestration), `pydantic` (Structured Output/Validation), `gemini` (or compatible API).

-   **Testing:** `pytest`, `pytest-asyncio` (Mechanics), `llm-evals` (Narrative).

-   **Environment:** Docker Compose (for DB/Backend orchestration).

2\. Directory Structure
-----------------------

```
infinite_echoes/
├── docker-compose.yml          # Orchestrates Postgres + Backend
├── pyproject.toml              # Unified dependencies
├── README.md                   # Setup instructions
├── src/
│   ├── client/                 # Textual TUI Application
│   │   ├── app.py              # Entry point
│   │   ├── screens/            # (Login, GameLoop, DebugConsole)
│   │   ├── widgets/            # (TerminalOutput, StatBlock, InputBar)
│   │   └── api_client.py       # HTTPX wrapper
│   ├── server/                 # FastAPI Backend
│   │   ├── main.py
│   │   ├── core/               # Configuration & Security
│   │   ├── db/                 # Database Connection
│   │   │   ├── models.py       # SQL Tables (Strict Stats)
│   │   │   └── vector_store.py # PGVector wrapper (Narrative)
│   │   ├── game_mechanics/     # D&D 5e Logic (Deterministic)
│   │   │   ├── dice.py
│   │   │   └── rules.py        # Resolvers (AC vs Hit, Saves)
│   │   ├── ai_engine/          # The "Reasoning Router"
│   │   │   ├── tools.py        # Functions exposed to LLM
│   │   │   ├── prompts.py      # System prompts
│   │   │   └── router.py       # Hybrid Agent logic
│   │   └── api/                # REST Endpoints
│   └── shared/                 # Shared Pydantic Schemas
│       ├── commands.py         # User Input schemas
│       └── events.py           # Game State update schemas
└── tests/
    ├── unit/                   # Mechanics (Option A)
    ├── integration/            # API & DB State (Option B)
    └── e2e_evals/              # LLM-as-Judge (Option C)

```

3\. Core Data Interfaces
------------------------

### A. The Hybrid Entity (ECS)

*Strict SQL columns for math; JSON for narrative.*

```
class Entity(Base):
    __tablename__ = "entities"
    id = Column(UUID, primary_key=True)
    zone_id = Column(UUID, ForeignKey("zones.id"))

    # Strict Mechanics (SQL) - Deterministic Data
    name = Column(String)
    hp_current = Column(Integer)
    hp_max = Column(Integer)
    ac = Column(Integer)
    initiative = Column(Integer)
    is_dead = Column(Boolean, default=False)

    # Flavor/Narrative (JSON) - "Infinite" Attributes
    attributes = Column(JSON) # e.g. {"scent": "sulfur", "fear": "fire"}

```

### B. The "Dream" Memory (Vector)

*Stores the narrative summary when a player leaves a zone.*

```
class ZoneMemory(Base):
    __tablename__ = "zone_memories"
    id = Column(UUID, primary_key=True)
    zone_id = Column(UUID)
    summary_text = Column(Text) # "Player killed the goblin king..."
    embedding = Column(Vector(1536)) # For RAG retrieval
    timestamp = Column(DateTime)

```

### C. The Reasoning Output (Structured JSON)

*The exact shape the LLM must return to the Backend.*

```
class DMResponse(BaseModel):
    narrative_description: str
    mechanics_triggered: Optional[List[MechanicAction]]
    state_updates: Optional[List[EntityUpdate]]
    hidden_thought_process: str # For Debug Console visibility

```

4\. Step-by-Step Generation Order
---------------------------------

*Crucial: Follow this order to prevent reference errors.*

1.  **Infrastructure Layer:**

    -   Create `docker-compose.yml` with PostgreSQL + PGVector.

    -   Setup `src/server/db` with SQLAlchemy async engine.

2.  **Domain Logic (The Mechanics):**

    -   Implement `src/server/game_mechanics/`.

    -   **Task:** Build dice rollers and resolution logic (Attack Roll vs AC) *without* AI.

    -   *Test:* Write Unit Tests (Option A) to prove math is correct.

3.  **The Reasoning Router (AI Layer):**

    -   Implement `src/server/ai_engine/`.

    -   Create Pydantic models for `DMResponse`.

    -   Implement the "Tool" functions that call the code from Step 2.

4.  **Backend API & State Management:**

    -   Implement `FastAPI` endpoints (`POST /action`, `GET /state`).

    -   Implement the **Dream Protocol**: Logic to serialize entities to Vector DB upon exiting a zone.

5.  **Client Application (TUI):**

    -   Implement `src/client/`.

    -   Build the `TerminalOutput` widget (rendering Markdown/Text).

    -   Build the `DebugConsole` (hidden overlay to trigger API overrides).

6.  **Testing & Validation:**

    -   Implement `tests/integration` (Golden Master Replays).

    -   Implement `tests/e2e_evals` (LLM-as-Judge scripts).