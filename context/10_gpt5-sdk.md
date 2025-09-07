# GPT-5 (High Reasoning) — Implementation Guide

This guide shows how to **use the `gpt-5` API with high reasoning effort**: what the setting does, when to use it, request syntax (Python, JavaScript, cURL), streaming, tool calling, Structured Outputs, cost planning, and practical tips.

---

## What “reasoning effort: high” does

`gpt-5` exposes a control that dials how hard the model “thinks” before answering. **Higher effort** improves multi-step reasoning, tool use planning, and adherence to tricky instructions, at the cost of **more output/“reasoning” tokens** and **higher latency**. Defaults to **`medium`** if you don’t set it. ([OpenAI][1])

On GPT-5 specifically, reasoning effort supports **`minimal`**, `low`, `medium` (default), and **`high`**. (The new **`minimal`** mode trades depth for speed; we mention it only to clarify the scale—this doc focuses on `high`.) ([OpenAI][2])

### When to choose `high`

* Complex, multi-step tasks (analysis, planning, code refactors, multihop QA)
* Agentic flows that require long chains of tool calls
* Safety-critical or quality-critical outputs where extra thought is worth the cost
  OpenAI’s cookbook guidance aligns with this: increase reasoning for complex tasks and agentic workflows. ([OpenAI Cookbook][3])

---

## Key model facts you’ll likely care about

* **Model ID:** `gpt-5` (use this exact string in API calls).
* **Context limits:** up to **\~272k input tokens** and **\~128k reasoning+output tokens** (≈ **400k total**). Plan headroom accordingly. ([OpenAI][2])
* **New controls:** `reasoning_effort` and `verbosity` (short/long answer bias). ([OpenAI][2])
* **Available in:** **Responses API** (recommended) and **Chat Completions**. ([OpenAI][2])
* **Supports:** streaming, tool calling, **Structured Outputs**, prompt caching, Batch API. ([OpenAI][2])

---

## Pricing (API)

OpenAI lists GPT-5 API pricing as:

* **Input tokens:** **\$1.25 per 1M tokens**
* **Output (incl. reasoning) tokens:** **\$10.00 per 1M tokens** ([OpenAI][2])

> Notes
> • **Reasoning tokens are billed as output tokens.** Expect higher spend when you set `high`. (Confirmed by OpenAI staff guidance on the official forum.) ([OpenAI Community][4])
> • Tokens for built-in tools (e.g., web/file) are billed at the chosen model’s token rates; see API pricing for tool-call fees and details. ([OpenAI][5])

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
    reasoning={"effort": "high"},     # <-- High reasoning
    verbosity="high",                 # Optional: steer longer answers
    max_output_tokens=1200            # Always cap to control cost/latency
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
  verbosity: "high",
  max_output_tokens: 1200
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
    "verbosity": "high",
    "max_output_tokens": 900
  }'
