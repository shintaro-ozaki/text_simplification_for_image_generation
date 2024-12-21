import os
import glob
import numpy as np
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import torch.nn.functional as F
import json
import argparse
from pathlib import Path
from tqdm import tqdm

project_root = Path(
    '/cl/home2/shintaro/text_simplification_for_image_generation')

MODEL_DIR = '/tmp/imagenet'
DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'


def save_json(file_path, data):
  with open(file_path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


def download_inception_model():
  if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
  filename = DATA_URL.split('/')[-1]
  filepath = os.path.join(MODEL_DIR, filename)
  if not os.path.exists(filepath):
    import urllib.request

    def _progress(count, block_size, total_size):
      print(
          f"\r>> Downloading {filename} {count * block_size / total_size * 100:.1f}%",
          end="")

    filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
    print(f"\nSuccessfully downloaded {filename}")
  return filepath


def load_inception_model():
  model = models.inception_v3(pretrained=True, transform_input=False)
  model.eval()
  return model


# Preprocess input images to match InceptionV3 requirements
def preprocess_image(image):
  transform = transforms.Compose([
      transforms.Resize((299, 299)),
      transforms.ToTensor(),
      transforms.Normalize(
          mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
  ])
  return transform(image).unsqueeze(0)


def get_inception_score(images, model, splits=10):
  assert isinstance(images, list)
  assert all(isinstance(img, np.ndarray) for img in images)
  assert all(len(img.shape) == 3 for img in images)

  inps = torch.cat([preprocess_image(Image.fromarray(img)) for img in images],
                   dim=0)
  bs = 100  # Batch size
  preds = []

  with torch.no_grad():
    for i in range(0, len(inps), bs):
      batch = inps[i:i + bs]
      preds.append(F.softmax(model(batch), dim=1).cpu().numpy())

  preds = np.concatenate(preds, axis=0)
  scores = []

  for i in tqdm(range(splits)):
    part = preds[(i * preds.shape[0] // splits):((i + 1) * preds.shape[0] //
                                                 splits), :]
    kl = part * (
        np.log(part) - np.log(np.expand_dims(np.mean(part, axis=0), 0)))
    kl = np.mean(np.sum(kl, axis=1))
    scores.append(np.exp(kl))

  return np.mean(scores), np.std(scores)


def load_images_from_directory(directory):
  filenames = glob.glob(os.path.join(directory, '*.*'))
  images = [
      np.array(Image.open(filename).convert('RGB')) for filename in filenames
  ]
  return images


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--pattern', type=int, required=True)
  parser.add_argument('--diffusion_model', type=str, required=True)
  parser.add_argument('--summarize_model', type=str)
  return parser.parse_args()


if __name__ == '__main__':
  args = parse_args()
  pattern = args.pattern
  diffusion_model = args.diffusion_model
  diffusion_model_suffix = diffusion_model.split('/')[-1]
  if not (pattern == 1 or pattern == 2):
    summarize_model = args.summarize_model
    summarize_model_suffix = summarize_model.split('/')[-1]
  if pattern == 1 or pattern == 2:
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}'
    output_eval_dir = project_root / 'evaluated-IS' / f'pattern{pattern}' / f'{diffusion_model_suffix}'
    response = {
        'pattern': pattern,
        'diffusion_model': diffusion_model_suffix,
    }
  if pattern == 3:
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.512'
    output_eval_dir = project_root / 'evaluated-IS' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.512'
    response = {
        'pattern': pattern,
        'diffusion_model': diffusion_model_suffix,
        'summarize_model': summarize_model_suffix,
        'max_tokens': 512,
    }
  elif pattern == 4:
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200'
    output_eval_dir = project_root / 'evaluated-IS' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200'
    response = {
        'pattern': pattern,
        'diffusion_model': diffusion_model_suffix,
        'summarize_model': summarize_model_suffix,
        'max_tokens': 200,
    }
  elif pattern == 5:
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200.iterative3'
    output_eval_dir = project_root / 'evaluated-IS' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200.iterative3'
    response = {
        'pattern': pattern,
        'diffusion_model': diffusion_model_suffix,
        'summarize_model': summarize_model_suffix,
        'max_tokens': 200,
        'iterative': 3,
    }
  output_eval_dir.mkdir(parents=True, exist_ok=True)
  model = load_inception_model()
  images = load_images_from_directory(model_generated_dir)
  print(f"Loaded {len(images)} images.")
  mean_score, std_score = get_inception_score(images, model)
  response['mean_score'] = float(mean_score)
  response['std_score'] = float(std_score)
  print(f"Inception Score: {mean_score:.2f} ± {std_score:.2f}")
  print(response)
  save_json(output_eval_dir / 'inception_score.json', response)
  print(f"Saved Inception Score to {output_eval_dir / 'inception_score.json'}")
