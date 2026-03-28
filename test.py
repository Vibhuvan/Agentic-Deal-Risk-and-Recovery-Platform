# agent_openai.py

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI


# ---------------------------
# 1. Define State
# ---------------------------
class AgentState(TypedDict):
    input: str
    output: str


# ---------------------------
# 2. Initialize OpenAI Model
# ---------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ---------------------------
# 3. Define LLM Node
# ---------------------------
def llm_node(state: AgentState) -> AgentState:
    user_input = state["input"]

    prompt = f"""
You are a helpful, precise AI assistant.

User: {user_input}
"""

    response = llm.invoke(prompt)

    return {
        "input": user_input,
        "output": response.content
    }


# ---------------------------
# 4. Build LangGraph Agent
# ---------------------------
builder = StateGraph(AgentState)

builder.add_node("llm_node", llm_node)

builder.set_entry_point("llm_node")
builder.add_edge("llm_node", END)

graph = builder.compile()


# ---------------------------
# 5. Run Agent (CLI loop)
# ---------------------------
def run_agent():
    print("🤖 OpenAI LangGraph Agent (type 'exit' to quit)\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            if not user_input:
                continue

            result = graph.invoke({
                "input": user_input,
                "output": ""
            })

            print("\nAgent:", result["output"], "\n")

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting...")
            break

        except Exception as e:
            print("Error:", str(e))


# ---------------------------
# 6. Entry Point
# ---------------------------
if __name__ == "__main__":
    run_agent()