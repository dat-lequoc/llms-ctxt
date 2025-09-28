
# Function calling with OpenAI SDK

Connect language models to external tools and systems to build AI assistants and various integrations.

## Introduction

Function calling enables language models to use external tools, which can intimately connect models to the digital and physical worlds.

This is a powerful capability that can be used to enable a wide range of use cases:

*   Calling public APIs for actions ranging from looking up football game results to getting real-time satellite positioning data.
*   Analyzing internal databases.
*   Browsing web pages.
*   Executing code.
*   Interacting with the physical world (e.g., booking a flight ticket, opening your Tesla car door, controlling robot arms).

## Walkthrough

The request/response flow for function calling involves the model receiving the user's prompt and a list of available tools, and then responding with a request to call one or more of those tools with specific arguments. Your code then executes these tools and sends the results back to the model, which uses that information to generate a final response.

The whole process looks like this in pseudocode:

```python
# ... Define tool functions and their JSON schemas
messages = []

# Step 1: Send a new user request along with tool definitions
messages.append({"role": "user", "content": "<new user request message>"})
response = send_request_to_model(messages, tools)
response_message = response.choices[0].message
messages.append(response_message) # Append assistant's response

# Step 2: Check if the model wants to call a tool
if response_message.tool_calls:
    # Step 3: Execute the tool calls
    for tool_call in response_message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        function_response = call_local_function(function_name, **function_args)
        
        # Step 4: Append the tool's result to the messages
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(function_response),
            }
        )

    # Step 5: Send the tool results back to the model to get a final response
    final_response = send_request_to_model(messages, tools)
    print(final_response.choices[0].message.content)
```

We will demonstrate this flow in the following Python script. First, let's create an API client:

```python
import os
import json
from openai import OpenAI

# It's recommended to set the API key as an environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
```

### Preparation - Define tool functions and function mapping

First, define the Python functions that will act as your tools. These functions will be executed locally by your code when the model requests them.

For this demonstration, we'll create functions that return hardcoded weather data.

```python
from typing import Literal

def get_current_temperature(location: str, unit: Literal["celsius", "fahrenheit"] = "fahrenheit"):
    """Get the current temperature in a given location."""
    temperature = 59 if unit == "fahrenheit" else 15
    return {
        "location": location,
        "temperature": temperature,
        "unit": unit,
    }

def get_current_ceiling(location: str):
    """Get the current cloud ceiling in a given location."""
    return {
        "location": location,
        "ceiling": 15000,
        "ceiling_type": "broken",
        "unit": "ft",
    }
```

Next, create a mapping from the function names to the actual function objects. This will allow you to dynamically call the correct function based on the model's response.

```python
tools_map = {
    "get_current_temperature": get_current_temperature,
    "get_current_ceiling": get_current_ceiling,
}
```

### Preparation - Define tool schemas for the model

Now, you must define the structure (schema) of your functions in a format the model can understand. This tells the model what tools are available, what they do, and what parameters they accept.

You can define these schemas using raw dictionaries or by leveraging a library like Pydantic to generate the JSON schema automatically, which helps reduce errors.

#### Option 1: Function definition using Pydantic

```python
from typing import Literal
from pydantic import BaseModel, Field

# Define Pydantic models for request parameters
class TemperatureRequest(BaseModel):
    location: str = Field(description="The city and state, e.g. San Francisco, CA")
    unit: Literal["celsius", "fahrenheit"] = Field(
        "fahrenheit", description="Temperature unit"
    )

class CeilingRequest(BaseModel):
    location: str = Field(description="The city and state, e.g. San Francisco, CA")

# Generate the JSON schema from the Pydantic models
get_current_temperature_schema = TemperatureRequest.model_json_schema()
get_current_ceiling_schema = CeilingRequest.model_json_schema()

# Create the final tool definitions list
tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "get_current_temperature",
            "description": "Get the current temperature in a given location",
            "parameters": get_current_temperature_schema,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_ceiling",
            "description": "Get the current cloud ceiling in a given location",
            "parameters": get_current_ceiling_schema,
        }
    },
]
```

#### Option 2: Function definition using raw dictionary

```python
# Raw dictionary definition of parameters
tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "get_current_temperature",
            "description": "Get the current temperature in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "default": "fahrenheit",
                    },
                },
                "required": ["location"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_ceiling",
            "description": "Get the current cloud ceiling in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        }
    },
]
```

### 1. Send initial message

With the functions and schemas defined, you can now send the initial request to the model. The `messages` list contains the user's prompt, and the `tools` parameter contains your function schemas.

```python
# Start the conversation with a user message
messages = [{"role": "user", "content": "What's the temperature like in San Francisco?"}]

# Make the first API call
response = client.chat.completions.create(
    model="grok-4",
    messages=messages,
    tools=tool_definitions,
    tool_choice="auto"  # 'auto' is the default
)

response_message = response.choices[0].message

# You can inspect the response to see the tool call request
print(response_message)
```

### 2. Run tool functions and append results

Next, check if the model's response contains a `tool_calls` request. If it does, iterate through each call, execute the corresponding local function with the provided arguments, and append the results to the `messages` list.

It's crucial that the appended message has the `role` set to `"tool"` and includes the `tool_call_id` from the model's request.

```python
# Append the assistant's response (which contains the tool call) to the messages list
messages.append(response_message)

# Check if the model requested any tool calls
if response_message.tool_calls:
    for tool_call in response_message.tool_calls:
        # Get the function name and arguments
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Look up the function in our map and call it
        if function_name in tools_map:
            function_to_call = tools_map[function_name]
            result = function_to_call(**function_args)

            # Append the tool's result to the messages list
            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id,
                }
            )
        else:
            # Handle the case where the requested function does not exist
            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps({"error": f"Function {function_name} not found"}),
                    "tool_call_id": tool_call.id,
                }
            )
```

### 3. Send the tool results back to the model

Finally, send the updated `messages` list (which now includes the user prompt, the assistant's tool call request, and your tool's result) back to the model. The model will use the tool's output to formulate its final, user-facing answer.

```python
# Make the second API call with the tool results
final_response = client.chat.completions.create(
    model="grok-4",
    messages=messages,
)

# Print the final response from the model
print(final_response.choices[0].message.content)
```

### 4. (Optional) Continue the conversation

You can continue the conversation by appending new user messages and repeating the process from Step 1. The model will maintain the context of the previous turns, including the function calls and their results.
