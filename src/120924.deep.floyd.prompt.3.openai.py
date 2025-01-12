# https://huggingface.co/DeepFloyd/IF-II-M-v1.0
from diffusers import DiffusionPipeline
from diffusers.utils import pt_to_pil
import torch
from dotenv import load_dotenv
import os
import json
from pathlib import Path
import argparse
from loguru import logger

load_dotenv()
seed = 42
project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--prompt', type=int, required=True, choices=[3])
  parser.add_argument('--debug', action='store_true')
  return parser.parse_args()


def load_jsonl(file_path):
  with open(file_path, "r") as f:
    return [json.loads(line) for line in f]


def initizalize_model():
  stage_1 = DiffusionPipeline.from_pretrained(
      "DeepFloyd/IF-I-L-v1.0",
      variant="fp16",
      torch_dtype=torch.float16,
      token=os.getenv("WRITE_TOKEN"))
  stage_1.enable_model_cpu_offload()

  stage_2 = DiffusionPipeline.from_pretrained(
      "DeepFloyd/IF-II-L-v1.0",
      text_encoder=None,
      variant="fp16",
      torch_dtype=torch.float16,
      token=os.getenv("WRITE_TOKEN"))
  stage_2.enable_model_cpu_offload()

  safety_modules = {
      "feature_extractor": stage_1.feature_extractor,
      "safety_checker": stage_1.safety_checker,
      "watermarker": stage_1.watermarker
  }
  stage_3 = DiffusionPipeline.from_pretrained(
      "stabilityai/stable-diffusion-x4-upscaler",
      **safety_modules,
      torch_dtype=torch.float16,
      token=os.getenv("WRITE_TOKEN"))
  stage_3.enable_model_cpu_offload()
  return stage_1, stage_2, stage_3


def generate_image(prompt, stage_1, stage_2, stage_3):
  prompt_embeds, negative_embeds = stage_1.encode_prompt(prompt)
  generator = torch.manual_seed(seed)
  image = stage_1(
      prompt_embeds=prompt_embeds,
      negative_prompt_embeds=negative_embeds,
      generator=generator,
      output_type="pt").images
  image = stage_2(
      image=image,
      prompt_embeds=prompt_embeds,
      negative_prompt_embeds=negative_embeds,
      generator=generator,
      output_type="pt").images
  image = stage_3(prompt=prompt, image=image, generator=generator, noise_level=100).images
  return image[0]


# # {"id": "batch_req_675a98c12c388190802118ca61e0b6da", "custom_id": "request-0", "response": {"status_code": 200, "request_id": "96ff7bde03aaf2d439c40e7e5f929231", "body": {"id": "chatcmpl-AdXpODq05zcAOA8sP48UThr23JNLs", "object": "chat.completion", "created": 1733988190, "model": "gpt-4o-mini-2024-07-18", "choices": [{"index": 0, "message": {"role": "assistant", "content": "SummaryStart: The rock cycle is a geological process that explains the transformation and relationships between igneous, sedimentary, and metamorphic rocks over time, driven by forces like plate tectonics and the water cycle. Each rock type can change into another through various natural processes, illustrating the continuous nature of rock formation and alteration.\n\nOptimal Prompt: \"Illustration of the rock cycle showing igneous, sedimentary, and metamorphic rocks in a continuous transformation process.\"", "refusal": null}, "logprobs": null, "finish_reason": "stop"}], "usage": {"prompt_tokens": 866, "completion_tokens": 93, "total_tokens": 959, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 0, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}}, "system_fingerprint": "fp_818c284075"}}, "error": null}

if __name__ == "__main__":
  args = parse_args()
  prompt_pattern = args.prompt
  summarize_model_suffix = 'openai'
  max_token = 512
  wit_input_file = project_root / "data" / "wit" / f"en.wit.2k.prompt.summary.openai.{max_token}.jsonl"
  model_name = "DeepFloyd/IF-I-L-v1.0"
  model_name_suffix = model_name.split('/')[-1]
  if prompt_pattern == 3:
    image_dir = project_root / "generated_images" / "pattern3" / model_name_suffix / f"{summarize_model_suffix}.{max_token}"
  image_dir.mkdir(exist_ok=True, parents=True)
  stage_1, stage_2, stage_3 = initizalize_model()
  logger.info(f'image_dir: {image_dir}')

  wit_data = load_jsonl(wit_input_file)
  for i, line in enumerate(wit_data):
    logger.info(f'Iteration {i} / {len(wit_data)}')
    try:
      if prompt_pattern == 3:
        content = line["response"]["body"]["choices"][0]["message"]["content"].split('\n\n')[0]
        prompt = content.replace('SummaryStart:', '')
        prompt = prompt.split('<SummaryEnd>')[0]
        prompt = prompt.strip()
      else:
        raise ValueError(f"Invalid prompt pattern: {prompt_pattern}")
      image = generate_image(prompt, stage_1, stage_2, stage_3)
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
