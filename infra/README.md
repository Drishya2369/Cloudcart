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
