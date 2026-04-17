"""
FILE: agents/deps.py
TERM: Dependencies (deps)
ROLE: The Environment / Context
DESCRIPTION: Data injected into agents to give them access to the 'real world' (DBs, IDs).
"""

# -- https://medium.com/@laurentkubaski/python-data-classes-f98f8368f5c2
# -- https://medium.com/@laurentkubaski/pydantic-vs-data-classes-eaa36e01cd77


from dataclasses import dataclass

@dataclass
class AgentDeps:
    """
    TERM: Dependency Injection
    This object is passed into every 'Run' and is accessible by all 'Tools'.
    It acts as a security sandbox for multi-tenancy.
    """
    trainer_id: int
    client_id: int