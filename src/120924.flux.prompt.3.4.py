import torch
from diffusers import FluxPipeline
import random
import json
from pathlib import Path
import os
from loguru import logger
from diffusers import StableDiffusion3Pipeline
import argparse
from dotenv import load_dotenv

load_dotenv()
project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')
seed = 42


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--prompt', type=int, required=True, choices=[3, 4])
  parser.add_argument('--summarize_model', type=str, required=True)
  parser.add_argument('--max_token', type=int, required=True)
  parser.add_argument('--debug', action='store_true')
  return parser.parse_args()


def load_jsonl(file_path):
  with open(file_path, "r") as f:
    return [json.loads(line) for line in f]


def initizalize_model(model_name):
  pipeline = FluxPipeline.from_pretrained(model_name, torch_dtype=torch.bfloat16)
  pipeline = pipeline.to("cuda")
  pipeline.enable_model_cpu_offload()
  return pipeline


def generate_image(prompt, pipeline):
  image = pipeline(
      prompt,
      height=1024,
      width=1024,
      guidance_scale=3.5,
      num_inference_steps=50,
      max_sequence_length=512,
      generator=torch.Generator("cpu").manual_seed(seed),
  ).images[0]
  return image


if __name__ == "__main__":
  args = parse_args()
  prompt_pattern = args.prompt
  summarize_model_suffix = args.summarize_model.split("/")[-1]
  max_token = args.max_token
  wit_input_file = project_root / "data" / "wit" / f"en.wit.2k.prompt.summary.{summarize_model_suffix}.{max_token}.jsonl"
  model_name = "black-forest-labs/FLUX.1-dev"
  model_name_suffix = model_name.split("/")[-1]
  if prompt_pattern == 3:
    image_dir = project_root / "generated_images" / "pattern3" / model_name_suffix / f"{summarize_model_suffix}.{max_token}"
  elif prompt_pattern == 4:
    image_dir = project_root / "generated_images" / "pattern4" / model_name_suffix / f"{summarize_model_suffix}.{max_token}"
  image_dir.mkdir(exist_ok=True, parents=True)
  pipeline = initizalize_model(model_name)
  logger.info(f'image_dir: {image_dir}')

  wit_data = load_jsonl(wit_input_file)
  for i, line in enumerate(wit_data):
    try:
      logger.info(f'Iteration {i} / {len(wit_data)}')
      if prompt_pattern == 3:
        prompt = line["prompt3"].strip()
      elif prompt_pattern == 4:
        prompt = line["prompt4"].strip()
      else:
        raise ValueError(f"Invalid prompt pattern: {prompt_pattern}")
      image = generate_image(prompt, pipeline)
      image_path = image_dir / f"{i}.png"
      image.save(image_path)
      logger.info(f"Image is saved at {image_path}")
      if args.debug:
        if i == 10:
          break
    except Exception as e:
      logger.error(f"Error: {e}")

  logger.info("All images are generated")
  logger.info(f'Generated images are saved at {image_dir}')
