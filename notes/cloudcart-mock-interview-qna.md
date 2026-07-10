# CloudCart — Mock Interview Q&A
**Author:** Drishya Raj | AWS SAA | Cloud Engineer  
**Project:** Serverless Order Processing on AWS  
**Target:** Singapore Cloud/AWS Engineer roles

---

## Q1: Why not call SNS directly from Lambda instead of using SQS?

**Answer:**
If `order_processor` called SNS directly, order processing and email notification would be tightly coupled. If SNS is slow or fails, the customer waits longer or gets an error — even though the order was saved successfully.

By putting SQS in between, the two Lambdas are completely decoupled. `order_processor` saves to DynamoDB, drops a message in SQS, and immediately returns 200 OK to the customer. It doesn't care what happens next.

`notification_handler` picks up the message from SQS independently. If it fails, SQS retries automatically up to 3 times. If it still fails, the message goes to the DLQ — nothing is lost.

**Key term:** Loose coupling — services don't depend on each other directly.

---

## Q2: What is a Dead Letter Queue and why did you add one?

**Answer:**
A Dead Letter Queue is a secondary SQS queue that catches messages which repeatedly fail processing. In CloudCart I set maxReceiveCount to 3 — if `notification_handler` fails to process a message 3 times, SQS automatically moves it to the DLQ instead of retrying forever.

Without a DLQ, a failed message either loops forever wasting compute, or gets deleted after the retention period — permanently lost.

The DLQ acts as a safety net — I can inspect failed messages, fix the issue, and reprocess manually. No order notification is ever permanently lost.

**Key term:** DLQ = safety net that catches everything that falls through.

---

## Q3: Why does each Lambda have a separate IAM role?

**Answer:**
Each Lambda has a different job, so each needs different permissions.

- `order_processor` only needs DynamoDB and SQS access
- `notification_handler` only needs SQS and SNS access

Giving both a shared role with all permissions would violate least privilege. If one function is compromised, the attacker would also get access to services it has no business touching. With separate roles, the blast radius stays small.

**Key term:** Least Privilege Principle — grant only what is needed, nothing more.

---

## Q4: Why DynamoDB and not RDS?

**Answer:**
Two reasons — data model and architecture fit.

Orders in e-commerce are flexible. One order might have a discount code, another might have gift wrapping. DynamoDB handles this naturally without a fixed schema. RDS would require every order to have exactly the same columns.

Also, DynamoDB is fully serverless — it scales automatically and costs nothing when idle. Since the entire architecture is serverless, mixing in an RDS instance would mean running a server 24/7, adding cost and management overhead.

**Key term:** Serverless compatible, flexible schema, horizontal scaling.

---

## Q5: What does CloudWatch do in your architecture?

**Answer:**
CloudWatch is the observability layer. Every Lambda invocation automatically logs its execution to CloudWatch because of the `AWSLambdaBasicExecutionRole` policy attached to each IAM role.

To debug a production issue — for example, a customer placed an order but didn't receive an email:
1. CloudWatch → `order_processor` logs → check if DynamoDB write succeeded
2. Check if SQS message was sent
3. CloudWatch → `notification_handler` logs → check if it was triggered
4. Check if SNS publish succeeded
5. If notification_handler never triggered → check SQS for stuck messages
6. If it triggered but failed → check DLQ for the failed message

**Key term:** Observability — knowing what's happening inside your system at all times.

---

## Q6: What happens if 10,000 orders come in simultaneously?

**Answer:**
The architecture handles it automatically at every layer:

- **API Gateway** — scales to 10,000 requests per second automatically
- **Lambda** — spins up concurrent instances automatically, one per request
- **DynamoDB** — on-demand mode handles any spike without pre-configuration
- **SQS** — absorbs all 10,000 messages as a buffer, holds them safely
- **notification_handler** — processes at its own pace, not overwhelmed
- **SNS** — scales automatically

The most important protection is SQS — it acts as a shock absorber between order processing and notification. Even under massive load, no messages are lost.

**Key term:** Serverless auto-scaling, SQS as buffer.

---

## Q7: What if eu-west-1 goes down? How would you make this highly available?

**Answer:**
I'd use a multi-region active-passive setup — same concept as Disaster Recovery in traditional storage infrastructure.

- **DynamoDB Global Tables** — replicates Orders table across regions automatically
- **Lambda + API Gateway** — deploy same stack in a second region (e.g., us-east-1)
- **Route 53** — health checks monitor primary region, automatically failover to secondary if eu-west-1 goes down
- **SQS + SNS** — recreate same queues and topics in secondary region

**Key term:** Multi-region, active-passive, Route 53 failover routing.

---

## Q8: How does your EMC Storage background help you as an AWS Cloud Engineer?

**Answer:**
My storage background gives me three things that directly transfer to AWS Cloud.

First — infrastructure thinking. I understand how data flows, how systems fail, and how to design for resilience. That's exactly what I'm applying in CloudCart with DynamoDB, SQS, DLQ, and multi-region thinking.

Second — operational discipline. I've worked with incident management, change management, and problem management. I know how to respond under pressure, raise the right tickets, and find root cause — not just workarounds.

Third — DR experience. I've handled live disaster recovery activities where a single human error brings the entire system down. That experience makes me very deliberate about IAM permissions, testing, and documentation.

Storage taught me that the backend infrastructure is what everything depends on. AWS is just the next evolution of that.

---

## Q9: How did you collaborate with a QA engineer on this project?

**Answer:**
I set up a dedicated IAM user `bhavini-qa` with read-only DynamoDB access — following least privilege. She tested the end-to-end flow independently using Postman — placing orders, verifying data in DynamoDB, and confirming email notifications arrived after Phase 3.

Having a separate QA role mirrors real team structure where developers and testers have different access levels. It also meant I could give her access safely without sharing my credentials.

**Key point:** Real team collaboration with proper IAM separation — not a solo project.

---

## Q10: How would you explain this project in one minute?

**Answer:**
"I built a fully serverless, event-driven order processing backend on AWS — deployed in eu-west-1, tested end-to-end, and documented on GitHub with a QA engineer collaborating in parallel.

When a customer places an order, the request hits API Gateway which triggers my `order_processor` Lambda. The Lambda saves the order to DynamoDB and pushes a message to an SQS queue — immediately returning 200 OK to the customer. A second Lambda called `notification_handler` is triggered automatically by SQS, reads the message, and publishes to an SNS topic which delivers an email confirmation.

The architecture is loosely coupled — if notification fails, the order is still saved and SQS retries automatically. After 3 failures, the message moves to a Dead Letter Queue so nothing is lost. Each Lambda has its own least-privilege IAM role. CloudWatch logs every invocation for full observability.

Phase 4 is in progress — integrating Amazon Bedrock for intelligent order validation and AI-generated notifications."

---

## Quick Reference — Key Terms

| Term | One line definition |
|------|-------------------|
| Loose coupling | Services communicate via queues, not direct calls |
| Least privilege | Grant only permissions needed, nothing more |
| DLQ | Safety net for failed messages after max retries |
| Observability | Knowing what's happening inside your system |
| Serverless | No server management — AWS handles infrastructure |
| Event-driven | Services react to events, not direct invocations |
| Horizontal scaling | Add more instances, not bigger servers |

---

*Last updated — July 2026*
