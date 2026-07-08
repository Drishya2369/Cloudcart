# CloudCart — Serverless Order Processing on AWS

**Cloud Engineer:** Drishya Raj | **QA:** Bhavini  
**Region:** eu-west-1 | **Status:** Phase 3 Complete ✅

## Architecture

## Phases

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Core Infrastructure — DynamoDB, S3, IAM | ✅ Complete |
| Phase 2 | Serverless API — Lambda, API Gateway, CloudWatch | ✅ Complete |
| Phase 3 | Event-Driven Notifications — SQS, DLQ, SNS, Email | ✅ Complete |
| Phase 4 | GenAI Integration — Amazon Bedrock, CloudFormation | 🔄 In Progress |

## Phase 3 — What was built

- `cloudcart-order-queue` — SQS Standard queue for order processing
- `cloudcart-order-dlq` — Dead Letter Queue (maxReceiveCount: 3)
- `cloudcart-notifications` — SNS Topic with email subscription
- `notification_handler` Lambda — reads from SQS, publishes to SNS
- `LambdaNotificationRole` — least privilege IAM role for notification Lambda
- End-to-end tested via Postman — real email delivery confirmed ✅
## Tech Stack
AWS Lambda · DynamoDB · API Gateway · S3 · SQS · SNS · IAM · CloudWatch · Amazon Bedrock (Phase 3+)

## Docs
- [Infrastructure](infra/README.md)
- [Notes](notes/)
## Project Phases
