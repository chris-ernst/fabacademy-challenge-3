import openai
import requests
import json
from dotenv import dotenv_values

### AUTH
config = dotenv_values(".env")
API_KEY = config["API_KEY"]
openai.api_key = API_KEY


### GPT-3 Request
restart_sequence = "."

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Say this is a test",
  temperature=0.8,
  max_tokens=500,
  top_p=1,
  frequency_penalty=0.8,
  presence_penalty=1.5
)


print(type(response.choices))

for choice in response.choices:
	print(choice.text)
