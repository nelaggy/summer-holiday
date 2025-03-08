from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message)