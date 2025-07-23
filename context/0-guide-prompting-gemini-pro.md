---

## A Detailed Guide to Writing High-Quality Prompts

Writing a good prompt is like being a great director for a brilliant actor. You don't just give them a line; you give them a character, a motivation, a scene, and precise instructions on how to deliver the performance. The two IMO prompts are masterclasses in this.

Let's break down the core principles that make them so effective.

### The 5 Pillars of an Excellent Prompt

A world-class prompt is built on five key pillars. We will analyze each one using the provided examples.

1.  **Role & Goal:** Define a clear persona and a specific, singular objective.
2.  **Context & Constraints:** Provide the "rules of the game," including what to do and, crucially, what *not* to do.
3.  **Process & Logic:** Instruct the model on *how* to think and reason, not just what to produce.
4.  **Structure & Format:** Dictate the exact output format with non-negotiable clarity.
5.  **Examples & Refinement:** Show the model what you want and ask it to self-correct.

---

### Pillar 1: Define a Clear Role and Goal (The Persona & Task)

This sets the entire stage. A vague role leads to a generic, uninspired response. A specific role activates the model's specialized knowledge and sets a professional tone.

**Why it's important:**
*   **Activates Expertise:** Telling the model it's an "expert mathematician and meticulous grader" is far more effective than "check this solution." It primes the model to use a specific part of its training associated with rigor, skepticism, and mathematical formality.
*   **Sets the Tone:** The persona dictates the language, style, and level of detail.

**How the examples do it:**
*   **Verification Prompt:** `You are an expert mathematician and a meticulous grader for an International Mathematical Olympiad (IMO) level exam.` This is a perfect, multi-layered persona:
    *   `expert mathematician`: implies deep subject knowledge.
    *   `meticulous grader`: implies a focus on detail and finding errors, not just understanding.
    *   `IMO level`: sets the difficulty and standard of rigor to the highest level.
*   **Step 1 Prompt:** The role is more implicit but equally strong: a research mathematician whose `primary goal is to produce a complete and rigorously justified solution.`

**How to apply this:**

| Vague (Bad)                               | Specific (Good)                                                                                             |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| "Summarize this business report."         | "Act as a C-suite executive. Summarize this report into a 5-bullet point memo for the board of directors."    |
| "Write some code to parse a CSV file."    | "You are a senior Python developer writing production-grade code. Write a function that parses a CSV file..." |
| "Check my writing for errors."            | "You are a professional copy editor for a major newspaper. Review the following text for grammatical errors..." |

---

### Pillar 2: Provide Context & Constraints (The Rules of the Game)

This is where you build the "fences" for the AI to operate within. The most powerful prompts often include **negative constraints** (what *not* to do).

**Why it's important:**
*   **Prevents "Drifting":** AI models can try to be "too helpful" by correcting errors when you only asked them to find them, or by guessing when they don't know the answer. Constraints prevent this.
*   **Focuses the Output:** Clear rules ensure the AI's effort is spent only on the desired task.

**How the examples do it:**
*   **Positive Constraints (What to do):**
    *   `Rigor is Paramount` (Step 1 Prompt): This is the guiding star for the entire task.
    *   `Use TeX for All Mathematics` (Step 1 Prompt): A specific, non-negotiable formatting rule.
*   **Negative Constraints (What NOT to do):**
    *   `You must **not** guess or create a solution that appears correct but contains hidden flaws` (Step 1 Prompt): This is a brilliant instruction to prevent hallucination.
    *   `You must act as a **verifier**, NOT a solver. **Do NOT attempt to correct the errors or fill the gaps you find.**` (Verification Prompt): This is a critical instruction that keeps the AI laser-focused on its one job.

**How to apply this:**
*   **Task:** Generate marketing copy.
*   **Constraint:** `Do not use clichés like "game-changer" or "synergy." The tone should be professional but approachable. Avoid making promises we can't legally guarantee.`

---

### Pillar 3: Guide the Model's Reasoning Process (The "How-To")

This is an advanced technique that separates good prompts from great ones. Instead of just asking for an outcome, you are programming a **decision-making framework** for the model to follow.

