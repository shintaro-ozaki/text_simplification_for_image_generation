"""
latexに結果の表を生成するためのスクリプト
"""

from pathlib import Path
import json

def load_json(file):
  with open(file, "r") as f:
    return json.load(f)



if __name__ == "__main__":
  project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')
  summarization_models = [
    'Phi-3.5-mini-instruct',
    'Llama-3.1-8B-Instruct',
    'Llama-3.1-70B-Instruct',
    'Llama-3.3-70B-Instruct',
    'Qwen2.5-72B-Instruct',
    'openai',
  ]
  diffusion_models = [
    'stable-diffusion-3.5-large',
    'IF-I-L-v1.0',
    'dreamlike-photoreal-2.0',
  ]
  patterns = [1, 2, 3, 4, 5]
  metrics = ['inception_score', 'fid', 'lpips', 'clipscore']
  # text_simplification_for_image_generation/evaluated-IS/pattern1/IF-I-L-v1.0
  clip_score = load_json(project_root / 'data' / 'clipscore.json')

  # 列は パターン & 要約モデル & 拡散モデル & IS & FID & LPIPS
  # パターン1、パターン2は要約モデルがない
  # ヘッダーなどは要らず、結果のみを出力する
  print('pattern, summarization_model, diffusion_model, is, fid, lpips')
  for pattern in patterns:
    if pattern == 1 or pattern == 2:
      for diffusion_model in diffusion_models:
        try:
          is_result = load_json( project_root / 'evaluated-IS' / f'pattern{pattern}' / diffusion_model / f'inception_score.json')
        except Exception as e:
          is_result = {'mean_score': 0}
          print(e)
        try:
          fid_result = load_json(project_root / 'evaluated-fid' / f'pattern{pattern}' / diffusion_model / 'fid.json')
        except:
          fid_result = {'fid': 0}
        try:
          lpips_result = load_json(project_root / 'evaluated-lpips' / f'pattern{pattern}' / diffusion_model / f'lpips.json')
        except:
          lpips_result = {'avg_lpips_value': 0}
        print(f'{pattern} & - & {diffusion_model} & {is_result["mean_score"]:.2f} & {fid_result["fid"]:.2f} & {lpips_result["avg_lpips_value"]:.2f}  & {clip_score[f'pattern{pattern}'][diffusion_model]:.2f} \\\\')
    else:
      for summarization_model in summarization_models:
        if (pattern == 4 or pattern == 5) and summarization_model == 'openai':
          continue
        for diffusion_model in diffusion_models:
          try:
            if pattern == 3:
              is_result = load_json( project_root / 'evaluated-IS' / f'pattern{pattern}' / diffusion_model / f'{summarization_model}.512' / f'inception_score.json')
            elif pattern == 4:
              is_result = load_json( project_root / 'evaluated-IS' / f'pattern{pattern}' / diffusion_model / f'{summarization_model}.200' / f'inception_score.json')
            elif pattern == 5:
              is_result = load_json( project_root / 'evaluated-IS' / f'pattern{pattern}' / diffusion_model / f'{summarization_model}.200.iterative3' / f'inception_score.json')
          except Exception as e:
            is_result = {'mean_score': 0}
          try:
            if pattern == 3:
              fid_result = load_json(project_root / 'evaluated-fid' / f'pattern{pattern}' / diffusion_model / f'{summarization_model}.512' / 'fid.json')
            elif pattern == 4:
              fid_result = load_json(project_root / 'evaluated-fid' / f'pattern{pattern}' / diffusion_model / f'{summarization_model}.200' / 'fid.json')
            elif pattern == 5:
              fid_result = load_json(project_root / 'evaluated-fid' / f'pattern{pattern}' / diffusion_model / f'{summarization_model}.200.iterative3' / 'fid.json')
          except:
            fid_result = {'fid': 0}
          try:
            if pattern == 3:
              lpips_result = load_json(project_root / 'evaluated-lpips' / f'pattern{pattern}' / diffusion_model / f'{summarization_model}.512' / f'lpips.json')
            elif pattern == 4:
              lpips_result = load_json(project_root / 'evaluated-lpips' / f'pattern{pattern}' / diffusion_model / f'{summarization_model}.200' / f'lpips.json')
            elif pattern == 5:
              lpips_result = load_json(project_root / 'evaluated-lpips' / f'pattern{pattern}' / diffusion_model / f'{summarization_model}.200.iterative3' / f'lpips.json')
          except:
            lpips_result = {'avg_lpips_value': 0}
          print(f'{pattern} & {summarization_model} & {diffusion_model} & {is_result["mean_score"]:.2f} & {fid_result["fid"]:.2f} & {lpips_result["avg_lpips_value"]:.2f} & {clip_score[f'pattern{pattern}'][summarization_model][diffusion_model]:.2f} \\\\')
