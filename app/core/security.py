from pathlib import Path

BLOCKED_NAMES = {".env", ".env.local", "id_rsa", "id_ed25519", "credentials.json", "secrets.json"}
ALLOWED_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs", ".cs", ".cpp", ".c", ".h", ".md", ".txt", ".toml", ".yaml", ".yml", ".json", ".sql", ".html", ".css", ".sh"}

def safe_resolve(root: Path, requested: str | Path) -> Path:
    root = root.resolve()
    candidate = Path(requested)
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = candidate.resolve()
    if candidate != root and root not in candidate.parents:
        raise PermissionError("Requested path is outside the allowed workspace.")
    return candidate

def is_safe_text_file(path: Path) -> bool:
    return path.name not in BLOCKED_NAMES and path.suffix.lower() in ALLOWED_SUFFIXES
