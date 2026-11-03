# =====================================================================
#  SURVIVE THE QUARTER - Croissant Rocket marketing game
#  Name:  SABRI Mohammed Ouissam
#  Group: X          <- write your group letter here
#  Python, M1 - DESMI 2026
# =====================================================================
#
# 1. WHAT GOES IN?   (in my own words)
#    - separator:
#    - columns and what each one holds:
#    - how the numbers are written:
#    - where I find the impact of option B:
#
# 2. WHAT HAPPENS?   (one day, one step per line)
#    -
#
# 3. WHAT COMES OUT?
#    - on screen:
#    - one line of results.csv looks like:
#
# 4. WHAT COULD GO WRONG?   (at least three, and what my program does)
#    -
#
# FEATURE CHOSEN: c - High score
#    Why: it uses the csv module again, this time to READ the file the game
#    writes, so results.csv becomes a leaderboard and every player gets a
#    budget record to beat. Only games that survived count as a record.
#
# WHAT IS MISSING: nothing (update this line if you cut something)
# =====================================================================

import csv
import glob
import io
import os
import random
import re
import unicodedata
from datetime import datetime

# ---------- Game settings, taken from "The rules in numbers" ----------
SCENARIO_FILE = "scenarios_X.csv"      # replace X with your group letter
RESULTS_FILE = "results.csv"
START_BUDGET = 10000
START_REPUTATION = 50
MAX_REPUTATION = 100
DAYS = 10
LETTERS = ("A", "B", "C")

# Titles from the best down: the first threshold the score reaches gives the title
TITLES = [(140, "Viral Legend"), (120, "CMO Material"), (95, "Growth Hacker")]
LOWEST_TITLE = "Eternal Intern"
FIRED_TITLE = "Fired"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Words that tell what a column holds (English and French headers)
COLUMN_WORDS = {
    "id":         {"id", "num", "number", "no", "nr", "numero", "day", "jour"},
    "budget":     {"budget", "eur", "euro", "euros", "money", "cash", "cost", "spend", "argent"},
    "reputation": {"rep", "reputation", "reput", "image", "fame"},
    "feedback":   {"feedback", "result", "outcome", "consequence", "reaction", "response",
                   "message", "retour", "resultat"},
    "impact":     {"impact", "impacts", "effect", "effects", "delta", "change", "changes",
                   "effet", "effets"},
    "situation":  {"situation", "scenario", "event", "story", "description", "context",
                   "question", "prompt", "evenement", "histoire", "probleme"},
    "text":       {"option", "choice", "text", "label", "answer", "action", "choix",
                   "texte", "reponse"},
}
OPTION_KINDS = ("text", "budget", "reputation", "feedback", "impact")

# A number as people write it: -2000, +20, -2 000, 2,000, 1.500,50, 2k
NUMBER_PATTERN = re.compile(r"[+-]?\d+(?:[   .,]\d{3})*(?:[.,]\d+)?(?:\s?k\b)?")


# =====================================================================
# READING THE SCENARIO FILE
# =====================================================================

def simplify(text):
    """Lower-case and remove accents: 'Réputation B' -> 'reputation b'."""
    text = unicodedata.normalize("NFKD", str(text))
    return "".join(ch for ch in text if not unicodedata.combining(ch)).lower()


def normalise_signs(text):
    """Turn typographic minus signs into '-' and glue a sign to its number ('- 20' -> '-20')."""
    text = str(text).replace("−", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"([+-])\s+(?=\d)", r"\1", text)


def to_number(raw):
    """Read one number written by a human ('-2 000 EUR', '+20', '1.500,50', '2k') as an int.
    An empty cell means 'no change' and gives 0."""
    text = normalise_signs(raw).lower().strip()
    if not text:
        return 0
    match = NUMBER_PATTERN.search(text)
    if not match:
        raise ValueError(f"no number in {raw!r}")
    number = match.group()
    multiplier = 1000 if number.endswith("k") else 1
    number = re.sub(r"[\sk  ]", "", number)
    sign = -1 if number.startswith("-") else 1
    digits = number.lstrip("+-")
    if "," in digits and "." in digits:
        # 1.500,50 or 1,500.50: the last mark is the decimal one
        decimal = "," if digits.rfind(",") > digits.rfind(".") else "."
        thousands = "." if decimal == "," else ","
        digits = digits.replace(thousands, "").replace(decimal, ".")
    elif re.fullmatch(r"\d{1,3}([.,]\d{3})+", digits):
        digits = digits.replace(",", "").replace(".", "")    # 2,000 or 2.000 = two thousand
    else:
        digits = digits.replace(",", ".")                     # 2,5 = two and a half
    return sign * round(float(digits) * multiplier)


