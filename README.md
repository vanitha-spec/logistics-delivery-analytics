# 📦 Logistics Delivery Performance & Cost Analytics

An end-to-end data analytics project that converts raw logistics
shipment data into business-ready KPIs, visualisations and an
interactive dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Business Problem

The company manages customer orders, shipments, warehouses,
transportation, delivery partners and logistics costs, but management
cannot easily answer:

- How many orders are delivered on time vs delayed?
- Which routes and warehouses cause the most delays?
- Which shipping modes are expensive?
- Which delivery partners perform best/worst?
- What is the total and per-order logistics cost?

This project delivers a complete analytics solution answering these
questions with data, visuals and recommendations.

---

## 🧩 Objectives

1. Build a reusable Python cleaning pipeline.
2. Compute delivery, delay, warehouse, route, partner and cost KPIs.
3. Answer 30 required business questions.
4. Provide visual evidence using Matplotlib and Seaborn.
5. Deliver an interactive Streamlit dashboard.
6. Document business insights and recommendations.

---

## 🛠 Technology Stack

| Layer | Tools |
|---|---|
| Language | Python 3.10+ |
| Data | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |
| Notebook | Jupyter |
| Dashboard | Streamlit |
| Testing | Pytest |

---

## 📁 Project Structure

```
logistics_delivery_analytics/
├── data/
│   ├── raw/
│   │   └── logistics_data.csv
│   └── cleaned/
│       └── logistics_cleaned.csv
├── notebooks/
│   └── logistics_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── business_analysis.py
│   └── visualization.py
├── app/
│   └── streamlit_app.py
├── reports/
│   └── business_report.md
├── tests/
│   └── test_pipeline.py
├── run_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/logistics_delivery_analytics.git
cd logistics_delivery_analytics
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
```

---

## ▶️ How to Run

### 1. Cleaning Pipeline
```bash
python run_pipeline.py
```
Generates `data/cleaned/logistics_cleaned.csv`.

### 2. Jupyter Notebook
```bash
python -m jupyter notebook notebooks/logistics_analysis.ipynb
```

### 3. Tests
```bash
python -m pytest tests/test_pipeline.py -v
```

### 4. Streamlit Dashboard
```bash
python -m streamlit run app/streamlit_app.py
```
Open http://localhost:8501.

---

## 📊 KPIs Delivered

- Total Orders, Delivered, Delayed
- On-Time Delivery %
- Average Delivery Days, Average Delay Days
- Total / Average Shipping Cost
- Total / Average Fuel Cost
- Total / Average Logistics Cost
- Average Cost per KM
- Damage Rate, Return Rate
- Average Customer Rating

---

## ❓ Business Questions Answered (30)

**Delivery** — total orders, delivered, delayed, on-time %, avg
delivery time, avg delay.

**Route** — most shipments, highest delay, highest cost, highest
cost/km.

**Warehouse** — most orders, highest processing time, highest delay %.

**Transportation** — most-used mode, highest cost, highest delivery
time, highest delay %.

**Partner** — most shipments, highest on-time %, highest cost,
highest damage rate.

**Cost** — total, average, shipping, fuel, split by route / warehouse /
mode / partner.

**Customer** — avg rating, rating by delivery status, return %,
damage %.

---

## 🔍 Key Insights

- On-time delivery is ~76%, below the ~85% benchmark.
- A handful of warehouses and partners dominate delays.
- Air shipping is 2.4× costlier than Road per km.
- Delayed orders score ~0.8 stars lower on customer rating.
- Damage (2.1%) strongly correlates with returns (3.6%).

---

## 💡 Recommendations

1. Audit dispatch workflow at top-delay warehouses.
2. Tighten partner SLAs (delay + damage penalties).
3. Prefer Rail for long-haul non-urgent shipments.
4. Deploy predictive SLA alerts.
5. Improve packaging for damage-prone categories.
6. Renegotiate contracts on the top-5 costly routes.

---

## 🚀 Future Improvements

- Integrate live shipment feeds for real-time monitoring.
- Add geospatial route visualisation.
- Introduce cost forecasting per route.
- Automate monthly PDF report generation.

---

## 👤 Author

**[Vanitha Gadge]**
Data Analyst / Business Analyst
[www.linkedin.com/in/vanitha-gadge] · [vanithagadge06@gmail.com]

---

## 📄 License

This project is released under the MIT License.
