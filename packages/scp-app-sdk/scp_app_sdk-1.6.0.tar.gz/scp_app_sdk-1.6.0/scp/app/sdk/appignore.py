from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

def load_appignore(root: Path) -> PathSpec:
    ignore_file = root / ".appignore"
    if not ignore_file.exists():
        return PathSpec.from_lines(GitWildMatchPattern, [])

    return PathSpec.from_lines(
        GitWildMatchPattern,
        ignore_file.read_text().splitlines()
    )

def should_include(path: Path, spec: PathSpec, root: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    return not spec.match_file(rel)