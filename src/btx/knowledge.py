def build_project_knowledge(project_data: dict) -> dict:
    """
    Transform project inspection data into structured knowledge.
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

    # Testing maturity
    test_files = project_data.get("test_files", 0)

    if test_files == 0:
        maturity = "None"
    elif test_files < 5:
        maturity = "Low"
    elif test_files < 20:
        maturity = "Moderate"
    else:
        maturity = "High"

    knowledge["testing_maturity"] = maturity

    # Version
    knowledge["knowledge_version"] = "1.0"

    return knowledge