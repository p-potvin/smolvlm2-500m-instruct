"""Tests for WorkflowExportAgent logic."""
import pytest
from smolvlm2_wrapper.workflow_export_agent import WorkflowExportAgent
from smolvlm2_wrapper.shared_context import SharedContext

class DummyValidationUtils:
    @staticmethod
    def validate_context(schema, ctx):
        return []
    @staticmethod
    def report_error(ctx, agent, err):
        pass

class DummyEventBus:
    published = []
    @staticmethod
    def publish(event, payload):
        DummyEventBus.published.append((event, payload))


def test_export_to_comfyui_success(monkeypatch):
    monkeypatch.setattr("smolvlm2_wrapper.validation_utils.ValidationUtils", DummyValidationUtils)
    monkeypatch.setattr("smolvlm2_wrapper.event_bus.EventBus", DummyEventBus)
    agent = WorkflowExportAgent(SharedContext())
    result = agent.export_to_comfyui({"foo": "bar"})
    assert result["success"]
    assert "comfyui_workflow" in result
    assert DummyEventBus.published


def test_export_to_comfyui_validation_error(monkeypatch):
    class FailingValidation:
        @staticmethod
        def validate_context(schema, ctx):
            return ["bad input"]
        @staticmethod
        def report_error(ctx, agent, err):
            pass
    monkeypatch.setattr("smolvlm2_wrapper.validation_utils.ValidationUtils", FailingValidation)
    monkeypatch.setattr("smolvlm2_wrapper.event_bus.EventBus", DummyEventBus)
    agent = WorkflowExportAgent(SharedContext())
    result = agent.export_to_comfyui({"foo": "bar"})
    assert not result["success"]
    assert "errors" in result