```

> Why Responses API? It preserves and can reuse **reasoning items** between turns, improving agentic performance and cost when you chain tool calls or multi-turn plans. ([OpenAI Cookbook][3])

### Chat Completions (if you must)

```python
from openai import OpenAI
client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role":"user","content":"Outline a phased SOC2 rollout."}],
    reasoning_effort="high",
    max_tokens=900
)
print(resp.choices[0].message.content)
```

> GPT-5 is available in **Chat Completions** as well; `reasoning_effort` is the control for thinking depth. ([OpenAI][2])

---

## Streaming

Enable streaming to see tokens as they arrive (useful when `high` increases latency). See the streaming reference for event names and client helpers. ([OpenAI][6])

```js
const stream = await client.responses.stream({
  model: "gpt-5",
  input: "Produce a step-by-step rollout plan.",
  reasoning: { effort: "high" },
  max_output_tokens: 1200
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

> GPT-5 also supports **custom tools** using plaintext I/O and optional regex/CFG constraints—handy for legacy CLI or DSL integrations. ([OpenAI][2])

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
  },
  max_output_tokens=300
)
```

Structured Outputs are supported by GPT-5 in the API. ([OpenAI][2])

---

## Cost planning & examples

**Prices:** \$1.25 / 1M input; \$10.00 / 1M output (includes reasoning). ([OpenAI][2])

* Example A (medium task, high effort)

  * 5,000 input tokens → **\$0.00625** (5,000 ÷ 1,000,000 × 1.25)
  * 1,500 output tokens (final text) → **\$0.01500** (1,500 ÷ 1,000,000 × 10)
  * 2,000 reasoning tokens (hidden) → **\$0.02000** (2,000 ÷ 1,000,000 × 10)
  * **Total ≈ \$0.04125**

* Example B (large context, high effort)

  * 120,000 input → **\$0.15000**
  * 4,000 output + 6,000 reasoning → **\$0.10000**
  * **Total ≈ \$0.25000**

> Tip: cap `max_output_tokens`, and only switch to `high` on the calls that truly need it. Reasoning tokens are billed as output. ([OpenAI Community][4])

---

## Prompting tips for `high`

* **State goals and constraints crisply**, then let the model think: `reasoning_effort: "high"` shines when the problem is well-posed.
* Use **`verbosity`** to keep the final answer compact even when reasoning is deep (e.g., `verbosity: "low"` with `effort: "high"` = deep thinking, concise answer). ([OpenAI][2])
* Prefer **Responses API** for agentic flows; reuse **previous\_response\_id** to carry reasoning context across steps and save tokens. ([OpenAI Cookbook][3])

---

## Guardrails & limits

* Stay within **\~272k input** and **\~128k reasoning+output** tokens (≈ 400k total). Plan a safety margin for reasoning if you set `high`. ([OpenAI][2])
* Use **Structured Outputs** when downstream code expects JSON. ([OpenAI][2])
* For long tasks, **stream** results so users see progress while the model reasons. ([OpenAI][6])

---

## Minimal “Hello, High Reasoning” snippets

**Python**

```python
resp = client.responses.create(
  model="gpt-5",
  input="List attack trees for this threat model and mitigations.",
  reasoning={"effort":"high"},
  max_output_tokens=800
)
print(resp.output_text)
```

**JavaScript**

```js
const r = await client.responses.create({
  model: "gpt-5",
  input: "Produce a 3-phase migration plan with risks.",
  reasoning: { effort: "high" },
  max_output_tokens: 800
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
   "reasoning": {"effort":"high"},
   "max_output_tokens": 600
 }'
```

---

## Appendix: feature references

* GPT-5 launch & parameters (`reasoning_effort`, `verbosity`), context window, availability & pricing overview. ([OpenAI][2])
* Default reasoning effort and parameter behavior in docs. ([OpenAI][1])
* Cookbook guidance on using higher reasoning for complex tasks and agentic flows; Responses API benefits. ([OpenAI Cookbook][3])
* Streaming API reference for event streams. ([OpenAI][6])
* API pricing page (tools & billing mechanics for web/file search, etc.). ([OpenAI][5])

---

If you want, I can tailor a **drop-in SDK wrapper** that defaults to `reasoning: "high"` plus sensible caps (e.g., `max_output_tokens`, `verbosity`) for your stack (FastAPI/Express/Cloudflare Workers/etc.).

[1]: https://platform.openai.com/docs/guides/reasoning/advice-on-prompting?reasoning-prompt-examples=research&utm_source=chatgpt.com "Reasoning models - OpenAI API"
[2]: https://openai.com/index/introducing-gpt-5-for-developers/ "Introducing GPT‑5 for developers | OpenAI"
[3]: https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide "GPT-5 prompting guide"
[4]: https://community.openai.com/t/is-03-mini-in-the-api-the-low-medium-or-high-version/1110423?utm_source=chatgpt.com "Is 03-mini in the API the \"low\", \"medium\" or \"high\" version?"
[5]: https://openai.com/api/pricing/?utm_source=chatgpt.com "Pricing - OpenAI"
[6]: https://platform.openai.com/docs/api-reference/streaming?utm_source=chatgpt.com "Streaming API responses - OpenAI API"