**Why it's important:**
*   **Handles Ambiguity:** Real-world tasks have edge cases. Guiding the reasoning process tells the model how to handle them systematically.
*   **Increases Reliability:** A defined process is more likely to produce a correct and consistent result than leaving the model to its own devices.

**How the examples do it:**
The "Verification Prompt" is the gold standard here with its `How to Handle Issues` section.
*   **It creates a classification system:** `Critical Error` vs. `Justification Gap`. This is far better than just saying "find errors."
*   **It provides a procedure for each class:**
    *   For a `Critical Error`: "Explain the error... state that it invalidates the current line of reasoning... Do NOT check any further steps that rely on this error."
    *   For a `Justification Gap`: "Explain the gap... assume the step's conclusion is true... proceed to verify all subsequent steps."
    This is a sophisticated algorithm embedded directly in the prompt.

**How to apply this:**
*   **Task:** Triage customer support tickets.
*   **Process:** `First, classify the ticket's sentiment as Positive, Neutral, or Negative. Second, categorize the issue as one of: [Billing, Technical, Feature Request]. If the sentiment is Negative AND the category is Billing, flag it as URGENT. For all others, flag as NORMAL.`

---

### Pillar 4: Specify the Desired Output Structure and Format (The Blueprint)

Never assume the model will format its response the way you want. You must be ruthlessly specific. This is critical for consistency and for making the output easy to parse, either by a human or another program.

**Why it's important:**
*   **Predictability:** You get the same structure every time.
*   **Parsability:** If you're using the AI's output in a downstream application, a strict format (like JSON, Markdown with specific headers, etc.) is essential.
*   **Clarity:** A well-structured output is easier for a human to read and understand.

**How the examples do it:**
Both prompts are exceptionally strong here.
*   **Forceful Language:** They use words like `MUST`, `in this exact order`, and `ONLY`.
*   **Clear Hierarchy:** They use Markdown headers (`###`), bolding (`**`), and numbered/lettered lists to define a clear document structure.
    *   `1. Summary`
        *   `a. Verdict`
        *   `b. Method Sketch`
    *   `2. Detailed Solution`
*   **Content Prescription:** They don't just name the sections; they describe exactly what content goes in each one (e.g., "State clearly whether you have found a complete solution...").

**How to apply this:**
*   **Bad:** "Give me the pros and cons."
*   **Good:**
    ```markdown
    Your response MUST be a Markdown document with the following structure:

    # Analysis of [Topic]

    ## Pros
    - [Bulleted list of advantages]

    ## Cons
    - [Bulleted list of disadvantages]

    ## Final Recommendation
    **Recommendation:** [State your final recommendation in one bolded sentence]
    **Justification:** [Provide a 2-3 sentence justification for your recommendation]
    ```

---

### Pillar 5: Include Examples and Refinement Loops (Show, Don't Tell)

Models learn well from examples (this is called "few-shot" or "one-shot" prompting). Providing a small, concrete example of the desired output within the prompt itself is incredibly effective. Furthermore, asking the model to review its own work adds a layer of quality control.

**Why it's important:**
*   **Reduces Ambiguity:** An example can clarify complex formatting or stylistic requirements better than words alone.
*   **Improves Quality:** A self-correction step forces the model to do an internal check against the rules you've set, catching errors before the final output is generated.

**How the examples do it:**
*   **Example (One-Shot Learning):** The "Verification Prompt" includes a perfect, concise `Example of the Required Summary Format`. It shows exactly how to structure the `List of Findings` with `Location` and `Issue` sub-bullets.
*   **Refinement Loop:** The "Step 1 Prompt" has a `Self-Correction Instruction` section. It explicitly tells the model: `Before finalizing your output, carefully review your "Method Sketch" and "Detailed Solution" to ensure they are clean, rigorous, and strictly adhere to all instructions...`

**How to apply this:**
*   **Task:** Extract information from a block of text.
*   **Prompt Snippet:**
    ```
    ...
    ### Output Format ###
    Your output must be a JSON object with the keys "name", "date", and "amount".

    ### Example ###
    Text: "The invoice for John Smith is due on 2024-12-01 for a total of $150.75."
    Output:
    {
      "name": "John Smith",
      "date": "2024-12-01",
      "amount": 150.75
    }

    ### Final Review ###
    Before providing the final JSON, double-check that all values have the correct data type (e.g., amount is a number, not a string).
    ```

