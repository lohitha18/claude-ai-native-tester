from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

SCAN_ROOTS = (
    ROOT / "starter-repo/src",
    ROOT / "scripts",
    ROOT / "rag/knowledge",
    ROOT / "docs",
)


def repository_text():
    chunks = []
    for root in SCAN_ROOTS:
        for path in root.rglob("*"):
            if path.is_file():
                try:
                    chunks.append(path.read_text(encoding="utf-8"))
                except UnicodeDecodeError:
                    pass
    return "\n".join(chunks)


def test_no_openai_style_secret_is_committed():
    assert not re.search(r"\bsk-[A-Za-z0-9_-]{12,}", repository_text(), re.I)


def test_no_real_card_number_fixture_is_committed():
    assert not re.search(r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)", repository_text())


def test_api_keys_are_environment_based():
    workflow = (ROOT / ".github/workflows/quality.yml").read_text(encoding="utf-8")
    rag = (ROOT / "scripts/run_rag_eval.py").read_text(encoding="utf-8")
    assert "secrets.OPENAI_API_KEY" in workflow
    assert 'os.getenv("OPENAI_API_KEY")' in rag


def test_mcp_token_is_not_embedded():
    mcp = (ROOT / ".mcp.json").read_text(encoding="utf-8")
    assert '${GITHUB_PAT}' in mcp
    assert '"Authorization": "Bearer ${GITHUB_PAT}"' in mcp
    assert not re.search(r'Bearer\s+[A-Za-z0-9_-]{20,}', mcp)
