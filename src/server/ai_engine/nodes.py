from langchain_core.messages import SystemMessage, HumanMessage
from src.server.ai_engine.state import AgentState

"""
Node Implementations (Stubs).
These functions represent the "work" done at each step of the graph.
"""

async def router_node(state: AgentState) -> AgentState:
    """
    Step 1: Analyze user input.
    Decides if we need strict game mechanics or just storytelling.
    """
    # TODO: Implement LLM classification here.
    # Mock Logic:
    last_msg = state["messages"][-1].content.lower()
    
    intent = "NARRATIVE"
    if "attack" in last_msg or "cast" in last_msg:
        intent = "MECHANICS"
        
    return {
        "intent": intent,
        "reasoning_log": [f"Router classified input as {intent}"]
    }

async def mechanics_node(state: AgentState) -> AgentState:
    """
    Step 2 (Conditional): Execute Rules.
    Parses the action, rolls dice, checks AC, updates HP (via tools).
    """
    # TODO: Call src.server.game_mechanics
    result = "Attack Roll: 15 (Hit). Damage: 6 slashing."
    return {
        "mechanics_results": [result],
        "reasoning_log": ["Executed mechanics successfully."]
    }

async def narrator_node(state: AgentState) -> AgentState:
    """
    Step 3: Generate Response.
    Synthesizes the conversation history + mechanics results into flavor text.
    """
    # TODO: Implement LLM generation.
    mech_context = "\n".join(state.get("mechanics_results", []))
    
    response = "The goblin shrieks as your sword connects!" 
    if not mech_context:
        response = "You look around the room. It is quiet."
        
    return {
        "messages": [SystemMessage(content=response)],
        "final_response": response
    }