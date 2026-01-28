from backward_chaining import backward_chaining
from forward_chaining import forward_chaining
from luna_city_rules import RULES


def get_one_condition_field_from_rule(condition):
    if not isinstance(condition, tuple):
        return None

    if condition[0] in ["eq", "lt", "gt"]:
        return condition[1]
    elif condition[0] in ["is_true", "is_false"]:
        return condition[1]
    elif condition[0] == "between":
        return condition[1]
    return None


def get_all_condition_fields_from_rules(rule):
    fields = []
    for condition in rule["if"]:
        if isinstance(condition, tuple):
            field = get_one_condition_field_from_rule(condition)
            if field:
                fields.append(field)
    return fields


class QuestionAsker:
    def __init__(self):
        self.field_questions = {
            "origin": {
                "question": "Where is the tourist from?",
                "options": ["earth", "mars", "luna_city"]
            },
            "attire": {
                "question": "What attire is the tourist wearing?",
                "options": ["business", "academic", "casual", "work_uniform"]
            },
            "has_briefcase": {
                "question": "Does the tourist have a briefcase?",
                "type": "yes/no"
            },
            "discusses_earth_business": {
                "question": "Does the tourist discuss Earth business/politics?",
                "type": "yes/no"
            },
            "visits_research_facilities": {
                "question": "Does the tourist visit research facilities?",
                "type": "yes/no"
            },
            "has_laptop": {
                "question": "Does the tourist have a laptop?",
                "type": "yes/no"
            },
            "has_camera": {
                "question": "Does the tourist have a camera?",
                "type": "yes/no"
            },
            "visits_beautiful_places": {
                "question": "Does the tourist visit beautiful places?",
                "type": "yes/no"
            },
            "interested_in_luna_culture": {
                "question": "Is the tourist interested in Luna-City culture?",
                "type": "yes/no"
            },
            "visits_industrial_facilities": {
                "question": "Does the tourist visit industrial facilities?",
                "type": "yes/no"
            },
            "has_technical_equipment": {
                "question": "Does the tourist have technical equipment?",
                "type": "yes/no"
            },
            "has_local_id": {
                "question": "Does the tourist have a local Luna-City ID?",
                "type": "yes/no"
            },
            "discusses_local_politics": {
                "question": "Does the tourist discuss local Luna-City politics?",
                "type": "yes/no"
            },
            "books_hotel": {
                "question": "Does the tourist book a hotel?",
                "type": "yes/no"
            },
            "stay_days": {
                "question": "How many days will the tourist stay?",
                "type": "number"
            }
        }

        self.asked_fields = set()

    def ask_for_field(self, field, facts):
        if field in facts or field in self.asked_fields:
            return

        if field not in self.field_questions:
            return

        self.asked_fields.add(field)
        question_info = self.field_questions[field]

        print(f"\n{question_info['question']}")

        if question_info.get("type") == "yes/no":
            print("  1 - Yes")
            print("  2 - No")
            answer = input("Answer (1 or 2): ").strip()
            facts[field] = True if answer == "1" else False

        elif question_info.get("type") == "number":
            answer = input("Enter number of days: ").strip()
            try:
                facts[field] = int(answer)
            except ValueError:
                print("Invalid number, skipping...")

        elif "options" in question_info:
            for i, option in enumerate(question_info["options"], 1):
                print(f"  {i} - {option}")
            answer = input(f"Answer (1-{len(question_info['options'])}): ").strip()
            try:
                idx = int(answer) - 1
                if 0 <= idx < len(question_info["options"]):
                    facts[field] = question_info["options"][idx]
            except ValueError:
                print("Invalid option, skipping...")


def run_forward_chaining():
    print("\n" + "=" * 60)
    print("DYNAMIC FORWARD CHAINING")
    print("=" * 60)
    print("\nI will ask questions to determine the tourist type.")
    print("After each answer, I'll check if we can reach a conclusion.\n")

    asker = QuestionAsker()
    facts = {}

    # Step 1: Always ask origin first
    asker.ask_for_field("origin", facts)

    if "origin" not in facts:
        print("\nCannot proceed without origin information.")
        return

    # Step 2: Filter rules by origin
    relevant_rules = [rule for rule in RULES if any(
        isinstance(condition, tuple) and condition[0] == "eq" and condition[1] == "origin" and condition[2] == facts["origin"]
        for condition in rule["if"]
    )]

    print(f"\nBased on origin '{facts['origin']}', checking {len(relevant_rules)} relevant rules...")

    # Step 3: Ask questions and check
    max_iterations = 15
    iteration = 0

    while iteration < max_iterations:
        # Check if we can conclude with current facts
        status, result = forward_chaining(facts, RULES)

        if status == "one":
            print(f"\n{'=' * 60}")
            print(f"CONCLUSION REACHED: {result}")
            print(f"{'=' * 60}")
            return

        # Ask next unanswered question from relevant rules
        asked_something = False
        for rule in relevant_rules:
            condition_fields = get_all_condition_fields_from_rules(rule)
            for field in condition_fields:
                if field not in facts and field not in asker.asked_fields:
                    asker.ask_for_field(field, facts)
                    asked_something = True
                    iteration += 1
                    break
            if asked_something:
                break

        if not asked_something:
            break

    # Final check
    status, result = forward_chaining(facts, RULES)

    print(f"\n{'=' * 60}")
    if status == "one":
        print(f"CONCLUSION REACHED: {result}")
    else:
        print("Could not determine tourist type with given information.")
    print(f"{'=' * 60}")


def run_backward_chaining():
    print("\n" + "=" * 60)
    print("DYNAMIC BACKWARD CHAINING")
    print("=" * 60)

    asker = QuestionAsker()

    # Step 1: Get all possible goals
    goals = sorted(set(rule["then"] for rule in RULES))
    print("\nAvailable tourist types to prove:")
    for i, goal in enumerate(goals, 1):
        print(f"  {i} - {goal}")

    choice = input(f"\nSelect goal to prove (1-{len(goals)}): ").strip()
    try:
        goal_idx = int(choice) - 1
        if not (0 <= goal_idx < len(goals)):
            print("Invalid choice.")
            return
        goal = goals[goal_idx]
    except ValueError:
        print("Invalid input.")
        return

    print(f"\nAttempting to prove: {goal}")

    facts = {}

    # Step 2: Find rules that can prove this goal
    relevant_rules = [rule for rule in RULES if rule["then"] == goal]

    if not relevant_rules:
        print(f"\nNo rules can prove '{goal}'")
        return

    print(f"\n[Found {len(relevant_rules)} rule(s) that can prove this goal]")

    # Step 3: Try each rule
    for rule_idx, rule in enumerate(relevant_rules, 1):
        fields = get_all_condition_fields_from_rules(rule)
        for field in fields:
            if field not in facts:
                asker.ask_for_field(field, facts)

        status, result = backward_chaining(goal, facts, RULES)

        if status == "one":
            print(f"\n{'=' * 60}")
            print(f"GOAL '{goal}' SUCCESSFULLY PROVEN!")
            print(f"{'=' * 60}")
            return
        else:
            continue

    print(f"\n{'=' * 60}")
    print(f"Could not prove '{goal}' with given information.")
    print(f"{'=' * 60}")
