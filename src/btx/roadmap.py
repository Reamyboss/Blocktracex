def build_roadmap(knowledge: dict) -> dict:
    """
    Generate an engineering roadmap based on project knowledge.
    """

    roadmap = {}

    roadmap["current_stage"] = knowledge.get(
        "engineering_maturity",
        "Unknown",
    )

    roadmap["health_score"] = knowledge.get(
        "engineering_health_score",
        "Unknown",
    )

    roadmap["immediate_goal"] = knowledge.get(
        "next_best_action",
        "Maintain current engineering practices.",
    )

    roadmap["estimated_impact"] = knowledge.get(
        "estimated_impact",
        "Low",
    )

    milestones = []

    if knowledge.get("testing_maturity") in ("None", "Low"):
        milestones.append("Reach 5 automated test files.")

    if knowledge.get("configuration_status") == "Configuration Missing":
        milestones.append("Create a btx.toml configuration file.")

    if knowledge.get("engineering_maturity") == "Early":
        milestones.append("Reach Emerging engineering maturity.")

    elif knowledge.get("engineering_maturity") == "Emerging":
        milestones.append("Reach Advanced engineering maturity.")

    if knowledge.get("engineering_health_status") != "Excellent":
        milestones.append("Achieve a 90+ Engineering Health Score.")

    roadmap["milestones"] = milestones

    if milestones:
        roadmap["next_milestone"] = milestones[0]
    else:
        roadmap["next_milestone"] = "Continue current engineering practices."

    return roadmap
