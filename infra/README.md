# CloudCart — Infrastructure

## Project Overview
Serverless order processing backend built on AWS.
Cloud Engineer: Drishya
Region: eu-west-1

---

## AWS Resources — Phase 1

### S3 Bucket
- **Name:** cloudcart-orders-bucket
- **Region:** eu-west-1
- **Purpose:** Stores order receipt files generated after each order
- **ARN:** arn:aws:s3:::cloudcart-orders-bucket

### DynamoDB Table
- **Name:** Orders
- **Region:** eu-west-1
- **Partition Key:** orderId (String)
- **Capacity Mode:** Provisioned (Read: 1, Write: 1)
- **Purpose:** Stores all order records written by Lambda
- **ARN:** arn:aws:dynamodb:eu-west-1:442729101590:table/Orders

### IAM User — Bhavini QA
- **Username:** bhavini-qa
- **Access type:** Programmatic only
- **Policies attached:**
  - ReadOnlyAccess
  - AmazonSQSReadOnlyAccess
  - AmazonDynamoDBReadOnlyAccess
  - CloudWatchReadOnlyAccess
- **Purpose:** QA engineer access for testing and validation only

---

## AWS Resources — Phase 2 (Coming)
- Lambda: order_processor
- API Gateway: POST /orders endpoint
- CloudWatch: Log group /aws/lambda/order_processor

---

## AWS Resources — Phase 3 (Coming)
- SQS Queue: cloudcart-order-queue
- SQS Dead Letter Queue: cloudcart-order-dlq
- Lambda: notification_handler
- SNS Topic: cloudcart-notifications

---

## Important Notes
- Never commit .env files or AWS credentials to GitHub
- All resources in eu-west-1
- Bhavini's IAM credentials shared via secure channel
- Root account MFA enabled — root credentials never shared

---

## Branch Strategy
| Branch | Owner | Purpose |
|---|---|---|
| main | Both | Final clean code only |
| feature/infra-setup | Drishya | All infrastructure setup |
| feature/week1-setup | Bhavini | Initial project structure |
| feature/week2-api-tests | Bhavini | Functional tests |
| feature/week3-integration | Bhavini | SQS + SNS tests |
| feature/week4-negative | Bhavini | Negative and edge case tests |
| feature/reporting | Bhavini | Final reports |

---

*Last updated: June 2026 — Phase 1 complete*

## AWS Resources — Phase 2 (Complete)

### Overview
Phase 2 builds the core order processing flow: an HTTP API that
receives an order and persists it to DynamoDB. The goal was to get
a real, working serverless request path end-to-end before adding
any complexity like queues or notifications.

```
Postman / Client
      |
      v
API Gateway  (public entry point)
      |
      v
Lambda: order_processor  (business logic)
      |
      v
DynamoDB: Orders  (persistence)
```

---

### IAM Role — LambdaOrderProcessorRole

**What:** Execution role attached to the Lambda function.

**Policies attached:**
- `AmazonDynamoDBFullAccess` — write/read access to DynamoDB
- `AWSLambdaBasicExecutionRole` — permission to write logs to CloudWatch

**Why a dedicated role:**
Lambda has zero permissions by default. Every AWS service it touches
needs to be explicitly granted. A dedicated role (rather than reusing
an admin role) keeps the blast radius small — this Lambda can only
touch DynamoDB and CloudWatch, nothing else in the account.

---

### Lambda Function — order_processor

- **Runtime:** Python 3.11
- **Region:** eu-west-1 (matches DynamoDB and S3 — see note below)
- **Timeout:** 30 seconds
- **Execution role:** LambdaOrderProcessorRole
- **Source:** [`src/order_processor.py`](../src/order_processor.py)

**What it does:**
1. Receives the incoming request (`event`)
2. Parses the JSON order payload from `event['body']`
3. Connects to DynamoDB via boto3
4. Writes the order to the `Orders` table using `put_item`
5. Returns a `200` response with a confirmation message

**Why Lambda instead of EC2:**
This is a short-lived task — receive one order, write one record,
respond. No need for an always-on server. Lambda only runs (and only
costs anything) when a request actually comes in, and scales
automatically if multiple orders arrive at once.

---

### API Gateway — order_processor-API

- **Type:** HTTP API (chosen over REST API for lower cost/latency —
  not needed for this project's complexity)
- **Route:** `POST /order_processor`
- **Stage:** default
- **Endpoint:**
  `https://5hlc6h2wh4.execute-api.eu-west-1.amazonaws.com/default/order_processor`

**Why API Gateway:**
Lambda has no public URL on its own. API Gateway is the public-facing
entry point that receives HTTP requests and invokes the Lambda
function. Without it, the Lambda exists but nothing outside AWS can
reach it — which is also why Bhavini needs this URL, not the Lambda
console, to run her tests.

---

### Problem solved: Region mismatch

**Issue:** The Lambda function was first created in `us-east-1` by
default, while the DynamoDB `Orders` table and S3 bucket were in
`eu-west-1`. The function deployed and ran without error, but every
invocation failed with `ResourceNotFoundException` — Lambda was
looking for the `Orders` table in the wrong region.

**Fix:** Deleted and recreated the Lambda function with the AWS
Console region switched to `eu-west-1` first, so the function,
table, and bucket are now co-located.

**Takeaway:** A region mismatch doesn't throw an error at creation
time — it only surfaces at runtime, and the error message
(`ResourceNotFoundException`) looks identical to "the table doesn't
exist" rather than "the table is in another region." Always confirm
the active region in the console before creating any resource that
needs to talk to another one.

---

### Verification

Tested end-to-end via Postman:

**Request:**
```
POST https://5hlc6h2wh4.execute-api.eu-west-1.amazonaws.com/default/order_processor
Body:
{
  "orderId": "ORD-002",
  "customerName": "Anita Sharma",
  "product": "iPhone 15",
  "amount": 80000
}
```

**Response:**
```
200 OK
{"message": "Order received successfully!", "orderId": "ORD-002"}
```

Confirmed in DynamoDB — both `ORD-001` (test event) and `ORD-002`
(Postman request) are present in the `Orders` table with all
attributes correctly saved.

---

### What Phase 2 deliberately does NOT include

- No input validation beyond what `json.loads` enforces — added in
  a later hardening pass, not needed to prove the flow works
- No SQS/SNS yet — that's Phase 3, kept separate so each phase has
  one clear responsibility
- No authentication on the API Gateway endpoint — fine for an
  internal QA testing phase, would need to be addressed before any
  public exposure
