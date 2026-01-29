.PHONY: help test tests format lint docker-build toolservice toolservice-async sidecar driver driver-async e2e e2e-sync e2e-async e2e-tls clean-e2e clean generate-certs proto

# Configurable knobs
IMAGE_NAME ?= codemode-executor
EXECUTOR_TAG ?= 0.1.0
API_KEY ?= dev-secret-key
# Target for the main app ToolService that the executor sidecar calls
MAIN_APP_TARGET ?= host.docker.internal:50051
LOG_LEVEL ?= INFO

help:
	@echo "Make targets:"
	@echo "  test / tests      Run pytest test suite"
	@echo "  format            Format code with black and isort"
	@echo "  lint              Lint code with ruff"
	@echo "  proto             Regenerate proto files from codemode.proto"
	@echo "  clean             Clean up pycache, coverage, tmp files, and logs"
	@echo "  generate-certs    Generate self-signed test certificates for TLS"
	@echo "  docker-build      Build the executor sidecar image"
	@echo "  toolservice       Run the gRPC ToolService with SYNC tools (blocking)"
	@echo "  toolservice-async Run the gRPC ToolService with ASYNC tools (blocking)"
	@echo "  sidecar           Run the executor sidecar container (blocking)"
	@echo "  driver            Run the demo driver with SYNC tools"
	@echo "  driver-async      Run the demo driver with ASYNC tools"
	@echo "  e2e               Build image and run BOTH sync and async test suites"
	@echo "  e2e-sync          Build image and run SYNC test suite only"
	@echo "  e2e-async         Build image and run ASYNC test suite only"
	@echo "  e2e-tls           Build image and run BOTH sync and async with TLS enabled"
	@echo "  clean-e2e         Stop stray processes/containers from the e2e target"

test:
	@echo "Running pytest..."
	uv run pytest tests/ -v

tests: test

format:
	@echo "Formatting code with black..."
	uv run black codemode/ tests/ scripts/ examples/
	@echo "Sorting imports with isort..."
	uv run isort codemode/ tests/ scripts/ examples/
	@echo "✓ Code formatted"

lint:
	@echo "Linting code with ruff..."
	uv run ruff check codemode/ tests/ scripts/ examples/
	@echo "✓ Linting complete"

proto:
	@echo "Regenerating proto files..."
	uv run python -m grpc_tools.protoc \
		-Icodemode/protos \
		--python_out=codemode/protos \
		--grpc_python_out=codemode/protos \
		codemode/protos/codemode.proto
	@echo "✓ Proto files regenerated"

clean:
	@echo "Cleaning up Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaning up pytest cache..."
	rm -rf .pytest_cache
	@echo "Cleaning up coverage files..."
	rm -rf htmlcov
	rm -f .coverage
	rm -f coverage.xml
	@echo "Cleaning up build artifacts..."
	rm -rf build dist
	@echo "Cleaning up temporary files..."
	rm -f /tmp/codemode_toolservice*.log
	rm -f /tmp/codemode_toolservice.pid
	find . -type f -name "*.log" -path "*/tmp/*" -delete 2>/dev/null || true
	@echo "Cleaning up mypy cache..."
	rm -rf .mypy_cache
	@echo "Cleaning up ruff cache..."
	rm -rf .ruff_cache
	@echo "✓ Clean complete"

docker-build:
	docker build -t $(IMAGE_NAME):$(EXECUTOR_TAG) -f docker_sidecar/Dockerfile .

toolservice:
	CODEMODE_API_KEY=$(API_KEY) LOG_LEVEL=$(LOG_LEVEL) uv run python scripts/e2e_demo_toolservice.py

toolservice-async:
	CODEMODE_API_KEY=$(API_KEY) LOG_LEVEL=$(LOG_LEVEL) uv run python scripts/e2e_demo_toolservice_async.py

