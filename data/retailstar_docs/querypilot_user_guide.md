---
title: QueryPilot User Guide
tags: [querypilot, analytics, user-guide, retail, arts-and-crafts]
department: Analytics & Operations
document_type: User Guide
version: 1.0
last_updated: 2026-08-03
---

# QueryPilot — User Guide

## Welcome

QueryPilot is RetailStar's internal AI assistant for business questions. Instead of waiting on a report or digging through spreadsheets, you can ask a question in plain English — the same way you'd ask a colleague — and get a concise answer back.

This guide is for RetailStar team members: store managers, category managers, regional ops, and leadership. It covers what QueryPilot can help with today, how to ask good questions, and what to do when it can't answer yet.

---

## What QueryPilot Is For

Use QueryPilot when you need a quick answer about RetailStar performance, policies, or terminology — especially before a meeting, during a weekly review, or when something flags on your store dashboard.

**Good reasons to use QueryPilot:**

- "Which Core Staples are low inventory at my store?"
- "What is our return rate threshold for project kits?"
- "What does net revenue mean in our reporting?"
- "Which category had the highest sales last quarter?"

**QueryPilot is not for:**

- Customer-facing support or sharing answers outside RetailStar
- Questions about individual customer names, emails, or payment details
- Replacing official financial sign-off or compliance decisions

QueryPilot is an internal tool. Treat its outputs like any other internal report — for RetailStar eyes only.

---

## Who Uses QueryPilot

| If you are a… | QueryPilot can help you with… |
|---------------|------------------------------|
| **Store Manager** | Low inventory, top sellers at your store, return trends, Core Staple stockouts |
| **Category Manager** | Category performance, return rates by product line, seasonal sell-through |
| **Regional Operations** | Comparing stores in your region, stockout patterns, channel mix |
| **Leadership** | Quarter-over-quarter growth, net revenue by category, margin overview |

You don't need a technical background to use QueryPilot. Ask your question the way you would in a team chat.

---

## How to Ask a Question

