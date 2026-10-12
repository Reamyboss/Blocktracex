def build_project_knowledge(project_data: dict) -> dict:
    """
    Transform project inspection data into structured engineering knowledge.
    """

    knowledge = {}

    # Project type
    knowledge["project_type"] = "Python Project"

    # Repository
    knowledge["repository_status"] = (
        "Git Enabled" if project_data.get("git") else "Not a Git Repository"
    )

    # Configuration
    knowledge["configuration_status"] = (
        "Configured" if project_data.get("btx_config") else "Configuration Missing"
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

    # Engineering Health

    documentation_scores = {
        "Missing": 20,
        "Basic": 60,
        "Excellent": 100,
    }

    testing_scores = {
        "None": 20,
        "Low": 50,
        "Moderate": 80,
        "High": 100,
    }

    structure_scores = {
        "Needs Improvement": 40,
        "Healthy": 100,
    }

    engineering_scores = {
        "Early": 30,
        "Emerging": 70,
        "Advanced": 100,
    }

    risk_scores = {
        "High": 20,
        "Medium": 60,
        "Low": 100,
    }

    health_inputs = [
        documentation_scores[documentation],
        testing_scores[testing],
        structure_scores[structure],
        engineering_scores[engineering],
        risk_scores[risk],
    ]

    health_score = round(sum(health_inputs) / len(health_inputs))

    if health_score >= 90:
        health_status = "Excellent"
    elif health_score >= 75:
        health_status = "Healthy"
    elif health_score >= 60:
        health_status = "Fair"
    elif health_score >= 40:
        health_status = "Needs Attention"
    else:
        health_status = "Critical"

    knowledge["engineering_health_score"] = f"{health_score}/100"
    knowledge["engineering_health_value"] = health_score
    knowledge["engineering_health_status"] = health_status

    # Engineering Recommendations

    recommendations = []

    if documentation == "Missing":
        recommendations.append(
            "Add a README.md to help developers understand and use the project."
        )
    elif documentation == "Basic":
        recommendations.append(
            "Improve project documentation with a CHANGELOG and docs directory."
        )

    if testing == "None":
        recommendations.append(
            "Introduce automated tests to improve reliability and engineering confidence."
        )
    elif testing == "Low":
        recommendations.append("Increase test coverage to improve project quality.")

    if structure == "Needs Improvement":
        recommendations.append(
            "Improve project organization by separating source code and documentation."
        )

    if engineering == "Early":
        recommendations.append(
            "Adopt engineering best practices such as Git, configuration management, and testing."
        )
    elif engineering == "Emerging":
        recommendations.append(
            "Continue strengthening engineering maturity with CI/CD and automation."
        )

    if risk == "High":
        recommendations.append(
            "Reduce engineering risk by enabling Git and introducing automated testing."
        )
    elif risk == "Medium":
        recommendations.append("Lower project risk by increasing testing maturity.")

    knowledge["recommendations"] = recommendations

    # Engineering Evidence

    evidence = []

    # Repository
    if project_data.get("git"):
        evidence.append("✓ Git repository detected.")
    else:
        evidence.append("✗ Git repository not detected.")

    # Configuration
    if project_data.get("btx_config"):
        evidence.append("✓ Blocktracex configuration detected.")
    else:
        evidence.append("⚠ Blocktracex configuration missing.")

    # Documentation
    if readme:
        evidence.append("✓ README.md documentation found.")
    else:
        evidence.append("✗ README.md not found.")

    if changelog:
        evidence.append("✓ CHANGELOG.md found.")
    else:
        evidence.append("⚠ CHANGELOG.md not found.")

    if docs:
        evidence.append("✓ Documentation directory detected.")
    else:
        evidence.append("⚠ Documentation directory missing.")

    # Source Code
    if source_files > 0:
        evidence.append(f"✓ {source_files} Python source file(s) discovered.")
    else:
        evidence.append("✗ No Python source files discovered.")

    # Testing
    if test_files == 0:
        evidence.append("✗ No automated tests detected.")
    elif test_files < 5:
        evidence.append(
            f"⚠ {test_files} automated test file(s) detected (Low coverage)."
        )
    elif test_files < 20:
        evidence.append(
            f"✓ {test_files} automated test file(s) detected (Moderate coverage)."
        )
    else:
        evidence.append(
            f"✓ {test_files} automated test file(s) detected (High coverage)."
        )

    # Runtime
    evidence.append(f"✓ Python {project_data['python_version']} detected.")

    knowledge["engineering_evidence"] = evidence

    # Engineering Verdict

    if health_score >= 90:
        verdict = (
            "This project demonstrates excellent engineering practices. "
            "Documentation, structure, testing, and repository health are all "
            "well maintained."
        )

    elif health_score >= 75:
        verdict = (
            "This project has strong engineering foundations with only minor "
            "areas for improvement. Increasing automated testing will further "
            "improve long-term reliability."
        )

    elif health_score >= 60:
        verdict = (
            "The project shows promising engineering practices but requires "
            "improvements before reaching a mature engineering standard."
        )

    elif health_score >= 40:
        verdict = (
            "The project requires engineering attention. Documentation, "
            "testing, or project organization should be strengthened."
        )

    else:
        verdict = (
            "The project is currently in an early engineering state. "
            "Foundational engineering practices should be established before "
            "future expansion."
        )

    knowledge["engineering_verdict"] = verdict

    # Engineering Intelligence

    priorities = []

    if testing in ("None", "Low"):
        priorities.append("Increase automated testing to improve software reliability.")

    if not project_data.get("btx_config"):
        priorities.append("Create a Blocktracex configuration file.")

    if documentation == "Basic":
        priorities.append("Expand project documentation.")

    if structure == "Needs Improvement":
        priorities.append("Improve project structure.")

    if not priorities:
        priorities.append("Maintain current engineering practices.")

    knowledge["engineering_priorities"] = priorities

    # Next Best Action

    if priorities:
        knowledge["next_best_action"] = priorities[0]
    else:
        knowledge["next_best_action"] = "Maintain current engineering practices."

        # Estimated Impact

    if testing == "None":
        impact = "Very High"

    elif testing == "Low" or documentation == "Missing":
        impact = "High"

    elif structure == "Needs Improvement" or not project_data.get("btx_config"):
        impact = "Medium"

    else:
        impact = "Low"

    knowledge["estimated_impact"] = impact

    # Knowledge version

    knowledge["knowledge_version"] = "1.3"

    return knowledge
