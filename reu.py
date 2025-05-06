
from together import Together
import os

# Set your API key directly (not recommended for prod)
os.environ["TOGETHER_API_KEY"] = "581c6afa68a3f1c547d6ae2e3531f2c424e80b29ca6eb463619207c439c20e8a"

# Initialize Together client
client = Together()

# Send test message
response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=[
        {"role": "user", "content": "What are 3 business ideas a student in Nigeria can start with 10,000 Naira?"}
    ]
)

# Print response
print("AI Response:\n", response.choices[0].message.content)
