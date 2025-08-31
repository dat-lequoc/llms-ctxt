# Introduction

For teams who want to build the best AI coding agents.

## What is Morph?

Morph Fast Apply is a tool that you give to your AI agent that allows it to edit code or files. When building AI agents that edit code or files you have 3 options:

1.  **Rewrite entire files** (slow, expensive, loses context, hallucinates updates)
2.  **Use search-and-replace** (brittle, fails on whitespace/formatting, needs self correction loops)
3.  **Fast Apply via an edit_file tool** (fast, accurate, semantic)

Current AI code editing is broken. Agents either rewrite entire files (which is slow, expensive, and loses context) or use search-and-replace (which is brittle, fails, and needs self-correction). You lose customers while your agents are fixing patch errors.

Fast Apply solves this. Your agent uses an `edit_file` tool that writes lazy edit snippets, and Fast Apply handles the merging - the same way Cursor does it. This ensures fast, reliable edits every time.

## How It Looks in Your Code

1.  **Give your agent an `edit_file` tool** - It generates abbreviated edit snippets in this tool call.
2.  **Call Morph's API inside the tool** - We merge the edit with the original file FAST, using our specialized models.
3.  **Write the result** - Get the merged code back and save it to your filesystem.

```typescript
const response = await openai.chat.completions.create({
  model: "morph-v3-large",
  messages: [{
    role: "user",
    content: `<instruction>${instructions}</instruction>\n<code>${originalCode}</code>\n<update>${codeEdit}</update>`
  }]
});
```

## Why Choose Morph?

*   **Built for Code:** Specialized models trained for code understanding and editing.
*   **Universal Integration:** OpenAI-compatible with native support for OpenRouter, Vercel AI SDK, and MCP.
*   **Enterprise Ready:** Dedicated instances, self-hosted, and on-premises options.

## Morph's Models

*   **Apply Model**: Apply code changes at high speed with high accuracy.
*   **Embedding Model**: Embeddings built for code.
*   **Rerank Model**: Reorder code results with code reranking.

# Quickstart: Fast Apply

Replace full file rewrites or search and replace with Fast Apply in 5 minutes.

## Overview

Morph Fast Apply looks like a new `edit_file` tool you give your agent access to. The agent will output lazily into this tool when it wants to make an edit. In the tool's execution, the Morph API will merge the lazy edit output by the agent into the file.

If you like using Cursor, you already like the Fast Apply UX. Fast Apply is a concept used in Cursor.

## How to use Morph Fast Apply

### Step 1. Add an `edit_file` tool to your agent

Add the `edit_file` tool to your agent. Use one of the formats below.

#### General Prompt

````xml
Tool Description
Use this tool to make an edit to an existing file.

This will be read by a less intelligent model, which will quickly apply the edit. You should make it clear what the edit is, while also minimizing the unchanged code you write.
When writing the edit, you should specify each edit in sequence, with the special comment // ... existing code ... to represent unchanged code in between edited lines.

For example:

// ... existing code ...
FIRST_EDIT
// ... existing code ...
SECOND_EDIT
// ... existing code ...
THIRD_EDIT
// ... existing code ...

You should still bias towards repeating as few lines of the original file as possible to convey the change.
But, each edit should contain minimally sufficient context of unchanged lines around the code you're editing to resolve ambiguity.
DO NOT omit spans of pre-existing code (or comments) without using the // ... existing code ... comment to indicate its absence. If you omit the existing code comment, the model may inadvertently delete these lines.
If you plan on deleting a section, you must provide context before and after to delete it. If the initial code is ```code \n Block 1 \n Block 2 \n Block 3 \n code```, and you want to remove Block 2, you would output ```// ... existing code ... \n Block 1 \n  Block 3 \n // ... existing code ...```.
Make sure it is clear what the edit should be, and where it should be applied.
Make edits to a file in a single edit_file call instead of multiple edit_file calls to the same file. The apply model can handle many distinct edits at once.

**Parameters:**

* `target_file` (string, required): The target file to modify
* `instructions` (string, required): A single sentence written in the first person describing what you're changing. Used to help disambiguate uncertainty in the edit.
* `code_edit` (string, required): Specify ONLY the precise lines of code that you wish to edit. Use `// ... existing code ...` for unchanged sections.
````

#### JSON Tool (Claude)

