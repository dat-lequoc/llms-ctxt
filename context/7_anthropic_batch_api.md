# ANTHORPIC BATCH API

### Batch processing

Batch processing is a powerful approach for handling large volumes of requests efficiently. Instead of processing requests one at a time with immediate responses, batch processing allows you to submit multiple requests together for asynchronous processing. This pattern is particularly useful when:

*   You need to process large volumes of data
*   Immediate responses are not required
*   You want to optimize for cost efficiency
*   You're running large-scale evaluations or analyses

The Message Batches API is our first implementation of this pattern.

### **Message BatCHES API.**

The Message Batches API is a powerful, cost-effective way to asynchronously process large volumes of Messages requests. This approach is well-suited to tasks that do not require immediate responses, with most batches finishing in less than 1 hour while reducing costs by 50% and increasing throughput.

You can explore the API reference directly, in addition to this guide.

### **How the Message Batches API works**

When you send a request to the Message Batches API:

1.  The system creates a new Message Batch with the provided Messages requests.
2.  The batch is then processed asynchronously, with each request handled independently.
3.  You can poll for the status of the batch and retrieve results when processing has ended for all requests.

This is especially useful for bulk operations that don't require immediate results, such as:

*   **Large-scale evaluations**: Process thousands of test cases efficiently.
*   **Content moderation**: Analyze large volumes of user-generated content asynchronously.
*   **Data analysis**: Generate insights or summaries for large datasets.
*   **Bulk content generation**: Create large amounts of text for various purposes (e.g., product descriptions, article summaries).

### **Batch limitations**

*   A Message Batch is limited to either 100,000 Message requests or 256 MB in size, whichever is reached first.
*   We process each batch as fast as possible, with most batches completing within 1 hour.
*   You will be able to access batch results when all messages have completed or after 24 hours, whichever comes first.
*   Batches will expire if processing does not complete within 24 hours.
*   Batch results are available for 29 days after creation. After that, you may still view the Batch, but its results will no longer be available for download.
*   Batches are scoped to a Workspace. You may view all batches—and their results—that were created within the Workspace that your API key belongs to.
*   Rate limits apply to both Batches API HTTP requests and the number of requests within a batch waiting to be processed. See Message Batches API rate limits.
*   Additionally, we may slow down processing based on current demand and your request volume. In that case, you may see more requests expiring after 24 hours.
*   Due to high throughput and concurrent processing, batches may go slightly over your Workspace's configured spend limit.

### **Supported models**

The Message Batches API currently supports:

