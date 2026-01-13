from typing import Protocol, runtime_checkable, List, Optional, Dict, Any
from .types import AgentPersona, AgentResult

@runtime_checkable
class PersonaProvider(Protocol):
    """Interface for loading agent personas."""
    
    def load_persona(self, name: str) -> AgentPersona:
        """
        Load a persona by name.
        
        Args:
            name: The name of the agent persona.
            
        Returns:
            AgentPersona object.
            
        Raises:
            KeyError: If the persona is not found.
        """
        ...
    
    def list_personas(self) -> List[str]:
        """
        List all available persona names.
        
        Returns:
            List of persona names.
        """
        ...

@runtime_checkable
class AgentExecutor(Protocol):
    """Interface for executing agents."""
    
    async def execute(self, persona: AgentPersona, prompt: str, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        """
        Execute an agent with a prompt.
        
        Args:
            persona: The agent persona to execute.
            prompt: The user input or task description.
            context: Optional context dictionary.
            
        Returns:
            AgentResult object containing the response.
        """
        ...

@runtime_checkable
class MemoryBackend(Protocol):
    """Interface for memory storage backend."""
    
    async def store(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Store a value in memory.
        
        Args:
            key: Storage key.
            value: Data to store (must be serializable).
            ttl: Time to live in seconds (optional).
        """
        ...
    
    async def retrieve(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from memory.
        
        Args:
            key: Storage key.
            
        Returns:
            The stored value or None if not found/expired.
        """
        ...
    
    async def delete(self, key: str) -> bool:
        """
        Delete a value from memory.
        
        Args:
            key: Storage key.
            
        Returns:
            True if deleted, False if not found.
        """
        ...
