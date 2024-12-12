# text-simplification-for-image-generation
https://www.notion.so/Text-Simplification-for-Image-Generation-d77e57b800d5484db9efcd695b1fd766


モデルのインプットには77トークンしか入らない。
1. captionのみ
2. エンティティの各所を説明したもの
3. 普通に要約したもの
4. xトークンあるので、77トークンに納めなさいとする。
5. iterativeにもやってみる。　(n = 10)

要約モデルは、
- llama3-70b
- Qwen2.5-70b
- phi-3.5

画像の生成モデルには
- diffusion model3.5
- DeepFloyd
- SG161222/Realistic_Vision_V1.4
