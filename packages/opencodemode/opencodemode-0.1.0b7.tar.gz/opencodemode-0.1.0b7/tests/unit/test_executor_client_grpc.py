import grpc
import pytest

import codemode.core.executor_client as executor_client
from codemode.core.executor_client import (
    ExecutorClient,
    ExecutorClientError,
    ExecutorConnectionError,
    ExecutorTimeoutError,
)


class FakeChannel:
    def close(self):
        return None


class FakeResponse:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class FakeRpcError(grpc.RpcError):
    def __init__(self, code, details="err"):
        self._code = code
        self._details = details

    def code(self):
        return self._code

    def details(self):
        return self._details


class FakeStub:
    def __init__(self, *_args, **_kwargs):
        self.calls = []

    def Execute(self, request, timeout=None, metadata=None):
        self.calls.append((request, timeout, metadata))
        return FakeResponse(success=True, result="ok", stdout="", stderr="", error="")

    def Health(self, request, timeout=None):
        return FakeResponse(status="healthy")

    def Ready(self, request, timeout=None):
        return FakeResponse(status="ready")


class TimeoutStub(FakeStub):
    def Execute(self, request, timeout=None, metadata=None):
        raise FakeRpcError(grpc.StatusCode.DEADLINE_EXCEEDED)


class UnavailableStub(FakeStub):
    def Execute(self, request, timeout=None, metadata=None):
        raise FakeRpcError(grpc.StatusCode.UNAVAILABLE)


@pytest.fixture(autouse=True)
def patch_grpc(monkeypatch):
    # Use fake channel for all tests
    monkeypatch.setattr(
        executor_client.grpc, "insecure_channel", lambda *_args, **_kwargs: FakeChannel()
    )


def test_execute_success(monkeypatch):
    monkeypatch.setattr(executor_client.codemode_pb2_grpc, "ExecutorServiceStub", FakeStub)
    client = ExecutorClient("http://localhost:8001", "key", timeout=5)

    result = client.execute(code="print('hi')", available_tools=[], config={}, execution_timeout=10)

    assert result.success
    assert result.result == "ok"
    client.close()


def test_execute_timeout(monkeypatch):
    monkeypatch.setattr(executor_client.codemode_pb2_grpc, "ExecutorServiceStub", TimeoutStub)
    client = ExecutorClient("localhost:8001", "key", timeout=1)

    with pytest.raises(ExecutorTimeoutError):
        client.execute(code="sleep", available_tools=[], config={}, execution_timeout=1)


def test_execute_connection_error(monkeypatch):
    monkeypatch.setattr(executor_client.codemode_pb2_grpc, "ExecutorServiceStub", UnavailableStub)
    client = ExecutorClient("localhost:8001", "key", timeout=1)

    with pytest.raises(ExecutorConnectionError):
        client.execute(code="sleep", available_tools=[], config={}, execution_timeout=1)


def test_health_and_ready(monkeypatch):
    monkeypatch.setattr(executor_client.codemode_pb2_grpc, "ExecutorServiceStub", FakeStub)
    client = ExecutorClient("localhost:8001", "key", timeout=1)

    assert client.health_check() is True
    assert client.ready_check() is True


def test_generic_error(monkeypatch):
    class ErrorStub(FakeStub):
        def Execute(self, *_args, **_kwargs):
            raise FakeRpcError(grpc.StatusCode.INTERNAL, "boom")

    monkeypatch.setattr(executor_client.codemode_pb2_grpc, "ExecutorServiceStub", ErrorStub)
    client = ExecutorClient("localhost:8001", "key", timeout=1)

    with pytest.raises(ExecutorClientError):
        client.execute(code="x", available_tools=[], config={}, execution_timeout=1)
