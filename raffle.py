import json
import os
import random
from typing import Dict

RAFFLE_FILE = "raffle_data.json"


def load_data() -> Dict[str, int]:
    """Load participant data from the JSON file."""
    if os.path.exists(RAFFLE_FILE):
        try:
            with open(RAFFLE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return {str(k): int(v) for k, v in data.items()}
        except Exception:
            pass
    return {}


def save_data(participants: Dict[str, int]) -> None:
    """Persist participant data to the JSON file."""
    with open(RAFFLE_FILE, "w", encoding="utf-8") as file:
        json.dump(participants, file, indent=2)


def add_entrant(participants: Dict[str, int]) -> None:
    """Prompt the user to add a new entrant or update ticket count."""
    name = input("Enter participant name: ").strip()
    if not name:
        print("Name cannot be blank.")
        return
    ticket_str = input("Enter number of tickets: ").strip()
    if not ticket_str.isdigit() or int(ticket_str) <= 0:
        print("Ticket count must be a positive integer.")
        return
    tickets = int(ticket_str)
    participants[name] = participants.get(name, 0) + tickets
    save_data(participants)
    print(f"Added {tickets} ticket(s) for {name}.")


def list_entrants(participants: Dict[str, int]) -> None:
    """Display a table of all entrants sorted by name."""
    if not participants:
        print("No entrants found.")
        return
    print(f"{'Name':<20} {'Tickets':>7}")
    print("-" * 28)
    for name in sorted(participants):
        print(f"{name:<20} {participants[name]:>7}")


def run_raffle_once(participants: Dict[str, int]) -> str:
    """Return a random winner based on ticket weights."""
    rng = random.SystemRandom()
    names = list(participants.keys())
    weights = list(participants.values())
    return rng.choices(names, weights=weights, k=1)[0]


def draw_winner(participants: Dict[str, int]) -> None:
    """Select and announce the raffle winner."""
    if not participants:
        print("No entrants to draw from.")
        return
    total_tickets = sum(participants.values())
    winner = run_raffle_once(participants)
    probability = participants[winner] / total_tickets
    print(f"Winner: {winner} (probability {probability:.2%})")
    while True:
        choice = input(
            "Keep entrants for another round? (y/n): "
        ).strip().lower()
        if choice in {"y", "n"}:
            break
        print("Please enter 'y' or 'n'.")
    if choice == "n":
        reset_raffle(participants)
    else:
        save_data(participants)


def reset_raffle(participants: Dict[str, int]) -> None:
    """Clear all entrants from the raffle."""
    participants.clear()
    save_data(participants)
    print("Raffle has been reset.")


def show_menu() -> str:
    """Display the main menu and return the user's choice."""
    print("\nRaffle Menu")
    print("1) Add entrant")
    print("2) List entrants")
    print("3) Draw winner")
    print("4) Reset raffle")
    print("5) Quit")
    return input("Choose an option: ").strip()


def main() -> None:
    """Run the raffle application loop."""
    participants = load_data()
    while True:
        choice = show_menu()
        if choice == "1":
            add_entrant(participants)
        elif choice == "2":
            list_entrants(participants)
        elif choice == "3":
            draw_winner(participants)
        elif choice == "4":
            reset_raffle(participants)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()
