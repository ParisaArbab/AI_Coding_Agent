from pathlib import Path
import pytest
from app.core.security import is_safe_text_file, safe_resolve

def test_safe_resolve_blocks_parent(tmp_path: Path):
    with pytest.raises(PermissionError): safe_resolve(tmp_path, "../secret.txt")

def test_file_filter():
    assert is_safe_text_file(Path("service.py"))
    assert not is_safe_text_file(Path(".env"))
    assert not is_safe_text_file(Path("image.png"))
