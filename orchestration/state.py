from typing import TypedDict, Dict, Any, List

class DealState(TypedDict):
    deal_id: str

    raw_data: Dict[str, Any]
    signals: Dict[str, Any]

    risk: Dict[str, Any]
    strategy: Dict[str, Any]
    actions: Dict[str, Any]

    feedback: Dict[str, Any]

    logs: List[str]