---

### Putting It All Together: A General-Purpose Template

Based on this analysis, here is a template you can adapt for your own complex tasks.

```markdown
### Role and Goal ###
You are a [EXPERT PERSONA]. Your primary goal is to [SPECIFIC, SINGULAR OBJECTIVE].

### Core Instructions & Constraints ###
- The most important principle is [GUIDING PRINCIPLE, e.g., clarity, accuracy, brevity].
- You MUST [POSITIVE CONSTRAINT #1].
- You MUST [POSITIVE CONSTRAINT #2].
- You MUST NOT [NEGATIVE CONSTRAINT #1, e.g., invent information, exceed 500 words].
- You MUST NOT [NEGATIVE CONSTRAINT #2].

### Reasoning Process ###
To accomplish your goal, follow these steps in order:
1.  **First,** [Step 1 of your desired thought process].
2.  **Second,** [Step 2 of your desired thought process].
3.  **If you encounter [EDGE CASE], you must handle it by [PROCEDURE FOR EDGE CASE].**

### Output Format ###
Your response MUST be structured using Markdown in the following exact format. Do not add any conversational text or introductions outside of this structure.

# [Main Title]

## [Section 1 Title]
[Description of content for Section 1. Be specific about formatting, e.g., "A bulleted list..."]

## [Section 2 Title]
[Description of content for Section 2. Be specific about formatting, e.g., "A table with three columns..."]

### Example of Section 2 ###
| Column A | Column B | Column C |
|----------|----------|----------|
| ...      | ...      | ...      |

### Self-Correction Step ###
Before finalizing your response, review your entire output. Ensure that it strictly adheres to all instructions, that the format is correct, and that you have fulfilled the [ROLE AND GOAL] accurately.

### Input Data ###

[PASTE YOUR INPUT TEXT/DATA/QUESTION HERE]
```

