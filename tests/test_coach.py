from btx.coach import build_engineering_coach


def test_coach_returns_dictionary():
    knowledge = {
        "next_best_action": "Increase automated testing.",
        "estimated_impact": "High",
    }

    coach = build_engineering_coach(knowledge)

    assert isinstance(coach, dict)


def test_contains_next_action():
    knowledge = {
        "next_best_action": "Increase automated testing.",
        "estimated_impact": "High",
    }

    coach = build_engineering_coach(knowledge)

    assert "next_action" in coach


def test_contains_impact():
    knowledge = {
        "next_best_action": "Increase automated testing.",
        "estimated_impact": "High",
    }

    coach = build_engineering_coach(knowledge)

    assert "impact" in coach


def test_contains_estimated_effort():
    knowledge = {
        "next_best_action": "Increase automated testing.",
        "estimated_impact": "High",
    }

    coach = build_engineering_coach(knowledge)

    assert "estimated_effort" in coach


def test_contains_why():
    knowledge = {
        "next_best_action": "Increase automated testing.",
        "estimated_impact": "High",
    }

    coach = build_engineering_coach(knowledge)

    assert "why" in coach


def test_contains_first_step():
    knowledge = {
        "next_best_action": "Increase automated testing.",
        "estimated_impact": "High",
    }

    coach = build_engineering_coach(knowledge)

    assert "first_step" in coach
