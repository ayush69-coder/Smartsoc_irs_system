"""
Domain graph endpoint
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/graph/query")
async def query_graph(domain: str):
    """Query domain graph"""
    # TODO: Implement graph query logic
    return {"domain": domain, "neighbors": [], "cluster_score": 0.0}