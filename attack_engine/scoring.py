from typing import List, Union, Dict, Optional
from dataclasses import dataclass


@dataclass
class EscalationAnalysis:
    """Complete escalation analysis results."""
    is_escalating: bool
    consecutive_increases: int
    total_delta: float
    avg_delta: float
    max_single_jump: float
    severity: str
    confidence: float


def detect_escalation(
    pressure_history: List[Union[int, float]],
    detailed: bool = False,
    tolerance: float = 0.0
) -> Union[bool, EscalationAnalysis]:
    """
    Robust escalation detection with optional detailed analysis.
    
    Args:
        pressure_history: Chronological pressure values
        detailed: Return full analysis instead of bool
        tolerance: Ignore decreases within this threshold
    
    Returns:
        bool or EscalationAnalysis
    """
    
    n = len(pressure_history)
    
    if n < 2:
        if detailed:
            return EscalationAnalysis(
                is_escalating=False,
                consecutive_increases=0,
                total_delta=0.0,
                avg_delta=0.0,
                max_single_jump=0.0,
                severity="none",
                confidence=0.0
            )
        return False
    
    # Analyze pressure changes
    consecutive_increases = 0
    max_consecutive = 0
    total_delta = 0.0
    max_jump = 0.0
    violations = 0
    
    for i in range(n - 1):
        delta = pressure_history[i + 1] - pressure_history[i]
        
        if delta >= -tolerance:
            consecutive_increases += 1
            total_delta += max(delta, 0)
            max_jump = max(max_jump, delta)
        else:
            max_consecutive = max(max_consecutive, consecutive_increases)
            consecutive_increases = 0
            violations += 1
    
    max_consecutive = max(max_consecutive, consecutive_increases)
    
    # Determine if escalating
    is_escalating = violations == 0
    
    if not detailed:
        return is_escalating
    
    # Detailed analysis
    avg_delta = total_delta / (n - 1) if n > 1 else 0.0
    
    # Classify severity
    if not is_escalating:
        severity = "none"
        confidence = 0.0
    elif avg_delta < 1:
        severity = "mild"
        confidence = max_consecutive / (n - 1)
    elif avg_delta < 3:
        severity = "moderate"
        confidence = max_consecutive / (n - 1)
    else:
        severity = "severe"
        confidence = max_consecutive / (n - 1)
    
    return EscalationAnalysis(
        is_escalating=is_escalating,
        consecutive_increases=max_consecutive,
        total_delta=total_delta,
        avg_delta=avg_delta,
        max_single_jump=max_jump,
        severity=severity,
        confidence=min(confidence, 1.0)
    )


# Usage examples
if __name__ == "__main__":
    
    # Basic usage
    history1 = [2, 3, 5, 7, 9]
    print(detect_escalation(history1))  # True
    
    history2 = [2, 5, 4, 7, 9]
    print(detect_escalation(history2))  # False
    
    # With tolerance
    history3 = [5, 5.5, 5.4, 6, 7]
    print(detect_escalation(history3, tolerance=0.2))  # True (allows small dip)
    
    # Detailed analysis
    analysis = detect_escalation(history1, detailed=True)
    print(analysis)
    # EscalationAnalysis(is_escalating=True, consecutive_increases=4, 
    #                    total_delta=7.0, avg_delta=1.75, ...)
