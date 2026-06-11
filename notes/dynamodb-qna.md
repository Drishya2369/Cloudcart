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

## Q4: What is a Table, Item and Attribute in DynamoDB?

Table:
- The entire collection of data
- Like a phone book which has the entire list of contacts

Item:
- One single entry in the table
- Like one contact in the phone book

Attribute:
- The individual parameters/fields for each item
- Like name, phone number, email, address of one contact

---

## Q5: What is a Partition Key and Sort Key?

Partition Key:
- The most important and UNIQUE attribute in the table
- No two items can have the same Partition Key
- Like a contact's phone number — always unique
- DynamoDB uses it to decide where to store the item

Sort Key:
- Used when many items belong to the same partition
- Sorts items within that group
- Optional — not always needed
- Like emails received from Rajesh — sorted by date sent

Two types of Primary Keys:
- Simple Primary Key = Partition Key only
- Composite Primary Key = Partition Key + Sort Key

---

## Q6: What are the 4 DynamoDB Operations?

put_item:
- Adds a new item to the table
- If same Partition Key exists — it overwrites!
- Like a librarian adding a new book to the library

get_item:
- Retrieves one specific item using its unique Partition Key
- Fastest operation in DynamoDB
- Like a librarian finding a book using its unique ID number

update_item:
- Updates specific fields of an existing item
- Does NOT replace the entire item — only what you specify
- Like a librarian updating the price of an existing book

delete_item:
- Permanently removes an item from the table
- Cannot be undone — gone forever!
- Like a librarian permanently removing a book from the rack

Bonus:
query — searches by Partition Key — FAST ✅ always use this
scan — reads entire table — SLOW ❌ avoid in production!

## Q7: What is Schema-less Structure in DynamoDB?

Definition:
- No fixed structure defined upfront
- Each item can have different attributes
- No predefined columns needed
- New attributes can be added anytime without affecting existing items

Example:
Item 1: orderId, customerName, amount
Item 2: orderId, customerName, amount, discount, giftWrap
Both valid in DynamoDB — no errors, no schema changes needed!

SQL vs DynamoDB on Schema:
SQL — adding a new column means altering the ENTIRE table. Risky in production!
DynamoDB — just add new attributes to new items. Old items untouched! ✅

---

## Q8: What is Simple Primary Key vs Composite Primary Key?

Simple Primary Key:
- Partition Key ONLY
- Used when each item is completely independent
- Example: orderId alone identifies each order uniquely

Composite Primary Key:
- Partition Key + So
