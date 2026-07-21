from pathlib import Path

from btx.scaffold import scaffold_directory


def init_project():
    root = Path.cwd()
    scaffold_directory(root, root.name)
