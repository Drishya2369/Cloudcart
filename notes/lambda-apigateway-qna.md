# Lambda & API Gateway Q&A Notes

## Q1: What is AWS Lambda?

AWS Lambda lets you run code without owning or managing a server.
You upload a function, AWS keeps it dormant, and the moment
something "wakes it up," it runs your code and then goes back to
sleep. You're billed only for the milliseconds it actually executed.

The light switch analogy:
- Light is OFF when nobody needs it
- Flip the switch → light turns ON instantly
- Light does its job → you flip it off
- You pay only for electricity actually used

---

## Q2: What are the 3 things every Lambda function needs?

| Thing | What it is | In CloudCart |
|-------|------------|--------------|
| Trigger | What wakes it up | API Gateway (a POST request) |
| Code | What it does once awake | order_processor.py — validates and saves order |
| Role | What it's allowed to touch | LambdaOrderProcessorRole — DynamoDB access |

Without all three, Lambda is useless — code with no trigger never runs; a trigger with no permissions fails the moment it tries to do anything.

---

## Q3: What are `event` and `context` in the Lambda handler?

```python
def lambda_handler(event, context):
    # your code
    return {...}
```

- **event** = the data coming IN (in CloudCart: the order JSON from the API request body, accessed via `event['body']`)
- **context** = metadata about the execution itself (time remaining, function name) — barely used in CloudCart

---

## Q4: Why does Lambda need IAM permissions at all?

Lambda has zero permissions by default. Every AWS service it touches must be explicitly granted via an execution role. CloudCart uses a dedicated role — `LambdaOrderProcessorRole` — with exactly two policies:

- `AmazonDynamoDBFullAccess` — read/write access to DynamoDB
- `AWSLambdaBasicExecutionRole` — permission to write CloudWatch logs

A narrowly-scoped role keeps the blast radius small: this Lambda can only touch DynamoDB and CloudWatch, nothing else in the account.

---

## Q5: Why Lambda instead of EC2 for this project?

| | EC2 | Lambda |
|---|---|---|
| Model | Always-ON server | Runs only when triggered |
| Pricing | Pay 24/7 | Pay per execution |
| Scaling | Manual setup | Auto-scales instantly |
| Management | You manage everything | AWS manages everything |
| Startup | Minutes | Milliseconds |

Order processing is a short-lived task — receive one order, write one record, respond. No need for an always-on server.

---

# Lambda & API Gateway Q&A Notes

## Q1: What is AWS Lambda?

AWS Lambda lets you run code without owning or managing a server.
You upload a function, AWS keeps it dormant, and the moment
something "wakes it up," it runs your code and then goes back to
sleep. You're billed only for the milliseconds it actually executed.

The light switch analogy:
- Light is OFF when nobody needs it
- Flip the switch → light turns ON instantly
- Light does its job → you flip it off
- You pay only for electricity actually used

---

## Q2: What are the 3 things every Lambda function needs?

| Thing | What it is | In CloudCart |
|-------|------------|--------------|
| Trigger | What wakes it up | API Gateway (a POST request) |
| Code | What it does once awake | order_processor.py — validates and saves order |
| Role | What it's allowed to touch | LambdaOrderProcessorRole — DynamoDB access |

Without all three, Lambda is useless — code with no trigger never runs; a trigger with no permissions fails the moment it tries to do anything.

---

## Q3: What are `event` and `context` in the Lambda handler?

```python
def lambda_handler(event, context):
    # your code
    return {...}
```

- **event** = the data coming IN (in CloudCart: the order JSON from the API request body, accessed via `event['body']`)
- **context** = metadata about the execution itself (time remaining, function name) — barely used in CloudCart

---

## Q4: Why does Lambda need IAM permissions at all?

Lambda has zero permissions by default. Every AWS service it touches must be explicitly granted via an execution role. CloudCart uses a dedicated role — `LambdaOrderProcessorRole` — with exactly two policies:

- `AmazonDynamoDBFullAccess` — read/write access to DynamoDB
- `AWSLambdaBasicExecutionRole` — permission to write CloudWatch logs

A narrowly-scoped role keeps the blast radius small: this Lambda can only touch DynamoDB and CloudWatch, nothing else in the account.

---

## Q5: Why Lambda instead of EC2 for this project?

| | EC2 | Lambda |
|---|---|---|
| Model | Always-ON server | Runs only when triggered |
| Pricing | Pay 24/7 | Pay per execution |
| Scaling | Manual setup | Auto-scales instantly |
| Management | You manage everything | AWS manages everything |
| Startup | Minutes | Milliseconds |

Order processing is a short-lived task — receive one order, write one record, respond. No need for an always-on server.

---

## Q6: What problem does API Gateway solve?

A Lambda function has no public URL. It's a worker sitting inside AWS with no door to the outside world.

API Gateway is the public door. When a request hits that URL, API Gateway decides which Lambda to invoke.

Without API Gateway, Lambda exists but is functionally invisible to the outside world.

---

## Q7: Why HTTP API instead of REST API?

| | HTTP API (chosen) | REST API |
|---|---|---|
| Primary use | Simple, thin door to Lambda | Caching, API keys, usage plans |
| Cost | Cheaper, lower latency | More expensive |
| Complexity | Minimal | More configuration |

CloudCart needs one simple thing — a `POST /order_processor` route that triggers Lambda. HTTP API is built exactly for this pattern.

---

## Q8: What caused the region mismatch bug, and how was it fixed?

**Issue:** Lambda created in `us-east-1` (console default) while DynamoDB Orders table was in `eu-west-1`. Deployed without error but every invocation failed with `ResourceNotFoundException`.

**Fix:** Deleted and recreated Lambda after switching console region to `eu-west-1`.

**Takeaway:** Region mismatch does not surface at creation time — only at runtime. The error looks identical to "table doesn't exist." Always confirm the active region before creating any resource that needs to talk to another one.

---

## Q9: Console Test Event vs Postman — what's the difference?

- **Test Event in console** — proves the CODE LOGIC is correct. Hand-feeds the function an event manually, no API Gateway involved.
- **Postman → API Gateway** — proves the ENTIRE SYSTEM is correct. All three layers wired together.

Test the Lambda directly first — isolate code correctness before testing the full path.

---

## Q10: What was verified end-to-end for Phase 2?

