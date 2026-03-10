class AttackMemory:
    """
    Stores previous attack / defense interaction state.
    Used to apply pressure history between rounds.
    """

    def __init__(self):
        self.previous_attack = None
        self.previous_defense = None
        self.previous_pressure = 0

    def update(self, attack: str, defense: str, pressure: int):
        """
        Update memory with latest round results.
        """
        self.previous_attack = attack
        self.previous_defense = defense
        self.previous_pressure = pressure

    def reset(self):
        """
        Clear memory state.
        """
        self.previous_attack = None
        self.previous_defense = None
        self.previous_pressure = 0