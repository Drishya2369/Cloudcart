# Lambda & API Gateway Q&A Notes

## Q1: What is AWS Lambda?

AWS Lambda lets you run code without owning or managing a server.
You upload a function, AWS keeps it dormant, and the moment
something "wakes it up," it runs your code and then goes back to
sleep. You're billed only for the milliseconds it actually executed.

The light switch analogy:
- Light is OFF when nobody needs it
- Flip the switch -> light turns ON instantly
- Light does its job -> you flip it off
- You pay only for electricity actually used

---

## Q2: What are the 3 things every Lambda function needs?

| Thing    | What it is                  | In CloudCart                                  |
|----------|------------------------------|------------------------------------------------|
| Trigger  | What wakes it up             | API Gateway (a POST request)                   |
| Code     | What it does once awake      | order_processor.py — validates and saves order |
| Role     | What it's allowed to touch   | LambdaOrderProcessorRole — DynamoDB access      |

Without all three, Lambda is useless — code with no trigger never
runs; a trigger with no permissions fails the moment it tries to do
anything.

---

## Q3: What are `event` and `context` in the Lambda handler?

```python
def lambda_handler(event, context):
    # your code
    return {...}
```

- **event** = the data coming IN (in CloudCart: the order JSON from
  the API request body, accessed via `event['body']`)
- **context** = metadata about the execution itself (time remaining,
  function name) — barely used in CloudCart

---

## Q4: Why does Lambda need IAM permissions at all?

Lambda has zero permissions by default. Every AWS service it touches
must be explicitly granted via an execution role. CloudCart uses a
dedicated role — `LambdaOrderProcessorRole` — rather than reusing an
admin role, with exactly two policies:

- `AmazonDynamoDBFullAccess` — read/write access to DynamoDB
- `AWSLambdaBasicExecutionRole` — permission to write CloudWatch logs

A narrowly-scoped role keeps the blast radius small: this Lambda can
only touch DynamoDB and CloudWatch, nothing else in the account.

---

## Q5: Why Lambda instead of EC2 for this project?

Order processing is a short-lived task — receive one order, write
one record, respond. There's no need for an always-on server.

| | EC2 | Lambda |
|---|---|---|
| Model | Always-ON server | Runs only when triggered |
| Pricing | Pay 24/7 | Pay per execution |
| Scaling | Manual setup | Auto-scales instantly |
| Management | You manage everything | AWS manages everything |
| Startup | Minutes | Milliseconds |

Lambda only runs (and only costs anything) when a request actually
arrives, and scales automatically if multiple orders come in at once.

---

## Q6: What problem does API Gateway solve?

A Lambda function has no public URL. It's a worker sitting inside
AWS with no door to the outside world — nobody can call it directly.

API Gateway is the public door. It's the only thing with an
internet-facing URL. When a request hits that URL, API Gateway
decides which Lambda function to invoke.

```
Postman/Bhavini -> API Gateway (public door) -> Lambda (the worker) -> DynamoDB (the filing cabinet)
```

Without API Gateway, Lambda exists but is functionally invisible to
the outside world.

---

## Q7: Why HTTP API instead of REST API?

CloudCart needs one simple thing — a `POST /order_processor` route
that triggers Lambda. Nothing more.

| | HTTP API (chosen) | REST API |
|---|---|---|
| Primary use | Simple, thin door to Lambda | Caching, API keys, usage plans |
| Cost | Cheaper, lower latency | More expensive |
| Complexity | Minimal | More configuration |

HTTP API is built specifically for the "thin door to Lambda" pattern
this project needs. REST API's extra features (caching, API keys,
usage plans, WAF integration) aren't needed here.

---

## Q8: What caused the region mismatch bug, and how was it fixed?

**Issue:** The Lambda function was first created in `us-east-1` (the
console's default region) while the `Orders` table and S3 bucket
were in `eu-west-1`. The function deployed without error, but every
invocation failed at runtime with `ResourceNotFoundException`.

**Fix:** Deleted and recreated the Lambda function after switching
the console's active region to `eu-west-1`, so the function, table,
and bucket are now co-located.

**Takeaway:** A region mismatch does not surface as an error at
creation time — only at runtime — and the error message looks
identical to "the table doesn't exist" rather than "the table is in
another region." Always confirm the active region before creating
any resource that needs to talk to another one.

---

## Q9: What's the difference between testing a Test Event in the Lambda console vs. testing via Postman?

- **Test Event in console** (proves the CODE LOGIC is correct) —
  hand-feeds the function an `event` manually, with no API Gateway
  involved. Good for catching bugs in the code itself.
- **Postman -> API Gateway** (proves the ENTIRE SYSTEM is correct) —
  door, worker, and filing cabinet all wired together properly.

Both matter. Skipping straight to API Gateway risks debugging a code
bug through a network call. Testing the Lambda directly first is the
right order — isolate code correctness before testing the full path.

---

## Q10: What was actually verified end-to-end for Phase 2?

Tested via Postman:

```
POST https://5hlc6h2wh4.execute-api.eu-west-1.amazonaws.com/default/order_processor

Request body:
{
  "orderId": "ORD-002",
  "customerName": "Anita Sharma",
  "product": "iPhone 15",
  "amount": 80000
}

Response: 200 OK
{"message": "Order received successfully!", "orderId": "ORD-002"}
```

Confirmed directly in DynamoDB — both `ORD-001` (console test event)
and `ORD-002` (Postman request) are present in the `Orders` table
with all attributes correctly saved.