sidecar:
	docker run --rm --name $(IMAGE_NAME)-e2e -p 8001:8001 \
	  -e CODEMODE_API_KEY=$(API_KEY) \
	  -e MAIN_APP_GRPC_TARGET=$(MAIN_APP_TARGET) \
	  $(IMAGE_NAME):$(EXECUTOR_TAG)

driver:
	CODEMODE_API_KEY=$(API_KEY) LOG_LEVEL=$(LOG_LEVEL) uv run python scripts/e2e_demo_driver.py

driver-async:
	CODEMODE_API_KEY=$(API_KEY) LOG_LEVEL=$(LOG_LEVEL) uv run python scripts/e2e_demo_driver_async.py

e2e-sync: docker-build
	@set -e; \
	  echo "========================================"; \
	  echo "SYNC TOOLS E2E TEST SUITE"; \
	  echo "========================================"; \
	  START_TIME=$$(date +%s); \
	  echo "Ensuring no previous sidecar is running..."; \
	  docker stop $(IMAGE_NAME)-e2e >/dev/null 2>&1 || true; \
	  if [ -f /tmp/codemode_toolservice.pid ]; then \
	    echo "Stopping previous ToolService from pid file..."; \
	    kill $$(cat /tmp/codemode_toolservice.pid) >/dev/null 2>&1 || true; \
	    rm -f /tmp/codemode_toolservice.pid; \
	  fi; \
	  if lsof -ti :50051 >/dev/null 2>&1; then \
	    echo "Port 50051 in use, stopping existing listener..."; \
	    kill $$(lsof -ti :50051) >/dev/null 2>&1 || true; \
	  fi; \
	  echo "Starting SYNC ToolService..."; \
	  CODEMODE_API_KEY=$(API_KEY) LOG_LEVEL=$(LOG_LEVEL) uv run python scripts/e2e_demo_toolservice.py > /tmp/codemode_toolservice_sync.log 2>&1 & \
	  TOOL_PID=$$!; \
	  echo $$TOOL_PID > /tmp/codemode_toolservice.pid; \
	  echo "ToolService pid $$TOOL_PID (log: /tmp/codemode_toolservice_sync.log)"; \
	  cleanup() { \
	    echo "Stopping executor sidecar..."; \
	    docker stop $(IMAGE_NAME)-e2e >/dev/null 2>&1 || true; \
	    echo "Stopping ToolService..."; \
	    kill $$TOOL_PID >/dev/null 2>&1 || true; \
	    wait $$TOOL_PID 2>/dev/null || true; \
	  }; \
	  trap cleanup EXIT; \
	  sleep 2; \
	  echo "Starting executor sidecar container..."; \
	  docker run --rm --name $(IMAGE_NAME)-e2e -d -p 8001:8001 \
	    -e CODEMODE_API_KEY=$(API_KEY) \
	    -e MAIN_APP_GRPC_TARGET=$(MAIN_APP_TARGET) \
	    $(IMAGE_NAME):$(EXECUTOR_TAG); \
	  echo "Waiting for executor sidecar on localhost:8001..."; \
	  for i in $$(seq 1 20); do \
	    if python -c "import socket,sys; s=socket.socket(); \
try: s.connect((\"localhost\",8001)); sys.exit(0) \
except Exception: sys.exit(1) \
finally: s.close()" >/dev/null 2>&1; then \
	      echo "Executor sidecar is up."; break; \
	    fi; \
	    sleep 1; \
	  done; \
	  echo "Running SYNC driver..."; \
	  CODEMODE_API_KEY=$(API_KEY) LOG_LEVEL=$(LOG_LEVEL) uv run python scripts/e2e_demo_driver.py; \
	  STATUS=$$?; \
	  END_TIME=$$(date +%s); \
	  ELAPSED=$$((END_TIME - START_TIME)); \
	  echo ""; \
	  echo "========================================"; \
	  if [ $$STATUS -eq 0 ]; then \
	    echo "✓ SYNC E2E TESTS PASSED ($$ELAPSED seconds)"; \
	  else \
	    echo "✗ SYNC E2E TESTS FAILED ($$ELAPSED seconds)"; \
	  fi; \
	  echo "========================================"; \
	  exit $$STATUS

