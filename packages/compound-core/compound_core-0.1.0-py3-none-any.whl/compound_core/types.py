from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class DelegationRequest:
    """A request from an agent to delegate work to sub-agents."""
    target_agent: str
    task: str
    context: Optional[str] = None
    priority: str = "normal"  # 'high', 'normal', 'low'

@dataclass
class AgentPersona:
    """Agent configuration loaded from markdown."""
    name: str
    description: str
    model: str
    system_prompt: str
    output_format: str = "text"
    temperature: float = 0.1
    max_tokens: int = 2000
    # Phase 10: Delegation Capabilities
    can_delegate: bool = False
    delegation_strategy: str = "flat"  # "flat" or "recursive"
    # Phase 11: Context-Aware Fallback
    fallback_strategy: str = "balanced" # "balanced", "code", "reasoning", "speed"

@dataclass
class AgentResult:
    """Result from an agent execution."""
    agent_name: str
    model: str
    response: str
    instance_id: Optional[str] = None  # NEW: For disambiguating duplicate agents
    severity: Optional[str] = None
    structured_data: Optional[dict] = None
    execution_time: float = 0.0
    cached: bool = False
    error: Optional[str] = None
    # Phase 10: Delegation artifacts
    delegation_requests: List['DelegationRequest'] = field(default_factory=list)
    sub_results: List['AgentResult'] = field(default_factory=list)
    validation_status: str = "unchecked"  # 'valid', 'hallucinated', 'unchecked'
    # Phase 2: Token Usage Tracking (P2 Recommendation)
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    # Phase 5: Tiered Trust
    trust_decision: Optional[Any] = None # Stores TrustDecision object
    validation_warnings: List[str] = field(default_factory=list)

@dataclass
class DelegationResult:
    """The outcome of a delegation operation."""
    requesting_agent: str
    sub_results: List['AgentResult']
    synthesis: str  # The parent agent's summary of the sub-results
    validation_status: str = "unchecked" # 'verified', 'hallucinated', 'uncertain'
    validation_notes: str = ""
    depth: int = 0
