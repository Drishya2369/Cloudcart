Interview questions:
# DynamoDB Q&A Notes

## Q1: What is the difference between SQL and NoSQL?

SQL:
- Stands for Structured Query Language
- Fixed schema — structure defined upfront, cannot be changed easily
- Structured data — every record has same fields
- Slower processing due to strict structure
- Best for Banking, Finance, Accounting where accuracy matters

NoSQL:
- Stands for "Not Only SQL" (not "No Structure"!)
- Flexible schema — each item can have different fields
- No predefined structure needed
- Faster processing — speed over strict accuracy
- Best for real-time apps, IoT, gaming, activity logs
- Example: UPI activity logs stored in DynamoDB

---

## Q2: What are ACID Properties and why do banks use them?

A — Atomicity:
All or nothing. Either the transaction completes fully or nothing happens.
Example: ₹20,000 debited from Rajesh AND credited to Anita — or neither happens.

C — Consistency:
Data always remains valid. Rules are always enforced.
Example: Cannot debit ₹20,000 from an account with only ₹15,000 balance.

I — Isolation:
No two transactions from the same account happen simultaneously.
Example: While Rajesh's transaction is processing, no other transaction can touch his account.

D — Durability:
Once committed it's permanent. Even a server crash cannot undo it.
Example: Once ₹20,000 transfer is confirmed — it stays confirmed forever.

Why banks use ACID:
Money requires 100% accuracy. ACID properties ensure no transaction is lost,
duplicated or partially completed. That's why RDS (SQL) is used for banking.

---

## Q3: What is Horizontal vs Vertical Scaling?

Vertical Scaling:
- Make the existing server BIGGER
- Add more CPU, RAM, storage to same server
- Like upgrading laptop from 8GB to 16GB RAM
- Has a limit — can only scale so much
- Used by SQL databases

Horizontal Scaling:
- Add MORE servers to share the load
- Like adding more cashiers at a busy supermarket
- No limit — keep adding servers as you grow
- Used by DynamoDB
- This is how DynamoDB handles billions of records!

One line to remember:
Vertical = Grow UP (bigger server) ⬆️
Horizontal = Grow WIDE (more servers) ➡️➡️➡️
