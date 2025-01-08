import argparse
import os
import lpips
from tqdm import tqdm
from loguru import logger
from pathlib import Path
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import torch
import json


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d0', '--dir0', type=str, default='./imgs/ex_dir0')
  parser.add_argument('-d1', '--dir1', type=str, default='./imgs/ex_dir1')
  parser.add_argument('-o', '--out', type=str, default='./imgs/example_dists.txt')
  parser.add_argument('-v', '--version', type=str, default='0.1')
  parser.add_argument('--use_gpu', action='store_true', help='turn on flag to use GPU')
  return parser.parse_args()


def save_jsonl(file, data):
  with open(file, 'w') as f:
    for line in data:
      f.write(json.dumps(line, ensure_ascii=False) + '\n')


def calculate_lpips(ref_dir, pred_dir, output_file, use_gpu):
  loss_fn = lpips.LPIPS(net='alex', version='0.1')
  if use_gpu:
    loss_fn.cuda()

  ref_files = list(ref_dir.glob("*"))
  pred_files = list(pred_dir.glob("*"))

  transform = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])

  output_list = []
  for pred_file, ref_file in tqdm(zip(pred_files, ref_files)):
    try:
      img0 = lpips.load_image(str(ref_file))
      img1 = lpips.load_image(str(pred_file))

      img0 = Image.fromarray(
          (img0 *
           255).astype(np.uint8)) if img0.max() <= 1 else Image.fromarray(img0.astype(np.uint8))
      img1 = Image.fromarray(
          (img1 *
           255).astype(np.uint8)) if img1.max() <= 1 else Image.fromarray(img1.astype(np.uint8))

      img0 = transform(img0).unsqueeze(0)
      img1 = transform(img1).unsqueeze(0)

      if use_gpu:
        img0 = img0.cuda()
        img1 = img1.cuda()

      dist01 = loss_fn.forward(img0, img1)
      logger.info(f'{ref_file.name}: {dist01.item():.3f}')

      output_list.append({
          'ref_file': ref_file.name,
          'lpips_value': dist01.item(),
      })
    except Exception as e:
      logger.error(f'Error processing {ref_file.name} and {pred_file.name}')
      logger.error(e)

  # 平均を取る
  avg_lpips_value = np.mean([d['lpips_value'] for d in output_list])
  avg_output_list = [{'avg_lpips_value': avg_lpips_value}]
  output_dir = output_file.parent
  output_dir.mkdir(parents=True, exist_ok=True)
  save_jsonl(output_file, avg_output_list)
  logger.info(f'Saved LPIPS results to {output_file}')


if __name__ == "__main__":
  args = parse_args()
  calculate_lpips(Path(args.dir0), Path(args.dir1), Path(args.out), args.use_gpu)
  logger.info(f"LPIPS calculation completed. Results saved to: {args.out}")
