from luna_city_rules import check_condition


def backward_chaining(goal, facts, rules, visited=None):
    if visited is None:
        visited = set()

    if goal in visited:
        return "none", []
    visited.add(goal)

    for rule in rules:
        if rule["then"] == goal:
            all_conditions_proven = True

            for condition in rule["if"]:
                if isinstance(condition, tuple):
                    if not check_condition(facts, condition):
                        all_conditions_proven = False
                        break
                else:
                    result = backward_chaining(condition, facts, rules, visited.copy())
                    if isinstance(result, tuple):
                        if result[0] == "none":
                            all_conditions_proven = False
                            break
                    elif not result:
                        all_conditions_proven = False
                        break

            if all_conditions_proven:
                return "one", goal

    return "none", []