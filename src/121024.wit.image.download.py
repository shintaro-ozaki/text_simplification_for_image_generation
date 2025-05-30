from pathlib import Path
import json
import requests
from loguru import logger
from PIL import Image

# /cl/home2/shintaro/text_simplification_for_image_generation/data/wit/en.wit.2k.jsonl


def check_image_is_valid(image_file_path):
  try:
    with Image.open(image_file_path) as img:
      img.verify()  # ファイルが有効な画像かどうかを確認
    return True
  except Exception as e:
    logger.info(f"Invalid: {image_file_path}: {e}")
    return False


def load_jsonl(file_path):
  with open(file_path, 'r') as f:
    return [json.loads(l) for l in f.readlines()]


project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')
wit_data_path = project_root / 'data/wit/en.wit.2k.prompt.jsonl'
wit_data = load_jsonl(wit_data_path)
image_output_dir = project_root / 'wit_images_2k'
image_output_dir.mkdir(exist_ok=True, parents=True)

for i, data in enumerate(wit_data):
  image_url = data['image_url']
  try:
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    response = requests.get(image_url, timeout=10, headers=headers)
    response.raise_for_status()

    file_extension = image_url.split('.')[-1]
    if file_extension not in ['jpg', 'jpeg', 'png']:
      file_extension = 'jpg'
    image_file_path = image_output_dir / f"{i}.{file_extension}"

    with open(image_file_path, 'wb') as image_file:
      image_file.write(response.content)
    logger.info(f"Downloaded: {image_file_path}")

    if not check_image_is_valid(image_file_path):
      logger.info(f"Invalid: {image_file_path}")
      # 削除
      image_file_path.unlink()

  except requests.exceptions.RequestException as e:
    logger.info(f"Failed to download {image_url}: {e}")

logger.info("Done")
