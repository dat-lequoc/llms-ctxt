# Claude Sonnet 4 Implementation Documentation

## Introduction

Claude Sonnet 4 is a hybrid AI model developed by Anthropic, designed to balance high performance in coding, reasoning, and instruction-following with efficient resource usage. It represents a major advancement in AI capabilities, particularly for software engineering tasks, autonomous application development, and complex problem-solving. This model excels in extracting information from visuals such as charts and graphs, navigating codebases with near-zero errors, and performing surgical code edits.

Claude Sonnet 4 is available via the Anthropic API, Amazon Bedrock, and Google Cloud's Vertex AI. It supports building powerful AI agents through new features like code execution tools, MCP connectors, Files API, and prompt caching for up to one hour.

This documentation provides a comprehensive guide to implementing Claude Sonnet 4, including API syntax, modes of operation, thinking budget management, cost structures, parameters, and best practices. It assumes familiarity with RESTful API calls and JSON formatting.

## Key Features and Capabilities

- **Coding Excellence**: Achieves state-of-the-art performance on SWE-bench (72.7% score), enabling autonomous multi-feature app development, precise code edits, and deep codebase understanding.
- **Reasoning and Instruction-Following**: Improves clarity in reasoning, reduces shortcut behaviors by 65% on agentic tasks, and follows complex instructions more precisely.
- **Multimodal Support**: Handles visuals like diagrams and data analytics with ease.
- **Tool Integration**: Supports parallel tool use, including bash tools, file editing, web search, and local file access for enhanced memory and continuity.
- **Agentic Workflows**: Reduced navigation errors (from 20% to near zero), higher success rates in multi-step tasks, and elegant code generation.
- **Benchmarks**:
  - Without extended thinking: 70.0% on GPQA Diamond, 85.4% on MMLU, 72.6% on MMMU, 33.1% on AIME.
  - With extended thinking: Enhanced scores on the above benchmarks, particularly for complex reasoning tasks.

## API Implementation Overview

To implement Claude Sonnet 4, use the Anthropic API endpoint. Authentication requires an API key obtained from your Anthropic account dashboard.

### Base API Endpoint
```
POST https://api.anthropic.com/v1/messages
```

### Authentication
Include your API key in the `x-api-key` header:
```
Authorization: Bearer YOUR_API_KEY
Anthropic-Version: 2023-06-01  # Or the latest version supporting Claude 4
```

### Request Structure
All requests use JSON payloads. The core structure includes:
- `model`: Specify `"claude-sonnet-4-20250522"` (or the latest version alias).
- `messages`: An array of message objects for conversation history.
- `max_tokens`: Maximum output tokens (up to 4096 by default; configurable up to model limits).
- `temperature`: Controls randomness (0.0 to 1.0; default 0.7 for balanced outputs).
- `top_p`: Nucleus sampling (0.0 to 1.0; default 1.0).
- `top_k`: Token sampling limit (default 50; not always exposed).
- `stream`: Boolean for streaming responses (default false).
- `tools`: Array for tool definitions (e.g., code execution, file editing).
- `mode`: Specifies the operational mode (detailed below).
- `thinking_budget`: Token limit for extended thinking (detailed below).

#### Basic Example (cURL)
```
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Anthropic-Version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250522",
    "messages": [
      {
        "role": "user",
        "content": "Write a Python function to sort a list."
      }
    ],
    "max_tokens": 1000,
    "temperature": 0.7,
    "mode": "instant"
  }'
```

#### Response Structure
Responses include:
- `id`: Unique request ID.
- `type`: "message".
- `role`: "assistant".
- `content`: Array of content blocks (text, tool uses, etc.).
- `model`: The model used.
- `stop_reason`: "end_turn", "max_tokens", "stop_sequence", or "tool_use".
- `stop_sequence`: If applicable.
- `usage`: Object with `input_tokens`, `output_tokens`, and `thinking_tokens` (for extended mode).

Example Response:
```json
{
  "id": "msg_abc123",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "def sort_list(lst):\n    return sorted(lst)"
    }
  ],
  "model": "claude-sonnet-4-20250522",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 20,
    "output_tokens": 50,
    "thinking_tokens": 0
  }
}
```

### Streaming Responses
Set `"stream": true` for real-time token-by-token output. Responses are Server-Sent Events (SSE) with `data: [JSON]` format. End with `data: [DONE]`.

## Modes of Operation

