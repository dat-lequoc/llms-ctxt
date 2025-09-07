# GPT-5 (High Reasoning) — Implementation Guide (no max-output-token setting)

This guide shows how to **use the `gpt-5` API with high reasoning effort**: what the setting does, when to use it, request syntax (Python, JavaScript, cURL), streaming, tool calling, Structured Outputs, cost planning, and practical tips. Per your request, **all uses and mentions of “max output tokens” (e.g., `max_output_tokens`, `max_tokens`) have been removed**.

---

## What “reasoning effort: high” does

`gpt-5` exposes a control that dials how hard the model “thinks” before answering. **Higher effort** improves multi-step reasoning, tool-use planning, and adherence to tricky instructions, at the cost of **more output/“reasoning” tokens** and **higher latency**. If you don’t set it, the default is typically `medium`.

### When to choose `high`

* Complex, multi-step tasks (analysis, planning, code refactors, multi-hop QA)
* Agentic flows that require long chains of tool calls
* Safety- or quality-critical outputs where extra thought is worth the cost

---

## Key model facts you’ll likely care about

* **Model ID:** `gpt-5` (use this exact string in API calls).
* **Context limits:** large context (hundreds of thousands of tokens) supporting long inputs plus substantial reasoning and output.
* **Controls:** `reasoning` (with `effort`: `minimal` / `low` / `medium` / **`high`**) and optional `verbosity` (nudges shorter vs. longer answers).
* **Available in:** **Responses API** (recommended) and **Chat Completions**.
* **Supports:** streaming, tool calling, **Structured Outputs**, prompt caching, and batch.

> Practical note: With **high** effort, the model will often spend extra tokens internally to plan and verify steps before it speaks. Those “reasoning” tokens are billed as output tokens.

---

## Pricing (high-level)

* **Input tokens:** billed per million input tokens.
* **Output tokens (includes reasoning):** billed per million output tokens.

> Because reasoning tokens are counted as output, **high** effort usually increases output-side cost and latency. Use it deliberately on the steps that benefit most (e.g., planning or critical checks), and keep prompts crisp.

---

## Request syntax (set “High”)

### Responses API (recommended)

**Python**

```python
from openai import OpenAI
client = OpenAI()

resp = client.responses.create(
    model="gpt-5",
    input="Summarize key risks in this architecture and propose mitigations.",
    reasoning={"effort": "high"},   # <-- High reasoning
    verbosity="high"                # Optional: steer longer answers
)

print(resp.output_text)
```

**JavaScript (Node)**

```js
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
  model: "gpt-5",
  input: "Draft a migration plan with milestones and rollbacks.",
  reasoning: { effort: "high" },
  verbosity: "high"
});

console.log(response.output_text);
```

**cURL**

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5",
    "input": "Explain tradeoffs of eventual vs strong consistency.",
    "reasoning": { "effort": "high" },
    "verbosity": "high"
  }'
```

> Why Responses API? It’s designed for modern, tool-using, multi-step workflows and can preserve structured “reasoning items” across turns.

### Chat Completions (if you must)

```python
from openai import OpenAI
client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role":"user","content":"Outline a phased SOC2 rollout."}],
    reasoning_effort="high"
)
print(resp.choices[0].message.content)
```

---

## Streaming

Enable streaming to surface tokens as they arrive—handy when **high** effort increases latency.

```js
const stream = await client.responses.stream({
  model: "gpt-5",
  input: "Produce a step-by-step rollout plan.",
  reasoning: { effort: "high" }
});

for await (const event of stream) {
  if (event.type === "response.output_text.delta") {
    process.stdout.write(event.delta);
  }
}
```

---

## Tool calling (functions) with high reasoning

High effort helps GPT-5 plan multi-tool workflows and recover from tool errors.

```js
const response = await client.responses.create({
  model: "gpt-5",
  input: "Is it going to rain in Paris tomorrow? If yes, give clothing tips.",
  reasoning: { effort: "high" },
  tools: [{
    type: "function",
    function: {
      name: "get_weather",
      description: "Get forecast for a city",
      parameters: {
        type: "object",
        properties: { city: { type: "string" }, day: { type: "string" } },
        required: ["city","day"]
      }
    }
  }],
  tool_choice: "auto"
});
```

> Tip: If your tools are brittle or slow, add guardrails (schema validation, retries, timeouts) and let GPT-5 handle errors and fallback plans under `high`.

---

## Structured Outputs (strongly recommended)

Force valid JSON with your schema to reduce retries and post-processing.

```python
resp = client.responses.create(
  model="gpt-5",
  input="Extract PII and return fields if found.",
  reasoning={"effort":"high"},
  response_format={
    "type":"json_schema",
    "json_schema":{
      "name":"PiiReport",
      "schema":{
        "type":"object",
        "properties":{
          "has_pii":{"type":"boolean"},
          "fields":{"type":"array","items":{"type":"string"}}
        },
        "required":["has_pii","fields"],
        "additionalProperties": False
      },
      "strict": True
    }
  }
)
```

---

## Cost planning & examples

* Example A (medium task, high effort)

  * 5,000 input tokens → input cost
  * 1,500 output tokens (final text) → output cost
  * 2,000 reasoning tokens (hidden) → output cost
  * **Total = input + output (incl. reasoning)**

* Example B (large context, high effort)

  * 120,000 input → input cost
  * 4,000 output + 6,000 reasoning → output cost
  * **Total = input + output (incl. reasoning)**

> Cost levers that don’t rely on a max-output setting:
>
> * Keep prompts focused; remove irrelevant context.
> * Use **`reasoning.effort: "high"` selectively**—only on steps that truly benefit.
> * Prefer **Structured Outputs** to avoid re-asks and long, verbose prose.
> * Stream to show progress while longer answers generate.

---

## Prompting tips for `high`

* **State goals and constraints crisply**; `high` shines when the problem is well-posed.
* Pair **deep thinking** with **concise delivery** by nudging `verbosity` to `"low"` if you want shorter final texts.
* In agentic flows, keep tools’ contracts small and precise; `high` uses those definitions to plan better.

---

## Guardrails & limits

* Leave headroom in the context for the model’s own hidden planning when you request **high** effort.
* Use **Structured Outputs** when downstream code expects JSON.
* For long tasks, **stream** results so users see progress while the model reasons.

---

## Minimal “Hello, High Reasoning” snippets

**Python**

```python
resp = client.responses.create(
  model="gpt-5",
  input="List attack trees for this threat model and mitigations.",
  reasoning={"effort":"high"}
)
print(resp.output_text)
```

**JavaScript**

```js
const r = await client.responses.create({
  model: "gpt-5",
  input: "Produce a 3-phase migration plan with risks.",
  reasoning: { effort: "high" }
});
console.log(r.output_text);
```

**cURL**

```bash
curl https://api.openai.com/v1/responses \
 -H "Authorization: Bearer $OPENAI_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{
   "model": "gpt-5",
   "input": "Design an eval to measure hallucinations.",
   "reasoning": {"effort":"high"}
 }'
```

---

If you want, I can tailor a **drop-in SDK wrapper** that defaults to `reasoning: "high"` plus sensible behaviors (streaming, Structured Outputs, tool guards) for your stack (FastAPI/Express/Cloudflare Workers/etc.).
