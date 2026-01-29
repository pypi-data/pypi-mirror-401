import uuid
from agenthink.models import ConnectionRequest

def build_d365_read_call(
    data: ConnectionRequest,
    primary_key: str = "Entry_No",
    filter_query: str | None = None
) -> dict:
    """
    Builds a d365_execute tool-call response from ConnectionRequest
    """

    if not data.d365request or not isinstance(data.d365request, list):
        raise ValueError("d365request must be a non-empty list")

    target_url = data.d365request[0].get("url")
    if not target_url:
        raise ValueError("Missing url in d365request")

    return {
        "status": "tool_calls_pending",
        "session_id": data.session_id,
        "tools_used": ["d365_execute"],
        "tool_call_plan": [
            {
                "tool_call_id": f"call_{uuid.uuid4().hex}",
                "params": {
                    "name": "d365_execute",
                    "arguments": {
                        "operation": "read",
                        "target_url": target_url,
                        "primary_key": primary_key,
                        "filter_query": filter_query,
                    }
                }
            }
        ]
    }
