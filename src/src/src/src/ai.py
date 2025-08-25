from .models import Character, Move, calculate_damage

class SimpleAI:
    """A tiny rule-based AI.

    Priorities:
    1) If low HP (<35%) and heal is available+affordable, heal.
    2) Otherwise pick the ready, affordable attack that yields highest expected damage.
    3) If no good attack, defend if possible.
    4) Else pick any ready, affordable move.
    """

    def choose_move(self, me: Character, enemy: Character) -> Move:
        affordable_ready = [m for m in me.moves if m.ready() and m.mana_cost <= me.mana]
        if not affordable_ready:
            # fallback: choose any ready move (even if can't afford) or the first move
            ready = [m for m in me.moves if m.ready()]
            return ready[0] if ready else me.moves[0]

        # 1) try heal if low
        low_hp = me.hp / me.max_hp <= 0.35
        heals = [m for m in affordable_ready if m.kind == 'heal' and m.heal_amount > 0]
        if low_hp and heals:
            # prefer the biggest heal
            return sorted(heals, key=lambda m: m.heal_amount, reverse=True)[0]

        # 2) best expected damage
        attacks = [m for m in affordable_ready if m.kind == 'attack' and m.power > 0]
        if attacks:
            def expected_dmg(m: Move) -> float:
                dmg = calculate_damage(me, enemy, m)
                return m.accuracy * dmg
            attacks.sort(key=expected_dmg, reverse=True)
            return attacks[0]

        # 3) defend
        defends = [m for m in affordable_ready if m.kind == 'defend']
        if defends:
            # prefer the strongest defend
            return sorted(defends, key=lambda m: m.defend_amount, reverse=True)[0]

        # 4) anything else
        return affordable_ready[0]
