import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import env
from core.exceptions import APIException, api_exception_handler
from routers import audio


class FakeResponse:
    def __init__(self, payload=None, headers=None, status_code=200):
        self._payload = payload or {}
        self.headers = headers or {}
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise audio.requests.HTTPError(f"{self.status_code} error")

    def json(self):
        return self._payload


@pytest.fixture(autouse=True)
def reset_env(monkeypatch):
    monkeypatch.setattr(env, "ASR_API_VERSION", "v1", raising=False)
    monkeypatch.setattr(env, "AUC_APP_ID", "v1-app")
    monkeypatch.setattr(env, "AUC_ACCESS_TOKEN", "v1-token")
    monkeypatch.setattr(env, "AUC_CLUSTER_ID", "v1-cluster")
    monkeypatch.setattr(env, "ASR_API_KEY", None, raising=False)
    monkeypatch.setattr(env, "ASR_RESOURCE_ID", "volc.bigasr.auc", raising=False)


@pytest.fixture
def client():
    app = FastAPI()
    app.add_exception_handler(APIException, api_exception_handler)
    app.include_router(audio.router, prefix="/api/v1")
    return TestClient(app)


def test_submit_transcription_defaults_to_v1(monkeypatch, client):
    calls = []
    monkeypatch.setattr(
        audio,
        "generate_download_url",
        lambda filename: f"https://storage.example/{filename}",
    )

    def fake_post(url, data=None, headers=None):
        calls.append({"url": url, "data": data, "headers": headers})
        return FakeResponse({"resp": {"message": "success", "id": "v1-task"}})

    monkeypatch.setattr(audio.requests, "post", fake_post)

    response = client.post(
        "/api/v1/audio/transcription-tasks",
        json={"filename": "audio.mp3"},
    )

    assert response.status_code == 200
    assert response.json()["data"] == {"task_id": "v1-task"}
    assert calls[0]["url"] == "https://openspeech.bytedance.com/api/v1/auc/submit"
    assert calls[0]["headers"] == {"Authorization": "Bearer; v1-token"}
    assert '"cluster": "v1-cluster"' in calls[0]["data"]


def test_submit_transcription_uses_v3_api_key(monkeypatch, client):
    calls = []
    monkeypatch.setattr(env, "ASR_API_VERSION", "v3", raising=False)
    monkeypatch.setattr(env, "ASR_API_KEY", "v3-api-key", raising=False)
    monkeypatch.setattr(env, "ASR_RESOURCE_ID", "volc.seedasr.auc", raising=False)
    monkeypatch.setattr(
        audio,
        "generate_download_url",
        lambda filename: f"https://storage.example/{filename}",
    )

    def fake_post(url, json=None, headers=None):
        calls.append({"url": url, "json": json, "headers": headers})
        return FakeResponse(
            payload={"message": "submitted"},
            headers={"X-Api-Task-Id": "v3-task"},
        )

    monkeypatch.setattr(audio.requests, "post", fake_post)

    response = client.post(
        "/api/v1/audio/transcription-tasks",
        json={"filename": "audio.mp3"},
    )

    assert response.status_code == 200
    assert response.json()["data"] == {"task_id": "v3-task"}
    assert calls[0]["url"] == (
        "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
    )
    assert calls[0]["headers"]["X-Api-Key"] == "v3-api-key"
    assert calls[0]["headers"]["X-Api-Resource-Id"] == "volc.seedasr.auc"
    assert calls[0]["json"]["audio"]["url"] == "https://storage.example/audio.mp3"


def test_query_transcription_uses_v3_finished_response(monkeypatch, client):
    monkeypatch.setattr(env, "ASR_API_VERSION", "v3", raising=False)
    monkeypatch.setattr(env, "ASR_API_KEY", "v3-api-key", raising=False)

    def fake_post(url, json=None, headers=None):
        assert url == "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"
        assert headers["X-Api-Task-Id"] == "v3-task"
        return FakeResponse(
            payload={
                "result": {
                    "utterances": [
                        {
                            "start_time": 0,
                            "end_time": 1200,
                            "text": "hello",
                        }
                    ]
                }
            },
            headers={"X-Api-Status-Code": "20000000"},
        )

    monkeypatch.setattr(audio.requests, "post", fake_post)

    response = client.get("/api/v1/audio/transcription-tasks/v3-task")

    assert response.status_code == 200
    assert response.json()["data"] == {
        "status": "finished",
        "result": [{"start_time": 0, "end_time": 1200, "text": "hello"}],
    }


def test_query_transcription_uses_v3_running_response(monkeypatch, client):
    monkeypatch.setattr(env, "ASR_API_VERSION", "v3", raising=False)
    monkeypatch.setattr(env, "ASR_API_KEY", "v3-api-key", raising=False)

    def fake_post(url, json=None, headers=None):
        return FakeResponse(headers={"X-Api-Status-Code": "20000001"})

    monkeypatch.setattr(audio.requests, "post", fake_post)

    response = client.get("/api/v1/audio/transcription-tasks/v3-task")

    assert response.status_code == 200
    assert response.json()["data"] == {"status": "running", "result": None}
