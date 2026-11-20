from fastapi.testclient import TestClient

from pm_hook.main import app
from pm_hook.api.routes import chat
from pm_hook.core.exceptions import AppError


client = TestClient(app)


def test_chat_endpoint_accepts_valid_message():
    response = client.post(
        "/api/chat/messages",
        json={
            "message": "Create a task for tomorrow"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "success": True,
        "message": "Create a task for tomorrow",
        "status": "received"
    }


def test_chat_endpoint_rejects_empty_message():
    response = client.post(
        "/api/chat/messages",
        json={
            "message": ""
        }
    )

    assert response.status_code == 422

    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_chat_endpoint_rejects_missing_message():
    response = client.post(
        "/api/chat/messages",
        json={}
    )

    assert response.status_code == 422


def test_unknown_endpoint_returns_404():
    response = client.get("/api/unknown")

    assert response.status_code == 404

    assert response.json()["error"]["code"] == "HTTP_ERROR"


def test_application_error_returns_expected_response(monkeypatch):

    def raise_project_error(message: str):
        raise AppError(
            message="Project not found",
            code="PROJECT_NOT_FOUND",
            status_code=404
        )

    monkeypatch.setattr(
        chat,
        "acknowledge_message",
        raise_project_error
    )

    response = client.post(
        "/api/chat/messages",
        json={
            "message": "Create a task"
        }
    )

    assert response.status_code == 404

    assert response.json()["error"]["code"] == "PROJECT_NOT_FOUND"
    assert response.json()["error"]["message"] == "Project not found"
    
    
def test_unexpected_error_returns_generic_500(monkeypatch):

    def raise_unexpected_error(message: str):
        raise RuntimeError("Internal database connection details")

    monkeypatch.setattr(
        chat,
        "acknowledge_message",
        raise_unexpected_error
    )

    safe_client = TestClient(
        app,
        raise_server_exceptions=False
    )

    response = safe_client.post(
        "/api/chat/messages",
        json={
            "message": "Create a task"
        }
    )

    assert response.status_code == 500

    assert response.json() == {
        "success": False,
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred"
        },
        "details": None
    }