e2e-async: docker-build
	@set -e; \
	  echo "========================================"; \
	  echo "ASYNC TOOLS E2E TEST SUITE"; \
	  echo "========================================"; \
	  START_TIME=$$(date +%s); \
	  echo "Ensuring no previous sidecar is running..."; \
	  docker stop $(IMAGE_NAME)-e2e >/dev/null 2>&1 || true; \
	  if [ -f /tmp/codemode_toolservice.pid ]; then \
	    echo "Stopping previous ToolService from pid file..."; \
	    kill $$(cat /tmp/codemode_toolservice.pid) >/dev/null 2>&1 || true; \
	    rm -f /tmp/codemode_toolservice.pid; \
	  fi; \
	  if lsof -ti :50051 >/dev/null 2>&1; then \
	    echo "Port 50051 in use, stopping existing listener..."; \
	    kill $$(lsof -ti :50051) >/dev/null 2>&1 || true; \
	  fi; \
	  echo "Starting ASYNC ToolService..."; \
	  CODEMODE_API_KEY=$(API_KEY) LOG_LEVEL=$(LOG_LEVEL) uv run python scripts/e2e_demo_toolservice_async.py > /tmp/codemode_toolservice_async.log 2>&1 & \
	  TOOL_PID=$$!; \
	  echo $$TOOL_PID > /tmp/codemode_toolservice.pid; \
	  echo "ToolService pid $$TOOL_PID (log: /tmp/codemode_toolservice_async.log)"; \
	  cleanup() { \
	    echo "Stopping executor sidecar..."; \
	    docker stop $(IMAGE_NAME)-e2e >/dev/null 2>&1 || true; \
	    echo "Stopping ToolService..."; \
	    kill $$TOOL_PID >/dev/null 2>&1 || true; \
	    wait $$TOOL_PID 2>/dev/null || true; \
	  }; \
	  trap cleanup EXIT; \
	  sleep 2; \
	  echo "Starting executor sidecar container..."; \
	  docker run --rm --name $(IMAGE_NAME)-e2e -d -p 8001:8001 \
	    -e CODEMODE_API_KEY=$(API_KEY) \
	    -e MAIN_APP_GRPC_TARGET=$(MAIN_APP_TARGET) \
	    $(IMAGE_NAME):$(EXECUTOR_TAG); \
	  echo "Waiting for executor sidecar on localhost:8001..."; \
	  for i in $$(seq 1 20); do \
	    if python -c "import socket,sys; s=socket.socket(); \
try: s.connect((\"localhost\",8001)); sys.exit(0) \
except Exception: sys.exit(1) \
finally: s.close()" >/dev/null 2>&1; then \
	      echo "Executor sidecar is up."; break; \
	    fi; \
	    sleep 1; \
	  done; \
	  echo "Running ASYNC driver..."; \
	  CODEMODE_API_KEY=$(API_KEY) LOG_LEVEL=$(LOG_LEVEL) uv run python scripts/e2e_demo_driver_async.py; \
	  STATUS=$$?; \
	  END_TIME=$$(date +%s); \
	  ELAPSED=$$((END_TIME - START_TIME)); \
	  echo ""; \
	  echo "========================================"; \
	  if [ $$STATUS -eq 0 ]; then \
	    echo "✓ ASYNC E2E TESTS PASSED ($$ELAPSED seconds)"; \
	  else \
	    echo "✗ ASYNC E2E TESTS FAILED ($$ELAPSED seconds)"; \
	  fi; \
	  echo "========================================"; \
	  exit $$STATUS

