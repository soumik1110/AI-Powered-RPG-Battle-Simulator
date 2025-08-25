from .models import Character, Move, calculate_damage

def apply_move(user: Character, target: Character, move: Move) -> str:
    if move.mana_cost > 0 and user.mana < move.mana_cost:
        return f"{user.name} tried {move.name} but lacked mana!"

    # spend mana & set cooldown
    if move.mana_cost > 0:
        user.mana -= move.mana_cost
    move.use()

    # accuracy
    import random as _r
    if _r.random() > move.accuracy:
        return f"{user.name}'s {move.name} missed!"

    if move.kind == 'attack':
        dmg = calculate_damage(user, target, move)
        target.receive_damage(dmg)
        end = f" {target.name} has been defeated!" if target.hp == 0 else ""
        return f"{user.name} used {move.name} and dealt {dmg} damage." + end
    elif move.kind == 'defend':
        user.defend_buff_active = move.defend_amount
        return f"{user.name} used {move.name} and raised defense by {move.defend_amount} for this turn."
    elif move.kind == 'heal':
        before = user.hp
        user.heal(move.heal_amount)
        healed = user.hp - before
        return f"{user.name} used {move.name} and healed {healed} HP."
    else:
        return f"{user.name} used {move.name}. (No special effect implemented)"

def take_turn(attacker: Character, defender: Character, move: Move) -> str:
    # start_turn resets defend buff and ticks cooldowns
    attacker.start_turn()
    return apply_move(attacker, defender, move)
