```
/**
 * A reusable function to run a generation query against the Gemini API.
 * This function handles the boilerplate for making the fetch request,
 * managing the loading state of UI elements, and basic error handling.
 *
 * @param {object} payload - The complete payload to send to the Gemini API, including contents and generationConfig.
 * @param {object} buttonElements - An object containing references to UI elements to manage during the API call.
 * @param {HTMLElement} buttonElements.createBtn - The main button that triggers the action.
 * @param {HTMLElement} buttonElements.btnText - The text element inside the button.
 * @param {HTMLElement} buttonElements.spinner - The loading spinner element inside the button.
 * @param {HTMLElement} buttonElements.statusEl - An element to display error or status messages.
 * @returns {Promise<object|null>} - A promise that resolves with the parsed JSON response from the AI, or null if an error occurs.
 */
async function runAiGeneration(payload, buttonElements) {
    const { createBtn, btnText, spinner, statusEl } = buttonElements;
    // Disable the button and show the spinner to indicate loading
    createBtn.disabled = true;
    btnText.classList.add('hidden');
    spinner.classList.remove('hidden');
    statusEl.textContent = '';

    try {
        // The API key is left as an empty string. The environment will provide it.
        const apiKey = "";
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;
        
        // Make the POST request to the Gemini API
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }
        
        const result = await response.json();

        // Basic validation of the response structure
        if (!result.candidates || !result.candidates[0].content.parts[0].text) {
            throw new Error("Invalid response from AI.");
        }
        
        // The Gemini API returns the JSON as a string, so it needs to be parsed.
        return JSON.parse(result.candidates[0].content.parts[0].text);

    } catch (error) {
        console.error("AI Generation Error:", error);
        statusEl.textContent = "Sorry, an error occurred. Please try again.";
        return null;
    } finally {
        // Re-enable the button and hide the spinner regardless of the outcome
        createBtn.disabled = false;
        btnText.classList.remove('hidden');
        spinner.classList.add('hidden');
    }
}

/**
 * EXAMPLE 1: Creating a task using natural language.
 * This function builds a specific payload for the Gemini API to extract structured
 * task data from a user's text prompt.
 */
async function createTaskWithAI() {
    const prompt = document.getElementById('ai-prompt-input').value;
    if (!prompt) return;

    // UI elements to be controlled by the runAiGeneration function
    const buttonElements = {
        createBtn: document.getElementById('confirm-ai-modal'),
        btnText: document.getElementById('ai-confirm-btn-text'),
        spinner: document.getElementById('ai-spinner'),
        statusEl: document.getElementById('ai-status')
    };
    
    // Construct the payload with a specific prompt and a JSON schema
    // for the expected response.
    const payload = {
        contents: [{ 
            parts: [{ 
                text: `Extract task details from the following text. Today's date is ${moment().format('YYYY-MM-DD')}. The response must be a valid JSON object. Text: "${prompt}"` 
            }] 
        }],
        generationConfig: {
            responseMimeType: "application/json",
            responseSchema: {
                type: "OBJECT",
                properties: {
                    title: { type: "STRING", description: "The main title of the task." },
                    dueDate: { type: "STRING", description: "The due date in YYYY-MM-DD format. If a relative date is given, calculate it based on today's date." },
                    priority: { type: "STRING", description: "The priority level (low, medium, high). Infer from context if possible." },
                    notes: { type: "STRING", description: "Any additional notes or details from the prompt." }
                },
                required: ["title"]
            }
        }
    };
    
    const taskData = await runAiGeneration(payload, buttonElements);
    
    // If the API call was successful, proceed to save the data
    if (taskData) {
        console.log("AI Generated Task Data:", taskData);
        // In the actual app, this data would be saved to Firestore.
        // Example: await saveTaskToDatabase(taskData);
        document.getElementById('ai-modal').classList.add('hidden');
    }
}

/**
 * EXAMPLE 2: A simple text generation call for a motivational quote.
 * This function does not use the reusable `runAiGeneration` because it has
 * unique UI update logic and simpler error handling.
 */
async function getMotivationQuote() {
    const quoteEl = document.getElementById('motivation-quote');
    quoteEl.textContent = 'Thinking...';
    try {
        const apiKey = "";
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;
        const payload = { 
            contents: [{ 
                parts: [{ text: "Generate a short, powerful, and inspiring productivity quote." }] 
            }] 
        };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('API request failed');
        
        const result = await response.json();
        const quote = result.candidates[0].content.parts[0].text;
        
        // Update the UI with the generated quote
        quoteEl.textContent = `"${quote.replace(/"/g, '')}"`;

    } catch (error) {
        console.error("Motivation Quote Error:", error);
        // Provide a fallback quote on error
        quoteEl.textContent = '"The journey of a thousand miles begins with a single step."';
    }
}


```
