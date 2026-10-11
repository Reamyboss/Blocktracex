from btx.knowledge import build_project_knowledge


def sample_project():
    return {
        "git": True,
        "btx_config": False,
        "readme": True,
        "changelog": True,
        "docs": True,
        "source_files": 19,
        "test_files": 1,
        "python_version": "3.14.0",
    }


def test_returns_dictionary():
    knowledge = build_project_knowledge(sample_project())

    assert isinstance(knowledge, dict)


def test_engine_version_exists():
    knowledge = build_project_knowledge(sample_project())

    assert "knowledge_version" in knowledge


def test_health_score_exists():
    knowledge = build_project_knowledge(sample_project())

    assert "engineering_health_score" in knowledge


def test_engineering_verdict_exists():
    knowledge = build_project_knowledge(sample_project())

    assert "engineering_verdict" in knowledge


def test_engineering_evidence_exists():
    knowledge = build_project_knowledge(sample_project())

    assert "engineering_evidence" in knowledge


def test_engineering_priorities_exist():
    knowledge = build_project_knowledge(sample_project())

    assert "engineering_priorities" in knowledge


def test_next_best_action_exists():
    knowledge = build_project_knowledge(sample_project())

    assert "next_best_action" in knowledge


def test_estimated_impact_exists():
    knowledge = build_project_knowledge(sample_project())

    assert "estimated_impact" in knowledge
