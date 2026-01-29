"""
Basic Codemode example with CrewAI.

This example demonstrates using Codemode with mock tools.
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from codemode import Codemode
from codemode.grpc import start_tool_service_async


# Mock tools for demonstration
class WeatherTool:
    """Mock weather tool."""

    def run(self, location: str) -> str:
        """Get weather for location."""
        return f"Weather in {location}: 72°F, Sunny, Light winds"


class DatabaseTool:
    """Mock database tool."""

    def run(self, query: str) -> str:
        """Execute database query."""
        if "SELECT" in query.upper():
            return "[{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]"
        elif "INSERT" in query.upper():
            return "1 row inserted"
        return "Query executed"


# Request model
class ChatRequest(BaseModel):
    message: str


# Application state
codemode = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage ToolService lifecycle."""
    global codemode

    # Startup
    print("=" * 60)
    print("Codemode Basic Example")
    print("=" * 60)

    codemode = Codemode.from_config("codemode.yaml")
    codemode.registry.register_tool("weather", WeatherTool())
    codemode.registry.register_tool("database", DatabaseTool())

    # Start gRPC tool service - properly waits for server to be ready
    server = await start_tool_service_async(codemode.registry, host="0.0.0.0", port=50051)

    print("To run this example:")
    print("1. Install: pip install opencodemode[crewai]")
    print("2. Start executor: python -m codemode.executor.service")
    print("3. Uncomment code in app.py")
    print("4. Run: python app.py")
    print("=" * 60)

    yield

    # Shutdown: clean stop
    await server.stop(0)


# Create FastAPI app with lifespan
app = FastAPI(title="Codemode Basic Example", lifespan=lifespan)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Codemode Basic Example",
        "endpoints": {
            "/chat": "POST - Send message to orchestrator",
            "/health": "GET - Health check",
        },
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint using orchestrator agent.

    In a real implementation, this would:
    1. Create a task from user message
    2. Create a crew with orchestrator agent
    3. Execute the crew
    4. Return result
    """

    # In a real app, uncomment:
    # task = Task(
    #     description=request.message,
    #     agent=orchestrator,
    #     expected_output="Task completed"
    # )
    #
    # crew = Crew(agents=[orchestrator], tasks=[task])
    # result = crew.kickoff()
    #
    # return {"result": str(result)}

    # Mock response for now
    return {
        "message": "Example not fully configured",
        "instructions": "See startup logs for setup instructions",
        "your_message": request.message,
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
