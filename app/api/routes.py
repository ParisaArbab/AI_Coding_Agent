from fastapi import APIRouter, Depends, HTTPException
from app.agents.graph import CodingAgent
from app.core.dependencies import get_agent
from app.models.requests import AgentRequest
from app.models.responses import AgentResponse

router = APIRouter(prefix="/api/v1", tags=["agent"])

@router.post("/agent/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest, agent: CodingAgent = Depends(get_agent)) -> AgentResponse:
    try:
        return await agent.run(request)
    except (ValueError, FileNotFoundError, PermissionError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Agent execution failed.") from exc