def is_number(text):
    """True when a piece of text is only a number, maybe with a unit ('-2000 EUR', '+20 rep')."""
    cleaned = re.sub(r"euros?|eur|€|points?|pts?|reputation|rep|budget|[:\s  ]",
                     "", simplify(normalise_signs(text)))
    return bool(re.fullmatch(r"[+-]?\d[\d.,]*k?", cleaned))


def budget_comes_first(first, second):
    """Decide which of two numbers is the budget. Labels win when present
    ('rep +20 / -2000 EUR'); without labels the budget is written first."""
    first, second = simplify(first), simplify(second)
    if "rep" in first and "rep" not in second:
        return False
    money_words = ("eur", "€", "budget")
    if any(w in second for w in money_words) and not any(w in first for w in money_words):
        return False
    return True


def split_impact(cell):
    """One cell holding both impacts ('-2000/+20', 'budget -2000, rep +20') -> (budget, reputation)."""
    text = normalise_signs(cell)
    found = list(NUMBER_PATTERN.finditer(text))
    if len(found) < 2:
        raise ValueError(f"expected two numbers in {cell!r}")
    gap = text[found[0].end():found[1].start()]
    cut = found[0].end() + next((i for i, ch in enumerate(gap) if ch in "/|;,"), len(gap))
    budget, reputation = to_number(found[0].group()), to_number(found[1].group())
    if not budget_comes_first(text[:cut], text[cut:]):
        budget, reputation = reputation, budget
    return budget, reputation


def unpack_cell(cell):
    """One cell holding a whole option ('Pay the cat|-2000|+20|Sales explode')
    -> (text, budget, reputation, feedback)."""
    for mark in ("|", ";", "~", "/", "#"):
        parts = [part.strip() for part in str(cell).split(mark)]
        numbers = [part for part in parts if is_number(part)]
        if len(parts) >= 3 and len(numbers) >= 2:
            words = [part for part in parts if not is_number(part)]
            text = words[0] if words else ""
            feedback = words[-1] if len(words) > 1 else ""
            budget, reputation = to_number(numbers[0]), to_number(numbers[1])
            if not budget_comes_first(numbers[0], numbers[1]):
                budget, reputation = reputation, budget
            return text, budget, reputation, feedback
    raise ValueError(f"cannot find the budget and reputation impact in {cell!r}")


def make_option(text="", budget=None, reputation=None, feedback="", impact=None):
    """Build the option tuple (text, budget_change, reputation_change, feedback)
    from whatever cells the file gives for that option."""
    if impact is not None and (budget is None or reputation is None):
        budget, reputation = split_impact(impact)          # impacts packed in one column
    elif impact and not feedback:
        try:
            split_impact(impact)
        except ValueError:
            feedback = impact                              # an "effect" column that is really text
    if budget is None or reputation is None:
        text, budget, reputation, packed_feedback = unpack_cell(text)  # whole option in one cell
        feedback = feedback or packed_feedback
    text = str(text).strip()
    if not text:
        raise ValueError("option without text")
    return (text, to_number(budget), to_number(reputation), str(feedback).strip())


def header_words(name):
    """Split a column name into words: 'budgetA' / 'budget_a' / 'Budget A (EUR)' -> ['budget', 'a', ...]."""
    name = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(name))
    return re.findall(r"[a-z]+|\d+", simplify(name))


def describe_column(name):
    """Guess what a column holds from its name: returns (kind, option letter or None)."""
    words = set(header_words(name))
    letters = words & {"a", "b", "c"}
    letter = letters.pop().upper() if len(letters) == 1 else None
    if letter is None:
        # option_1 / budget_2 style: digits 1-3 stand for A-C when the name says what it holds
        digits = words & {"1", "2", "3"}
        option_words = set().union(*(COLUMN_WORDS[k] for k in OPTION_KINDS if k != "text"),
                                   COLUMN_WORDS["text"])
        if len(digits) == 1 and words & option_words and not words & COLUMN_WORDS["id"]:
            letter = "ABC"[int(digits.pop()) - 1]
    order = ["budget", "reputation", "feedback", "impact"] if letter else \
            ["id", "budget", "reputation", "feedback", "impact", "situation", "text"]
    for kind in order:
        if words & COLUMN_WORDS[kind]:
            return kind, letter
    return ("text", letter) if letter else (None, None)