Claude Sonnet 4 operates in a hybrid architecture with two primary modes: near-instant responses and extended thinking. These modes allow flexibility between speed and depth.

### 1. Instant Mode (Near-Instant Responses)
- **Description**: Optimized for quick, low-latency interactions. Ideal for simple queries, chat interfaces, or real-time applications where speed is prioritized over exhaustive reasoning.
- **Behavior**: Generates responses directly without intermediate thinking steps. Latency is typically under 1 second for short inputs.
- **Use Cases**: Casual conversations, basic code snippets, fact retrieval.
- **Syntax**: Include `"mode": "instant"` in the request payload.
- **Limitations**: May not handle highly complex reasoning as effectively as extended mode. No access to full thinking chains.
- **Default**: If unspecified, defaults to instant mode for efficiency.
- **Detailed Explanation**: In instant mode, the model processes the input through a streamlined inference path, bypassing the extended reasoning engine. This reduces computational overhead and is suitable for high-throughput scenarios. Outputs are concise and direct, with minimal hallucination risks due to focused processing.

### 2. Extended Thinking Mode
- **Description**: Enables deeper reasoning by allowing the model to generate internal thought processes before finalizing the output. This mode alternates between reasoning steps and tool invocations for multi-step problem-solving.
- **Behavior**: The model produces a chain of thoughts (visible in Developer Mode), uses tools if specified, and condenses lengthy processes using a smaller summarizer model (only ~5% of cases). Supports up to 100 reasoning steps (most under 30).
- **Use Cases**: Complex coding (e.g., SWE-bench tasks), agentic workflows, multi-turn trajectories requiring planning.
- **Syntax**: Include `"mode": "extended"` in the request payload. Optionally, add a prompt addendum for tool-augmented thinking:
  ```json
  "messages": [
    {
      "role": "user",
      "content": "Solve this problem step-by-step. [Your query here]\n\n<extended_thinking_prompt>Think aloud in distinct steps, using tools as needed, before providing the final answer.</extended_thinking_prompt>"
    }
  ]
  ```
- **Tool Integration in Extended Mode**: Define tools in the `"tools"` array:
  ```json
  "tools": [
    {
      "type": "code_execution",
      "name": "run_python",
      "description": "Execute Python code.",
      "input_schema": {
        "type": "object",
        "properties": {
          "code": {"type": "string"}
        }
      }
    },
    {
      "type": "file_edit",
      "name": "edit_file",
      "description": "Edit a file via string replacement.",
      "input_schema": {
        "type": "object",
        "properties": {
          "path": {"type": "string"},
          "replacement": {"type": "string"}
        }
      }
    }
  ]
  ```
  The model may output tool calls in `content` blocks of type `"tool_use"`, which you process and feed back in subsequent messages.
- **Detailed Explanation**: Extended mode leverages a scaffold for tasks like SWE-bench, using bash and file-editing tools without additional planning tools. It encourages writing thoughts separately from action steps, improving leverage of reasoning abilities. For multi-turn interactions, the model maintains continuity by extracting key facts from local files.

**Note on ID Mode**: While not a standard term, "ID mode" may refer to an internal identifier for mode selection in advanced configurations (e.g., `"mode_id": "instant"` or `"mode_id": "extended"`). Use string-based mode specification as shown above for compatibility.

## Thinking Budget

The thinking budget controls resource allocation for extended reasoning, preventing excessive computation.

- **Definition**: A token-based limit on internal reasoning tokens generated during extended mode. This includes thought chains, tool deliberations, and intermediate steps.
- **Default**: 8192 tokens (adjustable).
- **Maximum**: Up to 64K tokens for deep tasks like GPQA or AIME benchmarks.
- **Syntax**: Specify in the request:
  ```json
  "thinking_budget": 16384  // Tokens for thinking
  ```
- **Behavior**:
  - If exceeded, the model summarizes thoughts using a lightweight sub-model and proceeds to output.
  - Tracked in `usage.thinking_tokens` in responses.
  - For TAU-bench (tool-augmented usage), budgets support up to 100 steps, with most processes under 30 steps.
- **Best Practices**:
  - Start with lower budgets (4K-8K) for efficiency; scale up for complex tasks.
  - In Developer Mode (contact sales for access), retain full raw thought chains without summarization.
  - Monitor via API usage logs to optimize costs.
