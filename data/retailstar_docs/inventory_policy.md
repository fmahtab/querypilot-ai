---
title: RetailStar Inventory Policy
tags: [inventory, retail, arts-and-crafts, operations, policy]
department: Merchandising & Operations
document_type: Inventory Policy
version: 1.0
last_updated: 2026-08-03
---

# RetailStar — Inventory Policy

## Purpose

This document defines RetailStar's inventory management standards across physical stores, e-commerce fulfillment, and BOPIS operations. It establishes how stock levels are planned, monitored, replenished, and reported — with specific guidance for art and craft product categories where demand, seasonality, and product form (consumables, tools, cut-to-order fabric, project kits) vary significantly.

All store managers, category managers, and operations teams should follow these guidelines when making buying, transfer, and markdown decisions.

---

## Scope

This policy applies to:

- All RetailStar physical store locations
- E-commerce ship-to-home fulfillment
- BOPIS (Buy Online, Pick Up In Store) orders fulfilled from store inventory
- Central replenishment from RetailStar's distribution center to stores

Inventory is tracked at the **SKU × store** level. E-commerce fulfillment may draw from a designated warehouse or eligible store locations depending on SKU and region.

---

## Inventory Classification

RetailStar classifies products into four inventory tiers to determine stocking rules and replenishment priority.

| Tier | Description | Examples | Replenishment Priority |
|------|-------------|----------|------------------------|
| **Core Staples** | High-velocity consumables expected at every store | White acrylic paint, school glue, 12×12 cardstock, #8 crochet hooks, black thread | Highest — daily monitoring |
| **Category Essentials** | Regularly stocked items within a category but not required at every location | Specialty brush sets, DK-weight yarn colors, die-cutting dies | High — weekly monitoring |
| **Seasonal / Trend** | Time-bound or trend-driven assortment | Holiday wreath kits, viral craft kits, back-to-school classroom packs | Planned — pre-season build, post-season markdown |
| **Long-Tail / Specialty** | Lower-velocity tools, premium, or niche items | Professional easels, precious-metal jewelry findings, large-format canvas | Moderate — reorder on demand or regional allocation |

---

## Core Staples Policy

Every RetailStar store must maintain minimum on-hand quantities for **Core Staples** across all major categories. A stockout on a Core Staple is treated as a operational failure and should be escalated to the regional manager.

### Minimum on-hand quantities (store level)

| Category | Core Staple Examples | Minimum Units |
|----------|---------------------|---------------|
| Fine Art Supplies | White acrylic paint (8 oz), stretched canvas (8×10, 11×14) | 12 units per size |
| Adhesives & Finishes | School glue, glue sticks, hot glue sticks | 24 units |
| Paper & Scrapbooking | 12×12 white cardstock, 8.5×11 cardstock | 50 sheets (equivalent units) |
| Yarn & Needlecraft | Worsted-weight yarn (basic colors), #8 crochet hook | 10 skeins / 6 hooks |
| Fabric & Sewing | All-purpose thread (black, white), straight pins | 12 spools / 10 boxes |
| Kids & Classroom Crafts | Construction paper packs, washable markers (basic sets) | 15 units |

Category managers may adjust minimums by region (e.g., higher yarn minimums in colder-climate stores) but may not reduce Core Staple minimums without regional approval.

---

## Stock Level Definitions

RetailStar uses the following inventory status labels in reporting and store dashboards.

| Status | Definition | Action Required |
|--------|------------|-----------------|
| **In Stock** | On-hand quantity at or above minimum threshold | None |
| **Low Inventory** | On-hand quantity below minimum threshold but above zero | Reorder triggered automatically; store manager notified |
| **Stockout** | On-hand quantity equals zero | Escalate if Core Staple; expedite replenishment or inter-store transfer |
| **Overstock** | On-hand quantity exceeds maximum threshold by more than 20% | Hold reorders; consider transfer to another store or markdown if seasonal |

### Low inventory

A SKU is flagged as **low inventory** when:

```
on_hand_quantity < minimum_threshold
```

For Core Staples, low inventory alerts are sent to the store manager and regional operations team. For all other tiers, alerts are sent to the category manager on a weekly review cycle.

### Maximum thresholds

Maximum on-hand quantities are set at **3× the minimum threshold** for Core Staples and Category Essentials, unless overridden by category manager for bulky items (e.g., easels, wreath forms).

---

## Replenishment Rules

### Automatic reorder

- Core Staples and Category Essentials trigger an automatic replenishment order when quantity falls below the minimum threshold.
- Reorder quantity is calculated as:

```
maximum_threshold − on_hand_quantity
```

- Replenishment lead time is **3–5 business days** from the distribution center to store.

### Manual reorder

- Seasonal / Trend and Long-Tail / Specialty items are reordered manually by the category manager based on sales velocity, upcoming promotions, and workshop schedules.
- Store managers may request manual reorders for localized demand spikes (e.g., a school district placing a large classroom order).

### Inter-store transfers

