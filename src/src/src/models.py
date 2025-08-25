from dataclasses import dataclass, field
from typing import List
import random

@dataclass
class Move:
    name: str
    kind: str  # 'attack' | 'defend' | 'heal' | 'special'
    power: int = 0                # for attack
    heal_amount: int = 0          # for heal
    defend_amount: int = 0        # flat defense buff applied this turn
    mana_cost: int = 0
    accuracy: float = 1.0         # 0.0 - 1.0
    cooldown: int = 0             # turns between uses
    _cooldown_remaining: int = 0  # internal tracker, not user-set

    def ready(self) -> bool:
        return self._cooldown_remaining <= 0

    def tick(self):
        if self._cooldown_remaining > 0:
            self._cooldown_remaining -= 1

    def use(self):
        self._cooldown_remaining = self.cooldown

@dataclass
class Character:
    name: str
    max_hp: int
    attack: int
    defense: int
    max_mana: int
    moves: List[Move] = field(default_factory=list)

    hp: int = field(init=False)
    mana: int = field(init=False)
    defend_buff_active: int = field(default=0, init=False)  # defense buff for this turn

    def __post_init__(self):
        self.hp = self.max_hp
        self.mana = self.max_mana

    def is_alive(self) -> bool:
        return self.hp > 0

    def start_turn(self):
        # reduce any lingering defend buff (only lasts 1 opponent turn)
        self.defend_buff_active = 0
        # tick move cooldowns
        for m in self.moves:
            m.tick()

    def spend_mana(self, amount: int) -> bool:
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def receive_damage(self, dmg: int):
        self.hp = max(0, self.hp - dmg)

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

    def effective_defense(self) -> int:
        return self.defense + self.defend_buff_active

def calculate_damage(attacker: Character, defender: Character, move: Move) -> int:
    # simple damage model: base = power + attacker.attack - defender.defense
    base = move.power + attacker.attack - defender.effective_defense()
    return max(1, base)
