from dataclasses import dataclass
from pathlib import Path

from app.core.config import Settings
from app.core.security import is_safe_text_file, safe_resolve


@dataclass
class RepositorySnapshot:
    context: str
    files: list[str]


class RepositoryService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _root(self, repository_path: str) -> Path:
        requested = Path(repository_path)
        root = (
            requested.resolve()
            if requested.is_absolute()
            else safe_resolve(self.settings.workspace_root, requested)
        )
        if not root.exists() or not root.is_dir():
            raise FileNotFoundError(f"Repository directory not found: {repository_path}")
        return root

    def list_files(self, repository_path: str, limit: int = 200) -> list[str]:
        root = self._root(repository_path)
        ignored = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build"}
        output: list[str] = []
        for path in sorted(root.rglob("*")):
            if (
                path.is_file()
                and not any(part in ignored for part in path.parts)
                and is_safe_text_file(path)
            ):
                output.append(path.relative_to(root).as_posix())
                if len(output) >= limit:
                    break
        return output

    def read_file(self, repository_path: str, relative_path: str) -> str:
        root = self._root(repository_path)
        path = safe_resolve(root, relative_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {relative_path}")
        if not is_safe_text_file(path):
            raise PermissionError(f"File type is not allowed: {relative_path}")
        if path.stat().st_size > self.settings.max_file_bytes:
            raise ValueError(f"File is too large: {relative_path}")
        return path.read_text(encoding="utf-8", errors="replace")

    def search(self, repository_path: str, query: str, limit: int = 20) -> list[str]:
        query_lower = query.lower()
        result: list[str] = []
        for path in self.list_files(repository_path):
            if query_lower in path.lower() or query_lower in self.read_file(repository_path, path).lower():
                result.append(path)
                if len(result) >= limit:
                    break
        return result

    def snapshot(
        self,
        repository_path: str,
        instruction: str,
        max_files: int = 25,
        max_chars: int = 60_000,
    ) -> RepositorySnapshot:
        files = self.list_files(repository_path)
        keywords = {
            token.lower().strip(".,:;()[]{}")
            for token in instruction.split()
            if len(token) >= 4
        }

        def rank(path: str) -> tuple[int, str]:
            score = sum(2 for keyword in keywords if keyword in path.lower())
            if path in {"README.md", "pyproject.toml", "package.json", "requirements.txt"}:
                score += 3
            return -score, path

        selected = sorted(files, key=rank)[:max_files]
        blocks: list[str] = []
        included: list[str] = []
        total = 0

        for path in selected:
            content = self.read_file(repository_path, path)
            block = f"\n--- FILE: {path} ---\n{content}\n"
            if total + len(block) > max_chars:
                break
            blocks.append(block)
            included.append(path)
            total += len(block)

        context = (
            "REPOSITORY FILE TREE:\n"
            + "\n".join(files[:200])
            + "\n\nSELECTED FILE CONTENTS:\n"
            + "".join(blocks)
        )
        return RepositorySnapshot(context=context, files=included)
