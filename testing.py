import google.generativeai as genai
import json

with open ("credentials.json") as f:
    creds = json.load(f)
generation_config = genai.types.GenerationConfig(system_instructions= "hello")
model = "gemini-2.0-flash-exp"
history = []
genai.configure(api_key=creds["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.0-flash-exp", system_instruction=s)

response = model.generate_content([], generation_config=generation_config)
print(response.text)