1. Open QueryPilot through your internal access point (ask your manager or the Analytics & Operations team if you don't have the link yet).
2. Type your question in plain English.
3. Read the answer. QueryPilot keeps responses short and direct.

### Keep in mind

- Ask **one question at a time** for the clearest answer.
- Keep your question under **255 characters** — short and specific works best.
- Include a **time period** when it matters: "last quarter," "this month," "year-over-year."
- Name the **store, region, category, or channel** when you can — it helps QueryPilot understand what you need.

**Instead of:** "How are we doing?"

**Try:** "What were the top 5 selling SKUs at Store 104 last week?"

---

## What Happens When You Ask

QueryPilot reads your question and decides how to answer:

1. **Policy or definition questions** — If you're asking about a RetailStar rule, term, or process (e.g., "What counts as low inventory?" or "What is the e-commerce return window?"), QueryPilot answers from our internal documentation.
2. **Data questions** — If you're asking about live sales, inventory counts, or return figures, QueryPilot recognizes that you need real business data.

When a question needs live data, QueryPilot will tell you honestly if that capability isn't available yet — it won't make up numbers. You'll see a message like:

> *This question requires RetailStar business data. Database querying has not been implemented yet.*

If you see that, rephrase your question if it's partly a definition question, or reach out to Analytics & Operations for the report you need.

QueryPilot **never invents sales figures, inventory counts, or return rates**. If it doesn't know, it says so.

---

## Questions You Can Ask

### Sales and revenue

Ask about how we're performing — by store, region, category, or channel.

- Which product categories generated the highest net revenue last quarter?
- What was our average order value this month?
- Which region had the highest sales last month?
- How do online sales compare to in-store sales this quarter?

### Inventory

Ask about stock levels, low inventory, and stockouts. QueryPilot uses the same rules as our Inventory Policy.

- Which stores have low inventory?
- Which Core Staples are at stockout this week?
- What yarn SKUs are below minimum threshold in the Northeast region?

At RetailStar, a SKU is **low inventory** when:

```
on_hand_quantity < minimum_threshold
```

### Returns

Ask about return rates and category performance. QueryPilot follows our Returns Policy definitions.

- Which product category has the highest return rate?
- What is the return rate for project kits this season?
- Which SKUs exceed the elevated return rate threshold?

Return rate is calculated as:

```
return_rate = (returned_units / sold_units) × 100
```

### Products and categories

Ask about assortment and trends across our art and craft catalog.

- Which fine art supplies had the highest units sold last month?
- How are yarn sales trending going into fall?
- Which seasonal kits underperformed after holiday peak?

### Definitions and policy

Not sure what a term means or what our policy says? Ask directly.

- What is a Core Staple?
- What is the return window for e-commerce orders?
- What categories are included in Home Décor & DIY?

These questions don't require live data — QueryPilot can answer them from our internal docs.

---

## Examples by Role

### Store Manager

- Which Core Staples are low inventory at my store?
- What were the top 5 selling SKUs at my store last week?
- How many returns did we process this month?

### Category Manager

- What is the return rate for Paper & Scrapbooking this quarter?
- Which project kits exceeded the 12% elevated return threshold?
- How did Yarn & Needlecraft perform during the fall seasonal peak?

### Leadership

- What was net revenue by category last quarter?
- Which region had the highest gross margin?
- How are BOPIS sales trending compared to ship-to-home?

---

## Tips for Getting Better Answers

1. **Use our language** — Terms like *Core Staple*, *net revenue*, *return rate*, and *BOPIS* are defined in the Business Glossary. QueryPilot understands them better when you use them.
2. **Be specific about time** — "Last quarter" beats "recently."
3. **Name the place or category** — "Store 104" or "Yarn & Needlecraft" beats "my store" or "that category" when you can.
4. **One question per ask** — Split compound questions into separate asks.
5. **Start with definitions if you're unsure** — If you're not sure how we measure something, ask what it means first, then ask for the number.

---

## What QueryPilot Can Do Today

| You can… | Status |
|----------|--------|
| Ask questions in plain English | Available now |
| Get answers about RetailStar terms and policies | Available after RAG integration |
| Ask data questions (sales, inventory, returns) | Recognized — live data answers coming soon |
| Ask follow-up questions that remember prior context | Coming soon |
| Get answers grounded in our RetailStar documentation | Coming soon |

We're actively building out live database answers and conversation memory. This guide will be updated as new capabilities roll out.

---

## What QueryPilot Won't Do

- **Make up numbers** — If QueryPilot doesn't have the data, it won't guess.
- **Handle customer personal information** — Don't include customer names, emails, or payment details in your questions.
- **Replace official reporting for finance or compliance** — Use QueryPilot for quick insight; use official channels for signed-off reports.
- **Work outside RetailStar** — This tool is for internal use only.

---

## Helpful Documents to Know

QueryPilot draws on RetailStar's internal documentation. You'll get better answers if you're familiar with these:

| Document | When to reference it |
|----------|------------------------|
| **Company Overview** | Understanding our business, categories, channels, and goals |
| **Business Glossary** | Standard definitions for metrics and product terminology |
| **Inventory Policy** | Stock rules, Core Staples, and low inventory thresholds |
| **Returns Policy** | Return eligibility, return rate benchmarks, and reason codes |

If QueryPilot's answer references a policy term you don't recognize, check the relevant document above.

---

## When to Escalate

Contact the **Analytics & Operations** team directly when:

- QueryPilot tells you it can't access the data you need yet
- You need a formal report for leadership or finance review
- Your question involves data QueryPilot answered but you need verified for a decision
- You need access to QueryPilot and don't have it yet

QueryPilot is here to speed things up — not to replace the team behind our reporting.

---

## Quick Reference

**Ask like a colleague:**
> "Which stores have low inventory for white acrylic paint?"

**Include time and place when it matters:**
> "What was net revenue for Yarn & Needlecraft in the Northeast last quarter?"

**Ask about policy without needing live data:**
> "What is the return window for a BOPIS order?"

**If you get a 'requires business data' response:**
> Rephrase if it's a definition question, or contact Analytics & Operations for the live report.
