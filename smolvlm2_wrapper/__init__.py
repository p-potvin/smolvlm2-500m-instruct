"""
SmolVLM2 Wrapper – multi-modal manipulation toolkit
====================================================

Top-level exports for the most commonly used classes and helpers so that
callers only need a single import::

    from smolvlm2_wrapper import SmolVLM2Wrapper, ImageProcessor, VideoProcessor, TextProcessor

See README.md for full usage examples and workflow documentation.
"""

from smolvlm2_wrapper.core.model import BaseModelWrapper
from smolvlm2_wrapper.core.smolvlm2 import GenericTextModelWrapper
from smolvlm2_wrapper.image.processor import ImageProcessor
from smolvlm2_wrapper.video.processor import VideoProcessor
from smolvlm2_wrapper.text.processor import TextProcessor
from smolvlm2_wrapper.workflows.base import Workflow
from smolvlm2_wrapper.utils.device import DeviceManager
from smolvlm2_wrapper.context_schema import ImageContext, VideoContext, TextContext, WorkflowContext
from smolvlm2_wrapper.agent_registry import AgentRegistry
from smolvlm2_wrapper.event_bus import EventBus

# Register core agents for discovery
AgentRegistry.register(
    'text', TextProcessor, 'Text generation, editing, VQA, prompt engineering', TextContext
)
AgentRegistry.register(
    'image', ImageProcessor, 'Image generation, editing, masking, inpainting', ImageContext
)
AgentRegistry.register(
    'video', VideoProcessor, 'Video generation, editing, analysis', VideoContext
)
AgentRegistry.register(
    'workflow', Workflow, 'Workflow parsing, export, validation', WorkflowContext
)


__version__ = "0.1.0"

__all__ = [
    "BaseModelWrapper",
    "GenericTextModelWrapper",
    "ImageProcessor",
    "VideoProcessor",
    "TextProcessor",
    "Workflow",
    "DeviceManager",
]