e2e: docker-build
	@OVERALL_START=$$(date +%s); \
	  echo ""; \
	  echo "========================================"; \
	  echo "RUNNING ALL E2E TEST SUITES"; \
	  echo "========================================"; \
	  echo ""; \
	  SYNC_STATUS=0; \
	  ASYNC_STATUS=0; \
	  $(MAKE) e2e-sync || SYNC_STATUS=$$?; \
	  echo ""; \
	  sleep 2; \
	  $(MAKE) e2e-async || ASYNC_STATUS=$$?; \
	  echo ""; \
	  OVERALL_END=$$(date +%s); \
	  OVERALL_ELAPSED=$$((OVERALL_END - OVERALL_START)); \
	  echo "========================================"; \
	  echo "E2E TEST RESULTS SUMMARY"; \
	  echo "========================================"; \
	  if [ $$SYNC_STATUS -eq 0 ]; then \
	    echo "✓ SYNC tests:  PASSED"; \
	  else \
	    echo "✗ SYNC tests:  FAILED"; \
	  fi; \
	  if [ $$ASYNC_STATUS -eq 0 ]; then \
	    echo "✓ ASYNC tests: PASSED"; \
	  else \
	    echo "✗ ASYNC tests: FAILED"; \
	  fi; \
	  echo "Total time: $$OVERALL_ELAPSED seconds"; \
	  echo "========================================"; \
	  if [ $$SYNC_STATUS -eq 0 ] && [ $$ASYNC_STATUS -eq 0 ]; then \
	    echo "✓ ALL E2E TESTS PASSED"; \
	    exit 0; \
	  else \
	    echo "✗ SOME E2E TESTS FAILED"; \
	    exit 1; \
	  fi

clean-e2e:
	docker stop $(IMAGE_NAME)-e2e >/dev/null 2>&1 || true
	rm -f /tmp/codemode_toolservice_sync.log /tmp/codemode_toolservice_async.log /tmp/codemode_toolservice.pid

generate-certs:
	@bash scripts/generate_test_certs.sh

