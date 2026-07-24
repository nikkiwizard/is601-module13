from uuid import uuid4

import pytest
import requests
from playwright.sync_api import Page, expect


def create_test_user() -> dict:
    """Create unique valid user data for each test."""
    unique_id = uuid4().hex[:8]

    return {
        "username": f"playwright_{unique_id}",
        "email": f"playwright_{unique_id}@example.com",
        "first_name": "Playwright",
        "last_name": "Tester",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!",
    }

def register_user_through_api(base_url: str, user: dict) -> None:
    """Register a test user directly through the API."""
    response = requests.post(
        f"{base_url}/auth/register",
        json=user,
        timeout=10,
    )

    assert response.status_code == 201, response.text

@pytest.mark.e2e
def test_successful_registration(
    page: Page,
    fastapi_server: str,
):
    """A user can successfully register through the registration page."""
    base_url = fastapi_server.rstrip("/")
    user = create_test_user()

    page.goto(f"{base_url}/register")

    page.fill("#username", user["username"])
    page.fill("#email", user["email"])
    page.fill("#first_name", user["first_name"])
    page.fill("#last_name", user["last_name"])
    page.fill("#password", user["password"])
    page.fill("#confirm_password", user["confirm_password"])

    page.click("#registerButton")

    expect(page.locator("#successAlert")).to_be_visible()
    expect(page.locator("#successMessage")).to_contain_text(
        "Registration successful"
    )


@pytest.mark.e2e
def test_registration_rejects_short_password(
    page: Page,
    fastapi_server: str,
):
    """The registration page displays an error for a short password."""
    base_url = fastapi_server.rstrip("/")
    user = create_test_user()

    page.goto(f"{base_url}/register")

    page.fill("#username", user["username"])
    page.fill("#email", user["email"])
    page.fill("#first_name", user["first_name"])
    page.fill("#last_name", user["last_name"])
    page.fill("#password", "Short1!")
    page.fill("#confirm_password", "Short1!")

    page.click("#registerButton")

    expect(page.locator("#errorAlert")).to_be_visible()
    expect(page.locator("#errorMessage")).to_contain_text(
        "Password must be at least 8 characters"
    )


@pytest.mark.e2e
def test_successful_login_stores_token(
    page: Page,
    fastapi_server: str,
):
    """A registered user can log in and the JWT is stored locally."""
    base_url = fastapi_server.rstrip("/")
    user = create_test_user()

    register_user_through_api(base_url, user)
    page.goto(f"{base_url}/login")

    page.fill("#username", user["username"])
    page.fill("#password", user["password"])

    page.click("#loginButton")

    expect(page.locator("#successAlert")).to_be_visible()
    expect(page.locator("#successMessage")).to_contain_text(
        "Login successful"
    )

    access_token = page.evaluate(
        "() => localStorage.getItem('access_token')"
    )
    refresh_token = page.evaluate(
        "() => localStorage.getItem('refresh_token')"
    )

    assert access_token is not None
    assert len(access_token) > 0

    assert refresh_token is not None
    assert len(refresh_token) > 0


@pytest.mark.e2e
def test_login_rejects_wrong_password(
    page: Page,
    fastapi_server: str,
):
    """The login page displays an error when the password is incorrect."""
    base_url = fastapi_server.rstrip("/")
    user = create_test_user()

    register_user_through_api(base_url, user)
    page.goto(f"{base_url}/login")

    page.fill("#username", user["username"])
    page.fill("#password", "WrongPassword123!")

    page.click("#loginButton")

    expect(page.locator("#errorAlert")).to_be_visible()
    expect(page.locator("#errorMessage")).to_have_text(
        "Invalid username or password"
    )