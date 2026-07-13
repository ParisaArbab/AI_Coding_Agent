from pathlib import Path
from app.core.config import Settings
from app.services.repository_service import RepositoryService

def test_snapshot(tmp_path: Path):
    repo=tmp_path/"demo"; repo.mkdir()
    (repo/"app.py").write_text("def hello():\n    return 'hello'\n")
    (repo/"README.md").write_text("# Demo")
    service=RepositoryService(Settings(workspace_root=tmp_path))
    snap=service.snapshot("demo", "Explain hello")
    assert "app.py" in snap.context
    assert snap.files
