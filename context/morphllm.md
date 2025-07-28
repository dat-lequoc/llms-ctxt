```python

import openai
import litellm
import os 
import asyncio

import dotenv
dotenv.load_dotenv('backend/.env')

client = openai.OpenAI(
    api_key=os.getenv("MORPH_API_KEY"),
    base_url="https://api.morphllm.com/v1"
)


def apply_edit(instruction: str, original: str, update: str):
    response = client.chat.completions.create(
        model="morph-v3-large",
        messages=[{
            "role": "user",
            "content": f"<instruction>{instruction}</instruction>\n<code>{original}</code>\n<update>{update}</update>"
        }]
    )
    return response.choices[0].message.content

def apply_edit_openrouter_litellm(instruction: str, original: str, update: str):
    response = litellm.completion(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="openrouter/morph/morph-v3-large",
        messages=[{
            "role": "user",
            "content": f"<instruction>{instruction}</instruction>\n<code>{original}</code>\n<update>{update}</update>"
        }]
    )
    return response.choices[0].message.content

async def apply_edit_async(instruction: str, original: str, update: str):
    morph_api_key = os.getenv("MORPH_API_KEY")
    messages = [{
        "role": "user",
        "content": f"<instruction>{instruction}</instruction>\n<code>{original}</code>\n<update>{update}</update>"
    }]
    response = None
    if morph_api_key:
        print("Using direct Morph API for file editing.")
        client = openai.AsyncOpenAI(
            api_key=morph_api_key,
            base_url="https://api.morphllm.com/v1"
        )
        response = await client.chat.completions.create(
            model="morph-v3-large",
            messages=messages,
            temperature=0.0,
            timeout=30.0
        )
    if response:
        return response.choices[0].message.content
    return None

# Example
original = """
const a = 1
const authenticateUser = () => {
  return "Authenticated"
}
"""
# These should be coming from your Agent
instruction = "I will change the return text to be French"
update = """
// ... existing code ...
  return "Authentifié"
}
"""

async def main():
    print("--- Using Morph API ---")
    final_code_morph = apply_edit(instruction, original, update)
    print(final_code_morph)


    print("\n--- Using OpenRouter via LiteLLM ---")
    final_code_openrouter = apply_edit_openrouter_litellm(instruction, original, update)
    print(final_code_openrouter)

    print("\n--- Using Async Morph API ---")
    final_code_async = await apply_edit_async(instruction, original, update)
    print(final_code_async)


if __name__ == "__main__":
    asyncio.run(main())
```