*   Claude Opus 4.1 (`claude-opus-4-1-20250805`)
*   Claude Opus 4 (`claude-opus-4-20250514`)
*   Claude Sonnet 4 (`claude-sonnet-4-20250514`)
*   Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`)
*   Claude Sonnet 3.5 (deprecated) (`claude-3-5-sonnet-20240620` and `claude-3-5-sonnet-20241022`)
*   Claude Haiku 3.5 (`claude-3-5-haiku-20241022`)
*   Claude Haiku 3 (`claude-3-haiku-20240307`)
*   Claude Opus 3 (deprecated) (`claude-3-opus-20240229`)

### **What can be batched**

Any request that you can make to the Messages API can be included in a batch. This includes:

*   Vision
*   Tool use
*   System messages
*   Multi-turn conversations
*   Any beta features

Since each request in the batch is processed independently, you can mix different types of requests within a single batch.

Since batches can take longer than 5 minutes to process, consider using the 1-hour cache duration with prompt caching for better cache hit rates when processing batches with shared context.

### **Pricing**

The Batches API offers significant cost savings. All usage is charged at 50% of the standard API prices.

| Model | Batch input | Batch output |
| :--- | :--- | :--- |
| Claude Opus 4.1 | $7.50 / MTok | $37.50 / MTok |
| Claude Opus 4 | $7.50 / MTok | $37.50 / MTok |
| Claude Sonnet 4 | $1.50 / MTok | $7.50 / MTok |
| Claude Sonnet 3.7 | $1.50 / MTok | $7.50 / MTok |
| Claude Sonnet 3.5 (deprecated) | $1.50 / MTok | $7.50 / MTok |
| Claude Haiku 3.5 | $0.40 / MTok | $2 / MTok |
| Claude Opus 3 (deprecated) | $7.50 / MTok | $37.50 / MTok |
| Claude Haiku 3 | $0.125 / MTok | $0.625 / MTok |

### **How to use the Message Batches API**

#### **Prepare and create your batch**

A Message Batch is composed of a list of requests to create a Message. The shape of an individual request is comprised of:

*   A unique `custom_id` for identifying the Messages request
*   A `params` object with the standard Messages API parameters

You can create a batch by passing this list into the `requests` parameter.

When a batch is first created, the response will have a processing status of `in_progress`.

#### **Tracking your batch**

The Message Batch's `processing_status` field indicates the stage of processing the batch is in. It starts as `in_progress`, then updates to `ended` once all the requests in the batch have finished processing, and results are ready. You can monitor the state of your batch by visiting the Console, or using the retrieval endpoint.

You can poll this endpoint to know when processing has ended.

#### **Retrieving batch results**

Once batch processing has ended, each Messages request in the batch will have a result. There are 4 result types:

| Result Type | Description |
| :--- | :--- |
| `succeeded` | Request was successful. Includes the message result. |
| `errored` | Request encountered an error and a message was not created. Possible errors include invalid requests and internal server errors. You will not be billed for these requests. |
| `canceled` | User canceled the batch before this request could be sent to the model. You will not be billed for these requests. |
| `expired` | Batch reached its 24 hour expiration before this request could be sent to the model. You will not be billed for these requests. |

You will see an overview of your results with the batch's `request_counts`, which shows how many requests reached each of these four states.

Results of the batch are available for download at the `results_url` property on the Message Batch, and if the organization permission allows, in the Console. Because of the potentially large size of the results, it's recommended to stream results back rather than download them all at once.

The results will be in `.jsonl` format, where each line is a valid JSON object representing the result of a single request in the Message Batch. For each streamed result, you can do something different depending on its `custom_id` and result type.

If your result has an error, its `result.error` will be set to our standard error shape.

**Batch results may not match input order**

Batch results can be returned in any order, and may not match the ordering of requests when the batch was created. To correctly match results with their corresponding requests, always use the `custom_id` field.

### **Using prompt caching with Message Batches**

The Message Batches API supports prompt caching, allowing you to potentially reduce costs and processing time for batch requests. The pricing discounts from prompt caching and Message Batches can stack, providing even greater cost savings when both features are used together. However, since batch requests are processed asynchronously and concurrently, cache hits are provided on a best-effort basis. Users typically experience cache hit rates ranging from 30% to 98%, depending on their traffic patterns.

To maximize the likelihood of cache hits in your batch requests:

*   Include identical `cache_control` blocks in every Message request within your batch
*   Maintain a steady stream of requests to prevent cache entries from expiring after their 5-minute lifetime
*   Structure your requests to share as much cached content as possible

### **Best practices for effective batching**

To get the most out of the Batches API:

*   Monitor batch processing status regularly and implement appropriate retry logic for failed requests.
*   Use meaningful `custom_id` values to easily match results with requests, since order is not guaranteed.
*   Consider breaking very large datasets into multiple batches for better manageability.
*   Dry run a single request shape with the Messages API to avoid validation errors.

### **Troubleshooting common issues**

If experiencing unexpected behavior:

*   Verify that the total batch request size doesn't exceed 256 MB. If the request size is too large, you may get a `413 request_too_large` error.
*   Check that you're using supported models for all requests in the batch.
*   Ensure each request in the batch has a unique `custom_id`.
*   Ensure that it has been less than 29 days since batch `created_at` (not processing `ended_at`) time. If over 29 days have passed, results will no longer be viewable.
*   Confirm that the batch has not been canceled.

Note that the failure of one request in a batch does not affect the processing of other requests.

### **Batch storage and privacy**

*   **Workspace isolation**: Batches are isolated within the Workspace they are created in. They can only be accessed by API keys associated with that Workspace, or users with permission to view Workspace batches in the Console.
*   **Result availability**: Batch results are available for 29 days after the batch is created, allowing ample time for retrieval and processing.

### **FAQ**

**How long does it take for a batch to process?**

Batches may take up to 24 hours for processing, but many will finish sooner. Actual processing time depends on the size of the batch, current demand, and your request volume. It is possible for a batch to expire and not complete within 24 hours.

**Is the Batches API available for all models?**

See above for the list of supported models.

**Can I use the Message Batches API with other API features?**

Yes, the Message Batches API supports all features available in the Messages API, including beta features. However, streaming is not supported for batch requests.

**How does the Message Batches API affect pricing?**

The Message Batches API offers a 50% discount on all usage compared to standard API prices. This applies to input tokens, output tokens, and any special tokens. For more on pricing, visit our pricing page.

**Can I update a batch after it's been submitted?**

No, once a batch has been submitted, it cannot be modified. If you need to make changes, you should cancel the current batch and submit a new one. Note that cancellation may not take immediate effect.

**Are there Message Batches API rate limits and do they interact with the Messages API rate limits?**

The Message Batches API has HTTP requests-based rate limits in addition to limits on the number of requests in need of processing. See Message Batches API rate limits. Usage of the Batches API does not affect rate limits in the Messages API.

**How do I handle errors in my batch requests?**

When you retrieve the results, each request will have a `result` field indicating whether it `succeeded`, `errored`, was `canceled`, or `expired`. For `errored` results, additional error information will be provided. View the error response object in the API reference.

**How does the Message Batches API handle privacy and data separation?**

The Message Batches API is designed with strong privacy and data separation measures:

*   Batches and their results are isolated within the Workspace in which they were created. This means they can only be accessed by API keys from that same Workspace.
*   Each request within a batch is processed independently, with no data leakage between requests.
*   Results are only available for a limited time (29 days), and follow our data retention policy.
*   Downloading batch results in the Console can be disabled on the organization-level or on a per-workspace basis.

**Can I use prompt caching in the Message Batches API?**

Yes, it is possible to use prompt caching with Message Batches API. However, because asynchronous batch requests can be processed concurrently and in any order, cache hits are provided on a best-effort basis.

You are absolutely right. My apologies for omitting the code in the initial summary. The page does indeed contain Python code examples for using the Batch API. I have retrieved them for you now.

Here is the Python code from the documentation for each step of the batch processing workflow.

### 1. Create a Batch

This code demonstrates how to prepare a list of message requests and submit them as a new batch job. Each request includes a unique `custom_id` for tracking and the standard parameters you would use in the Messages API.

You are absolutely right. My apologies for omitting the code in the initial summary. The page does indeed contain Python code examples for using the Batch API. I have retrieved them for you now.

Here is the Python code from the documentation for each step of the batch processing workflow.

### 1. Create a Batch

This code demonstrates how to prepare a list of message requests and submit them as a new batch job. Each request includes a unique `custom_id` for tracking and the standard parameters you would use in the Messages API.

```python
import anthropic
import os

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="YOUR_API_KEY",
)

