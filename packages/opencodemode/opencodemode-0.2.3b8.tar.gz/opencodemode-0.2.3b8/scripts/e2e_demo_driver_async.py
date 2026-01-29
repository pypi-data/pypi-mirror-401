"""
Demo driver that tests ASYNC tools via the executor sidecar.

Tests ASYNC tools with matched proxy pattern (await required for async tools).

Prereqs:
- Sidecar running at localhost:8001 with CODEMODE_API_KEY set
- ToolService (ASYNC) running (see scripts/e2e_demo_toolservice_async.py) on localhost:50051

Run:
  CODEMODE_API_KEY=dev-secret-key uv run python scripts/e2e_demo_driver_async.py
"""

import ast
import os

from codemode.core.context import RuntimeContext
from codemode.core.executor_client import ExecutorClient


def main() -> None:
    api_key = os.environ.get("CODEMODE_API_KEY", "dev-secret-key")

    # Load TLS config from environment variables
    tls_config = None
    if os.environ.get("CODEMODE_GRPC_TLS_ENABLED", "false").lower() == "true":
        from codemode.config.models import GrpcTlsConfig

        tls_config = GrpcTlsConfig(
            enabled=True,
            mode=os.environ.get("CODEMODE_GRPC_TLS_MODE", "system"),
            cert_file=os.environ.get("CODEMODE_GRPC_TLS_CERT_FILE"),
            key_file=os.environ.get("CODEMODE_GRPC_TLS_KEY_FILE"),
            ca_file=os.environ.get("CODEMODE_GRPC_TLS_CA_FILE"),
            client_cert_file=os.environ.get("CODEMODE_GRPC_TLS_CLIENT_CERT_FILE"),
            client_key_file=os.environ.get("CODEMODE_GRPC_TLS_CLIENT_KEY_FILE"),
        )
        print(f"🔒 ExecutorClient using TLS (mode: {tls_config.mode})")

    client = ExecutorClient(
        executor_url="http://localhost:8001", api_key=api_key, timeout=30, tls_config=tls_config
    )

    def parse_result(res):
        try:
            return ast.literal_eval(res.result)
        except Exception:
            return {}

    def dump(label, res):
        print(f"{label} success:", res.success)
        print(f"{label} result:", res.result)
        if res.error:
            print(f"{label} error:", res.error)
        if res.stderr:
            print(f"{label} stderr:", res.stderr)
        if res.stdout:
            print(f"{label} stdout:", res.stdout)

    # --- Test 1: Basic async weather + database (await required!) ---
    print("\n--- Test 1: Basic async weather + database (await required) ---")
    code_1 = """
import asyncio

async def main():
    # Async tools - must use await
    weather = await tools['weather_async'].run(location='Berlin')
    db = await tools['database_async'].run(query='SELECT 1')
    return {'weather': weather, 'db': db}

result = asyncio.run(main())
"""

    res_1 = client.execute(
        code=code_1,
        available_tools=["weather_async", "database_async"],
        config={},
        execution_timeout=20,
    )

    dump("Test 1", res_1)
    assert res_1.success, f"Test 1 failed: {res_1.error}"

    # --- Test 2: Sequential async context-aware sleep (~10s) ---
    print("\n--- Test 2: Sequential async context-aware sleep (~10s) ---")
    code_2 = """
import asyncio
import time

async def main():
    start = time.perf_counter()
    # Async context-aware tool - must use await
    a = await tools['sleep_ctx_async'].run_with_context(context, value='A')
    b = await tools['sleep_ctx_async'].run_with_context(context, value='B')
    elapsed = round(time.perf_counter() - start, 2)
    return {'elapsed': elapsed, 'values': [a, b]}

result = asyncio.run(main())
"""

    seq_ctx = RuntimeContext(variables={"request_id": "seq-async-demo"})
    res_2 = client.execute(
        code=code_2,
        available_tools=["sleep_ctx_async"],
        config={},
        execution_timeout=30,
        context=seq_ctx,
    )
    data_2 = parse_result(res_2)
    dump("Test 2", res_2)
    print("Test 2 elapsed:", data_2.get("elapsed"))
    assert res_2.success, f"Test 2 failed: {res_2.error}"
    assert data_2.get("elapsed", 0) >= 9.5, f"Expected ~10s, got {data_2.get('elapsed')}"

    # --- Test 3: Parallel async with asyncio.gather (~5s) ---
    print("\n--- Test 3: Parallel async with asyncio.gather (~5s) ---")
    code_3 = """
import asyncio
import time

async def main():
    start = time.perf_counter()
    # Async tools can run in parallel using asyncio.gather
    vals = await asyncio.gather(
        tools['sleep_ctx_async'].run_with_context(context, value='A'),
        tools['sleep_ctx_async'].run_with_context(context, value='B')
    )
    elapsed = round(time.perf_counter() - start, 2)
    return {'elapsed': elapsed, 'values': vals}

result = asyncio.run(main())
"""

    conc_ctx = RuntimeContext(variables={"request_id": "conc-async-demo"})
    res_3 = client.execute(
        code=code_3,
        available_tools=["sleep_ctx_async"],
        config={},
        execution_timeout=30,
        context=conc_ctx,
    )
    data_3 = parse_result(res_3)
    dump("Test 3", res_3)
    print("Test 3 elapsed:", data_3.get("elapsed"))
    assert res_3.success, f"Test 3 failed: {res_3.error}"
    # Expect ~5s if both tool calls truly run in parallel
    assert 4.0 <= data_3.get("elapsed", 99) <= 7.0, f"Expected ~5s, got {data_3.get('elapsed')}"

    client.close()
    print("\n✓ All ASYNC tests passed!")


if __name__ == "__main__":
    main()
