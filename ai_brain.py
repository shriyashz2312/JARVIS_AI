from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("Your Api Key"))

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hello like Jarvis"}]
)

print(resp.choices[0].message.content)
