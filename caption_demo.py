from ai_model import TextModelWrapper
from PIL import Image
import torch
model = TextModelWrapper()
caption = model.caption(image=Image.open(
    "C:/Users/Administrator/Desktop/LoRA Training Sets/Characters/lanarhoades/17092466_008_56d5.jpg"),
    style="tags")
print(caption)
caption = model.enhance_prompt(caption, image=Image.open(
    "C:/Users/Administrator/Desktop/LoRA Training Sets/Characters/lanarhoades/17092466_008_56d5.jpg"),
    max_new_tokens=75,
    attention_mask=torch.ones((1, 312), dtype=torch.long)
)
print(caption)