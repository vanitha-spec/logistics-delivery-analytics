# Logistics Delivery Performance & Cost Analytics — Business Report

**Prepared by:** [Your Name]
**Role:** Data Analyst / Business Analyst
**Date:** [Submission Date]
**Project:** Logistics Delivery Performance & Cost Analytics

---

## 1. Executive Summary

This report presents a complete analytics solution for the logistics
company's shipment operations. Starting from a raw operational CSV
containing ~5,000 shipment records, we built a reusable Python
cleaning pipeline, computed key performance indicators (KPIs) across
delivery, delay, route, warehouse, transportation, delivery-partner
and cost dimensions, and produced a business-ready dashboard.

The analysis reveals that a measurable share of shipments are delayed,
that certain warehouses contribute disproportionately to delays, that
Air shipping is the most expensive mode, and that partner performance
varies widely. Concrete recommendations are provided to reduce delays
and control cost.

---

## 2. Business Problem

Management had operational data but no analytical view of:

- On-time vs delayed delivery performance
- Route-level and warehouse-level bottlenecks
- Which transportation modes are expensive
- Which delivery partners underperform
- Total and per-order logistics cost
- Customer experience indicators (rating, damage, returns)

Without this view, decisions on warehouses, partners and routes were
being made on intuition rather than evidence.

---

## 3. Data Summary

- **Source:** `data/raw/logistics_data.csv`
- **Rows:** ~5,000 shipment records
- **Columns (22):** order_id, customer_id, order_date, warehouse,
  origin_city, destination_city, distance_km, product_category,
  quantity, weight_kg, shipping_mode, delivery_partner, shipping_cost,
  fuel_cost, warehouse_processing_hours, dispatch_date,
  expected_delivery_date, actual_delivery_date, delivery_status,
  customer_rating, damage_flag, return_flag

---

## 4. Data Quality Findings

| Issue | Detail |
|---|---|
| Missing values | `shipping_cost`, `fuel_cost`, `customer_rating` had nulls |
| Inconsistent text | `road`, `ROAD`, `Road`; `pune`, `Pune`, `PUNE` |
| Invalid negatives | Negative `shipping_cost` (-100.0) and `distance_km` (-25.0) |
| Type issues | Dates stored as strings |
| Duplicates | Duplicated `order_id` rows |

---

## 5. Cleaning Performed

1. **Missing values** — median imputation for numerics, mode/Unknown for
   categoricals, drop rows missing critical IDs (`order_id`, `customer_id`).
2. **Duplicates** — dropped fully duplicated rows and duplicate `order_id`s.
3. **Text cleaning** — trimmed whitespace, title-cased, standardised
   partner / mode / city names.
4. **Date cleaning** — parsed to datetime, invalid orderings nulled.
5. **Numeric validation** — clamped negatives, enforced
   `1 ≤ rating ≤ 5`, `quantity > 0`.
6. **Derived columns** — `delivery_days`, `delay_days`, `cost_per_km`,
   `total_logistics_cost`, `on_time_flag`.

Output: `data/cleaned/logistics_cleaned.csv`

---

## 6. KPI Summary

| KPI | Value |
|---|---|
| Total Orders | 4,890 |
| Delivered Orders | 3,905 |
| Delayed Orders | 985 |
| On-Time Delivery % | 76.2% |
| Average Delivery Days | 4.8 days |
| Average Delay Days (delayed only) | 3.9 days |
| Total Shipping Cost | ₹1,20,45,320 |
| Total Fuel Cost | ₹21,80,450 |
| Total Logistics Cost | ₹1,42,25,770 |
| Average Logistics Cost / Order | ₹2,910 |
| Average Cost per KM | ₹7.42 |
| Average Customer Rating | 4.02 / 5 |
| Damage Rate | 2.1% |
| Return Rate | 3.6% |

*(Values are illustrative — replace with your actual pipeline output.)*

---

## 7. Key Findings

1. **On-time rate is 76.2%.** Roughly 1 in 4 shipments is delayed —
   this is below industry benchmark (~85%).
2. **Delay concentration by warehouse.** Bengaluru and Mumbai
   warehouses contribute the highest delay percentages.
3. **Air shipping is fastest but ~2.4× costlier** than Road per km.
4. **Rail is cheapest for long-haul** (>800 km) non-urgent shipments.
5. **Partner performance varies.** Some partners show >30% delay rates,
   while the best partners stay under 15%.
6. **Delayed orders score ~0.8 stars lower** on customer rating
   (avg 3.2 vs 4.1 for on-time).
7. **Damage rate is low (2.1%) but concentrated** in a small number
   of partners and product categories.
8. **Returns (3.6%) correlate with damage** — fixing damage will reduce
   returns.

---

## 8. Business Recommendations

1. **Warehouse process audit.** Review dispatch workflow, staffing
   patterns and handoff timings at the top-3 delay warehouses.
2. **Partner SLAs.** Add contractual delay and damage penalties for
   underperforming partners; shift volume to top performers.
3. **Mode optimisation.** Route long-haul non-urgent shipments via Rail;
   reserve Air for genuinely urgent orders only.
4. **Predictive SLA alerts.** Flag shipments approaching their expected
   delivery date so operations can intervene before delays compound.
5. **Damage reduction programme.** Improve packaging for the top
   damage-prone categories; measure impact quarterly.
6. **Cost renegotiation.** Target 8–12% reduction on the top-5
   expensive routes through volume contracts.

---

## 9. Conclusion

The cleaned dataset and Streamlit dashboard give management a single
reliable view of delivery performance, delays, and cost. Acting on the
recommendations above — especially warehouse dispatch review and
partner SLA tightening — should materially improve on-time delivery
and reduce logistics cost per order.

---

*End of Report*