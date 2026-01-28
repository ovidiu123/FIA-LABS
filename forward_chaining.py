from luna_city_rules import check_condition


def forward_chaining(facts, rules):
    for rule in rules:
        try:
            if all(check_condition(facts, cond) for cond in rule["if"]):
                print(f"{rule['name']} FIRED: {rule['desc']}")
                return "one", rule['then']
        except (KeyError, TypeError):
            pass

    return "none", []