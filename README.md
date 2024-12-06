# text-simplification-for-image-generation
https://www.notion.so/Text-Simplification-for-Image-Generation-d77e57b800d5484db9efcd695b1fd766


モデルのインプットには77トークンしか入らない。
1. captionのみ
2. エンティティの各所を説明したもの
3. xトークンあるので、77トークンに納めなさいとする。

要約モデルは、
- llama3-70b
- llama3-13b
- Qwen2.5-70b
- Qwen2.5-14b
- phi-3.5

画像の生成モデルには
- diffusion model3.5
- あと2つくらい
