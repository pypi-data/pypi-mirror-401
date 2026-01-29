"""
Unit tests for ComponentRegistry.
"""

import pytest

from codemode.core.registry import (
    ComponentAlreadyExistsError,
    ComponentNotFoundError,
    ComponentRegistry,
)


class DummyTool:
    """Dummy tool for testing."""

    def run(self, **kwargs):
        return "dummy_result"


class DummyAgent:
    """Dummy agent for testing."""

    def execute_task(self, task, context):
        return "agent_result"


class TestComponentRegistry:
    """Test ComponentRegistry class."""

    def test_init(self):
        """Test registry initialization."""
        registry = ComponentRegistry()

        assert len(registry.tools) == 0
        assert len(registry.agents) == 0
        assert len(registry.teams) == 0
        assert len(registry.flows) == 0
        assert len(registry.config) == 0

    def test_register_tool(self):
        """Test tool registration."""
        registry = ComponentRegistry()
        tool = DummyTool()

        registry.register_tool("test_tool", tool)

        assert "test_tool" in registry.tools
        assert registry.tools["test_tool"] == tool

    def test_register_tool_invalid_name(self):
        """Test tool registration with invalid name."""
        registry = ComponentRegistry()

        with pytest.raises(ValueError, match="Tool name cannot be empty"):
            registry.register_tool("", DummyTool())

    def test_register_tool_none(self):
        """Test tool registration with None."""
        registry = ComponentRegistry()

        with pytest.raises(ValueError, match="Tool instance cannot be None"):
            registry.register_tool("test", None)

    def test_register_tool_duplicate(self):
        """Test registering duplicate tool."""
        registry = ComponentRegistry()
        tool = DummyTool()

        registry.register_tool("test", tool)

        with pytest.raises(ComponentAlreadyExistsError):
            registry.register_tool("test", tool)

    def test_register_tool_overwrite(self):
        """Test overwriting existing tool."""
        registry = ComponentRegistry()
        tool1 = DummyTool()
        tool2 = DummyTool()

        registry.register_tool("test", tool1)
        registry.register_tool("test", tool2, overwrite=True)

        assert registry.tools["test"] == tool2

    def test_register_agent(self):
        """Test agent registration."""
        registry = ComponentRegistry()
        agent = DummyAgent()

        registry.register_agent("test_agent", agent)

        assert "test_agent" in registry.agents
        assert registry.agents["test_agent"] == agent

    def test_register_crew(self):
        """Test team registration."""
        registry = ComponentRegistry()
        team = object()

        registry.register_team("test_team", team)

        assert "test_team" in registry.teams
        assert registry.teams["test_team"] == team

    def test_register_flow(self):
        """Test flow registration."""
        registry = ComponentRegistry()
        flow = object()

        registry.register_flow("test_flow", flow)

        assert "test_flow" in registry.flows
        assert registry.flows["test_flow"] == flow

    def test_set_config(self):
        """Test setting configuration."""
        registry = ComponentRegistry()

        registry.set_config("key1", "value1")
        registry.set_config("key2", 42)

        assert registry.config["key1"] == "value1"
        assert registry.config["key2"] == 42

    def test_set_config_invalid_key(self):
        """Test setting config with invalid key."""
        registry = ComponentRegistry()

        with pytest.raises(ValueError, match="Config key cannot be empty"):
            registry.set_config("", "value")

    def test_get_config(self):
        """Test getting configuration."""
        registry = ComponentRegistry()

        registry.set_config("key1", "value1")

        assert registry.get_config("key1") == "value1"
        assert registry.get_config("missing") is None
        assert registry.get_config("missing", "default") == "default"

    def test_get_tool(self):
        """Test getting registered tool."""
        registry = ComponentRegistry()
        tool = DummyTool()

        registry.register_tool("test", tool)

        retrieved = registry.get_tool("test")
        assert retrieved == tool

    def test_get_tool_not_found(self):
        """Test getting non-existent tool."""
        registry = ComponentRegistry()

        with pytest.raises(ComponentNotFoundError, match="Tool 'missing' not found"):
            registry.get_tool("missing")

    def test_get_agent(self):
        """Test getting registered agent."""
        registry = ComponentRegistry()
        agent = DummyAgent()

        registry.register_agent("test", agent)

        retrieved = registry.get_agent("test")
        assert retrieved == agent

    def test_get_agent_not_found(self):
        """Test getting non-existent agent."""
        registry = ComponentRegistry()

        with pytest.raises(ComponentNotFoundError, match="Agent 'missing' not found"):
            registry.get_agent("missing")

    def test_get_component_names(self):
        """Test getting all component names."""
        registry = ComponentRegistry()

        registry.register_tool("tool1", DummyTool())
        registry.register_tool("tool2", DummyTool())
        registry.register_agent("agent1", DummyAgent())

        names = registry.get_component_names()

        assert set(names["tools"]) == {"tool1", "tool2"}
        assert set(names["agents"]) == {"agent1"}
        assert len(names["teams"]) == 0
        assert len(names["flows"]) == 0

    def test_clear(self):
        """Test clearing registry."""
        registry = ComponentRegistry()

        registry.register_tool("tool1", DummyTool())
        registry.register_agent("agent1", DummyAgent())
        registry.set_config("key1", "value1")

        registry.clear()

        assert len(registry.tools) == 0
        assert len(registry.agents) == 0
        assert len(registry.config) == 0

    def test_repr(self):
        """Test string representation."""
        registry = ComponentRegistry()

        registry.register_tool("tool1", DummyTool())
        registry.register_agent("agent1", DummyAgent())

        repr_str = repr(registry)

        assert "ComponentRegistry" in repr_str
        assert "tools=1" in repr_str
        assert "agents=1" in repr_str

    @pytest.mark.asyncio
    async def test_register_tool_async(self):
        """Test async tool registration."""
        registry = ComponentRegistry()
        tool = DummyTool()

        await registry.register_tool_async("test", tool)

        assert "test" in registry.tools

    def test_register_agent_invalid_name(self):
        """Test agent registration with invalid name."""
        registry = ComponentRegistry()

        with pytest.raises(ValueError, match="Agent name cannot be empty"):
            registry.register_agent("", DummyAgent())

    def test_register_agent_none(self):
        """Test agent registration with None."""
        registry = ComponentRegistry()

        with pytest.raises(ValueError, match="Agent instance cannot be None"):
            registry.register_agent("test", None)

    def test_register_agent_duplicate(self):
        """Test registering duplicate agent."""
        registry = ComponentRegistry()
        agent = DummyAgent()

        registry.register_agent("test", agent)

        with pytest.raises(ComponentAlreadyExistsError):
            registry.register_agent("test", agent)

    @pytest.mark.asyncio
    async def test_register_agent_async(self):
        """Test async agent registration."""
        registry = ComponentRegistry()
        agent = DummyAgent()

        await registry.register_agent_async("test", agent)

        assert "test" in registry.agents

    def test_register_team_invalid_name(self):
        """Test team registration with invalid name."""
        registry = ComponentRegistry()

        with pytest.raises(ValueError, match="Team name cannot be empty"):
            registry.register_team("", object())

    def test_register_team_none(self):
        """Test team registration with None."""
        registry = ComponentRegistry()

        with pytest.raises(ValueError, match="Team instance cannot be None"):
            registry.register_team("test", None)

    def test_register_team_duplicate(self):
        """Test registering duplicate team."""
        registry = ComponentRegistry()
        team = object()

        registry.register_team("test", team)

        with pytest.raises(ComponentAlreadyExistsError):
            registry.register_team("test", team)

    @pytest.mark.asyncio
    async def test_register_team_async(self):
        """Test async team registration."""
        registry = ComponentRegistry()
        team = object()

        await registry.register_team_async("test", team)

        assert "test" in registry.teams

    def test_register_flow_invalid_name(self):
        """Test flow registration with invalid name."""
        registry = ComponentRegistry()

        with pytest.raises(ValueError, match="Flow name cannot be empty"):
            registry.register_flow("", object())

    def test_register_flow_none(self):
        """Test flow registration with None."""
        registry = ComponentRegistry()

        with pytest.raises(ValueError, match="Flow instance cannot be None"):
            registry.register_flow("test", None)

    def test_register_flow_duplicate(self):
        """Test registering duplicate flow."""
        registry = ComponentRegistry()
        flow = object()

        registry.register_flow("test", flow)

        with pytest.raises(ComponentAlreadyExistsError):
            registry.register_flow("test", flow)

    @pytest.mark.asyncio
    async def test_register_flow_async(self):
        """Test async flow registration."""
        registry = ComponentRegistry()
        flow = object()

        await registry.register_flow_async("test", flow)

        assert "test" in registry.flows

    def test_set_context(self):
        """Test setting runtime context."""
        from codemode.core.context import RuntimeContext

        registry = ComponentRegistry()
        context = RuntimeContext(variables={"client_id": "acme", "user_id": "123"})

        registry.set_context(context)

        assert registry.get_context() == context
        assert registry.get_context().get("client_id") == "acme"

    def test_set_context_invalid_type(self):
        """Test setting context with invalid type."""
        registry = ComponentRegistry()

        with pytest.raises(TypeError, match="context must be a RuntimeContext instance"):
            registry.set_context({"not": "a context"})

    @pytest.mark.asyncio
    async def test_set_context_async(self):
        """Test async context setting."""
        from codemode.core.context import RuntimeContext

        registry = ComponentRegistry()
        context = RuntimeContext(variables={"client_id": "acme"})

        await registry.set_context_async(context)

        assert registry.get_context() == context

    @pytest.mark.asyncio
    async def test_get_context_async(self):
        """Test async context retrieval."""
        from codemode.core.context import RuntimeContext

        registry = ComponentRegistry()
        context = RuntimeContext(variables={"test": "value"})
        registry.set_context(context)

        result = await registry.get_context_async()

        assert result == context

    def test_clear_context(self):
        """Test clearing runtime context."""
        from codemode.core.context import RuntimeContext

        registry = ComponentRegistry()
        context = RuntimeContext(variables={"client_id": "acme"})
        registry.set_context(context)

        registry.clear_context()

        assert registry.get_context() is None

    @pytest.mark.asyncio
    async def test_clear_context_async(self):
        """Test async context clearing."""
        from codemode.core.context import RuntimeContext

        registry = ComponentRegistry()
        context = RuntimeContext(variables={"client_id": "acme"})
        registry.set_context(context)

        await registry.clear_context_async()

        assert registry.get_context() is None

    def test_get_team_success(self):
        """Test getting a registered team."""
        registry = ComponentRegistry()

        class DummyTeam:
            pass

        team = DummyTeam()
        registry.register_team("my_team", team)

        retrieved = registry.get_team("my_team")

        assert retrieved is team

    def test_get_flow_success(self):
        """Test getting a registered flow."""
        registry = ComponentRegistry()

        class DummyFlow:
            pass

        flow = DummyFlow()
        registry.register_flow("my_flow", flow)

        retrieved = registry.get_flow("my_flow")

        assert retrieved is flow

    def test_get_team_not_found(self):
        """Test getting non-existent team."""
        registry = ComponentRegistry()

        with pytest.raises(ComponentNotFoundError, match="Team 'missing' not found"):
            registry.get_team("missing")

    def test_get_flow_not_found(self):
        """Test getting non-existent flow."""
        registry = ComponentRegistry()

        with pytest.raises(ComponentNotFoundError, match="Flow 'missing' not found"):
            registry.get_flow("missing")

    def test_update_config(self):
        """Test updating multiple config values."""
        registry = ComponentRegistry()

        registry.update_config(timeout=30, max_retries=3, env="production")

        assert registry.config["timeout"] == 30
        assert registry.config["max_retries"] == 3
        assert registry.config["env"] == "production"


