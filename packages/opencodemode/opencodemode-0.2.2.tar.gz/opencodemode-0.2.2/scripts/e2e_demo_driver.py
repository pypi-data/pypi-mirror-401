"""
Demo driver that sends code to the executor sidecar via gRPC ExecutorService.

Tests SYNC tools with matched proxy pattern (no await needed for sync tools).

Prereqs:
- Sidecar running at localhost:8001 with CODEMODE_API_KEY set
- ToolService running (see scripts/e2e_demo_toolservice.py) on localhost:50051

Run:
  CODEMODE_API_KEY=dev-secret-key uv run python scripts/e2e_demo_driver.py
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

    # --- Test 1: Basic sync weather + database (NO await!) ---
    print("\n--- Test 1: Basic sync weather + database (no await) ---")
    code = """
# Sync tools - call directly without await
weather = tools['weather'].run(location='Berlin')
db = tools['database'].run(query='SELECT 1')
result = {'weather': weather, 'db': db}
"""

    res = client.execute(
        code=code,
        available_tools=["weather", "database"],
        config={},
        execution_timeout=20,
    )

    dump("Test 1", res)
    assert res.success, f"Test 1 failed: {res.error}"

    # --- Test 2: Sequential sync context-aware sleep (~10s) ---
    print("\n--- Test 2: Sequential sync context-aware sleep (~10s) ---")
    code_seq = """
import time

start = time.perf_counter()
# Sync context-aware tool - call directly without await
a = tools['sleep_ctx'].run_with_context(context, value='A')
b = tools['sleep_ctx'].run_with_context(context, value='B')
elapsed = round(time.perf_counter() - start, 2)
result = {'elapsed': elapsed, 'values': [a, b]}
"""

    seq_ctx = RuntimeContext(variables={"request_id": "seq-demo"})
    res_seq = client.execute(
        code=code_seq,
        available_tools=["sleep_ctx"],
        config={},
        execution_timeout=30,
        context=seq_ctx,
    )
    data_seq = parse_result(res_seq)
    dump("Test 2", res_seq)
    print("Test 2 elapsed:", data_seq.get("elapsed"))
    assert res_seq.success, f"Test 2 failed: {res_seq.error}"
    assert data_seq.get("elapsed", 0) >= 9.5, f"Expected ~10s, got {data_seq.get('elapsed')}"
    assert len(data_seq.get("values", [])) == 2

    # --- Test 3: Parallel sync with ThreadPoolExecutor (~5s) ---
    print("\n--- Test 3: Parallel sync with ThreadPoolExecutor (~5s) ---")
    code_conc = """
import time
from concurrent.futures import ThreadPoolExecutor

start = time.perf_counter()

# Sync tools can run in parallel using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=2) as ex:
    f1 = ex.submit(tools['sleep_ctx'].run_with_context, context, value='A')
    f2 = ex.submit(tools['sleep_ctx'].run_with_context, context, value='B')
    vals = [f1.result(), f2.result()]

elapsed = round(time.perf_counter() - start, 2)
result = {'elapsed': elapsed, 'values': vals}
"""

    conc_ctx = RuntimeContext(variables={"request_id": "conc-demo"})
    res_conc = client.execute(
        code=code_conc,
        available_tools=["sleep_ctx"],
        config={},
        execution_timeout=30,
        context=conc_ctx,
    )
    data_conc = parse_result(res_conc)
    dump("Test 3", res_conc)
    print("Test 3 elapsed:", data_conc.get("elapsed"))
    assert res_conc.success, f"Test 3 failed: {res_conc.error}"
    # Expect ~5s if both tool calls truly run in parallel
    assert (
        4.0 <= data_conc.get("elapsed", 99) <= 7.0
    ), f"Expected ~5s, got {data_conc.get('elapsed')}"
    assert len(data_conc.get("values", [])) == 2

    client.close()
    print("\n✓ All SYNC tests passed!")


if __name__ == "__main__":
    main()
