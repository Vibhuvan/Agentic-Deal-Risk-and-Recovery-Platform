from orchestration.graph import graph

initial_state = {
    "deal_id": "D001",
    "raw_data": {},
    "signals": {},
    "risk": {},
    "strategy": {},
    "actions": {},
    "feedback": {},
    "logs": []
}

result = graph.invoke(initial_state)

print("\nFINAL OUTPUT:\n")
print(result)