class TestRegistryConcurrency:
    """Test ComponentRegistry concurrent context isolation using ContextVar."""

    @pytest.mark.asyncio
    async def test_concurrent_context_isolation(self):
        """Test that concurrent async tasks have isolated contexts.

        This is the critical test that verifies ContextVar properly
        isolates context across concurrent async tasks, preventing
        multi-tenant data leakage.
        """
        import asyncio

        from codemode.core.context import RuntimeContext
        from codemode.core.registry import reset_context

        # Ensure clean state
        reset_context()

        registry = ComponentRegistry()
        results = []
        errors = []

        async def task(client_id: str, delay: float):
            """Simulate a request with context."""
            try:
                # Set context for this task
                context = RuntimeContext(variables={"client_id": client_id})
                registry.set_context(context)

                # Simulate async work (this is where race conditions would occur)
                await asyncio.sleep(delay)

                # Retrieve context - should be the same we set
                retrieved = registry.get_context()
                actual_client = retrieved.get("client_id") if retrieved else None

                results.append(
                    {
                        "expected": client_id,
                        "actual": actual_client,
                        "match": client_id == actual_client,
                    }
                )

                # Clean up
                registry.clear_context()

            except Exception as e:
                errors.append({"client_id": client_id, "error": str(e)})

        # Run concurrent tasks with different delays to create interleaving
        await asyncio.gather(
            task("client_a", 0.1),
            task("client_b", 0.05),
            task("client_c", 0.15),
            task("client_d", 0.02),
            task("client_e", 0.08),
        )

        # Verify no errors
        assert not errors, f"Errors occurred: {errors}"

        # Verify all tasks got their own context
        assert len(results) == 5, f"Expected 5 results, got {len(results)}"
        for r in results:
            assert r[
                "match"
            ], f"Context leaked! Task expected '{r['expected']}' but got '{r['actual']}'"

    @pytest.mark.asyncio
    async def test_context_clear_does_not_affect_other_tasks(self):
        """Test that clearing context in one task doesn't affect others."""
        import asyncio

        from codemode.core.context import RuntimeContext
        from codemode.core.registry import reset_context

        reset_context()
        registry = ComponentRegistry()

        async def task_that_clears():
            """Task that sets and clears context."""
            context = RuntimeContext(variables={"client_id": "task_clear"})
            registry.set_context(context)
            await asyncio.sleep(0.05)
            registry.clear_context()
            await asyncio.sleep(0.05)

        async def task_that_checks():
            """Task that sets context and checks it persists."""
            context = RuntimeContext(variables={"client_id": "task_check"})
            registry.set_context(context)
            await asyncio.sleep(0.1)  # Wait longer than the clear task
            retrieved = registry.get_context()
            # Should still have our context, not None
            assert retrieved is not None, "Context was unexpectedly cleared!"
            assert retrieved.get("client_id") == "task_check"
            registry.clear_context()

        # Run both concurrently
        await asyncio.gather(
            task_that_clears(),
            task_that_checks(),
        )

    @pytest.mark.asyncio
    async def test_many_concurrent_tasks(self):
        """Stress test with many concurrent tasks."""
        import asyncio
        import random

        from codemode.core.context import RuntimeContext
        from codemode.core.registry import reset_context

        reset_context()
        registry = ComponentRegistry()
        num_tasks = 50
        results = []

        async def task(task_id: int):
            client_id = f"client_{task_id}"
            context = RuntimeContext(variables={"client_id": client_id, "task_id": task_id})
            registry.set_context(context)

            # Random delay to create interleaving
            await asyncio.sleep(random.uniform(0.001, 0.05))

            retrieved = registry.get_context()
            actual_client = retrieved.get("client_id") if retrieved else None
            results.append({"expected": client_id, "actual": actual_client})

            registry.clear_context()

        tasks = [task(i) for i in range(num_tasks)]
        await asyncio.gather(*tasks)

        # All tasks should have gotten their own context
        assert len(results) == num_tasks
        failures = [r for r in results if r["expected"] != r["actual"]]
        assert not failures, f"Context leaked in {len(failures)} tasks: {failures[:5]}"

    def test_get_current_context_function(self):
        """Test the module-level get_current_context function."""
        from codemode.core.context import RuntimeContext
        from codemode.core.registry import get_current_context, reset_context

        reset_context()

        # Initially None
        assert get_current_context() is None

        # Set via registry
        registry = ComponentRegistry()
        context = RuntimeContext(variables={"test": "value"})
        registry.set_context(context)

        # Should be accessible via module function
        current = get_current_context()
        assert current is not None
        assert current.get("test") == "value"

        # Clear
        reset_context()
        assert get_current_context() is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
