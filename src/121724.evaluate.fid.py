import torch
from torch import nn
from torchvision.models import inception_v3
import cv2
import multiprocessing
import numpy as np
import glob
import os
from scipy import linalg
from pathlib import Path
import json
import argparse


def save_json(data, path):
  with open(path, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


project_root = Path(
    '/cl/home2/shintaro/text_simplification_for_image_generation')


def to_cuda(elements):
  if torch.cuda.is_available():
    return elements.cuda()
  return elements


class PartialInceptionNetwork(nn.Module):

  def __init__(self, transform_input=True):
    super().__init__()
    self.inception_network = inception_v3(pretrained=True)
    self.inception_network.Mixed_7c.register_forward_hook(self.output_hook)
    self.transform_input = transform_input

  def output_hook(self, module, input, output):
    self.mixed_7c_output = output

  def forward(self, x):
    assert x.shape[1:] == (3, 299, 299), "Expected input shape to be: (N,3,299,299)" + \
                                         ", but got {}".format(x.shape)
    x = x * 2 - 1  # Normalize to [-1, 1]
    self.inception_network(x)
    activations = self.mixed_7c_output
    activations = torch.nn.functional.adaptive_avg_pool2d(activations, (1, 1))
    activations = activations.view(x.shape[0], 2048)
    return activations


def get_activations(images, batch_size):
  assert images.shape[1:] == (3, 299, 299), "Expected input shape to be: (N,3,299,299)" + \
                                            ", but got {}".format(images.shape)

  num_images = images.shape[0]
  inception_network = PartialInceptionNetwork()
  inception_network = to_cuda(inception_network)
  inception_network.eval()
  n_batches = int(np.ceil(num_images / batch_size))
  inception_activations = torch.zeros(
      (num_images, 2048),
      dtype=torch.float32,
      device='cuda' if torch.cuda.is_available() else 'cpu')

  for batch_idx in range(n_batches):
    start_idx = batch_size * batch_idx
    end_idx = batch_size * (batch_idx + 1)

    ims = images[start_idx:end_idx]
    ims = to_cuda(ims)
    activations = inception_network(ims)
    activations = activations.detach()
    inception_activations[start_idx:end_idx, :] = activations

  return inception_activations.cpu().numpy()


def calculate_activation_statistics(images, batch_size):
  act = get_activations(images, batch_size)
  mu = np.mean(act, axis=0)
  sigma = np.cov(act, rowvar=False)
  return mu, sigma


def calculate_frechet_distance(mu1, sigma1, mu2, sigma2, eps=1e-6):
  mu1 = np.atleast_1d(mu1)
  mu2 = np.atleast_1d(mu2)

  sigma1 = np.atleast_2d(sigma1)
  sigma2 = np.atleast_2d(sigma2)

  assert mu1.shape == mu2.shape, "Training and test mean vectors have different lengths"
  assert sigma1.shape == sigma2.shape, "Training and test covariances have different dimensions"

  diff = mu1 - mu2
  # product might be almost singular
  covmean, _ = linalg.sqrtm(sigma1.dot(sigma2), disp=False)
  if not np.isfinite(covmean).all():
    msg = "fid calculation produces singular product; adding %s to diagonal of cov estimates" % eps
    warnings.warn(msg)
    offset = np.eye(sigma1.shape[0]) * eps
    covmean = linalg.sqrtm((sigma1 + offset).dot(sigma2 + offset))

  # numerical error might give slight imaginary component
  if np.iscomplexobj(covmean):
    if not np.allclose(np.diagonal(covmean).imag, 0, atol=1e-3):
      m = np.max(np.abs(covmean.imag))
      raise ValueError("Imaginary component {}".format(m))
    covmean = covmean.real

  tr_covmean = np.trace(covmean)

  return diff.dot(diff) + np.trace(sigma1) + np.trace(sigma2) - 2 * tr_covmean


def preprocess_image(im):
  assert im.shape[2] == 3
  assert len(im.shape) == 3
  if im.dtype == np.uint8:
    im = im.astype(np.float32) / 255
  im = cv2.resize(im, (299, 299))
  im = np.rollaxis(im, axis=2)
  im = torch.from_numpy(im)
  assert im.max() <= 1.0
  assert im.min() >= 0.0
  assert im.dtype == torch.float32
  assert im.shape == (3, 299, 299)
  return im


def preprocess_images(images, use_multiprocessing):
  if use_multiprocessing:
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
      jobs = []
      for im in images:
        job = pool.apply_async(preprocess_image, (im,))
        jobs.append(job)
      final_images = torch.zeros(images.shape[0], 3, 299, 299)
      for idx, job in enumerate(jobs):
        im = job.get()
        final_images[idx] = im
  else:
    final_images = torch.stack([preprocess_image(im) for im in images], dim=0)

  final_images = to_cuda(final_images)
  assert final_images.shape == (images.shape[0], 3, 299, 299)
  assert final_images.max() <= 1.0
  assert final_images.min() >= 0.0
  assert final_images.dtype == torch.float32
  return final_images


def calculate_fid(images1, images2, use_multiprocessing, batch_size):
  images1 = preprocess_images(images1, use_multiprocessing)
  images2 = preprocess_images(images2, use_multiprocessing)
  mu1, sigma1 = calculate_activation_statistics(images1, batch_size)
  mu2, sigma2 = calculate_activation_statistics(images2, batch_size)
  fid = calculate_frechet_distance(mu1, sigma1, mu2, sigma2)
  return fid


def load_images(path):
  image_paths = []
  image_extensions = ["png", "jpg", "jpeg"]
  for ext in image_extensions:
    print("Looking for images in", os.path.join(path, "*.{}".format(ext)))
    for impath in Path(path).glob(f'**/*.{ext}'):
      image_paths.append(str(impath))

  assert len(image_paths) > 0, "No images found in the specified directory."

  target_shape = None
  for impath in image_paths:
    first_image = cv2.imread(impath)
    if first_image is not None:
      target_shape = first_image.shape[:2]
      break
  assert target_shape is not None, "No valid images could be loaded."

  final_images = []
  for impath in image_paths:
    im = cv2.imread(impath)
    if im is None:
      print(f"Warning: Unable to load image {impath}. Skipping.")
      continue
    im = im[:, :, ::-1]  # Convert from BGR to RGB
    im_resized = cv2.resize(
        im, (target_shape[1], target_shape[0]))  # Resize to target shape
    final_images.append(im_resized)

  assert len(final_images) > 0, "No valid images could be processed."
  final_images = np.array(final_images, dtype=first_image.dtype)
  return final_images


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--pattern', type=int, required=True)
  parser.add_argument('--diffusion_model', type=str, required=True)
  parser.add_argument('--summarize_model', type=str)
  parser.add_argument('--batch_size', type=int, default=1)
  return parser.parse_args()


if __name__ == '__main__':
  args = parse_args()
  pattern = args.pattern
  diffusion_model = args.diffusion_model
  diffusion_model_suffix = diffusion_model.split('/')[-1]
  batch_size = args.batch_size
  # /cl/home2/shintaro/text_simplification_for_image_generation/wit_images_2k
  reference_images_dir = project_root / 'wit_images_2k'
  reference_images = load_images(reference_images_dir)

  if not (pattern == 1 or pattern == 2):
    summarize_model = args.summarize_model
    summarize_model_suffix = summarize_model.split('/')[-1]
  if pattern == 1 or pattern == 2:
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}'
    output_eval_dir = project_root / 'evaluated-fid' / f'pattern{pattern}' / f'{diffusion_model_suffix}'
    response = {
        'pattern': pattern,
        'diffusion_model': diffusion_model_suffix,
    }
  if pattern == 3:
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.512'
    output_eval_dir = project_root / 'evaluated-fid' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.512'
    response = {
        'pattern': pattern,
        'diffusion_model': diffusion_model_suffix,
        'summarize_model': summarize_model_suffix,
        'max_tokens': 512,
    }
  elif pattern == 4:
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200'
    output_eval_dir = project_root / 'evaluated-fid' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200'
    response = {
        'pattern': pattern,
        'diffusion_model': diffusion_model_suffix,
        'summarize_model': summarize_model_suffix,
        'max_tokens': 200,
    }
  elif pattern == 5:
    model_generated_dir = project_root / 'generated_images' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200.iterative3'
    output_eval_dir = project_root / 'evaluated-fid' / f'pattern{pattern}' / f'{diffusion_model_suffix}' / f'{summarize_model_suffix}.200.iterative3'
    response = {
        'pattern': pattern,
        'diffusion_model': diffusion_model_suffix,
        'summarize_model': summarize_model_suffix,
        'max_tokens': 200,
        'iterative': 3,
    }

  model_generated_images = load_images(model_generated_dir)
  fid_value = calculate_fid(reference_images, model_generated_images, False,
                            batch_size)
  response['fid'] = fid_value
  print(fid_value)

  output_eval_dir.mkdir(parents=True, exist_ok=True)
  save_json(response, output_eval_dir / 'fid.json')
