import openai


openai.api_key="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"

prompt="Plan a itenary for 2 days to mumbai"
response=openai.Completion.create(engine="text-davinci-003",prompt=prompt,temperature=0.7,max_tokens=500)
print(response)