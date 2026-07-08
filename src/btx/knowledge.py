def build_project_knowledge(project_data: dict) -> dict:
    """
    Transform project inspection data into structured engineering knowledge.
    """

    knowledge = {}

    # Project type
    knowledge["project_type"] = "Python Project"

    # Repository
    knowledge["repository_status"] = (
        "Git Enabled"
        if project_data.get("git")
        else "Not a Git Repository"
    )

    # Configuration
    knowledge["configuration_status"] = (
        "Configured"
        if project_data.get("btx_config")
        else "Configuration Missing"
    )

    # Documentation maturity
    readme = project_data.get("readme", False)
    changelog = project_data.get("changelog", False)
    docs = project_data.get("docs", False)

    if readme and changelog and docs:
        documentation = "Excellent"
    elif readme:
        documentation = "Basic"
    else:
        documentation = "Missing"

    knowledge["documentation_maturity"] = documentation

    # Testing maturity
    test_files = project_data.get("test_files", 0)

    if test_files == 0:
        testing = "None"
    elif test_files < 5:
        testing = "Low"
    elif test_files < 20:
        testing = "Moderate"
    else:
        testing = "High"

    knowledge["testing_maturity"] = testing

    # Project structure
    source_files = project_data.get("source_files", 0)

    if source_files > 0 and docs:
        structure = "Healthy"
    else:
        structure = "Needs Improvement"

    knowledge["project_structure"] = structure

    # Engineering maturity
    score = 0

    if project_data.get("git"):
        score += 1

    if project_data.get("btx_config"):
        score += 1

    if readme:
        score += 1

    if test_files > 0:
        score += 1

    if score == 4:
        engineering = "Advanced"
    elif score >= 2:
        engineering = "Emerging"
    else:
        engineering = "Early"

    knowledge["engineering_maturity"] = engineering

    # Risk level
    if not project_data.get("git"):
        risk = "High"
    elif test_files == 0:
        risk = "Medium"
    else:
        risk = "Low"

    knowledge["risk_level"] = risk

    # Knowledge version
    knowledge["knowledge_version"] = "1.1"

    return knowledge