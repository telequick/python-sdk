import pytest
import os
import json
from telequick.client import TeleQuickClient
from telequick.method_id import MethodID


@pytest.fixture
def dummy_service_account(tmp_path):
    sa_path = tmp_path / "dummy_sa.json"
    dummy_data = {
        "client_email": "test@telequick.local",
        "private_key": "---mock-private-key---",
        "private_key_id": "test-key",
    }
    with open(sa_path, "w") as f:
        json.dump(dummy_data, f)
    return str(sa_path)


def test_method_ids_mapped_correctly():
    assert MethodID.ORIGINATE == 1430677891
    assert MethodID.ORIGINATE_BULK == 721069100
    assert MethodID.TERMINATE == 3834253405
    assert MethodID.AUDIO_FRAME == 2991054320
    assert MethodID.STREAM_EVENTS == 959835745


def test_method_ids_are_unique():
    ids = [
        MethodID.ORIGINATE,
        MethodID.ORIGINATE_BULK,
        MethodID.ABORT_BULK,
        MethodID.TERMINATE,
        MethodID.STREAM_EVENTS,
        MethodID.BARGE,
        MethodID.AUDIO_FRAME,
    ]
    assert len(set(ids)) == len(ids)


def test_client_init(dummy_service_account):
    try:
        client = TeleQuickClient("quic://127.0.0.1:9090", dummy_service_account)
    except (FileNotFoundError, OSError):
        pytest.skip("Skipping initialization due to missing core library")
    assert client.endpoint == "quic://127.0.0.1:9090"
    assert client.tenant_id == "test@telequick.local"
    assert client.client_id
    assert client.on_audio_frame is None
    assert client.on_call_event is None


def test_client_init_missing_credentials(tmp_path):
    missing = tmp_path / "does-not-exist.json"
    with pytest.raises(FileNotFoundError):
        TeleQuickClient("quic://127.0.0.1:9090", str(missing))