````json
{
  "name": "edit_file",
  "description": "Use this tool to make an edit to an existing file.\n\nThis will be read by a less intelligent model, which will quickly apply the edit. You should make it clear what the edit is, while also minimizing the unchanged code you write.\nWhen writing the edit, you should specify each edit in sequence, with the special comment // ... existing code ... to represent unchanged code in between edited lines.\n\nFor example:\n\n// ... existing code ...\nFIRST_EDIT\n// ... existing code ...\nSECOND_EDIT\n// ... existing code ...\nTHIRD_EDIT\n// ... existing code ...\n\nYou should still bias towards repeating as few lines of the original file as possible to convey the change.\nBut, each edit should contain minimally sufficient context of unchanged lines around the code you're editing to resolve ambiguity.\nDO NOT omit spans of pre-existing code (or comments) without using the // ... existing code ... comment to indicate its absence. If you omit the existing code comment, the model may inadvertently delete these lines.\nIf you plan on deleting a section, you must provide context before and after to delete it. If the initial code is ```code \\n Block 1 \\n Block 2 \\n Block 3 \\n code```, and you want to remove Block 2, you would output ```// ... existing code ... \\n Block 1 \\n  Block 3 \\n // ... existing code ...```.\nMake sure it is clear what the edit should be, and where it should be applied.\nMake edits to a file in a single edit_file call instead of multiple edit_file calls to the same file. The apply model can handle many distinct edits at once.",
  "input_schema": {
    "type": "object",
    "properties": {
      "target_file": {
        "type": "string",
        "description": "Name or path of target file to modify."
      },
      "instructions": {
        "type": "string",
        "description": "A single sentence instruction describing what you are going to do for the sketched edit. This is used to assist the less intelligent model in applying the edit. Use the first person to describe what you are going to do. Use it to disambiguate uncertainty in the edit."
      },
      "code_edit": {
        "type": "string",
        "description": "Specify ONLY the precise lines of code that you wish to edit. NEVER specify or write out unchanged code. Instead, represent all unchanged code using the comment of the language you're editing in - example: // ... existing code ..."
      }
    },
    "required": ["target_file", "instructions", "code_edit"]
  }
}
````

**Warning:** The `instructions` field should be generated by your AI model, not user input. Follow the tool description above nearly verbatim - terminology like "use it to disambiguate uncertainty in the edit" should be used. Example: "I am adding error handling to the user authentication function".

### Step 2. Merge with Morph Fast Apply

Your tool's execution should use Morph's API to merge the code.

**TypeScript**
```typescript
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.MORPH_API_KEY,
  baseURL: "https://api.morphllm.com/v1",
});

const response = await openai.chat.completions.create({
  model: "morph-v3-large",
  messages: [
    {
      role: "user",
      content: `<instruction>${instructions}</instruction>\n<code>${initialCode}</code>\n<update>${codeEdit}</update>`,
    },
  ],
});

const mergedCode = response.choices[0].message.content;
```

**Python**
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("MORPH_API_KEY"),
    base_url="https://api.morphllm.com/v1"
)

response = client.chat.completions.create(
    model="morph-v3-large",
    messages=[
        {
            "role": "user",
            "content": f"<instruction>{instructions}</instruction>\n<code>{initial_code}</code>\n<update>{code_edit}</update>"
        }
    ]
)

merged_code = response.choices[0].message.content
```

**cURL**
```bash
curl -X POST "https://api.morphllm.com/v1/chat/completions" \
  -H "Authorization: Bearer $MORPH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "morph-v3-large",
    "messages": [
      {
        "role": "user",
        "content": "<instruction>INSTRUCTIONS</instruction>\n<code>INITIAL_CODE</code>\n<update>CODE_EDIT</update>"
      }
    ]
  }'
```

### Step 3. Handle the Response

Extract the merged code from the API response and use your filesystem to write it to a file.

**Response Format:**
The final merged code is in `response.choices[0].message.content`.

**TypeScript**
```typescript
const finalCode = response.choices[0].message.content;
// Write to file or return to your application
await fs.writeFile(targetFile, finalCode);
```

**Python**
```python
final_code = response.choices[0].message.content
# Write to file or return to your application
with open(target_file, 'w') as f:
    f.write(final_code)
```

**cURL**
```bash
# The response contains the merged code directly
echo "$response" > output_file.js
```

# Apply Model Details

The Apply Model intelligently merges your original code with update snippets. Unlike diff-based methods, it preserves code structure, comments, and syntax while understanding context semantically.

### Why Choose Fast Apply?

*   **Ultra-fast**: Processes edits quickly.
*   **High accuracy**: High success rate in one pass.
*   **Token efficient**: Processes only changed sections.

### Best Practices

**Update Snippets**: Use `// ... existing code ...` for unchanged sections:

```javascript
// Good
const authenticateUser = async (email, password) => {
  // ... existing code ...
  const result = await verifyUser(email, password)
  return result ? "Authenticated" : "Unauthenticated"
}
```

**Instructions**: Have the agent write clear, first-person descriptions to "disambiguate uncertainty in the edit":

*   ✅ "I will add async/await error handling"
*   ❌ "Change this function"

