from pathlib import Path

from btx.templates import BTX_CONFIG_TEMPLATE


def create_config(root: Path, project_name: str):
    (root / "btx.toml").write_text(
        BTX_CONFIG_TEMPLATE.format(name=project_name),
        encoding="utf-8",
    )
