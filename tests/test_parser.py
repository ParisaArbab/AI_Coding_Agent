from app.agents.parser import parse_agent_output

def test_parse_agent_output():
    text="""SUMMARY:
Done.

ANALYSIS:
Focused.

PROPOSED_CHANGES:
- Change one
- Change two

PATCH:
```diff
--- a/file.py
+++ b/file.py
```
"""
    result=parse_agent_output(text)
    assert result["summary"]=="Done."
    assert result["proposed_changes"]==["Change one", "Change two"]
    assert "--- a/file.py" in result["patch"]