# Prepare a list of requests
requests = [
    {
        "custom_id": "request_1",
        "params": {
            "model": "claude-3-haiku-20240307",
            "messages": [{"role": "user", "content": "Why is the sky blue?"}],
            "max_tokens": 1024,
        },
    },
    {
        "custom_id": "request_2",
        "params": {
            "model": "claude-3-haiku-20240307",
            "messages": [{"role": "user", "content": "What's the best thing about the number 42?"}],
            "max_tokens": 1024,
        },
    },
    # ... more requests
]

# Create the batch
try:
    batch = client.messages.create_batch(requests=requests)
    print("Batch created:", batch)
except anthropic.APIError as e:
    print(f"API Error: {e.status_code} {e.type} {e.message}")
```

### 2. Track Your Batch

After creating the batch, you can poll its status using the `id` from the creation response. The `processing_status` will change from `in_progress` to `ended` when the results are ready.

```python
import anthropic

client = anthropic.Anthropic()

batch_id = "msg_batch_abc123" # replace with your batch ID

try:
    retrieved_batch = client.messages.retrieve_batch(batch_id=batch_id)
    print("Retrieved batch:", retrieved_batch)
except anthropic.APIError as e:
    print(f"API Error: {e.status_code} {e.type} {e.message}")
```

### 3. Retrieve Batch Results

Once the batch has finished processing, you can download the results from the `results_url`. The results are in `.jsonl` format, so you should stream the response and process it line by line.

```python
import anthropic
import requests
import json

client = anthropic.Anthropic()

batch_id = "msg_batch_abc123" # replace with your batch ID

try:
    retrieved_batch = client.messages.retrieve_batch(batch_id=batch_id)

    if retrieved_batch.results_url:
        # The results_url is a pre-signed URL that is valid for 1 hour
        response = requests.get(retrieved_batch.results_url)
        response.raise_for_status()

        # Process the results line by line
        for line in response.iter_lines():
            if line:
                result = json.loads(line)
                # Process each result as needed
                print(result)

    else:
        print("Results are not yet available.")

except anthropic.APIError as e:
    print(f"API Error: {e.status_code} {e.type} {e.message}")
except requests.exceptions.RequestException as e:
    print(f"HTTP Request Error: {e}")
```
