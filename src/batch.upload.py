from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

batch_file = "/cl/home2/shintaro/text_simplification_for_image_generation/data/wit/en.wit.2k.batch.input.jsonl"

batch_input_file = client.files.create(
  file=open(batch_file, 'rb'),
  purpose="batch"
)

batch_input_file_id = batch_input_file.id

response = client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": f'Batch for Summarization'
    }
)
print(response)
print(f'Done uploading batch for Summarization')
