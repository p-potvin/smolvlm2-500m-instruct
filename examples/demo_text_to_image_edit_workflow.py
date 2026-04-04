"""
Demo: Complex text-to-image workflow with image editing and detailer chain.
This script instantiates agents, connects them via shared context and event bus,
and executes a multi-stage workflow: text→image→edit (bbox/segment swap, object removal, detailer).
"""
from smolvlm2_wrapper.shared_context import SharedContext
from smolvlm2_wrapper.agent_interface import AgentInterface
from smolvlm2_wrapper.event_bus import EventBus
from smolvlm2_wrapper.central_error_logger import CentralErrorLogger
# Assume these agent classes exist and are imported:
# from smolvlm2_wrapper.agent_text import TextProcessor
# from smolvlm2_wrapper.agent_image import ImageProcessor
# from smolvlm2_wrapper.workflow_export_agent import WorkflowExportAgent

# Dummy agent implementations for demonstration
class TextProcessor(AgentInterface):
    def run(self, prompt):
        # Simulate text-to-image prompt engineering
        self.set_context({'prompt': prompt, 'engineered_prompt': prompt + ' in photorealistic style'})
        return self.get_context()['engineered_prompt']

class ImageProcessor(AgentInterface):
    def run(self, prompt, edit_preset=None):
        # Simulate image generation and editing
        img = f"image_generated_from_{prompt}"
        edits = []
        if edit_preset == 'bbox_swap':
            edits.append('bbox swapped')
        if edit_preset == 'segment_swap':
            edits.append('segments swapped')
        if edit_preset == 'object_removal':
            edits.append('object removed')
        if edit_preset == 'detailer':
            edits.append('detailer chain applied')
        self.set_context({'image': img, 'edits': edits})
        return img, edits

class WorkflowExportAgent:
    def __init__(self, shared_context):
        self.shared_context = shared_context
    def export_to_comfyui(self, workflow_dict):
        # Simulate export
        return {'success': True, 'comfyui_workflow': workflow_dict}

# Setup shared context and error logger
shared_context = SharedContext(workflow_id='demo1')
CentralErrorLogger(shared_context)

# Instantiate agents
text_agent = TextProcessor('text', shared_context)
image_agent = ImageProcessor('image', shared_context)
workflow_exporter = WorkflowExportAgent(shared_context)

# 1. Text-to-image prompt engineering
prompt = "A futuristic cityscape at sunset with flying cars"
engineered_prompt = text_agent.run(prompt)

# 2. Image generation and editing chain
img, edits1 = image_agent.run(engineered_prompt, edit_preset='bbox_swap')
img, edits2 = image_agent.run(engineered_prompt, edit_preset='segment_swap')
img, edits3 = image_agent.run(engineered_prompt, edit_preset='object_removal')
img, edits4 = image_agent.run(engineered_prompt, edit_preset='detailer')

# 3. Aggregate workflow for export
workflow_dict = {
    'prompt': engineered_prompt,
    'image': img,
    'edits': edits1 + edits2 + edits3 + edits4
}
export_result = workflow_exporter.export_to_comfyui(workflow_dict)

# 4. Print results and error log
print("Workflow export result:", export_result)
print("Error log:", shared_context.errors)
print("Agent contexts:", shared_context.agents)
