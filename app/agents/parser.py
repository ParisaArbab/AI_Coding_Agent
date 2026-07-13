import re

def _section(text: str, start: str, end: str | None) -> str:
    match = re.search(rf"{start}:\s*", text, re.I)
    if not match: return ""
    content = text[match.end():]
    if end:
        end_match = re.search(rf"\n{end}:\s*", content, re.I)
        if end_match: content = content[:end_match.start()]
    return content.strip()

def parse_agent_output(text: str) -> dict[str, object]:
    summary = _section(text, "SUMMARY", "ANALYSIS")
    analysis = _section(text, "ANALYSIS", "PROPOSED_CHANGES")
    changes_text = _section(text, "PROPOSED_CHANGES", "PATCH")
    patch = _section(text, "PATCH", None)
    changes = [re.sub(r"^\s*[-*]\s*", "", line).strip() for line in changes_text.splitlines() if line.strip()]
    if patch.startswith("```") and patch.endswith("```"):
        patch = re.sub(r"^```(?:diff)?\s*", "", patch)
        patch = re.sub(r"\s*```$", "", patch)
    return {"summary": summary or "Analysis completed.", "analysis": analysis or text.strip(), "proposed_changes": changes, "patch": patch or None}
