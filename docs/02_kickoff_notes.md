# Step 2: Kickoff notes

> **Scenario note.** The data in this project is real (Hillstrom, 2008). The people, conversations and business figures here are invented to show how an experiment is scoped in practice.

**Attendees:** Head of E-mail Marketing, E-mail Operations Manager, Finance Business Partner (for the CFO), Data Scientist (Nathan Chen, author)

**Purpose:** turn the request into a decision, a metric and a design everyone agrees on *before* anything is sent.

## Questions and answers

The data scientist's job in a kickoff is mostly to ask questions. The answers become the inputs of the design doc.

### About the decision

**Q: What will you do differently depending on the result?**
*Marketing:* If the emails work, roll out to the full file and adopt the two-campaigns-a-month programme. Scale whichever campaign wins.
*Finance:* If they don't produce incremental purchases, the creative budget gets cut or moved to catalogue.

**Q: What result would change your mind?**
*Finance:* Evidence that the campaigns cause enough extra purchases to cover their cost. Revenue that would have happened anyway doesn't count.

**Q: Is "it brings people to the website" enough?**
*Finance:* No. Visits are nice, but the budget decision depends on purchases and revenue.

### About the economics

**Q: What does a sale and an email cost and earn?**

| Item | Value | Source |
|---|---|---|
| Average order value | $100 (SD about $90) | Order system |
| Gross margin | 40% | Finance |
| Sending cost | $0.01 per email | E-mail platform contract |
| Creative production | $8,000 per campaign | Finance |
| Active file | 640,000 customers | CRM |

**Q: How often do customers visit and buy when we send nothing?**
*Operations:* In a normal fortnight without email, roughly 1 in 10 active customers visits the website and about 1 in 200 places an order.

### About the design

**Q: Who is eligible?**
The active file: customers who bought in the last 12 months. Lapsed customers have different response and deliverability, so they're out of scope.

**Q: How many customers can we test on?**
*Data Science asked for about 145,000, which is what it takes to reliably detect the 30% lift Marketing expects (Appendix, notebook 01).*
*Operations:* Not possible this spring. The other 90% of the file is already allocated to the spring catalogue test, which runs at the same time. Putting customers in both tests would contaminate both. **We can give you a random 64,000 (10% of the file).**

**Q: How long should we measure?**
*Operations:* The next scheduled campaign goes out 15 days after this one. Most email responses happen within a few days.
*Decision:* **two weeks**, so the window closes before the next campaign.

**Q: How are visits and purchases recorded?**
*Operations:* Visits are matched to customers by login and cookie, purchases by customer ID. Both are recorded the same way whether or not a customer got an email.
*Data Science:* Good. If visits were only tracked through email clicks, the no-email group would look worse purely because of measurement.

**Q: What else could go wrong for customers?**
*Operations:* Unsubscribes and spam complaints. Both are tracked in the e-mail platform, not in the analysis dataset.

**Q: Anything else hitting these customers during the window?**
*Operations:* No other campaigns go to the 64,000 during the two weeks. Catalogue mailings to them are paused equally across groups.

## Decisions

1. Three groups: no email (holdout), men's email, women's email, assigned at random.
2. Test sample: a random 64,000 customers from the active file.
3. Measurement window: two weeks after the send.
4. Data Science writes the experiment design doc, including how to split the 64,000 and what result counts as success, for sign-off by Marketing and Finance.

## Action items

| Owner | Action |
|---|---|
| Data Science | Write the [experiment design doc](03_experiment_design_doc.md) |
| E-mail Operations | Confirm random assignment by customer ID in the platform; send seed tests |
| E-mail Operations | Report unsubscribes and complaints per group after the window |
| Finance | Confirm margin and cost figures in writing |