2 PROMPTS EXAMPLES: 
"""


Here is the exact text for the "Step 1 Prompt" from the paper "Gemini 2.5 Pro Capable of Winning Gold at IMO 2025":

```
### Core Instructions ###

**Rigor is Paramount:** Your primary goal is to produce a complete and rigorously justified solution. Every step in your solution must be logically sound and clearly explained. A correct final answer derived from flawed or incomplete reasoning is considered a failure.

**Honesty About Completeness:** If you cannot find a complete solution, you must **not** guess or create a solution that appears correct but contains hidden flaws or justification gaps. Instead, you should present only significant partial results that you can rigorously prove. A partial result is considered significant if it represents a substantial advancement toward a full solution. Examples include:

*   Proving a key lemma.
*   Fully resolving one or more cases within a logically sound case-based proof.
*   Establishing a critical property of the mathematical objects in the problem.
*   For an optimization problem, proving an upper or lower bound without proving that this bound is achievable.

**Use TeX for All Mathematics:** All mathematical variables, expressions, and relations must be enclosed in TeX delimiters (e.g., ‘Let $n$ be an integer.‘).

### Output Format ###

Your response MUST be structured into the following sections, in this exact order.

**1. Summary**

Provide a concise overview of your findings. This section must contain two parts:

*   **a. Verdict:** State clearly whether you have found a complete solution or a partial solution.
    *   **For a complete solution:** State the final answer, e.g., "I have successfully solved the problem. The final answer is..."
    *   **For a partial solution:** State the main rigorous conclusion(s) you were able to prove, e.g., "I have not found a complete solution, but I have rigorously proven that..."

*   **b. Method Sketch:** Present a high-level, conceptual outline of your solution. This sketch should allow an expert to understand the logical flow of your argument without reading the full detail. It should include:
    *   A narrative of your overall strategy.
    *   The full and precise mathematical statements of any key lemmas or major intermediate results.
    *   If applicable, describe any key constructions or case splits that form the backbone of your argument.

**2. Detailed Solution**

Present the full, step-by-step mathematical proof. Each step must be logically justified and clearly explained. The level of detail should be sufficient for an expert to verify the correctness of your reasoning without needing to fill in any gaps. This section must contain ONLY the complete, rigorous proof, free of any internal commentary, alternative approaches, or failed attempts.

### Self-Correction Instruction ###

Before finalizing your output, carefully review your "Method Sketch" and "Detailed Solution" to ensure they are clean, rigorous, and strictly adhere to all instructions provided above. Verify that every statement contributes directly to the final, coherent mathematical argument.
```



The other prompt in the paper is the "Verification Prompt". Here is the full text of that prompt:

```
You are an expert mathematician and a meticulous grader for an International Mathematical Olympiad (IMO) level exam. Your primary task is to rigorously verify the provided mathematical solution. A solution is to be judged correct **only if every step is rigorously justified.** A solution that arrives at a correct final answer through flawed reasoning, educated guesses, or with gaps in its arguments must be flagged as incorrect or incomplete.

### Instructions ###

**1. Core Instructions**

*   Your sole task is to find and report all issues in the provided solution. You must act as a **verifier**, NOT a solver. **Do NOT attempt to correct the errors or fill the gaps you find.**
*   You must perform a **step-by-step** check of the entire solution. This analysis will be presented in a **Detailed Verification Log**, where you justify your assessment of each step: for correct steps, a brief justification suffices; for steps with errors or gaps, you must provide a detailed explanation.

**2. How to Handle Issues in the Solution**

When you identify an issue in a step, you MUST first classify it into one of the following two categories and then follow the specified procedure.

*   **a. Critical Error:**
    This is any error that breaks the logical chain of the proof. This includes both **logical fallacies** (e.g., claiming that ‘A>B, C>D‘ implies ‘A-C>B-D‘) and **factual errors** (e.g., a calculation error like '2+3=6').
    **Procedure:**
    *   Explain the specific error and state that it **invalidates the current line of reasoning**.
    *   Do NOT check any further steps that rely on this error.
    *   You MUST, however, scan the rest of the solution to identify and verify any fully independent parts. For example, if a proof is split into multiple cases, an error in one case does not prevent you from checking the other cases.

*   **b. Justification Gap:**
    This is for steps where the conclusion may be correct, but the provided argument is incomplete, hand-wavy, or lacks sufficient rigor.
    **Procedure:**
    *   Explain the gap in the justification.
    *   State that you will **assume the step's conclusion is true** for the sake of argument.
    *   Then, proceed to verify all subsequent steps to check if the remainder of the argument is sound.

**3. Output Format**

Your response MUST be structured into two main sections: a **Summary** followed by the **Detailed Verification Log**.

*   **a. Summary**
    This section MUST be at the very beginning of your response. It must contain two components:
    *   **Final Verdict**: A single, clear sentence declaring the overall validity of the solution. For example: "The solution is correct," "The solution contains a Critical Error and is therefore invalid," or "The solution's approach is viable but contains several Justification Gaps."
    *   **List of Findings**: A bulleted list that summarizes **every** issue you discovered. For each finding, you must provide:
        *   **Location:** A direct quote of the key phrase or equation where the issue occurs.
        *   **Issue:** A brief description of the problem and its classification (**Critical Error** or **Justification Gap**).

*   **b. Detailed Verification Log**
    Following the summary, provide the full, step-by-step verification log as defined in the Core Instructions. When you refer to a specific part of the solution, **quote the relevant text** to make your reference clear before providing your detailed analysis of that part.

**Example of the Required Summary Format**
*This is a generic example to illustrate the required format. Your findings must be based on the actual solution provided below.*

**Final Verdict:** The solution is **invalid** because it contains a Critical Error.

**List of Findings:**
*   **Location:** "By interchanging the limit and the integral, we get..."
    *   **Issue:** Justification Gap - The solution interchanges a limit and an integral without providing justification, such as proving uniform convergence.
*   **Location:** "From $A > B$ and $C > D$, it follows that $A-C > B-D$"
    *   **Issue:** Critical Error - This step is a logical fallacy. Subtracting inequalities in this manner is not a valid mathematical operation.

### Problem ###

[Paste the TeX for the problem statement here]

### Solution ###

[Paste the TeX for the solution to be verified here]

### Verification Task Reminder ###

Your task is to act as an IMO grader. Now, generate the **summary** and the **step-by-step verification log** for the solution above. In your log, justify each correct step and explain in detail any errors or justification gaps you find, as specified in the instructions above.
```
"""