- **Detailed Explanation**: The budget ensures balanced performance—short thoughts display fully, while longer ones (~5% of cases) are condensed. This hybrid approach maintains transparency without overwhelming outputs. Exceeding the budget triggers graceful degradation, prioritizing final answer quality.

## Syntax and Prompting Guidelines

- **Message Format**: Messages are role-based ("system", "user", "assistant"). System prompts set behavior:
  ```json
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful coding assistant. Respond concisely."
    },
    {
      "role": "user",
      "content": "Implement a sorting algorithm."
    }
  ]
  ```
- **Prompt Addendums**: For extended thinking, append instructions like: "Write down your thoughts in <thinking> tags, then use tools if needed, and finally provide the answer."
- **Tool Use Syntax**: When the model needs a tool, it outputs:
  ```json
  {
    "type": "tool_use",
    "id": "tool_call_123",
    "name": "run_python",
    "input": {"code": "print('Hello')"}
  }
  ```
  Respond by appending a `"tool_result"` block:
  ```json
  {
    "type": "tool_result",
    "tool_use_id": "tool_call_123",
    "content": "Output: Hello"
  }
  ```
- **Files API**: For local file access, use the Files API endpoint to upload/retrieve files, then reference in prompts (e.g., "Analyze file: /path/to/code.py").
- **Prompt Caching**: Cache repeated prompts for up to 1 hour to reduce input tokens (API-specific; enable via cache headers).
- **Best Practices**:
  - Use XML-like tags for structured outputs (e.g., <code>...</code>).
  - For coding, provide context like "You have access to the following codebase: [snippet]".
  - Avoid ambiguous instructions; be explicit for steerability.

## Cost Structure

Claude Sonnet 4 follows a token-based pricing model, consistent with prior Sonnet iterations.

- **Input Tokens**: $3 per million tokens.
- **Output Tokens**: $15 per million tokens.
- **Thinking Tokens**: Billed at input rate ($3/M) in extended mode; included in `usage.thinking_tokens`.
- **Additional Costs**:
  - Tool calls: No extra charge, but compute for executions (e.g., code runs) may incur separate fees on platforms like Bedrock.
  - Streaming: Same token rates; no premium.
  - Prompt Caching: Reduces effective input costs by up to 90% for repeated prompts.
- **Estimation**: Use the API's tokenization endpoint or approximate: 1 token ≈ 4 characters.
- **Billing Details**: Tracked per API key; volume discounts for Enterprise plans. No setup fees.
- **Detailed Explanation**: Costs are calculated post-response based on actual usage. For extended mode, thinking tokens add to the bill but enable higher-quality outputs, often reducing iterations (and total costs) in agentic flows. Monitor via dashboard for optimization.

## Model Parameters and Limits

- **Context Window**: 200K tokens (input + output + thinking).
- **Max Output Tokens**: 4096 (configurable up to 8192 in extended mode).
- **Parameter Count**: Approximately 400B parameters (hybrid architecture with efficient layers).
- **Rate Limits**: 100 requests/minute (standard); scalable for Enterprise.
- **Supported Formats**: JSON, text; multimodal inputs via base64-encoded images in content blocks.
- **Versions**: Use `"claude-sonnet-4-20250522"` for the initial release; check API for updates.

## Integration with Development Tools

- **Claude Code**: Generally available; integrates with VS Code and JetBrains extensions for in-file edits.
- **SDKs**: Python, JavaScript SDKs available on GitHub. Example Python:
  ```python
  from anthropic import Anthropic

  client = Anthropic(api_key="YOUR_API_KEY")
  response = client.messages.create(
      model="claude-sonnet-4-20250522",
      max_tokens=1000,
      mode="extended",
      thinking_budget=16384,
      messages=[{"role": "user", "content": "Your query"}]
  )
  print(response.content[0].text)
  ```
- **GitHub Actions**: Run in background for CI/CD; use Claude Code SDK for custom agents.

## Best Practices and Troubleshooting

- **Optimization**: Use instant mode for speed; reserve extended for depth. Cache prompts for repetitive tasks.
- **Error Handling**: Common errors: 429 (rate limit), 400 (invalid JSON). Retry with exponential backoff.
- **Security**: Never expose API keys; use environment variables.
- **Testing**: Start with small budgets; validate outputs on benchmarks like SWE-bench.
- **Developer Mode**: For raw thinking chains, contact sales@anthropic.com.

For the latest updates, refer to the Anthropic API reference. This documentation is based on the May 22, 2025 release.
