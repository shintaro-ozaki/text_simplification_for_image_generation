import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)


def initialize_model(model_name, quantize_type, device, hf_token, flash_attn):
  tokenizer = AutoTokenizer.from_pretrained(
      model_name, token=hf_token, trust_remote_code=True)

  if tokenizer.pad_token is None:
    if tokenizer.eos_token is None:
      tokenizer.add_special_tokens({"pad_token": "<pad>"})
    else:
      tokenizer.add_special_tokens({"pad_token": tokenizer.eos_token})

  model_kwargs = {
      "low_cpu_mem_usage": True,
      "trust_remote_code": True,
      "token": hf_token,
      "device_map": "auto",
  }

  if quantize_type == "4bit":
    model_kwargs.update({
        "quantization_config":
            BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            ),
        "torch_dtype":
            torch.float16,
    })
  elif quantize_type == "8bit":
    model_kwargs.update({
        "device_map": "auto",
        "quantization_config": BitsAndBytesConfig(load_in_8bit=True),
        "use_cache": True,
    })
  elif quantize_type == "half":
    model_kwargs.update({"torch_dtype": torch.float16})

  model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)
  if quantize_type == "none" or quantize_type == "half":
    model.to(device)
  model.eval()
  return model, tokenizer
