from agent_core.local_llm import ask_llm
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import re


@dataclass
class AgentConfig:
    """Configuration for agent behavior."""
    temperature: float = 0.7
    max_tokens: int = 150
    max_retries: int = 2
    validate_responses: bool = True
    strip_whitespace: bool = True


class Agent:
    """
    Optimized AI agent with role-based prompting and robust error handling.
    
    Features:
    - Clean prompt construction
    - Response validation
    - Error handling with retries
    - Memory efficient with __slots__
    - Performance tracking
    """
    
    __slots__ = ('role', 'config', '_call_count', '_error_count')
    
    def __init__(
        self,
        role: str,
        config: Optional[AgentConfig] = None
    ):
        """
        Initialize agent with role and optional configuration.
        
        Args:
            role: The agent's role/persona (e.g., "Security Analyst")
            config: Optional configuration object
        """
        if not role or not role.strip():
            raise ValueError("Role cannot be empty")
        
        self.role = role.strip()
        self.config = config or AgentConfig()
        self._call_count = 0
        self._error_count = 0
    
    def act(
        self,
        prompt: str,
        context: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Execute agent action with given prompt.
        
        Args:
            prompt: The task or question for the agent
            context: Optional additional context
            temperature: Optional temperature override
        
        Returns:
            Agent's response string
        
        Example:
            >>> agent = Agent("Security Expert")
            >>> response = agent.act("List top 3 vulnerabilities")
        """
        self._call_count += 1
        
        if not prompt or not prompt.strip():
            return "[Error: Empty prompt provided]"
        
        # Build optimized prompt
        full_prompt = self._build_prompt(prompt.strip(), context)
        
        # Execute with retry logic
        temp = temperature if temperature is not None else self.config.temperature
        
        for attempt in range(self.config.max_retries + 1):
            try:
                response = ask_llm(
                    full_prompt,
                    temperature=temp,
                    max_tokens=self.config.max_tokens
                )
                
                # Validate and clean response
                if self.config.validate_responses:
                    if not self._is_valid_response(response):
                        if attempt < self.config.max_retries:
                            continue
                        return "[Error: Invalid response generated]"
                
                return self._clean_response(response)
                
            except Exception as e:
                self._error_count += 1
                
                if attempt == self.config.max_retries:
                    return f"[Error: {str(e)}]"
        
        return "[Error: Max retries exceeded]"
    
    def _build_prompt(self, prompt: str, context: Optional[str] = None) -> str:
        """Construct clean, effective prompt."""
        
        parts = [
            f"You are acting as: {self.role}",
            ""
        ]
        
        if context:
            parts.extend([
                f"Context: {context.strip()}",
                ""
            ])
        
        parts.extend([
            prompt,
            "",
            "Respond clearly and concisely."
        ])
        
        return "\n".join(parts)
    
    def _is_valid_response(self, response: str) -> bool:
        """Validate response quality."""
        
        if not response or not response.strip():
            return False
        
        # Check minimum length
        words = response.split()
        if len(words) < 3:
            return False
        
        # Check for common failure patterns
        failure_patterns = [
            r"^I (cannot|can't|am unable to|won't)",
            r"^(Sorry|I apologize)",
            r"^\[Error",
        ]
        
        response_lower = response.strip().lower()
        for pattern in failure_patterns:
            if re.match(pattern, response_lower):
                return False
        
        return True
    
    def _clean_response(self, response: str) -> str:
        """Clean and format response."""
        
        if not self.config.strip_whitespace:
            return response
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\n\s*\n', '\n\n', response)
        cleaned = cleaned.strip()
        
        return cleaned
    
    @property
    def stats(self) -> Dict[str, Any]:
        """Get agent performance statistics."""
        return {
            'role': self.role,
            'total_calls': self._call_count,
            'errors': self._error_count,
            'success_rate': (
                f"{((self._call_count - self._error_count) / self._call_count * 100):.1f}%"
                if self._call_count > 0 else "N/A"
            )
        }
    
    def reset_stats(self) -> None:
        """Reset performance statistics."""
        self._call_count = 0
        self._error_count = 0
    
    def __repr__(self) -> str:
        return f"Agent(role='{self.role}', calls={self._call_count})"
    
    def __str__(self) -> str:
        return f"{self.role} (Agent)"


# ================================================
# CONVENIENCE FACTORY FUNCTIONS
# ================================================

def create_agent(role: str, **kwargs) -> Agent:
    """
    Factory function for creating agents with custom config.
    
    Args:
        role: Agent role
        **kwargs: Configuration parameters
    
    Returns:
        Configured Agent instance
    
    Example:
        >>> agent = create_agent("Analyst", temperature=0.8, max_tokens=200)
    """
    config = AgentConfig(**kwargs)
    return Agent(role, config)


def create_concise_agent(role: str) -> Agent:
    """Create agent optimized for brief responses."""
    config = AgentConfig(
        temperature=0.5,
        max_tokens=100
    )
    return Agent(role, config)


def create_creative_agent(role: str) -> Agent:
    """Create agent optimized for creative responses."""
    config = AgentConfig(
        temperature=0.9,
        max_tokens=300
    )
    return Agent(role, config)


def create_precise_agent(role: str) -> Agent:
    """Create agent optimized for precise, factual responses."""
    config = AgentConfig(
        temperature=0.3,
        max_tokens=200
    )
    return Agent(role, config)


# ================================================
# USAGE EXAMPLES
# ================================================

if __name__ == "__main__":
    
    # Basic usage (original functionality)
    agent = Agent("Security Analyst")
    response = agent.act("List top 3 network vulnerabilities")
    print(response)
    print(agent.stats)
    
    # With context
    response = agent.act(
        "Recommend mitigations",
        context="Previous scan found SQL injection vulnerabilities"
    )
    print(response)
    
    # Custom configuration
    custom_agent = create_agent(
        "Strategic Advisor",
        temperature=0.8,
        max_tokens=250,
        max_retries=3
    )
    response = custom_agent.act("Analyze competitive landscape")
    
    # Specialized agents
    concise = create_concise_agent("Quick Responder")
    creative = create_creative_agent("Brainstormer")
    precise = create_precise_agent("Fact Checker")
    
    # Multiple interactions
    analyst = Agent("Threat Analyst")
    for question in [
        "What are current threats?",
        "How to detect them?",
        "Best prevention methods?"
    ]:
        print(f"\nQ: {question}")
        print(f"A: {analyst.act(question)}")
    
    print(f"\nStats: {analyst.stats}")
    
    # Temperature override
    response = agent.act(
        "Generate creative security slogans",
        temperature=0.9
    )
