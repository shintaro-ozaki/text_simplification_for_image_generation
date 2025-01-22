from pathlib import Path
import json


def load_json(file):
  with open(file, "r") as f:
    return json.load(f)

def find_best_scores(scores, higher_is_better):
  """
  Find the best score in a dictionary of scores.
  """
  if higher_is_better:
    return max(scores, key=scores.get)
  else:
    return min(scores, key=scores.get)



def compare_scores(base_scores, new_scores, metric, higher_is_better, flag):
  if higher_is_better:
    if new_scores > base_scores:
      return f"\\redbox{{{new_scores:.2f}}}"
    elif new_scores < base_scores:
      return f"\\bluebox{{{new_scores:.2f}}}"
  else:
    if new_scores < base_scores:
      return f"\\redbox{{{new_scores:.2f}}}"
    elif new_scores > base_scores:
      return f"\\bluebox{{{new_scores:.2f}}}"
  return f"{new_scores:.2f}"


if __name__ == "__main__":
  project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')
  summarization_models = [
      'Llama-3.1-8B-Instruct',
      'Llama-3.1-70B-Instruct',
      'Llama-3.3-70B-Instruct',
      'Qwen2.5-72B-Instruct',
      'openai',
  ]
  diffusion_models = [
      'dreamlike-photoreal-2.0', 'IF-I-L-v1.0', 'stable-diffusion-3.5-large'
  ]#clip,　t5, その両方, その両方
  patterns = [1, 4, 5]
  metrics = ['inception_score', 'fid', 'clipscore']
  clip_score = load_json(project_root / 'data' / 'clipscore.json')
  txt_clip_score = load_json(project_root / 'data' / 'text.clipscore.json')

  base_scores = {}
  last_pattern = None
  last_summarization_model = None

  for pattern in patterns:
    if last_pattern is not None and pattern != last_pattern:
      print("\\midrule")
    if pattern == 1 or pattern == 2:
      for diffusion_model in diffusion_models:
        try:
          is_result = load_json(project_root / 'evaluated-IS' / f'pattern{pattern}' /
                                diffusion_model / f'inception_score.json')
        except Exception as e:
          is_result = {'mean_score': 0}
          print(e)
        try:
          fid_result = load_json(project_root / 'evaluated-fid' / f'pattern{pattern}' /
                                 diffusion_model / 'fid.json')
        except:
          fid_result = {'fid': 0}

        # Store pattern 1 scores as baseline
        if pattern == 1:
          base_scores[diffusion_model] = {
              'is': is_result["mean_score"],
              'fid': fid_result["fid"],
              'clip_txt': txt_clip_score[f"pattern{pattern}"][diffusion_model],
              'clip_img': clip_score[f"pattern{pattern}"][diffusion_model]
          }

        encoder_model = ''
        if diffusion_model == "dreamlike-photoreal-2.0":
          encoder_model = "T5"
        elif diffusion_model == "IF-I-L-v1.0":
          encoder_model = "CLIP"
        elif diffusion_model == "FLUX.1-dev":
          # multilow{2}{*}{Both}
          encoder_model = "\\multirow{2}{*}{Both}"
        print(
            f'{pattern} & - & {diffusion_model} & {encoder_model} & {is_result["mean_score"]:.2f} & {fid_result["fid"]:.2f} & {txt_clip_score[f"pattern{pattern}"][diffusion_model]:.2f}  & {clip_score[f"pattern{pattern}"][diffusion_model]:.2f} \\\\'
        )
    else:
      for summarization_model in summarization_models:
        if (pattern == 4 or pattern == 5) and summarization_model == 'openai':
          continue
        if last_summarization_model is not None and summarization_model != last_summarization_model:
          print("\\cmidrule(lr){3-8}")
        for diffusion_model in diffusion_models:
          try:
            if pattern == 3:
              is_result = load_json(project_root / '1-evaluated-IS' / f'pattern{pattern}' /
                                    diffusion_model / f'{summarization_model}.512' /
                                    f'inception_score.json')
            elif pattern == 4:
              is_result = load_json(project_root / '1-evaluated-IS' / f'pattern{pattern}' /
                                    diffusion_model / f'{summarization_model}.200' /
                                    f'inception_score.json')
            elif pattern == 5:
              is_result = load_json(project_root / '1-evaluated-IS' / f'pattern{pattern}' /
                                    diffusion_model / f'{summarization_model}.200.iterative3' /
                                    f'inception_score.json')
          except Exception as e:
            is_result = {'mean_score': 0}
          try:
            if pattern == 3:
              fid_result = load_json(project_root / '1-evaluated-fid' / f'pattern{pattern}' /
                                     diffusion_model / f'{summarization_model}.512' / 'fid.json')
            elif pattern == 4:
              fid_result = load_json(project_root / '1-evaluated-fid' / f'pattern{pattern}' /
                                     diffusion_model / f'{summarization_model}.200' / 'fid.json')
            elif pattern == 5:
              fid_result = load_json(project_root / '1-evaluated-fid' / f'pattern{pattern}' /
                                     diffusion_model / f'{summarization_model}.200.iterative3' /
                                     'fid.json')
          except:
            fid_result = {'fid': 0}
          
          flag = False
          if pattern == 4 or pattern == 5:
            flag = True


          # Compare scores with pattern 1
          is_comparison = compare_scores(
              base_scores[diffusion_model]['is'],
              is_result['mean_score'],
              'is',
              higher_is_better=True,
              flag=flag
          )
          fid_comparison = compare_scores(
              base_scores[diffusion_model]['fid'], fid_result['fid'], 'fid', higher_is_better=False, flag=False)
          clip_txt_comparison = compare_scores(
              base_scores[diffusion_model]['clip_txt'],
              txt_clip_score[f"pattern{pattern}"][summarization_model][diffusion_model],
              'clip_txt',
              higher_is_better=True, flag=flag)
          clip_img_comparison = compare_scores(
              base_scores[diffusion_model]['clip_img'],
              clip_score[f"pattern{pattern}"][summarization_model][diffusion_model],
              'clip_img',
              higher_is_better=True, flag=flag
          )
          summarization_model_cell = f"\\multirow{{4}}{{*}}{{{summarization_model}}}" if diffusion_model == diffusion_models[
              0] else " "

          encoder_model = ''
          if diffusion_model == "dreamlike-photoreal-2.0":
            encoder_model = "T5"
          elif diffusion_model == "IF-I-L-v1.0":
            encoder_model = "CLIP"
          elif diffusion_model == "stable-diffusion-3.5-large":
            encoder_model = "Both"
          print(
              f'{pattern} & {summarization_model_cell} & {diffusion_model} & {encoder_model} & {is_comparison} & {fid_comparison} & {clip_txt_comparison}  & {clip_img_comparison} \\\\'
          )
          if encoder_model != '':
            print("\\cmidrule(lr){4-8}")
        last_summarization_model = summarization_model
    last_pattern = pattern
