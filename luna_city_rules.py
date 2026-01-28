def is_true(facts, key):
    return facts.get(key) is True


def get_days(facts):
    return facts.get("stay_days", None)


def check_condition(facts, condition):
    if condition[0] == "eq":
        field, _, value = condition[1], condition[0], condition[2]
        return facts.get(field) == value

    elif condition[0] == "is_true":
        return is_true(facts, condition[1])

    elif condition[0] == "lt":
        field, value = condition[1], condition[2]
        field_value = get_days(facts) if field == "stay_days" else facts.get(field)
        return field_value is not None and field_value < value

    elif condition[0] == "gt":
        field, value = condition[1], condition[2]
        field_value = get_days(facts) if field == "stay_days" else facts.get(field)
        return field_value is not None and field_value > value

    elif condition[0] == "between":
        field, min_val, max_val = condition[1], condition[2], condition[3]
        field_value = get_days(facts) if field == "stay_days" else facts.get(field)
        return field_value is not None and min_val <= field_value <= max_val

    elif condition[0] == "is_false":
        return facts.get(condition[1]) is False

    return False


RULES = [
    # Earth Business Tourist
    {
        "name": "R1",
        "then": "Earth Business Tourist",
        "desc": "From Earth AND business attire AND stay < 7 days",
        "if": [
            ("eq", "origin", "earth"),
            ("eq", "attire", "business"),
            ("lt", "stay_days", 7)
        ]
    },
    {
        "name": "R2",
        "then": "Earth Business Tourist",
        "desc": "From Earth AND has briefcase AND discusses Earth business/politics",
        "if": [
            ("eq", "origin", "earth"),
            ("is_true", "has_briefcase"),
            ("is_true", "discusses_earth_business")
        ]
    },

    # Earth Academic
    {
        "name": "R3",
        "then": "Earth Academic",
        "desc": "From Earth AND academic attire AND visits research facilities AND stay > 31 days",
        "if": [
            ("eq", "origin", "earth"),
            ("eq", "attire", "academic"),
            ("is_true", "visits_research_facilities"),
            ("gt", "stay_days", 31)
        ]
    },
    {
        "name": "R4",
        "then": "Earth Academic",
        "desc": "From Earth AND has laptop AND visits research facilities AND stay > 31 days",
        "if": [
            ("eq", "origin", "earth"),
            ("is_true", "has_laptop"),
            ("is_true", "visits_research_facilities"),
            ("gt", "stay_days", 31)
        ]
    },

    # Earth Adventure Tourist
    {
        "name": "R5",
        "then": "Earth Adventure Tourist",
        "desc": "From Earth AND has camera AND visits beautiful places AND stay 7–31 days",
        "if": [
            ("eq", "origin", "earth"),
            ("is_true", "has_camera"),
            ("is_true", "visits_beautiful_places"),
            ("between", "stay_days", 7, 31)
        ]
    },
    {
        "name": "R6",
        "then": "Earth Adventure Tourist",
        "desc": "From Earth AND casual attire AND has camera AND stay 7–31 days",
        "if": [
            ("eq", "origin", "earth"),
            ("eq", "attire", "casual"),
            ("is_true", "has_camera"),
            ("between", "stay_days", 7, 31)
        ]
    },

    # Mars Colony Visitor
    {
        "name": "R7",
        "then": "Mars Colony Visitor",
        "desc": "From Mars AND casual attire AND has camera AND stay < 31 days",
        "if": [
            ("eq", "origin", "mars"),
            ("eq", "attire", "casual"),
            ("is_true", "has_camera"),
            ("lt", "stay_days", 31)
        ]
    },
    {
        "name": "R8",
        "then": "Mars Colony Visitor",
        "desc": "From Mars AND interested in Luna-City culture AND has camera AND stay < 31 days",
        "if": [
            ("eq", "origin", "mars"),
            ("is_true", "interested_in_luna_culture"),
            ("is_true", "has_camera"),
            ("lt", "stay_days", 31)
        ]
    },

    # Mars Colony Worker
    {
        "name": "R9",
        "then": "Mars Colony Worker",
        "desc": "From Mars AND work uniform AND visits industrial facilities AND stay > 31 days",
        "if": [
            ("eq", "origin", "mars"),
            ("eq", "attire", "work_uniform"),
            ("is_true", "visits_industrial_facilities"),
            ("gt", "stay_days", 31)
        ]
    },
    {
        "name": "R10",
        "then": "Mars Colony Worker",
        "desc": "From Mars AND technical equipment AND visits industrial facilities AND stay > 31 days",
        "if": [
            ("eq", "origin", "mars"),
            ("is_true", "has_technical_equipment"),
            ("is_true", "visits_industrial_facilities"),
            ("gt", "stay_days", 31)
        ]
    },

    # Loonie
    {
        "name": "R11",
        "then": "Loonie",
        "desc": "From Luna-City AND has local ID AND discusses local politics",
        "if": [
            ("eq", "origin", "luna_city"),
            ("is_true", "has_local_id"),
            ("is_true", "discusses_local_politics")
        ]
    },
    {
        "name": "R12",
        "then": "Loonie",
        "desc": "From Luna-City AND has local ID AND no hotel booking",
        "if": [
            ("eq", "origin", "luna_city"),
            ("is_true", "has_local_id"),
            ("is_false", "books_hotel")
        ]
    },
]