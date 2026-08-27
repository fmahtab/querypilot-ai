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

Initial behavior:
- requires_database: false
- Sources:
  - returns_policy.md
  - inventory_policy.md
- Answer:
  "The information is not available in the RetailStar knowledge base."

Initial Result:
FAIL

Open-coding note:
QueryPilot reached the correct knowledge-base path and retrieved
inventory_policy.md. Further inspection showed that the document stated
that unpicked BOPIS inventory is released after 5 business days, but did
not explicitly state that customers have 5 business days to pick up an order.

Root cause:
The expected business rule was not explicitly documented in the
knowledge base.

Improvement:
The BOPIS policy was clarified in inventory_policy.md to explicitly state
that customers have 5 business days to pick up an order. The document
was re-indexed and the same evaluation case then passed.

Final result:
PASS

Failure label:
KNOWLEDGE_BASE_GAP


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

Initial behavior:
- requires_database: false
- Answered correctly
- Used RetailStar-specific information
- Sources: 
  - business_glossary.md
  - inventory_policy.md

Initial Result:
FAIL

Open-coding note:
QueryPilot classified a general retail terminology question as
RetailStar-specific knowledge. Although the answer was correct,
the knowledge base was used unnecessarily for a question that
could be answered with general knowledge.

Root cause:
The classifier prompt treated definitions and terminology as
KNOWLEDGE_BASE even when the question did not require RetailStar-specific
information.

Improvement:
The classifier instructions were clarified so common business or technical
terminology is classified as GENERAL unless the question requires a
RetailStar-specific definition or policy.

Final result:
PASS

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



## Failure Taxonomy

The manual review of 18 QueryPilot traces identified observed failures
and defined the following failure taxonomy for evaluating QueryPilot.

### 1. Routing Failure

The question is classified into the wrong processing path:
DATABASE, KNOWLEDGE_BASE, or GENERAL.

Observed:
- Trace #15: "What does SKU mean?"
- Expected GENERAL but QueryPilot classified it as KNOWLEDGE_BASE.

### 2. Retrieval Failure

The question is correctly routed to the knowledge base, but the
relevant document or context is not retrieved.

Observed:
- No retrieval failures were observed in the reviewed traces.

### 3. Knowledge Base Gap

The expected information is missing or not explicitly documented in the
knowledge base, preventing QueryPilot from providing the expected grounded answer.

Observed:
- Trace #13: "How long do customers have to pick up a BOPIS order?"
- The knowledge base documented that unpicked BOPIS inventory is released
  after 5 business days, but did not explicitly state the customer's pickup
  deadline.
- After the business rule was explicitly documented and the knowledge base
  was re-indexed, the evaluation case passed.

### 4. Unsupported Answer Failure

The requested information is not supported by the available knowledge,
but QueryPilot generates or invents an answer instead of refusing to answer.

Observed:
- No unsupported answer failures were observed.
- Traces #5, #10, and #12 correctly refused to provide an answer when the
  requested information was not available in the RetailStar knowledge base.

## Failure Prioritization

Failures were prioritized using frequency and impact.

Impact scale:
- Low = 1
- Medium = 2
- High = 3

Priority score = Frequency × Impact

| Failure Type | Frequency | Impact | Priority Score |
|---|---:|---:|---:|
| KNOWLEDGE_BASE_GAP | 1 | High (3) | 3 |
| ROUTING_FAILURE | 1 | Medium (2) | 2 |
| RETRIEVAL_FAILURE | 0 | High (3) | 0 |
| UNSUPPORTED_ANSWER_FAILURE | 0 | High (3) | 0 |

### Priority

KNOWLEDGE_BASE_GAP is the highest-priority observed failure.

Although KNOWLEDGE_BASE_GAP and ROUTING_FAILURE were each observed once,
the knowledge-base gap had greater user impact. In Trace #13, the expected
customer pickup deadline was not explicitly documented in the knowledge
base, preventing QueryPilot from providing the expected grounded answer.

The routing failure in Trace #15 had lower impact because QueryPilot used
the wrong route but still returned a correct answer.

## Evaluation Results

The expanded golden evaluation set initially passed 9 of 11 cases (81.8%).

After addressing the knowledge-base gap identified in Trace #13, the
evaluation improved to 10/11 (90.9%).

After clarifying the classifier behavior identified in Trace #15, the
evaluation improved to 11/11 (100%). Repeated evaluation runs continued
to pass all 11 cases.