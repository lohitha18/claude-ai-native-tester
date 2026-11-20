from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JAVA_ROOT = ROOT / "starter-repo/src/main/java"


def test_no_http_routes_exist():
    java_files = list(JAVA_ROOT.rglob("*.java"))
    joined = "\n".join(path.read_text(encoding="utf-8") for path in java_files)
    assert "HttpServer" not in joined
    assert "@RestController" not in joined
    assert "@GetMapping" not in joined
    assert "@PostMapping" not in joined


def test_no_payment_endpoint_exists():
    java_files = list(JAVA_ROOT.rglob("*.java"))
    joined = "\n".join(path.read_text(encoding="utf-8") for path in java_files)
    assert "PaymentController" not in joined
    assert "PaymentEndpoint" not in joined
    assert "processPayment" not in joined
    assert "@PostMapping" not in joined


def test_no_port_is_configured():
    java_files = list(JAVA_ROOT.rglob("*.java"))
    joined = "\n".join(path.read_text(encoding="utf-8") for path in java_files)
    assert "server.port" not in joined


def test_login_api_contract_is_not_implied():
    pom = (ROOT / "starter-repo/pom.xml").read_text(encoding="utf-8")
    assert "spring" not in pom.lower()
    assert "spark" not in pom.lower()
