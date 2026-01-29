"""
Unit tests for RuntimeContext and context management.
"""

import json

import pytest

from codemode.core.context import RuntimeContext, ToolContextRequirements


class TestRuntimeContext:
    """Test RuntimeContext class."""

    def test_init_empty(self):
        """Test creating empty context."""
        context = RuntimeContext()

        assert context.variables == {}
        assert context.metadata == {}

    def test_init_with_variables(self):
        """Test creating context with variables."""
        context = RuntimeContext(
            variables={"client_id": "acme", "user_id": "123"}, metadata={"source": "api"}
        )

        assert context.variables["client_id"] == "acme"
        assert context.variables["user_id"] == "123"
        assert context.metadata["source"] == "api"

    def test_post_init_validation_invalid_variables(self):
        """Test post_init validation with invalid variables type."""
        with pytest.raises(TypeError, match="variables must be a dictionary"):
            RuntimeContext(variables="not a dict")

    def test_post_init_validation_invalid_metadata(self):
        """Test post_init validation with invalid metadata type."""
        with pytest.raises(TypeError, match="metadata must be a dictionary"):
            RuntimeContext(variables={}, metadata="not a dict")

    def test_get_with_default(self):
        """Test get() method with default value."""
        context = RuntimeContext(variables={"client_id": "acme"})

        assert context.get("client_id") == "acme"
        assert context.get("missing") is None
        assert context.get("missing", "default") == "default"

    def test_require_success(self):
        """Test require() method with existing key."""
        context = RuntimeContext(variables={"client_id": "acme"})

        result = context.require("client_id")

        assert result == "acme"

    def test_require_failure(self):
        """Test require() method with missing key."""
        context = RuntimeContext(variables={"client_id": "acme"})

        with pytest.raises(KeyError, match="Required context variable 'missing' not found"):
            context.require("missing")

    def test_has(self):
        """Test has() method."""
        context = RuntimeContext(variables={"client_id": "acme", "user_id": "123"})

        assert context.has("client_id") is True
        assert context.has("user_id") is True
        assert context.has("missing") is False

    def test_to_dict(self):
        """Test serialization to dict."""
        context = RuntimeContext(variables={"client_id": "acme"}, metadata={"source": "api"})

        result = context.to_dict()

        assert result == {"variables": {"client_id": "acme"}, "metadata": {"source": "api"}}

    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {"variables": {"client_id": "acme"}, "metadata": {"source": "api"}}

        context = RuntimeContext.from_dict(data)

        assert context.variables["client_id"] == "acme"
        assert context.metadata["source"] == "api"

    def test_to_json(self):
        """Test serialization to JSON."""
        context = RuntimeContext(variables={"client_id": "acme"}, metadata={"source": "api"})

        json_str = context.to_json()

        # Parse JSON to verify it's valid
        data = json.loads(json_str)
        assert data["variables"]["client_id"] == "acme"
        assert data["metadata"]["source"] == "api"

    def test_from_json(self):
        """Test deserialization from JSON."""
        json_str = '{"variables": {"client_id": "acme"}, "metadata": {"source": "api"}}'

        context = RuntimeContext.from_json(json_str)

        assert context.variables["client_id"] == "acme"
        assert context.metadata["source"] == "api"

    def test_set(self):
        """Test set() method."""
        context = RuntimeContext()

        context.set("client_id", "acme")
        context.set("user_id", "123")

        assert context.variables["client_id"] == "acme"
        assert context.variables["user_id"] == "123"

    def test_update(self):
        """Test update() method."""
        context = RuntimeContext(variables={"client_id": "acme"})

        context.update(user_id="123", session_id="sess_456")

        assert context.variables["client_id"] == "acme"
        assert context.variables["user_id"] == "123"
        assert context.variables["session_id"] == "sess_456"

    def test_keys(self):
        """Test keys() method."""
        context = RuntimeContext(
            variables={"client_id": "acme", "user_id": "123", "session_id": "sess_456"}
        )

        keys = context.keys()

        assert set(keys) == {"client_id", "user_id", "session_id"}

    def test_repr(self):
        """Test string representation."""
        context = RuntimeContext(variables={"client_id": "acme", "user_id": "123"})

        repr_str = repr(context)

        assert "RuntimeContext" in repr_str
        assert "client_id" in repr_str or "user_id" in repr_str

    def test_bool_truthy(self):
        """Test bool() with variables."""
        context = RuntimeContext(variables={"client_id": "acme"})

        assert bool(context) is True

    def test_bool_falsy(self):
        """Test bool() without variables."""
        context = RuntimeContext()

        assert bool(context) is False

    def test_len(self):
        """Test len() method."""
        context = RuntimeContext(variables={"client_id": "acme", "user_id": "123"})

        assert len(context) == 2

    def test_len_empty(self):
        """Test len() with empty context."""
        context = RuntimeContext()

        assert len(context) == 0


