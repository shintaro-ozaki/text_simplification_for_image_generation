import torch
from diffusers import StableDiffusion3Pipeline, BitsAndBytesConfig, SD3Transformer2DModel
import random
import json
from pathlib import Path
import os
from loguru import logger
from diffusers import StableDiffusion3Pipeline
import argparse
from dotenv import load_dotenv

load_dotenv()
project_root = Path(
    '/cl/home2/shintaro/text_simplification_for_image_generation')
seed = 42


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--prompt', type=int, required=True, choices=[1, 2])
  parser.add_argument('--debug', action='store_true')
  return parser.parse_args()


def load_jsonl(file_path):
  with open(file_path, "r") as f:
    return [json.loads(line) for line in f]


def initizalize_model(model_name):
  pipeline = StableDiffusion3Pipeline.from_pretrained(
      model_name, torch_dtype=torch.bfloat16, token=os.getenv("WRITE_TOKEN"))
  pipeline = pipeline.to("cuda")
  pipeline.enable_model_cpu_offload()
  return pipeline


def generate_image(prompt, pipeline):
  generator = torch.manual_seed(seed)
  image = pipeline(
      prompt=prompt,
      num_inference_steps=35,
      guidance_scale=4.5,
      generator=generator,
      max_sequence_length=512).images[0]
  return image


if __name__ == "__main__":
  args = parse_args()
  prompt_pattern = args.prompt
  wit_input_file = project_root / "data" / "wit" / "en.wit.2k.prompt.jsonl"
  model_name = "stabilityai/stable-diffusion-3.5-large"
  model_name_suffix = model_name.split("/")[-1]
  if prompt_pattern == 1:
    image_dir = project_root / "generated_images" / "pattern1" / model_name_suffix
  elif prompt_pattern == 2:
    image_dir = project_root / "generated_images" / "pattern2" / model_name_suffix
  image_dir.mkdir(exist_ok=True, parents=True)
  pipeline = initizalize_model(model_name)
  logger.info(f'image_dir: {image_dir}')
  wit_data = load_jsonl(wit_input_file)
  for i, line in enumerate(wit_data):
    logger.info(f'Iteration {i} / {len(wit_data)}')
    if prompt_pattern == 1:
      prompt = line["prompt1"]
    elif prompt_pattern == 2:
      prompt = line["prompt2"]
    else:
      raise ValueError(f"Invalid prompt pattern: {prompt_pattern}")
    image = generate_image(prompt, pipeline)
    image_path = image_dir / f"{i}.png"
    image.save(image_path)
    logger.info(f"Image is saved at {image_path}")
    if args.debug:
      if i == 10:
        break

  logger.info("All images are generated")
  logger.info(f'Generated images are saved at {image_dir}')