def letter_in(value):
    """'A', 'b', 'Option C', 'A)' -> the letter; anything else -> None."""
    word = re.sub(r"option|choice|choix|answer", "", simplify(value))
    word = re.sub(r"[^a-z]", "", word)
    return word.upper() if word in ("a", "b", "c") else None


def read_rows(path):
    """Open the file whatever its encoding and separator; return (header, data rows)."""
    text = None
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):     # utf-8-sig also removes an Excel BOM
        try:
            with open(path, encoding=encoding, newline="") as f:
                text = f.read()
            break
        except UnicodeDecodeError:
            continue
    first_line = next((line for line in text.splitlines() if line.strip()), "")
    separator = max(",;\t|", key=first_line.count)          # the separator used most in the header
    rows = [row for row in csv.reader(io.StringIO(text), delimiter=separator)
            if any(cell.strip() for cell in row)]
    if len(rows) < 2:
        raise ValueError(f"{os.path.basename(path)} has no scenario rows")
    header = [cell.strip() for cell in rows[0]]
    width = len(header)
    data = [[cell.strip() for cell in row] + [""] * (width - len(row)) for row in rows[1:]]
    return header, data


def build_wide_scenarios(header, rows, columns):
    """One row = one scenario, with separate columns for options A, B and C."""
    fields = {}
    for index, kind, letter in columns:
        if kind:
            fields.setdefault((kind, letter), index)
    situation_col = fields.get(("situation", None), fields.get(("text", None)))
    if situation_col is None:
        raise ValueError(f"no situation column found. Header seen: {header}")
    for letter in LETTERS:
        if ("text", letter) not in fields:
            raise ValueError(f"no column for option {letter}. Header seen: {header}")

    scenarios, ignored = [], 0
    for number, row in enumerate(rows, start=1):
        try:
            options = {}
            for letter in LETTERS:
                cells = {kind: row[fields[(kind, letter)]]
                         for kind in OPTION_KINDS if (kind, letter) in fields}
                options[letter] = make_option(**cells)
            if not row[situation_col]:
                raise ValueError("empty situation")
        except ValueError:
            ignored += 1                                   # broken row: skip it, keep the game alive
            continue
        scenario_id = row[fields[("id", None)]] if ("id", None) in fields else str(number)
        scenarios.append({"id": scenario_id, "situation": row[situation_col], "options": options})
    return scenarios, ignored


def build_long_scenarios(header, rows, columns, letter_col):
    """One row = one option: rows are grouped by scenario id (or situation)."""
    by_kind = {}
    for index, kind, _ in columns:
        if kind and index != letter_col:
            by_kind.setdefault(kind, []).append(index)
    texts = by_kind.get("text", [])
    situation_col = by_kind["situation"][0] if "situation" in by_kind else (texts.pop(0) if texts else None)
    if situation_col is None or not texts:
        raise ValueError(f"cannot find the situation and the option text. Header seen: {header}")
    option_cols = {"text": texts[0]}
    for kind in ("budget", "reputation", "feedback", "impact"):
        if kind in by_kind:
            option_cols[kind] = by_kind[kind][0]
    id_col = by_kind["id"][0] if "id" in by_kind else None

    groups, ignored, current_key = {}, 0, None
    for row in rows:
        letter = letter_in(row[letter_col])
        key = (row[id_col] if id_col is not None else "") or row[situation_col] or current_key
        if letter is None or key is None:
            ignored += 1
            continue
        current_key = key
        group = groups.setdefault(key, {"id": key, "situation": "", "options": {}})
        group["situation"] = group["situation"] or row[situation_col]
        try:
            group["options"][letter] = make_option(**{k: row[i] for k, i in option_cols.items()})
        except ValueError:
            ignored += 1
    scenarios = [g for g in groups.values()
                 if g["situation"] and all(letter in g["options"] for letter in LETTERS)]
    return scenarios, ignored + len(groups) - len(scenarios)