When a store is at stockout and replenishment from the distribution center cannot arrive within 48 hours:

1. The regional manager may authorize a transfer from a nearby store with surplus stock.
2. Transfers are logged centrally and reflected in both stores' inventory records within 24 hours.
3. Core Staple transfers take priority over all other transfer requests.

---

## Category-Specific Inventory Rules

### Fabric & Sewing (cut-to-order)

- Fabric sold by the yard is tracked in **linear yards** on the bolt, not as pre-cut units.
- Minimum threshold applies to full bolts for Core Staple fabrics (quilting cotton basics, muslin).
- Fat quarters and precut bundles are tracked as individual SKU units.
- Cut-to-order sales reduce bolt inventory at time of purchase; returns on cut fabric do not restock unless the full uncut bolt is returned intact.

### Yarn & Needlecraft

- Yarn is tracked by skein. Color-level SKUs within the same yarn line are managed independently.
- Stores in colder-climate regions carry expanded yarn and needlecraft inventory per localized assortment guidelines.
- Yarn sales spike during fall and winter; pre-season build begins **6 weeks** before peak.

### Project Kits & Seasonal Items

- Project kits (candle-making, beginner crochet, wreath kits) are ordered as seasonal lots, not continuous replenishment.
- Initial buy is based on prior-year sell-through for the same season.
- Unsold seasonal kits are marked down **2 weeks** after the seasonal peak ends.
- Kits are not classified as Core Staples regardless of sales volume during peak.

### Adhesives & Finishes

- Adhesives with temperature sensitivity (certain glues, spray finishes) require climate-controlled storage at the distribution center.
- Hot glue sticks and Mod Podge are Core Staples with the highest reorder priority in this category.

### Craft Tools & Storage

- Reusable tools (cutting mats, rulers, pliers) are Long-Tail / Specialty unless tied to an active workshop promotion.
- Tools are not replenished automatically; reorder is triggered when store-level stock reaches zero and sales velocity warrants restocking.

---

## Seasonal Inventory Planning

RetailStar plans inventory around four major seasonal peaks:

| Season | Peak Period | Primary Categories | Planning Lead Time |
|--------|-------------|-------------------|-------------------|
| **Back-to-School** | July – August | Kids & Classroom Crafts, Adhesives, Paper | 8 weeks |
| **Fall / Holiday Crafting** | October – December | Home Décor & DIY, Yarn, Clay, Seasonal Kits | 10 weeks |
| **Spring DIY / Wedding** | March – May | Fabric & Sewing, Paper & Scrapbooking, Jewelry | 8 weeks |
| **Summer Camp** | May – June | Kids & Classroom Crafts, Clay, Beading | 6 weeks |

Category managers submit seasonal buy plans to operations **before** the planning lead time window closes. Stores receive seasonal inventory in two waves: early build and peak replenishment.

---

## Omnichannel Inventory Rules

### E-commerce (ship-to-home)

- E-commerce fulfillment draws from the central distribution center by default.
- If the distribution center is at stockout, eligible stores may fulfill e-commerce orders (ship-from-store) at regional manager discretion.
- E-commerce orders reduce inventory at the fulfilling location at time of shipment.

### BOPIS (Buy Online, Pick Up In Store)

- BOPIS orders reserve inventory at the selected store at time of order placement.
- Reserved quantity is deducted from available on-hand inventory immediately.
- If the reserved SKU falls below minimum threshold after reservation, a low inventory alert is triggered.
- Unpicked BOPIS orders release reserved inventory back to available stock after **5 business days**.

---

## Overstock Management

When a SKU exceeds maximum threshold by more than 20%:

1. **Hold reorders** until stock falls below maximum.
2. **Transfer** surplus to stores with low inventory or stockout on the same SKU.
3. **Markdown** if the item is Seasonal / Trend and the peak period has ended.
4. **Return to vendor** only if permitted by supplier agreement and the item is unopened/non-seasonal.

Overstock on Core Staples is rare and should be reviewed by the category manager before any markdown action.

---

## Inventory Accuracy

- Stores conduct a **full cycle count** of Core Staples monthly.
- All other tiers are cycle-counted quarterly.
- Discrepancies greater than 5% of on-hand quantity for Core Staples must be investigated and logged within 48 hours.
- Shrinkage on high-value items (professional-grade paints, precious-metal findings, die-cutting machines) is flagged separately in reporting.

---

## Reporting & Review Cadence

| Report | Audience | Frequency |
|--------|----------|-----------|
| Core Staple stockout report | Store managers, regional ops | Daily |
| Low inventory by store | Store managers, category managers | Daily (Core Staples); Weekly (all tiers) |
| Overstock report | Category managers | Weekly |
| Seasonal sell-through | Category managers, leadership | Weekly during peak; Monthly off-peak |
| Inventory accuracy / shrinkage | Regional ops, leadership | Monthly |

Leadership reviews inventory performance alongside sales and return metrics on a weekly and quarterly basis, as defined in the Company Overview.
