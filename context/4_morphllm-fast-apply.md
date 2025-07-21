### Using MorphLLM: A Guide to Applying Code Edits

MorphLLM is a powerful tool for applying AI-driven code edits with high speed and accuracy, trusted by startups and enterprises. It seems likely that you can use it either through its OpenAI-compatible API or by integrating it with the Model Context Protocol (MCP) for AI agents and development environments. Below is a concise guide to help you get started, including key steps and syntax for using MorphLLM effectively.

**Key Points:**
- MorphLLM enables fast code edits (4,500+ tokens/second, 98% accuracy) via its API or MCP integration.
- You’ll need an API key from the MorphLLM dashboard to authenticate requests.
- The API uses a JSON request with XML-formatted content for instructions, original code, and updates.
- MCP provides tools like `edit_file` for seamless integration with AI agents, with additional tools available when configured.
- Documentation is available at [MorphLLM Documentation](https://docs.morphllm.com/) for further details.

#### **Getting Started**
1. **Sign Up and Get an API Key**: Create an account at [MorphLLM Dashboard](https://morphllm.com/dashboard/api-keys) to obtain your API key.
2. **Use the API**: Send POST requests to the `/v1/chat/completions` endpoint with a JSON body containing your code edit instructions.
3. **Integrate with MCP**: Install the MCP tool to use MorphLLM’s file-editing capabilities in AI agents or IDEs.

#### **Basic API Syntax**
To apply a code edit, send a POST request to `[https://api.morphllm.com/v1/chat/completions](https://api.morphllm.com/v1/chat/completions)` with the following JSON:

```json
{
  "model": "morph-v3-large",
  "messages": [
    {
      "role": "user",
      "content": "<instructions>Add error handling</instructions>\n<code>function divide(a, b) { return a / b; }</code>\n<update>function divide(a, b) { if (b === 0) { throw new Error('Cannot divide by zero'); } return a / b; }</update>"
    }
  ]
}
```

Include the header `Authorization: Bearer <your-api-key>`.

#### **MCP Integration**
Run this command to set up MCP:
```bash
claude mcp add filesystem-with-morph -e MORPH_API_KEY=your-api-key-here -e ALL_TOOLS=false -- npx @morph-llm/morph-fast-apply
```
Verify by typing `/mcp` and `/tools` in your AI environment.

For more details, see the comprehensive guide below.

---

### Comprehensive Guide to Using MorphLLM

MorphLLM is a specialized AI service designed to apply code edits to files with exceptional speed (4,500+ tokens/second) and accuracy (98% at first pass). It is trusted by hundreds of startups and enterprises and offers OpenAI API compatibility, making it accessible for developers familiar with similar APIs. MorphLLM can be used directly via its API or integrated into AI agents and development environments through the Model Context Protocol (MCP). This guide provides a detailed explanation of how to use MorphLLM, including all necessary syntax and integration steps, based on available documentation.

#### **Overview of MorphLLM**
MorphLLM’s primary function is to apply precise code edits to existing files, reducing errors by 4x and performing 3x faster than traditional methods. It supports:
- **Direct API Usage**: For programmatic code edits via the `/v1/chat/completions` endpoint.
- **MCP Integration**: For AI agents and IDEs, offering tools like `edit_file` for seamless file manipulation.
- **Deployment Options**: Self-hosting on-premises or in the cloud with enterprise-level reliability and flexible rate limits.
- **Additional Features**: Endpoints for generating embeddings and reranking results, though the focus here is on code editing.

#### **Step-by-Step Guide to Using MorphLLM**

##### **1. Obtaining an API Key**
To use MorphLLM, you must first obtain an API key:
- Visit [MorphLLM Dashboard](https://morphllm.com/dashboard/api-keys) to sign up and generate your API key.
- This key is required for authenticating API requests and configuring MCP.

##### **2. Using the MorphLLM API**
The primary API endpoint for applying code edits is `/v1/chat/completions`. It is OpenAI-compatible, meaning developers familiar with OpenAI’s API can adapt their workflows with minimal changes.

###### **Endpoint Details**
| **Attribute**         | **Details**                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| **URL**               | [https://api.morphllm.com/v1/chat/completions](https://api.morphllm.com/v1/chat/completions) |
| **Method**            | POST                                                                        |
| **Authentication**    | Bearer token (e.g., `Authorization: Bearer <your-api-key>`)                 |
| **Content-Type**      | application/json                                                            |
| **Stream**            | false (non-streaming response)                                              |
| **Model Example**     | morph-v3-large                                                              |

###### **Request Format**
The request body is a JSON object with the following structure:
- **model**: The MorphLLM model to use (e.g., `"morph-v3-large"`).
- **messages**: An array of message objects, where at least one message has:
  - **role**: `"user"`.
  - **content**: A string with XML-formatted tags: `<instructions>`, `<code>`, and `<update>`.

###### **XML Content Structure**
| **Tag**           | **Description**                                                                 |
|-------------------|---------------------------------------------------------------------------------|
| `<instructions>`  | Optional, first-person description of the changes (e.g., "I will add error handling"). |
| `<code>`          | The complete original code to be edited.                                        |
| `<update>`        | The updated code, showing only changes. Use `// ... existing code ...` for unchanged sections. |

###### **Example API Request**
```json
{
  "model": "morph-v3-large",
  "messages": [
    {
      "role": "user",
      "content": "<instructions>I will add error handling to prevent division by zero</instructions>\n<code>function divide(a, b) { return a / b; }</code>\n<update>function divide(a, b) { if (b === 0) { throw new Error('Cannot divide by zero'); } return a / b; }</update>"
    }
  ]
}
```

- **Headers**:
  - `Authorization: Bearer <your-api-key>`
  - `Content-Type: application/json`
- **Response**: The API returns the result of the edit application, which can be used to update the target file.

###### **Testing in the API Playground**
You can test API endpoints directly in MorphLLM’s API Playground at [https://morphllm.com/dashboard/playground/apply](https://morphllm.com/dashboard/playground/apply). This interactive environment allows you to experiment with live examples and verify your API calls.

##### **3. Integrating with MCP**
The Model Context Protocol (MCP) enables MorphLLM to integrate with AI agents and development environments, providing tools for file manipulation. The most critical tool is `edit_file`, which applies precise code edits.

###### **Installation Steps**
1. **Install the MCP Tool**:
   - Run the following command in your terminal:
     ```bash
     claude mcp add filesystem-with-morph -e MORPH_API_KEY=your-api-key-here -e ALL_TOOLS=false -- npx @morph-llm/morph-fast-apply
     ```
   - Replace `your-api-key-here` with your API key from [MorphLLM Dashboard](https://morphllm.com/dashboard/api-keys).
   - Setting `ALL_TOOLS=false` limits the tools to `edit_file`. Use `ALL_TOOLS=true` to enable additional tools (see below).

2. **Verify Installation**:
   - In your AI agent or IDE, start a new conversation.
   - Type `/mcp` to confirm MCP is active.
   - Type `/tools` to list available tools.

###### **Available Tools**
| **Tool**            | **Description**                     | **Availability**         |
|---------------------|-------------------------------------|--------------------------|
| `edit_file`         | Lightning-fast code edits           | `ALL_TOOLS=false` or `true` |
| `read_file`         | Read file contents                 | `ALL_TOOLS=true`         |
| `write_file`        | Write to a file                    | `ALL_TOOLS=true`         |
| `list_directory`    | List files in a directory          | `ALL_TOOLS=true`         |
| `create_directory`  | Create a new directory             | `ALL_TOOLS=true`         |
| `search_files`      | Search for files                   | `ALL_TOOLS=true`         |
| `move_file`         | Move a file                        | `ALL_TOOLS=true`         |
| `get_file_info`     | Get file metadata                  | `ALL_TOOLS=true`         |

###### **Using the `edit_file` Tool**
The `edit_file` tool allows AI agents to apply code changes directly to files. The exact syntax depends on the AI agent or IDE, but typically involves:
- **File Path**: The path to the file to edit (e.g., `example.js`).
- **Original Code**: The current content of the file.
- **Update**: The desired changes or updated code.

**Example Interaction**:
- **User Input**: "Edit `example.js` to add error handling for division by zero."
- **Agent Action**: The agent uses the `edit_file` tool, passing:
  - File path: `example.js`
  - Original code: `function divide(a, b) { return a / b; }`
  - Update: `function divide(a, b) { if (b === 0) { throw new Error('Cannot divide by zero'); } return a / b; }`

The `edit_file` tool likely calls the `/v1/chat/completions` API under the hood, formatting the request as shown above.

##### **4. Additional Features**
- **Other Endpoints**: MorphLLM supports endpoints for generating embeddings and reranking results, but these are secondary to the code-editing functionality. Refer to [MorphLLM API Reference](https://docs.morphllm.com/api-reference) for details.
- **Self-Hosting**: MorphLLM offers self-hosted or on-premises deployments for enterprise users. Contact [info@morphllm.com](mailto:info@morphllm.com) for more information.
- **AI SDK Integration**: MorphLLM can be integrated via the AI SDK at [https://ai-sdk.dev/playground/morph:morph-v2](https://ai-sdk.dev/playground/morph:morph-v2).

##### **5. Documentation and Resources**
For further details, consult the following resources:
- **Main Documentation**: [https://docs.morphllm.com/](https://docs.morphllm.com/)
- **Quickstart Guide**: [https://docs.morphllm.com/guides/quickstart](https://docs.morphllm.com/guides/quickstart)
- **Apply Guide**: [https://docs.morphllm.com/guides/apply](https://docs.morphllm.com/guides/apply)
- **API Reference**: [https://docs.morphllm.com/api-reference](https://docs.morphllm.com/api-reference)
- **MCP Page**: [https://morphllm.com/mcp](https://morphllm.com/mcp)

#### **Best Practices**
- **API Usage**:
  - Always include clear instructions in the `<instructions>` tag to improve edit accuracy.
  - Use `// ... existing code ...` in the `<update>` tag to minimize unnecessary changes.
  - Test your API calls in the [API Playground](https://morphllm.com/dashboard/playground/apply) before integrating into production.
- **MCP Integration**:
  - Start with `ALL_TOOLS=false` to focus on `edit_file` for simplicity.
  - Configure your AI agent’s system prompt to use code edit tools only when necessary, as suggested in the quickstart guide.
- **Error Handling**:
  - Ensure your API key is valid and included in all requests.
  - Verify file paths and code syntax when using MCP tools to avoid errors.

#### **Limitations and Considerations**
- The exact syntax for MCP tools like `edit_file` may vary depending on the AI agent or IDE. Consult your platform’s documentation for specifics.
- Some documentation sections may require access to the MorphLLM dashboard for full details.
- For advanced use cases, such as embeddings or reranking, additional configuration may be needed.

#### **Conclusion**
MorphLLM offers a robust solution for applying AI-driven code edits, with flexible integration options via its API or MCP. By following the steps outlined above, you can leverage its high-speed, high-accuracy capabilities to enhance your development workflow. The provided syntax and examples should enable you to start using MorphLLM effectively, whether through direct API calls or MCP-integrated tools.

For any further assistance, reach out to [info@morphllm.com](mailto:info@morphllm.com) or explore the documentation links provided.
