from typing import Literal
from langgraph.graph import StateGraph, END
from src.server.ai_engine.state import AgentState
from src.server.ai_engine.nodes import router_node, mechanics_node, narrator_node

def route_decision(state: AgentState) -> Literal["mechanics", "narrator"]:
    """
    Conditional Edge Logic.
    Determines which node to visit after the Router.
    """
    if state["intent"] == "MECHANICS":
        return "mechanics"
    return "narrator"

# 1. Initialize the Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("router", router_node)
workflow.add_node("mechanics", mechanics_node)
workflow.add_node("narrator", narrator_node)

# 3. Define Edges
# Entry point is always the Router
workflow.set_entry_point("router")

# Router decides where to go next
workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "mechanics": "mechanics",
        "narrator": "narrator"
    }
)

# Mechanics always feed into the Narrator (to describe the outcome)
workflow.add_edge("mechanics", "narrator")

# Narrator is the end of the turn
workflow.add_edge("narrator", END)

# 4. Compile
app = workflow.compile()