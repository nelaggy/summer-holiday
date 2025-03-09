from openai import OpenAI


completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message)