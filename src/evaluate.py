"""
画像間の評価を行う。
ref: wit
pred: generated image

1. CLIPScore, which measures the text-image alignment
2. Improved Aesthetic Predictor, which measures how good-looking an image is
3. ImageReward, which measures the human rating of an image
4. Human Preference Score, which measures the human preference of an image
5. X-IQE, a comprehensive and explainable metric based on visual LLMs (MiniGPT-4)
"""