### Example Implementation

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-morph-api-key",
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

final_code = apply_edit(instruction, original, update)
```

# Agent Tools (edit_file)

Build precise AI agents that edit code fast without full file rewrites using Morph's `edit_file` tool.

### Agent Workflow

Effective agents follow this pattern:
1.  **🔍 Search**: Find relevant code with codebase or grep search.
2.  **📖 Read**: Get context with a file reader before editing.
3.  **✏️ Edit**: Make precise changes with `edit_file`.
4.  **✅ Verify**: Read again to confirm changes worked.

### Common Patterns for `edit_file`

**Delete a section in between:**
```javascript
// ... existing code ...
function keepThis() {
  return "stay";
}

function alsoKeepThis() {
  return "also stay";
}
// ... existing code ...
```

**Add imports:**
```javascript
import { useState, useEffect } from "react";
import { calculateTax } from "./utils"; // New import
// ... existing code ...
```

**Update configuration:**
```json
{
  "name": "my-app",
  "version": "2.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "test": "jest"
  }
}
```

**Add error handling:**
```javascript
// ... existing code ...
function divide(a, b) {
  if (b === 0) {
    throw new Error("Cannot divide by zero");
  }
  return a / b;
}
// ... existing code ...
```

### Error Handling

Morph is trained to be robust to poor quality update snippets, but you should still follow these steps to ensure the best quality. When tools fail, follow these steps:

1.  **Check file permissions**: Ensure the target file is writable.
2.  **Verify file path**: Confirm the file exists and the path is correct.
3.  **Review syntax**: Check that your edit snippet follows the `// ... existing code ...` pattern.
4.  **Retry with context**: Read the file again and provide more context around your changes.
5.  **Simplify changes**: Break complex edits into smaller, focused changes.

*Tip: For complex refactoring across multiple files, consider using multiple `edit_file` calls in sequence. For failed edits, read the file again and provide more context around your changes.*

# XML Tool Calls

Learn why XML tool calls outperform JSON for code editing and how to implement them with Claude and other LLMs.

## XML Tool Calls: Beyond JSON Constraints

When building AI coding assistants, the choice between JSON and XML tool calls can dramatically impact your model's performance. Research consistently shows that **XML tool calls produce significantly better coding results** than traditional JSON-based approaches. XML is tricky to get right - but Cursor has great support for it and we've found it to be a great way to get the best results from your LLM.

### The Problem with Constrained Decoding

Constrained decoding forces language models to generate outputs that conform to strict structural requirements—like valid JSON schemas. While this ensures parseable responses, it comes with significant trade-offs, such as cognitive overhead for the model, premature commitment to field values, and lower token efficiency. A single syntax error can invalidate an entire JSON tool call.

### Why XML Tool Calls Work Better

XML tool calls eliminate these constraints while maintaining structure and parseability.

**Benefits Over JSON:**
*   **Cognitive Freedom**: Models can focus entirely on code quality without syntax constraints.
*   **Flexible Structure**: XML tags can be nested, extended, or modified without breaking parsers.
*   **Natural Boundaries**: Clear start/end tags eliminate ambiguity about content boundaries.
*   **Error Tolerance**: Minor XML malformation is often recoverable, unlike JSON.
*   **Context Efficiency**: Less verbose syntax leaves more room for actual code content.

### Implementation Guide

Replace a JSON approach like this:
```json
{
  "tool": "edit_file",
  "parameters": {
    "file_path": "src/utils/api.ts",
    "instructions": "Add error handling",
    "code_changes": "..."
  }
}
```

With this more natural XML approach:
```xml
<edit_file>
<file_path>src/utils/api.ts</file_path>
<instruction>Add comprehensive error handling with retry logic</instruction>
<code_changes>
// ... existing code ...
export async function apiCall(endpoint: string, options?: RequestInit) {
  const maxRetries = 3;
  let lastError: Error;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(endpoint, options);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      lastError = error as Error;
      if (attempt === maxRetries) break;
      await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
    }
  }

  throw new Error(`API call failed after ${maxRetries} attempts: ${lastError.message}`);
}
// ... existing code ...
</code_changes>
</edit_file>
```

### System Prompt Configuration

Configure your model to use XML tool calls:
```text
You are an expert coding assistant. When making code changes, use XML tool calls in this format:

<tool_name>
<parameter_name>parameter_value</parameter_name>
<code>
actual code content here
</code>
</tool_name>

Focus on code quality and correctness. Don't worry about XML formatting - just ensure the content within tags is accurate and helpful.
```

### Parsing XML Tool Calls
You can use regex-based parsers to extract tool calls and their parameters from the model's output. Build robust parsers that can handle minor XML issues and attempt recovery strategies.
