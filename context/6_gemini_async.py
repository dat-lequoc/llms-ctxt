# To run this code you need to install the following dependencies:
# pip install google-genai

import asyncio
import base64
import os
from google import genai
from google.genai import types

API_KEY = ""


async def generate_async():
    """Test async content generation with Gemini"""
    client = genai.Client(
        api_key=API_KEY,  # Add your API key here
    )

    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Hello, world! This is an async test."""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=-1,
        ),
        response_mime_type="text/plain",
    )
    
    print("Testing async content generation...")
    response = await client.aio.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    print("Response:", response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Candidates tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Thoughts tokens: {response.usage_metadata.thoughts_token_count}")


async def generate_content_stream_async():
    """Test async streaming content generation"""
    client = genai.Client(
        api_key=API_KEY,  # Add your API key here
    )

    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="Write a short poem about Python programming."),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )
    
    print("\nTesting async streaming content generation...")
    stream = await client.aio.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    async for chunk in stream:
        print(chunk.text, end="", flush=True)
    print("\n")


async def test_async_pager():
    """Test async pager functionality"""
    client = genai.Client(
        api_key=API_KEY,  # Add your API key here
    )
    
    print("\nTesting async pager...")
    async_pager = await client.aio.models.list(config={'page_size': 3})
    print(f"Page size: {async_pager.page_size}")
    if len(async_pager) > 0:
        print(f"First model: {async_pager[0].name}")
        
        # Test next page
        await async_pager.next_page()
        if len(async_pager) > 0:
            print(f"First model on next page: {async_pager[0].name}")


async def main():
    """Main async function to run all tests"""
    try:
        await generate_async()
        await generate_content_stream_async()
        await test_async_pager()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your API key in the client initialization.")


if __name__ == "__main__":
    asyncio.run(main()) 
