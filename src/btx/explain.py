def build_score_explanation(knowledge: dict) -> list:
    """
    Explain how the Engineering Health Score was calculated.
    """

    explanation = []

    if knowledge["repository_status"] != "Git Enabled":
        explanation.append(
            {
                "reason": "Git repository not initialized.",
                "impact": -25,
            }
        )

    if knowledge["configuration_status"] == "Configuration Missing":
        explanation.append(
            {
                "reason": "Blocktracex configuration missing.",
                "impact": -15,
            }
        )

    if knowledge["testing_maturity"] in ("None", "Low"):
        explanation.append(
            {
                "reason": "Automated testing is below recommended level.",
                "impact": -20,
            }
        )

    if knowledge["documentation_maturity"] != "Excellent":
        explanation.append(
            {
                "reason": "Documentation can be improved.",
                "impact": -14,
            }
        )

    return explanation
