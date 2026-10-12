def build_engineering_coach(knowledge: dict) -> dict:
    """
    Generate actionable engineering coaching based on project knowledge.
    """

    coaching = {}

    next_action = knowledge.get(
        "next_best_action",
        "Maintain current engineering practices.",
    )

    impact = knowledge.get(
        "estimated_impact",
        "Low",
    )

    coaching["next_action"] = next_action
    coaching["impact"] = impact

    explanation = {
        "Increase automated testing to improve software reliability.": (
            "More automated tests reduce regressions and improve confidence "
            "when making changes."
        ),
        "Create a Blocktracex configuration file.": (
            "Configuration enables consistent project analysis and future automation."
        ),
        "Improve project structure.": (
            "A clean project structure improves maintainability and onboarding."
        ),
        "Expand project documentation.": (
            "Better documentation helps developers understand and contribute faster."
        ),
        "Maintain current engineering practices.": (
            "The project is already following strong engineering practices."
        ),
    }

    effort = {
        "Increase automated testing to improve software reliability.": "Medium",
        "Create a Blocktracex configuration file.": "Low",
        "Improve project structure.": "Medium",
        "Expand project documentation.": "Low",
        "Maintain current engineering practices.": "Low",
    }

    first_step = {
        "Increase automated testing to improve software reliability.": (
            "Add unit tests for your most important module first."
        ),
        "Create a Blocktracex configuration file.": (
            "Generate a default btx.toml configuration file."
        ),
        "Improve project structure.": (
            "Separate source code, documentation, and tests into dedicated directories."
        ),
        "Expand project documentation.": (
            "Create developer documentation inside the docs folder."
        ),
        "Maintain current engineering practices.": (
            "Continue monitoring engineering health as the project evolves."
        ),
    }

    coaching["why"] = explanation.get(
        next_action,
        "No explanation available.",
    )

    coaching["estimated_effort"] = effort.get(
        next_action,
        "Unknown",
    )

    coaching["first_step"] = first_step.get(
        next_action,
        "No first step available.",
    )

    return coaching
