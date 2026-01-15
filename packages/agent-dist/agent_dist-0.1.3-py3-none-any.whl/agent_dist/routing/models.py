from pydantic import BaseModel, Field
from typing import List, Dict, Literal, Optional, Any
from time import time
from agent_dist.registry.models import AgentRecord


class Capabilities(BaseModel):
    tasks: List[str]
    input_types: List[str]

    requires: List[str] = Field(default_factory=list)
    provides: List[str] = Field(default_factory=list)

    compliance: List[str] = Field(default_factory=list)
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None


class MultiRouteDecision(BaseModel):
    mode: Literal["llm_only", "agents", "react"]
    routes: Dict[str, Dict[str, List[AgentRecord]]] = Field(default_factory=dict)


class ExecutionStep(BaseModel):
    agent_name: str
    intent_group: str
    capability_cluster: str


class ExecutionPlan(BaseModel):
    mode: Literal["parallel", "chain", "llm_only", "react"]
    steps: List[ExecutionStep] = Field(default_factory=list)
