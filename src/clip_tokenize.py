from transformers import CLIPTokenizer


def initialize_clip_tokenizer(tokenizer_name):
  tokenizer = CLIPTokenizer.from_pretrained(tokenizer_name)
  return tokenizer


def tokenize_by_clip_tokenizer(tokenizer, text):
  tokens = tokenizer(
      text,
      max_length=77,
      truncation=True,
      return_tensors="pt",
  )
  return tokens


def clip_tokenized_words(tokenizer, text):
  tokens = tokenize_by_clip_tokenizer(tokenizer, text)
  decoded_text = tokenizer.decode(
      tokens["input_ids"][0], skip_special_tokens=True)
  count_words = len(decoded_text.split())
  return count_words


if __name__ == "__main__":
  text = "This is an example sentence for tokenization."
  # CLIP-L
  tokenizer_name = "openai/clip-vit-large-patch14"
  tokenizer = initialize_clip_tokenizer(tokenizer_name)
  count_words = clip_tokenized_words(tokenizer, text)
  print(count_words)
