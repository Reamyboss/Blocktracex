from btx.scaffold import create_project


def test_create_project(tmp_path):
    project = tmp_path / "demo"

    create_project(str(project))

    assert project.exists()
