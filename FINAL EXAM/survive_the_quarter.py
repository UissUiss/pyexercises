# Name: SABRI Mohammed Ouissam
# Group: A
# Feature choice: Streak bonus — three consecutive reputation gains earn €500.
# Why I chose it: I wanted to reward players for making consistently good choices, adding an extra layer of strategy to the game.
#
# CSV input: scenarios_A.csv contains scenario rows and separate columns for
# each option's text, budget change, reputation change, and feedback.
# Game flow: load and shuffle scenarios; show one situation; validate a choice;
# apply its changes; update gauges and streak; stop if either gauge reaches 0.
# Output: show survival/failure, score, title, best/worst reputation move;
# append name, budget, reputation, title, and date to results.csv.
# Possible problems: missing CSV (show an error); invalid choice (ask again);
# malformed numeric values (skip that scenario); gauge <= 0 (end the game).

import csv
import random
from datetime import date
from pathlib import Path

SCENARIO_FILE = Path(__file__).with_name("scenarios_A.csv")
RESULTS_FILE = Path(__file__).with_name("results.csv")
STARTING_BUDGET = 10000
STARTING_REPUTATION = 50
MAX_REPUTATION = 100
DAYS_TO_PLAY = 10


def load_scenarios(filename):
    """Read the CSV and convert each option into the required tuple."""
    scenarios = []
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                options = []
                for letter in "ABC":
                    option = (
                        row[f"Option{letter}"],
                        int(row[f"Budget{letter}"]),
                        int(row[f"Reputation{letter}"]),
                        row[f"Feedback{letter}"],
                    )
                    options.append(option)
                scenarios.append({"id": row["ID"], "scenario": row["Scenario"], "options": options})
            except (KeyError, ValueError):
                print(f"Skipping malformed scenario row: {row.get('ID', '?')}")
    return scenarios

# Display the current game state
def show_scenario(day, scenario, budget, reputation):
    """Display the current gauges, situation, and three options."""
    print(f"\n--- Day {day} ---")
    print(f"[Budget: €{budget} | Reputation: {reputation}/{MAX_REPUTATION}]")
    print(scenario["scenario"])
    for letter, option in zip("ABC", scenario["options"]):
        print(f"  {letter}: {option[0]}")


def get_choice():
    """Keep asking until the player enters A, B, or C."""
    while True:
        choice = input("Your choice (A, B, or C): ").strip().upper()
        if choice in ("A", "B", "C"):
            return "ABC".index(choice)
        print("Please type A, B, or C.")


def apply_choice(budget, reputation, option):
    """Apply one option and return the updated gauges as a tuple."""
    text, budget_change, reputation_change, feedback = option
    budget += budget_change
    reputation = min(MAX_REPUTATION, reputation + reputation_change)
    print(feedback)
    print(f"Budget {budget_change:+} EUR, Reputation {reputation_change:+}")
    return budget, reputation


def save_result(name, budget, reputation, title):
    """Append this game's result as one CSV row."""
    file_exists = RESULTS_FILE.exists() and RESULTS_FILE.stat().st_size > 0
    with open(RESULTS_FILE, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["name", "budget", "reputation", "title", "date"])
        writer.writerow([name, budget, reputation, title, date.today().isoformat()])


def get_title(score):
    """Return the title matching the final score."""
    if score < 95:
        return "Eternal Intern"
    elif score < 120:
        return "Growth Hacker"
    elif score < 140:
        return "CMO Material"
    return "Viral Legend"

# Main game function
def play_game():
    """Run one complete ten-day game."""
    name = input("Player name: ").strip() or "Player"
    budget = STARTING_BUDGET
    reputation = STARTING_REPUTATION
    scenarios = load_scenarios(SCENARIO_FILE)
    if len(scenarios) < DAYS_TO_PLAY:
        print("The scenario file must contain at least 10 valid scenarios.")
        return
# Shuffle the scenarios so each game is different, and prepare to track history and streaks
    random.shuffle(scenarios)
    history = []  # One tuple per day: (day, choice text, reputation change)
    reputation_gain_streak = 0
# Loop through the first ten scenarios, showing each and applying the player's choice
    for day, scenario in enumerate(scenarios[:DAYS_TO_PLAY], start=1):
        show_scenario(day, scenario, budget, reputation)
        option = scenario["options"][get_choice()]
        text, budget_change, reputation_change, feedback = option
        budget, reputation = apply_choice(budget, reputation, option)
        history.append((day, text, reputation_change))
# Check for streak bonus: three consecutive reputation gains earn €500
        if reputation_change > 0:
            reputation_gain_streak += 1
        else:
            reputation_gain_streak = 0
        if reputation_gain_streak == 3:
            budget += 500
            print("Streak bonus! Three reputation gains in a row: +€500.")
            reputation_gain_streak = 0

        if budget <= 0 or reputation <= 0:
            print("\nGAME OVER — you are fired!")
            if budget <= 0 and reputation <= 0:
                print("Both budget and reputation reached zero or less.")
            elif budget <= 0:
                print("Your budget reached zero or less.")
            else:
                print("Your reputation reached zero or less.")
            save_result(name, budget, reputation, "Fired")
            return

    score = reputation + budget // 200
    title = get_title(score)
    best_move = max(history, key=lambda move: move[2])
    worst_move = min(history, key=lambda move: move[2])
# End: show the result, then leave a trace in results.csv
    print("\n==============================")
    print("Quarter survived!")
    print(f"Budget left: €{budget}, reputation: {reputation}/{MAX_REPUTATION}")
    print(f"Final score: {score}")
    print(f"{name}, your title: {title}")
    print(f'Best move: day {best_move[0]}, "{best_move[1]}" ({best_move[2]:+})')
    print(f'Worst move: day {worst_move[0]}, "{worst_move[1]}" ({worst_move[2]:+})')
    save_result(name, budget, reputation, title)
    print("Saved in results.csv")


def main():
    """Start the game and handle a missing scenario file gracefully."""
    try:
        play_game()
    except FileNotFoundError:
        print(f"Could not find {SCENARIO_FILE.name}. Put it beside this Python file.")


if __name__ == "__main__":
    main()
