# Architecture Overview

Codemode is a secure code execution framework designed for multi-agent AI systems. It enables AI agents to safely execute dynamically generated Python code while maintaining access to registered tools and services.

## High-Level Architecture

```
+--------------------------------------------------+
|                   Main Application               |
|                                                  |
|  +------------------+    +-------------------+   |
|  |    Codemode      |    |  ComponentRegistry|   |
|  |    (Client)      |    |  - tools          |   |
|  +--------+---------+    |  - agents         |   |
|           |              |  - config         |   |
|           |              +--------+----------+   |
|           |                       |              |
|  +--------v---------+    +--------v----------+   |
|  |  ExecutorClient  |    |   ToolService     |   |
|  |  (gRPC Client)   |    |   (gRPC Server)   |   |
|  +--------+---------+    +--------+----------+   |
|           |                       ^              |
+-----------|-----------------------|--------------+
            |                       |
            | gRPC (TLS)            | gRPC (TLS)
            | Execute Request       | Tool Callbacks
            |                       |
+-----------v-----------------------|--------------+
|           Executor Sidecar (Docker Container)    |
|                                                  |
|  +------------------+    +-------------------+   |
|  | ExecutorService  |    |    CodeRunner     |   |
|  | (gRPC Server)    +--->|   (Subprocess)    |   |
|  +------------------+    +--------+----------+   |
|                                   |              |
|  +------------------+    +--------v----------+   |
|  |SecurityValidator |    |   Tool Proxies    |   |
|  | - blocked imports|    | (gRPC -> Main App)|   |
|  | - code limits    |    +-------------------+   |
|  +------------------+                            |
|                                                  |
+--------------------------------------------------+
```

## Two-Component Architecture

Codemode uses a **two-component architecture** that separates the main application from code execution:

### 1. Client (Main Application)

The client runs within your main application process and provides:

- **Codemode API**: High-level interface for code execution
- **ComponentRegistry**: Registration and management of tools, agents, and configuration
- **ExecutorClient**: gRPC client for communicating with the executor sidecar
- **ToolService**: gRPC server that handles tool invocation requests from the sidecar

### 2. Executor Sidecar (Docker Container)

The executor runs as an isolated Docker container and provides:

- **ExecutorService**: gRPC server that receives code execution requests
- **CodeRunner**: Executes code in sandboxed subprocess environments
- **SecurityValidator**: Validates code before execution
- **Tool Proxies**: gRPC clients that call back to the main application for tool access

## Communication Flow

The execution flow involves bidirectional communication between the client and sidecar:

```
1. Client sends Execute request to Sidecar
   Main App ----[ExecuteRequest]----> Executor Sidecar

2. Sidecar validates and executes code in subprocess
   SecurityValidator -> CodeRunner (subprocess)

3. Code calls tool proxy, which calls back to Main App
   Executor Sidecar ----[ToolCallRequest]----> Main App (ToolService)

4. Main App executes tool and returns result
   Main App ----[ToolCallResponse]----> Executor Sidecar

5. Sidecar returns execution result to Client
   Executor Sidecar ----[ExecuteResponse]----> Main App
```

### Request Lifecycle

1. **Code Submission**: The main application calls `codemode.execute(code)` with Python code
2. **gRPC Transport**: `ExecutorClient` sends the code to the sidecar via gRPC
3. **Security Validation**: `SecurityValidator` checks for blocked patterns and imports
4. **Code Wrapping**: `CodeRunner` wraps code with tool proxy infrastructure
5. **Subprocess Execution**: Code runs in an isolated Python subprocess
6. **Tool Callbacks**: When code calls `tools['name'].run()`, the proxy makes a gRPC call back to the main application's `ToolService`
7. **Tool Execution**: `ToolService` invokes the registered tool and returns results
8. **Result Collection**: `CodeRunner` captures stdout, stderr, and the `result` variable
9. **Response**: Results are returned to the main application via gRPC

## Why This Architecture

### Security Through Isolation

- **Process Isolation**: Code executes in a separate subprocess within the sidecar
- **Container Isolation**: The sidecar runs in a Docker container with restricted capabilities
- **Network Isolation**: The container can be configured with restricted network access
- **No Direct Access**: Executed code cannot directly access main application memory, filesystem, or credentials

### Controlled Tool Access

- **Explicit Registration**: Only registered tools are accessible from executed code
- **Callback Pattern**: Tools execute in the main application, not the sandbox
- **Authentication**: All gRPC communication uses API key authentication
- **Context Propagation**: Runtime context (user ID, session, etc.) is passed securely

### Operational Benefits

- **Independent Scaling**: The executor sidecar can be scaled independently
- **Resource Limits**: Container-level CPU, memory, and timeout limits
- **Crash Isolation**: Executor crashes do not affect the main application
- **Language Agnostic**: The main application can be any language that speaks gRPC

### Framework Agnostic

- **Multi-Framework Support**: Works with CrewAI, LangChain, LangGraph, and others
- **Standard Interface**: Tools are registered once and accessible from any framework
- **Flexible Integration**: Can be used as a standalone library or integrated into existing applications

## Deployment Patterns

### Development (Single Machine)

```
+------------------------+     +------------------------+
|    Main Application    |     |   Docker Container     |
|    localhost:50051     |<--->|   localhost:8001       |
+------------------------+     +------------------------+
```

### Production (Kubernetes)

```
+------------------------+     +------------------------+
|    Main App Pod        |     |   Executor Pod         |
|    (Service: tools)    |<--->|   (Service: executor)  |
+------------------------+     +------------------------+
```

### Production (Docker Compose)

```
+------------------------+     +------------------------+
|    main-app            |     |   executor             |
|    (network: codemode) |<--->|   (network: codemode)  |
+------------------------+     +------------------------+
```

## Next Steps

- [Components](components.md): Detailed breakdown of each component
- [Security Model](security-model.md): In-depth security architecture
- [Configuration](../configuration/index.md): Configuration options