def load_scenarios(path):
    """Read every scenario of the file. Each one is a dictionary whose 'options'
    map 'A', 'B', 'C' to a tuple (text, budget_change, reputation_change, feedback)."""
    header, rows = read_rows(path)
    columns = [(index, *describe_column(name)) for index, name in enumerate(header)]
    if any(letter for _, _, letter in columns):
        return build_wide_scenarios(header, rows, columns)
    for index in range(len(header)):
        values = [row[index] for row in rows if row[index]]
        letters = {letter_in(value) for value in values}
        if values and None not in letters and len(letters) >= 2:
            return build_long_scenarios(header, rows, columns, index)
    raise ValueError(f"cannot tell where options A, B and C are. Header seen: {header}")


def find_scenario_file():
    """Use SCENARIO_FILE; if it is not there, use the only scenarios_*.csv next to the game."""
    path = os.path.join(BASE_DIR, SCENARIO_FILE)
    if os.path.exists(path):
        return path
    found = sorted(glob.glob(os.path.join(BASE_DIR, "scenarios_*.csv")))
    if len(found) == 1:
        return found[0]
    if not found:
        raise FileNotFoundError(f"{SCENARIO_FILE} was not found next to the game")
    names = ", ".join(os.path.basename(p) for p in found)
    raise FileNotFoundError(f"several scenario files ({names}): set SCENARIO_FILE to yours")


# =====================================================================
# PLAYING
# =====================================================================

def ask_player_name():
    """Ask the name until the player types something."""
    name = input("Your name: ").strip()
    while not name:
        name = input("Please type your name: ").strip()
    return name


def ask_choice():
    """Ask A, B or C again and again until the answer is valid (lower case accepted)."""
    answer = input("Your choice (A, B or C): ").strip().upper()
    while answer not in LETTERS:
        answer = input("Please type A, B or C: ").strip().upper()
    return answer


def show_day(day, budget, reputation, scenario):
    """Print the day number, both gauges, the situation and the three options."""
    print(f"\n--- Day {day} ---")
    print(f"[Budget: {budget} EUR | Reputation: {reputation}/{MAX_REPUTATION}]")
    print(scenario["situation"])
    for letter in LETTERS:
        print(f"  {letter}: {scenario['options'][letter][0]}")


def apply_choice(budget, reputation, option):
    """Apply the option's impacts; reputation can never go above 100. Returns a tuple."""
    text, budget_change, reputation_change, feedback = option
    budget = budget + budget_change
    reputation = min(reputation + reputation_change, MAX_REPUTATION)
    return budget, reputation


def fired_reason(budget, reputation):
    """Why the manager is fired, or None while both gauges are above zero."""
    if budget <= 0 and reputation <= 0:
        return "your budget and your reputation both hit zero"
    if budget <= 0:
        return "your budget hit zero"
    if reputation <= 0:
        return "your reputation hit zero"
    return None


def play_quarter(scenarios):
    """Play up to 10 days. Returns (budget, reputation, history, reason, last_day).
    history holds one tuple per day: (reputation_change, day, option_text)."""
    budget, reputation = START_BUDGET, START_REPUTATION
    history = []
    reason = None
    day = 0
    for day, scenario in enumerate(scenarios[:DAYS], start=1):
        show_day(day, budget, reputation, scenario)
        option = scenario["options"][ask_choice()]
        budget, reputation = apply_choice(budget, reputation, option)
        text, budget_change, reputation_change, feedback = option
        if feedback:
            print(feedback)
        print(f"Budget {budget_change:+d} EUR, Reputation {reputation_change:+d}")
        history.append((reputation_change, day, text))
        reason = fired_reason(budget, reputation)
        if reason:
            break                                          # a gauge hit zero: the game stops at once
    return budget, reputation, history, reason, day


# =====================================================================
# END OF THE GAME
# =====================================================================

def compute_score_and_title(budget, reputation):
    """Final score of a survivor and the title it earns. Returns (score, title)."""
    score = reputation + budget // 200
    for threshold, title in TITLES:
        if score >= threshold:
            return score, title
    return score, LOWEST_TITLE


def best_and_worst_moves(history):
    """Tuples compare on their first item, the reputation change:
    max() is the best move, min() the worst."""
    return max(history), min(history)


