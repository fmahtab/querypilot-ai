# QueryPilot TRACE Analysis

## Purpose

This document records manual review and open-coding observations from
QueryPilot AI traces. The traces are reviewed to identify recurring failure
patterns before defining a formal failure taxonomy.

## Trace Analysis

### Trace #1

Question:
What is considered low inventory?

Expected route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Answer: on-hand quantity is below the minimum threshold but above zero.
- Sources: inventory_policy.md

Result:
PASS

Open-coding note:
Correctly routed a RetailStar inventory-policy question to the knowledge base.
The response was grounded in the relevant policy document and included a source.

Failure label:
None



### Trace #2

Question:
Can I return opened acrylic paint?

Expected route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Answer: opened acrylic paint cannot be returned because it is considered a consumable item.
- Sources: returns_policy.md

Result:
PASS

Open-coding note:
Correctly routed a RetailStar returns-policy question to the knowledge base.
The response was grounded in the relevant policy document and included a source.

Failure label:
None



### Trace #3

Question:
Can I return cut-to-order fabric?

Expected route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Answer: No, cut-to-order fabric is not returnable.
- Sources: returns_policy.md

Result:
PASS

Open-coding note:
Correctly routed a RetailStar returns-policy question to the knowledge base.
The response was grounded in the relevant policy document and included a source.

Failure label:
None



### Trace #4

Question:
What is BOPIS?

Expected route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Answer: BOPIS (Buy Online, Pick Up In Store).
- Sources: business_glossary.md

Result:
PASS

Open-coding note:
Correctly routed a RetailStar business-glossary question to the knowledge base.
The response was grounded in the relevant business terms document and included a source.

Failure label:
None



### Trace #5

Question:
How many days has RetailStar been in business?

Expected route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Answer: The information is not available in the RetailStar knowledge base.
- Sources: company_overview.md

Result:
PASS

Open-coding note:
Correctly routed a RetailStar company-overview question to the knowledge base.
The requested information was not available in the relevant document, and
QueryPilot correctly refused to provide an unsupported answer.

Failure label:
None



### Trace #6

Question:
Which store had the highest sales last month?

Expected route:
DATABASE

Actual behavior:
- requires_database: true
- Answer: This question requires RetailStar business data.
- Sources: []

Result:
PASS

Open-coding note:
Correctly routed a question requiring RetailStar's dynamic sales data to the database.
Since database querying has not been implemented yet, QueryPilot correctly refused to provide an unsupported answer.

Failure label:
None



### Trace #7

Question:
Which products are currently out of stock?

Expected route:
DATABASE

Actual behavior:
- requires_database: true
- Answer: This question requires RetailStar business data.
- Sources: []

Result:
PASS

Open-coding note:
Correctly routed a question requiring RetailStar's current inventory data to the database.
Since database querying has not been implemented yet, QueryPilot correctly
refused to provide an unsupported answer and did not invent inventory data.

Failure label:
None



### Trace #8

Question:
What is FastAPI?

Expected route:
GENERAL

Actual behavior:
- requires_database: false
- Answer: FastAPI is a modern, high-performance web framework.
- Sources: []

Result:
PASS

Open-coding note:
Correctly classified a non-RetailStar technical question as GENERAL.
The response was answered using general knowledge without accessing
RetailStar's knowledge base or database.

Failure label:
None


### Trace #9

Question:
What is RetailStar's return window for unopened products?

Expected route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Answer: 30 days from delivery date for e-commerce purchases
- Sources: returns_policy.md

Result:
PASS

Open-coding note:
Correctly routed a RetailStar return-policy question to the knowledge base.
The response was grounded in the relevant policy document and included a source.

Failure label:
None


### Trace #10

Question:
When is inventory considered critically low?

Expected route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Sources: inventory_policy.md
- Answer states the information is not available

Result:
PASS

Open-coding note:
Correctly used the knowledge-base path but did not invent a definition
that is absent from RetailStar documentation. Demonstrates grounded
refusal behavior.

Failure label:
None



### Trace #11

Question:
Which products are below their minimum inventory threshold right now?

Expected route:
DATABASE

Actual behavior:
- requires_database: true
- Correctly identifies that RetailStar business data is required
- Sources: []

Result:
PASS

Open-coding note:
Correctly distinguished current inventory data from a documented
inventory policy. The question requires dynamic product-level data,
so the DATABASE behavior is appropriate.

Failure label:
None



### Trace #12

Question:
Who founded RetailStar?

Expected route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Sources: company_overview.md
- Founder information was not available
- QueryPilot refused rather than inventing an answer

Result:
PASS

Open-coding note:
Correctly treated a company-history question as static knowledge-base
information. Retrieved the relevant company document and gave a
grounded refusal because the requested fact was not documented.

Failure label:
None



### Trace #13

Question:
How long do customers have to pick up a BOPIS order?

Expected route:
KNOWLEDGE_BASE

Expected answer:
5 business days

Actual behavior:
- requires_database: false
- Retrieved:
  - returns_policy.md
  - inventory_policy.md
- Answer:
  "The information is not available in the RetailStar knowledge base."

Result:
FAIL

Open-coding note:
QueryPilot reached the correct knowledge-base path and retrieved
inventory_policy.md, which contains the 5-business-day BOPIS rule,
but failed to use that information when generating the answer.

Failure label:
ANSWER_GROUNDING_FAILURE


### Trace #14

Question:
What happens to an unpicked BOPIS order after 5 business days?

Expected route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Correct answer: reserved inventory is released back to available stock
- Sources include inventory_policy.md

Result:
PASS

Open-coding note:
QueryPilot correctly retrieved and used the documented BOPIS policy
when the question closely matched the wording in the source.

Failure label:
None



### Trace #15

Question:
What does SKU mean?

Expected route:
GENERAL

Actual route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Answered correctly
- Used RetailStar-specific information
- Sources: business_glossary.md, inventory_policy.md

Result:
FAIL

Open-coding note:
QueryPilot classified a general retail terminology question as
RetailStar-specific knowledge. Although the answer was correct,
the knowledge base was used unnecessarily for a question that
could be answered with general knowledge.

Failure label:
ROUTING_OVERCLASSIFICATION



### Trace #16

Question:
What does SKU mean at RetailStar?

Expected route:
KNOWLEDGE_BASE

Actual behavior:
- requires_database: false
- Correct RetailStar-specific definition
- Sources:
  - business_glossary.md
  - inventory_policy.md

Result:
PASS

Open-coding note:
Correctly treated an explicitly RetailStar-specific terminology question
as knowledge-base content and grounded the answer in internal documents.

Failure label:
None



### Trace #17

Question:
What is RetailStar's best-selling product?

Expected route:
DATABASE

Actual behavior:
- requires_database: true
- Correctly states RetailStar business data is required
- Sources: []

Result:
PASS

Open-coding note:
Correctly recognized that identifying the best-selling product requires
dynamic sales data rather than static RetailStar documentation.

Failure label:
None



### Trace #18

Question:
How do you calculate inventory turnover?

Expected route:
GENERAL

Actual behavior:
- requires_database: false
- Correctly answered using general knowledge
- Sources: []

Result:
PASS

Open-coding note:
Correctly classified the question as general knowledge and explained
how inventory turnover is calculated without using RetailStar-specific
documents or database data.

Failure label:
None