class TestToolContextRequirements:
    """Test ToolContextRequirements class."""

    def test_init_defaults(self):
        """Test initialization with defaults."""
        requirements = ToolContextRequirements()

        assert requirements.requires_context is False
        assert requirements.required_keys == []
        assert requirements.optional_keys == []

    def test_init_with_requirements(self):
        """Test initialization with requirements."""
        requirements = ToolContextRequirements(
            requires_context=True,
            required_keys=["client_id", "user_id"],
            optional_keys=["session_id"],
        )

        assert requirements.requires_context is True
        assert requirements.required_keys == ["client_id", "user_id"]
        assert requirements.optional_keys == ["session_id"]

    def test_validate_no_requirements(self):
        """Test validation with no requirements."""
        requirements = ToolContextRequirements()

        # Should not raise
        requirements.validate(None)
        requirements.validate(RuntimeContext())

    def test_validate_requires_context_but_none_provided(self):
        """Test validation when context is required but not provided."""
        requirements = ToolContextRequirements(requires_context=True)

        with pytest.raises(ValueError, match="Tool requires context but none provided"):
            requirements.validate(None)

    def test_validate_missing_required_keys(self):
        """Test validation with missing required keys."""
        requirements = ToolContextRequirements(
            requires_context=True, required_keys=["client_id", "user_id"]
        )

        context = RuntimeContext(variables={"client_id": "acme"})  # Missing user_id

        with pytest.raises(ValueError, match="Tool requires context keys"):
            requirements.validate(context)

    def test_validate_all_required_keys_present(self):
        """Test validation when all required keys are present."""
        requirements = ToolContextRequirements(
            requires_context=True, required_keys=["client_id", "user_id"]
        )

        context = RuntimeContext(variables={"client_id": "acme", "user_id": "123"})

        # Should not raise
        requirements.validate(context)

    def test_validate_optional_keys_not_required(self):
        """Test that optional keys are not validated."""
        requirements = ToolContextRequirements(
            requires_context=True,
            required_keys=["client_id"],
            optional_keys=["session_id", "request_id"],
        )

        # Only required key present, optional keys missing
        context = RuntimeContext(variables={"client_id": "acme"})

        # Should not raise
        requirements.validate(context)

    def test_validate_context_provided_but_not_required(self):
        """Test validation when context is provided but not required."""
        requirements = ToolContextRequirements(requires_context=False, required_keys=["client_id"])

        # Context with required key
        context = RuntimeContext(variables={"client_id": "acme"})

        # Should not raise - context is optional, but if provided, required keys must be present
        requirements.validate(context)

    def test_validate_context_provided_missing_required_keys(self):
        """Test validation when context is provided but missing required keys."""
        requirements = ToolContextRequirements(
            requires_context=False,  # Context is optional
            required_keys=["client_id"],  # But if provided, must have client_id
        )

        # Context without required key
        context = RuntimeContext(variables={"user_id": "123"})

        # Should raise - context was provided but missing required key
        with pytest.raises(ValueError, match="Tool requires context keys"):
            requirements.validate(context)


class TestRuntimeContextIntegration:
    """Test RuntimeContext integration scenarios."""

    def test_multi_tenant_saas_scenario(self):
        """Test multi-tenant SaaS use case."""
        context = RuntimeContext(
            variables={
                "client_id": "acme_corp",
                "user_id": "user_123",
                "session_id": "sess_456",
                "subscription_tier": "premium",
            },
            metadata={"request_id": "req_789", "timestamp": "2024-01-01T00:00:00Z"},
        )

        assert context.get("client_id") == "acme_corp"
        assert context.get("subscription_tier") == "premium"
        assert context.has("user_id") is True
        assert len(context) == 4

    def test_feature_flags_scenario(self):
        """Test feature flags use case."""
        context = RuntimeContext(
            variables={
                "client_id": "acme",
                "features": {"new_ui": True, "beta_search": False, "ai_assistant": True},
            }
        )

        features = context.get("features", {})
        assert features["new_ui"] is True
        assert features["beta_search"] is False
        assert features["ai_assistant"] is True

    def test_context_serialization_round_trip(self):
        """Test full serialization round trip."""
        original = RuntimeContext(
            variables={"client_id": "acme", "user_id": "123"},
            metadata={"source": "api", "version": "v2"},
        )

        # To JSON and back
        json_str = original.to_json()
        restored = RuntimeContext.from_json(json_str)

        assert restored.variables == original.variables
        assert restored.metadata == original.metadata

    def test_context_modification_chain(self):
        """Test chaining context modifications."""
        context = RuntimeContext()

        context.set("client_id", "acme")
        context.update(user_id="123", session_id="sess_456")
        context.set("tier", "premium")

        assert len(context) == 4
        assert context.get("client_id") == "acme"
        assert context.get("user_id") == "123"
        assert context.get("session_id") == "sess_456"
        assert context.get("tier") == "premium"