def read_best_budget():
    """Feature c: best budget among the previous games that survived (None if there is none)."""
    best = None
    try:
        with open(os.path.join(BASE_DIR, RESULTS_FILE), newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("title") == FIRED_TITLE:
                    continue
                try:
                    budget = int(row["budget"])
                except (KeyError, TypeError, ValueError):
                    continue                               # damaged line: ignore it
                if best is None or budget > best:
                    best = budget
    except (OSError, UnicodeDecodeError, csv.Error):
        return None                                        # no results yet, or unreadable file
    return best


def show_high_score(budget, title):
    """Feature c: say whether the player beat the best budget so far."""
    best = read_best_budget()
    if title == FIRED_TITLE:
        if best is not None:
            print(f"Record to beat next time: {best} EUR left at the end of a quarter.")
    elif best is None:
        print(f"First quarter survived in {RESULTS_FILE}: {budget} EUR is the record to beat.")
    elif budget > best:
        print(f"NEW RECORD! You beat the best budget ({best} EUR) by {budget - best} EUR.")
    elif budget == best:
        print(f"You equalled the best budget: {best} EUR.")
    else:
        print(f"Best budget so far: {best} EUR. You were {best - budget} EUR short.")


def show_results(name, budget, reputation, history, reason, last_day):
    """Print the end screen (fired and why, or score and title) and return the title."""
    print("\n" + "=" * 34)
    if reason:
        title = FIRED_TITLE
        print(f"YOU ARE FIRED on day {last_day}: {reason}.")
        print(f"Budget: {budget} EUR, reputation: {reputation}/{MAX_REPUTATION}")
        print(f"{name}, your title: {title}")
    else:
        score, title = compute_score_and_title(budget, reputation)
        print("Quarter survived!")
        print(f"Budget left: {budget} EUR, reputation: {reputation}/{MAX_REPUTATION}")
        print(f"Final score: {score}")
        print(f"{name}, your title: {title}")
    show_high_score(budget, title)

    best, worst = best_and_worst_moves(history)
    print(f"\nBest move:  day {best[1]}, \"{best[2]}\" ({best[0]:+d})")
    print(f"Worst move: day {worst[1]}, \"{worst[2]}\" ({worst[0]:+d})")
    return title


def save_result(name, budget, reputation, title):
    """Append one line to results.csv: name, budget, reputation, title, date."""
    path = os.path.join(BASE_DIR, RESULTS_FILE)
    new_file = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["name", "budget", "reputation", "title", "date"])
        writer.writerow([name, budget, reputation, title, datetime.now().strftime("%Y-%m-%d %H:%M")])


# =====================================================================
# MAIN: load, play, show, save - and never crash
# =====================================================================

def main():
    print("=" * 34)
    print(" SURVIVE THE QUARTER - Croissant Rocket")
    print("=" * 34)

    # Load the scenarios; a missing or unreadable file ends the game with a message
    try:
        path = find_scenario_file()
        scenarios, ignored = load_scenarios(path)
    except (OSError, ValueError) as error:
        print(f"Cannot start the game: {error}")
        return
    if not scenarios:
        print(f"No playable scenario in {os.path.basename(path)}.")
        return
    print(f"{len(scenarios)} scenarios loaded from {os.path.basename(path)}"
          + (f" ({ignored} broken line(s) ignored)." if ignored else "."))
    if len(scenarios) < DAYS:
        print(f"Only {len(scenarios)} scenarios: the quarter will last {len(scenarios)} days.")

    # Play: Ctrl+C or Ctrl+D stops the game cleanly instead of crashing
    try:
        name = ask_player_name()
        random.shuffle(scenarios)
        budget, reputation, history, reason, last_day = play_quarter(scenarios)
    except (KeyboardInterrupt, EOFError):
        print("\nGame stopped. Nothing saved.")
        return

    # End: show the result, then leave a trace in results.csv
    title = show_results(name, budget, reputation, history, reason, last_day)
    try:
        save_result(name, budget, reputation, title)
        print(f"Saved in {RESULTS_FILE}")
    except OSError as error:
        print(f"Could not save in {RESULTS_FILE} ({error}). Close it if it is open in Excel.")


if __name__ == "__main__":
    main()
