"""
wit_images_2kの番号のみを残しそれ以外は必要ない。
"""
from pathlib import Path
import json
import argparse
import shutil
import logging
import sys

logging.basicConfig(
    format="| %(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
    stream=sys.stdout,
)
logger: logging.Logger = logging.getLogger(__name__)

project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')


def load_jsonl(file_path):
  with open(file_path, "r") as f:
    return [json.loads(line) for line in f]


def save_jsonl(file_path, data):
  with open(file_path, "w") as f:
    for line in data:
      f.write(json.dumps(line, ensure_ascii=Falsea) + "\n")


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--pattern', type=int, required=True)
  parser.add_argument('--diffusion_model', type=str, required=True)
  parser.add_argument('--summarize_model', type=str)
  return parser.parse_args()


# /cl/home2/shintaro/text_simplification_for_image_generation/wit_images_2k
def main(model_generated_dir, filtered_model_generated_dir):
  reference_wit2k_dir = project_root / 'wit_images_2k'
  reference_wit2k_files = list(reference_wit2k_dir.glob('*'))
  reference_wit2k_files = sorted(reference_wit2k_files)
  for i, reference_wit2k_file in enumerate(reference_wit2k_files):
    logger.info(f'{i+1} / {len(reference_wit2k_files)}')
    try:
      image_num = int(reference_wit2k_file.stem)
      model_generated_file = model_generated_dir / f'{image_num}.png'
      filtered_model_generated_file = filtered_model_generated_dir / f'{image_num}.png'
      shutil.copy(model_generated_file, filtered_model_generated_file)
    except Exception as e:
      logger.error(f'Error: {e}')
  logger.info(f'Done! {filtered_model_generated_dir}')


if __name__ == '__main__':
  args = parse_args()
  pattern = args.pattern
  diffusion_model = args.diffusion_model
  diffusion_model_suffix = diffusion_model.split('/')[-1]
  if not (pattern == 1 or pattern == 2):
    summarize_model = args.summarize_model
    summarize_model_suffix = summarize_model.split('/')[-1]
  if pattern == 1 or pattern == 2:
    # /cl/home2/shintaro/text_simplification_for_image_generation/generated_images/pattern1/dreamlike-photoreal-2.0
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}'
    filtered_model_generated_dir = project_root / 'filtered_generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}'
  if pattern == 3:
    # /cl/home2/shintaro/text_simplification_for_image_generation/generated_images/pattern3/dreamlike-photoreal-2.0/Llama-3.1-70B-Instruct.512
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.512'
    filtered_model_generated_dir = project_root / 'filtered_generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.512'
  elif pattern == 4:
    # /cl/home2/shintaro/text_simplification_for_image_generation/generated_images/pattern4/IF-I-L-v1.0/Llama-3.1-8B-Instruct.200/0.png
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200'
    filtered_model_generated_dir = project_root / 'filtered_generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200'
  elif pattern == 5:
    # /cl/home2/shintaro/text_simplification_for_image_generation/generated_images/pattern5/dreamlike-photoreal-2.0/Llama-3.1-8B-Instruct.200.iterative3
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200.iterative3'
    filtered_model_generated_dir = project_root / 'filtered_generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200.iterative3'
  filtered_model_generated_dir.mkdir(parents=True, exist_ok=True)
  main(model_generated_dir, filtered_model_generated_dir)
