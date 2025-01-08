from pathlib import Path
import json


def save_json(data, path):
  with open(path, 'w') as f:
    json.dump(data, f, indent=2)


if __name__ == "__main__":
  project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')
  data_root = project_root / 'data'
  clipscore_file = data_root / 'clipscore.json'

  response = {
      'pattern1': {
          'stable-diffusion-3.5-large': 69.97618103027344,
          'IF-I-L-v1.0': 67.84034729003906,
          'dreamlike-photoreal-2.0': 67.91835021972656,
      },
      'pattern2': {
          'stable-diffusion-3.5-large': 69.97618103027344,
          'IF-I-L-v1.0': 67.84034729003906,
          'dreamlike-photoreal-2.0': 67.91835021972656,
      },
      'pattern3': {
          'Llama-3.1-70B-Instruct': {
              'dreamlike-photoreal-2.0': 64.2811279296875,
              'IF-I-L-v1.0': 63.63726806640625,
              'stable-diffusion-3.5-large': 66.28581237792969,
          },
          'LLama-3.1-8B-Instruct': {
              'dreamlike-photoreal-2.0': 63.25804138183594,
              'IF-I-L-v1.0': 61.77434539794922,
              'stable-diffusion-3.5-large': 64.9386215209961,
          },
          'LLama-3.3-70B-Instruct': {
              'dreamlike-photoreal-2.0': 63.89054489135742,
              'IF-I-L-v1.0': 63.37232971191406,
              'stable-diffusion-3.5-large': 65.84052276611328,
          },
          'openai': {
              'dreamlike-photoreal-2.0': 65.50823974609375,
              'IF-I-L-v1.0': 64.92284393310547,
              'stable-diffusion-3.5-large': 64.23778533935547,
          },
          'Phi-3.5-mini-instruct': {
              'dreamlike-photoreal-2.0': 56.44272232055664,
              'IF-I-L-v1.0': 55.470733642578125,
              'stable-diffusion-3.5-large': 56.398372650146484,
          },
          'Qwen2.5-72B-Instruct': {
              'dreamlike-photoreal-2.0': 66.36167907714844,
              'IF-I-L-v1.0': 66.38899993896484,
              'stable-diffusion-3.5-large': 67.52140045166016,
          },
      },
      'pattern4': {
          'Llama-3.1-70B-Instruct': {
              'dreamlike-photoreal-2.0': 63.861122131347656,
              'IF-I-L-v1.0': 63.47257995605469,
              'stable-diffusion-3.5-large': 65.01911163330078,
          },
          'LLama-3.1-8B-Instruct': {
              'dreamlike-photoreal-2.0': 63.42265319824219,
              'IF-I-L-v1.0': 62.8231964111328,
              'stable-diffusion-3.5-large': 64.34114074707031,
          },
          'LLama-3.3-70B-Instruct': {
              'dreamlike-photoreal-2.0': 65.44915008544922,
              'IF-I-L-v1.0': 65.3926773071289,
              'stable-diffusion-3.5-large': 66.55513763427734,
          },
          'Phi-3.5-mini-instruct': {
              'dreamlike-photoreal-2.0': 55.74161148071289,
              'IF-I-L-v1.0': 54.722381591796875,
              'stable-diffusion-3.5-large': 56.09598159790039,
          },
          'Qwen2.5-72B-Instruct': {
              'dreamlike-photoreal-2.0': 62.83840560913086,
              'IF-I-L-v1.0': 62.77419662475586,
              'stable-diffusion-3.5-large': 63.72092056274414,
          },
      },
      'pattern5': {
          'Llama-3.1-70B-Instruct': {
              'dreamlike-photoreal-2.0': 63.861122131347656,
              'IF-I-L-v1.0': 63.47257995605469,
              'stable-diffusion-3.5-large': 65.01911163330078,
          },
          'LLama-3.1-8B-Instruct': {
              'dreamlike-photoreal-2.0': 63.42265319824219,
              'IF-I-L-v1.0': 62.82319641113281,
              'stable-diffusion-3.5-large': 64.34114074707031,
          },
          'LLama-3.3-70B-Instruct': {
              'dreamlike-photoreal-2.0': 65.44915008544922,
              'IF-I-L-v1.0': 65.3926773071289,
              'stable-diffusion-3.5-large': 66.55513763427734,
          },
          'Phi-3.5-mini-instruct': {
              'dreamlike-photoreal-2.0': 55.74161148071289,
              'IF-I-L-v1.0': 54.722381591796875,
              'stable-diffusion-3.5-large': 56.09598159790039,
          },
          'Qwen2.5-72B-Instruct': {
              'dreamlike-photoreal-2.0': 62.83840560913086,
              'IF-I-L-v1.0': 62.77419662475586,
              'stable-diffusion-3.5-large': 63.72092056274414,
          },
      },
  }

  save_json(response, clipscore_file)
  print(f'saved: {clipscore_file}')
