from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_user_repository_contains_only_synthetic_demo_account():
    source = (ROOT / "starter-repo/src/main/java/com/technova/payment/auth/UserRepository.java").read_text()
    assert 'users.put("demo.user"' in source
    assert "DemoPass123!" in source


def test_login_service_is_explicitly_unimplemented():
    source = (ROOT / "starter-repo/src/main/java/com/technova/payment/auth/LoginService.java").read_text()
    assert "throw new UnsupportedOperationException" in source


def test_login_service_does_not_claim_http_behavior():
    source = (ROOT / "starter-repo/src/main/java/com/technova/payment/auth/LoginService.java").read_text()
    assert "Http" not in source
    assert "Controller" not in source


def test_login_tests_are_not_treated_as_real_coverage():
    source = (ROOT / "starter-repo/src/test/java/com/technova/payment/auth/LoginServiceTest.java").read_text()
    assert "assertTrue(true)" in source


def test_main_is_console_only():
    source = (ROOT / "starter-repo/src/main/java/com/technova/payment/Main.java").read_text()
    assert "public static void main" in source
    assert "Login functionality is intentionally not implemented" in source


def test_placeholder_password_is_not_a_real_production_secret():
    source = (ROOT / "starter-repo/src/main/java/com/technova/payment/auth/User.java").read_text()
    assert "Starter-only model" in source
    assert "Do not use plain-text passwords" in source
