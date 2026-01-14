from functools import lru_cache
from pathlib import Path
from git import Repo
from pathlib import Path
from typing import Dict

from dumpster.logs import getLogger

logger = getLogger(__name__)


@lru_cache(maxsize=1)
def _cached_repo(root: Path):
    try:
        return Repo(root, search_parent_directories=True, expand_vars=False)
    except Exception:
        return None


@lru_cache(maxsize=100_000)
def _is_git_ignored_cached(repo_root: str, rel_path: str) -> bool:
    repo = Repo(repo_root, search_parent_directories=True, expand_vars=False)
    ignored = repo.ignored(rel_path)
    return rel_path in ignored


def git_repo(root: Path):
    try:
        return _cached_repo(root)
    except Exception as e:
        logger.warning(f"Failed to find git repo from {root}: {e}")
        return None


def is_git_repo(path: Path) -> bool:
    return git_repo(path) is not None


def build_gitignore_set(repo: Repo, files: list[Path]) -> set[Path]:
    rels = [str(f.relative_to(repo.working_dir)) for f in files]
    ignored = repo.git.check_ignore(*rels).splitlines()
    return set(ignored)


def is_git_ignored(path: Path) -> bool:
    repo = git_repo(path)
    if not repo:
        logger.info(f"{path} is not in the git repo")
        return False

    try:
        # Get relative path to repository root
        rel_path = path.relative_to(repo.working_dir)
        return _is_git_ignored_cached(repo.working_dir, rel_path)
    except Exception as e:
        logger.warning(f"Failed to check ignored file for {path}: {e}")
        return False


def git_ignored_set(repo, paths: list[Path]) -> set[str]:
    """
    Returns a set of repo-relative paths ignored by git.
    """
    if not paths:
        return set()

    rels = [str(p.relative_to(repo.working_dir)) for p in paths if p.exists()]

    if not rels:
        return set()

    try:
        out = repo.git.check_ignore(*rels)
        return set(out.splitlines())
    except Exception:
        return set()


def get_git_metadata(path: Path) -> Dict[str, str] | None:
    try:
        working_dir = str(path)

        git_dir_exists = Path(path / ".git").exists()
        if not git_dir_exists:
            return None

        repo = Repo(path, search_parent_directories=True, expand_vars=False)
        head = repo.head
        commit = head.commit
        remote = repo.remote()

        return {
            "working_dir": working_dir,
            "remote_url": str(remote.url),
            "remote_name": str(remote.name),
            "branch": head.ref.name if head.is_detached else "detached",
            "commit": str(commit.hexsha),
            "commit_time": commit.committed_datetime.isoformat(),
            "author": f"{commit.author.name} <{commit.author.email}>",
            "message": str(commit.message).strip() if commit.message else "",
            "dirty": "yes" if repo.is_dirty() else "no",
        }
    except Exception as e:
        logger.warning(f"Failed to get repo metadata from {path}: {e}")
        return None


def render_git_metadata(meta: Dict[str, str] | None) -> str:
    if meta is None:
        return ""
    lines = ["# Git metadata"]
    for k, v in meta.items():
        lines.append(f"# {k}: {v}")
    return "\n".join(lines)
