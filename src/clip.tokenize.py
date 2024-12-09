from transformers import CLIPTokenizer

def initialize_clip_tokenizer(tokenizer_name):
  tokenizer = CLIPTokenizer.from_pretrained(tokenizer_name)
  return tokenizer

def tokenize_by_clip_tokenizer(tokenizer, text):
  tokens = tokenizer(text, padding="max_length", max_length=77, truncation=True, return_tensors="pt")
  return tokens

if __name__ == "__main__":
  text = "This is an example sentence for tokenization."
  tokenizer_name = "openai/clip-vit-base-patch32"
  tokenizer = initialize_clip_tokenizer(tokenizer_name)
  tokens = tokenize_by_clip_tokenizer(tokenizer, text)
  decoded_text = tokenizer.decode(tokens["input_ids"][0])
  print("Decoded Text:", decoded_text)
