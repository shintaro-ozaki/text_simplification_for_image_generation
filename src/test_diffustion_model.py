import torch
from diffusers import StableDiffusion3Pipeline
from dotenv import load_dotenv
import os

load_dotenv()

pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3.5-large", torch_dtype=torch.bfloat16, device="cuda", access_token=os.environ["HUGGINGFACE_TOKEN"])
pipe = pipe.to("cuda")

image = pipe(
    "A capybara holding a sign that reads Hello World",
    num_inference_steps=28,
    guidance_scale=3.5,
).images[0]
image.save("capybara.png")

