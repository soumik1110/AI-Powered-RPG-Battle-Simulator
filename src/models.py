import random
from src.models import Character, Move
from src.battle import take_turn
from src.ai import SimpleAI

def create_default_characters():
    player_moves = [
        Move(name="Slash", kind="attack", power=8, mana_cost=0, accuracy=0.95),
        Move(name="Guard", kind="defend", defend_amount=6, mana_cost=0, cooldown=1),
        Move(name="First Aid", kind="heal", heal_amount=12, mana_cost=5, cooldown=2, accuracy=1.0),
        Move(name="Heavy Strike", kind="attack", power=14, mana_cost=4, accuracy=0.8, cooldown=1),
    ]
    enemy_moves = [
        Move(name="Claw", kind="attack", power=7, mana_cost=0, accuracy=0.95),
        Move(name="Roar Guard", kind="defend", defend_amount=5, mana_cost=0, cooldown=1),
        Move(name="Regenerate", kind="heal", heal_amount=10, mana_cost=5, cooldown=2, accuracy=1.0),
        Move(name="Bite", kind="attack", power=12, mana_cost=3, accuracy=0.85),
    ]
    player = Character(name="Hero", max_hp=60, attack=10, defense=5, max_mana=10, moves=player_moves)
    enemy = Character(name="Goblin", max_hp=55, attack=9, defense=4, max_mana=10, moves=enemy_moves)
    return player, enemy

def list_moves(entity: Character):
    for i, m in enumerate(entity.moves, 1):
        ready = "" if m.ready() else f" (cooldown {m._cooldown_remaining})"
        print(f"{i}. {m.name} [{m.kind}] - cost:{m.mana_cost}, acc:{int(m.accuracy*100)}%{ready}")

def get_player_move(entity: Character):
    while True:
        try:
            choice = int(input("Choose your move (number): "))
            if 1 <= choice <= len(entity.moves):
                m = entity.moves[choice-1]
                if not m.ready():
                    print("That move is on cooldown. Pick another.")
                    continue
                if m.mana_cost > entity.mana:
                    print("Not enough mana. Pick another.")
                    continue
                return m
        except ValueError:
            pass
        print("Invalid choice. Try again.")

def main():
    random.seed()  # different each run
    player, enemy = create_default_characters()
    ai = SimpleAI()

    print("=== AI-powered RPG Battle Simulator ===\n")
    print(f"You are {player.name} (HP {player.hp}/{player.max_hp}, Mana {player.mana}/{player.max_mana})")
    print(f"Enemy: {enemy.name} (HP {enemy.hp}/{enemy.max_hp}, Mana {enemy.mana}/{enemy.max_mana})\n")

    turn = 1
    while player.is_alive() and enemy.is_alive():
        print(f"\n-- Turn {turn} --")
        turn += 1

        # Player turn
        print(f"\nYour HP: {player.hp}/{player.max_hp} | Mana: {player.mana}/{player.max_mana}")
        print(f"Enemy HP: {enemy.hp}/{enemy.max_hp} | Mana: {enemy.mana}/{enemy.max_mana}")
        print("\nYour moves:")
        list_moves(player)
        pmove = get_player_move(player)
        log = take_turn(player, enemy, pmove)
        print(log)
        if not enemy.is_alive():
            print(f"\nYou win! {enemy.name} is defeated.")
            break

        # Enemy turn
        emove = ai.choose_move(enemy, player)
        print(f"\nEnemy chooses: {emove.name}")
        log = take_turn(enemy, player, emove)
        print(log)
        if not player.is_alive():
            print(f"\nDefeat... {player.name} has fallen.")
            break

    print("\nThanks for playing!")

if __name__ == "__main__":
    main()