e2e-tls: docker-build
	@if [ ! -f test_certs/ca.crt ]; then \
		echo "Generating test certificates..."; \
		$(MAKE) generate-certs; \
	fi; \
	OVERALL_START=$$(date +%s); \
	echo ""; \
	echo "========================================"; \
	echo "RUNNING E2E TESTS WITH TLS ENABLED"; \
	echo "========================================"; \
	echo ""; \
	SYNC_STATUS=0; \
	ASYNC_STATUS=0; \
	echo "Testing SYNC with TLS..."; \
	set -e; \
	echo "Ensuring no previous sidecar is running..."; \
	docker stop $(IMAGE_NAME)-e2e >/dev/null 2>&1 || true; \
	if [ -f /tmp/codemode_toolservice.pid ]; then \
		kill $$(cat /tmp/codemode_toolservice.pid) >/dev/null 2>&1 || true; \
		rm -f /tmp/codemode_toolservice.pid; \
	fi; \
	if lsof -ti :50051 >/dev/null 2>&1; then \
		kill $$(lsof -ti :50051) >/dev/null 2>&1 || true; \
	fi; \
	echo "Starting SYNC ToolService with TLS..."; \
	CODEMODE_API_KEY=$(API_KEY) \
	CODEMODE_GRPC_TLS_ENABLED=true \
	CODEMODE_GRPC_TLS_MODE=custom \
	CODEMODE_GRPC_TLS_CERT_FILE=./test_certs/server.crt \
	CODEMODE_GRPC_TLS_KEY_FILE=./test_certs/server.key \
	CODEMODE_GRPC_TLS_CA_FILE=./test_certs/ca.crt \
	LOG_LEVEL=$(LOG_LEVEL) \
	uv run python scripts/e2e_demo_toolservice.py > /tmp/codemode_toolservice_tls_sync.log 2>&1 & \
	TOOL_PID=$$!; \
	echo $$TOOL_PID > /tmp/codemode_toolservice.pid; \
	echo "ToolService pid $$TOOL_PID (TLS enabled, log: /tmp/codemode_toolservice_tls_sync.log)"; \
	cleanup() { \
		echo "Stopping executor sidecar..."; \
		docker stop $(IMAGE_NAME)-e2e >/dev/null 2>&1 || true; \
		echo "Stopping ToolService..."; \
		kill $$TOOL_PID >/dev/null 2>&1 || true; \
		wait $$TOOL_PID 2>/dev/null || true; \
	}; \
	trap cleanup EXIT; \
	sleep 2; \
	echo "Starting executor sidecar with TLS..."; \
	docker run --rm --name $(IMAGE_NAME)-e2e -d -p 8001:8001 \
		-e CODEMODE_API_KEY=$(API_KEY) \
		-e MAIN_APP_GRPC_TARGET=$(MAIN_APP_TARGET) \
		-e CODEMODE_GRPC_TLS_ENABLED=true \
		-e CODEMODE_GRPC_TLS_MODE=custom \
		-e CODEMODE_GRPC_TLS_CERT_FILE=/certs/server.crt \
		-e CODEMODE_GRPC_TLS_KEY_FILE=/certs/server.key \
		-e CODEMODE_GRPC_TLS_CA_FILE=/certs/ca.crt \
		-e CODEMODE_GRPC_TLS_CLIENT_CERT_FILE=/certs/client.crt \
		-e CODEMODE_GRPC_TLS_CLIENT_KEY_FILE=/certs/client.key \
		-v $$(pwd)/test_certs:/certs:ro \
		$(IMAGE_NAME):$(EXECUTOR_TAG); \
	echo "Waiting for executor sidecar..."; \
	for i in $$(seq 1 20); do \
		if python3 -c "import socket,sys; s=socket.socket(); \
try: s.connect(('localhost',8001)); sys.exit(0) \
except Exception: sys.exit(1) \
finally: s.close()" >/dev/null 2>&1; then \
			echo "Executor sidecar is up."; break; \
		fi; \
		sleep 1; \
	done; \
	echo "Running SYNC driver with TLS..."; \
	CODEMODE_API_KEY=$(API_KEY) \
	CODEMODE_GRPC_TLS_ENABLED=true \
	CODEMODE_GRPC_TLS_MODE=custom \
	CODEMODE_GRPC_TLS_CA_FILE=./test_certs/ca.crt \
	CODEMODE_GRPC_TLS_CLIENT_CERT_FILE=./test_certs/client.crt \
	CODEMODE_GRPC_TLS_CLIENT_KEY_FILE=./test_certs/client.key \
	LOG_LEVEL=$(LOG_LEVEL) \
	uv run python scripts/e2e_demo_driver.py || SYNC_STATUS=$$?; \
	cleanup; \
	trap - EXIT; \
	sleep 2; \
	echo ""; \
	echo "Testing ASYNC with TLS..."; \
	set -e; \
	docker stop $(IMAGE_NAME)-e2e >/dev/null 2>&1 || true; \
	if [ -f /tmp/codemode_toolservice.pid ]; then \
		kill $$(cat /tmp/codemode_toolservice.pid) >/dev/null 2>&1 || true; \
		rm -f /tmp/codemode_toolservice.pid; \
	fi; \
	if lsof -ti :50051 >/dev/null 2>&1; then \
		kill $$(lsof -ti :50051) >/dev/null 2>&1 || true; \
	fi; \
	echo "Starting ASYNC ToolService with TLS..."; \
	CODEMODE_API_KEY=$(API_KEY) \
	CODEMODE_GRPC_TLS_ENABLED=true \
	CODEMODE_GRPC_TLS_MODE=custom \
	CODEMODE_GRPC_TLS_CERT_FILE=./test_certs/server.crt \
	CODEMODE_GRPC_TLS_KEY_FILE=./test_certs/server.key \
	CODEMODE_GRPC_TLS_CA_FILE=./test_certs/ca.crt \
	LOG_LEVEL=$(LOG_LEVEL) \
	uv run python scripts/e2e_demo_toolservice_async.py > /tmp/codemode_toolservice_tls_async.log 2>&1 & \
	TOOL_PID=$$!; \
	echo $$TOOL_PID > /tmp/codemode_toolservice.pid; \
	echo "ToolService pid $$TOOL_PID (TLS enabled, log: /tmp/codemode_toolservice_tls_async.log)"; \
	cleanup() { \
		echo "Stopping executor sidecar..."; \
		docker stop $(IMAGE_NAME)-e2e >/dev/null 2>&1 || true; \
		echo "Stopping ToolService..."; \
		kill $$TOOL_PID >/dev/null 2>&1 || true; \
		wait $$TOOL_PID 2>/dev/null || true; \
	}; \
	trap cleanup EXIT; \
	sleep 2; \
	echo "Starting executor sidecar with TLS..."; \
	docker run --rm --name $(IMAGE_NAME)-e2e -d -p 8001:8001 \
		-e CODEMODE_API_KEY=$(API_KEY) \
		-e MAIN_APP_GRPC_TARGET=$(MAIN_APP_TARGET) \
		-e CODEMODE_GRPC_TLS_ENABLED=true \
		-e CODEMODE_GRPC_TLS_MODE=custom \
		-e CODEMODE_GRPC_TLS_CERT_FILE=/certs/server.crt \
		-e CODEMODE_GRPC_TLS_KEY_FILE=/certs/server.key \
		-e CODEMODE_GRPC_TLS_CA_FILE=/certs/ca.crt \
		-e CODEMODE_GRPC_TLS_CLIENT_CERT_FILE=/certs/client.crt \
		-e CODEMODE_GRPC_TLS_CLIENT_KEY_FILE=/certs/client.key \
		-v $$(pwd)/test_certs:/certs:ro \
		$(IMAGE_NAME):$(EXECUTOR_TAG); \
	echo "Waiting for executor sidecar..."; \
	for i in $$(seq 1 20); do \
		if python3 -c "import socket,sys; s=socket.socket(); \
try: s.connect(('localhost',8001)); sys.exit(0) \
except Exception: sys.exit(1) \
finally: s.close()" >/dev/null 2>&1; then \
			echo "Executor sidecar is up."; break; \
		fi; \
		sleep 1; \
	done; \
	echo "Running ASYNC driver with TLS..."; \
	CODEMODE_API_KEY=$(API_KEY) \
	CODEMODE_GRPC_TLS_ENABLED=true \
	CODEMODE_GRPC_TLS_MODE=custom \
	CODEMODE_GRPC_TLS_CA_FILE=./test_certs/ca.crt \
	CODEMODE_GRPC_TLS_CLIENT_CERT_FILE=./test_certs/client.crt \
	CODEMODE_GRPC_TLS_CLIENT_KEY_FILE=./test_certs/client.key \
	LOG_LEVEL=$(LOG_LEVEL) \
	uv run python scripts/e2e_demo_driver_async.py || ASYNC_STATUS=$$?; \
	cleanup; \
	trap - EXIT; \
	OVERALL_END=$$(date +%s); \
	OVERALL_ELAPSED=$$((OVERALL_END - OVERALL_START)); \
	echo ""; \
	echo "========================================"; \
	echo "E2E TLS TEST RESULTS SUMMARY"; \
	echo "========================================"; \
	if [ $$SYNC_STATUS -eq 0 ]; then \
		echo "✓ SYNC with TLS:  PASSED"; \
	else \
		echo "✗ SYNC with TLS:  FAILED"; \
	fi; \
	if [ $$ASYNC_STATUS -eq 0 ]; then \
		echo "✓ ASYNC with TLS: PASSED"; \
	else \
		echo "✗ ASYNC with TLS: FAILED"; \
	fi; \
	echo "Total time: $$OVERALL_ELAPSED seconds"; \
	echo "========================================"; \
	if [ $$SYNC_STATUS -eq 0 ] && [ $$ASYNC_STATUS -eq 0 ]; then \
		echo "✓ ALL TLS E2E TESTS PASSED"; \
		echo "🔒 TLS encryption verified working!"; \
		exit 0; \
	else \
		echo "✗ SOME TLS E2E TESTS FAILED"; \
		exit 1; \
	fi
