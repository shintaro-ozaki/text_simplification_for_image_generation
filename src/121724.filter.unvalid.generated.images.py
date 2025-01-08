from pathlib import Path
import json
import os
from PIL import Image
import argparse


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_dir', type=str, required=True)
  parser.add_argument('--output_dir', type=str, required=True)
  return parser.parse_args()


project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')


def check_images_in_directory(directory):
  supported_extensions = ('.png', '.jpg', '.jpeg')
  files = [f for f in os.listdir(directory) if f.lower().endswith(supported_extensions)]
  results = {}

  for i, file in enumerate(files):
    file_path = directory / file
    try:
      with Image.open(file_path) as img:
        img.verify()  # ファイルが有効な画像かどうかを確認
    except Exception as e:
      results[file] = f"Invalid ({str(e)})"
      # そのファイルを削除
      # os.remove(file_path)
  return results


if __name__ == "__main__":
  args = parse_args()
  input_dir = Path(args.input_dir)
  output_dir = Path(args.output_dir)
  # input_dirの.pngを取得
  results = check_images_in_directory(input_dir)
  print(f'Input directory: {input_dir}')
  print(f'Output directory: {output_dir}')
  print(results)
  # resultsが何件かあるかprint
  print(f"Found {len(results)} invalid images")
