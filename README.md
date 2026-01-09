# Integrated Credit Risk & Mobility Operations Analysis

**Senior Analytics Case Study | Strategic Data Engineering & Predictive Modeling**

## Executive Summary

This project addresses a complex business challenge: **How do we scale lending in a high-risk environment while maintaining operational efficiency?** By synthesizing German credit data with real-time bureau extraction and mobility logistics, I developed a risk engine that optimizes for a **10:1 cost-of-error ratio**. The final result is an interactive **Risk Management Portal** that bridges the gap between raw data science and executive decision-making.

---

## 1. Project Structure & Repository Architecture

The repository is organized following industry-standard modularity, ensuring that data pipelines are separated from the deployment layer.

```text
credit_risk_case_study/
├── data/
│   ├── raw/                 # Baseline datasets: GermanCredit.csv, BikerDatav2.csv
│   └── processed/           # Feature-engineered outputs for model training
├── Images & Analysis/       # Visualizations for Stakeholder Reports
├── notebooks/
│   ├── 01_eda_and_modeling.ipynb    # Model training, Hyperparameter tuning, Cost curves
│   ├── 02_bureau_extraction.ipynb   # JSON ETL & automated feature engineering
│   └── 03_biker_queries.ipynb       # SQL-based operational audit
├── src/
│   ├── features.py          # Class: BureauFeatureExtractor (Production-grade ETL)
│   └── scoring_logic.py     # Class: CreditScoringService (Encapsulates business rules)
├── templates/
│   └── index.html           # Dashboard: Plotly.js + Bootstrap 5
├── app.py                   # Flask REST API & Web Dashboard Engine
├── requirements.txt         # Managed dependencies
└── README.md

```

---

## 2. Technical Deep Dive

### **Part 1: Predictive Risk Engine**

* **The Problem:** Standard accuracy metrics (like F1-score) ignore the reality that a **False Negative (Default)** costs 10x more than a **False Positive (Opportunity Cost)**.
* **The Solution:** I utilized a **Random Forest Classifier** but moved beyond the default  decision boundary. By plotting the **Total Business Cost Curve**, I identified **** as the optimal threshold.
* **Result:** This strategy caught **58 out of 60 actual defaults**, significantly reducing catastrophic portfolio loss.

### **Part 2: Automated Bureau ETL**

* **Infrastructure:** Developed a Python-based parser to transform nested JSON credit bureau data into flat features.
* **Logic:** Implemented a **Hard Reject** filter: Any applicant with a **Bureau Bad Ratio > 30%** is automatically declined, regardless of the internal model score, providing a second layer of defense.

### **Part 3: Operational Logistics Audit**

* **Analytics:** Using SQL window functions and aggregations, I analyzed mobility patterns in the "Biker" dataset.
* **Finding:** A critical bottleneck occurs on **Sundays**, where average trip durations spike to ** minutes**. This suggests that while credit risk is optimized, the physical fleet is under-supplied during weekend peaks.

---

## 3. How to Execute

### **Environment Setup**

1. **Create Virtual Environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```



### **Running the Application**

To launch the interactive **Risk Management Portal**:

```bash
python app.py

```

* **Web Dashboard:** Open `http://127.0.0.1:5000` to view the Plotly visualizations.
* **API Endpoint:** Send POST requests to `/predict` for real-time applicant scoring.

---

## 4. Key Performance Indicators (KPIs)

The dashboard displays live metrics derived from the analysis:

* **Strategic Threshold:**  (Minimizes Business Cost)
* **Recall for Defaults:** 
* **Peak Operational Load:** Sunday Evenings (Biker Capacity Breach)

---

## Risk Management Portal (Executive View)

### Portfolio Risk & Cost Optimization Dashboard
![Risk Management Portal – Overview](./Images%20%26%20Analysis/Risk%20Management%20Portal%201.JPG)

### Applicant Scoring & Operational Intelligence
![Risk Management Portal – Scoring & Operations](./Images%20%26%20Analysis/Risk%20Management%20Portal%202.JPG)

---

## 5. Strategic Recommendations

1. **Dynamic Thresholding:** The threshold should be adjusted quarterly based on the current cost of capital.
2. **Fraud Prevention:** Integrate the `checking_balance` importance with a real-time verification service, as it remains our #1 predictor.
3. **Fleet Rebalancing:** Shift biker maintenance schedules to **Tuesday-Wednesday** to ensure 100% fleet availability for the Sunday peak.

---

**Author:** Henry Dibie

**Role:** Senior Data Analyst / Risk Specialist

**Submission Date:** January 12th 2026