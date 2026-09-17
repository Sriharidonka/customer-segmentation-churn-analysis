# 🏦 Customer Segmentation & Churn Pattern Analytics in European Banking

## 📌 Project Overview

This project analyzes customer churn patterns in a European banking dataset containing **10,000 customers**.

The analysis focuses on customer demographics, financial characteristics, engagement, customer value, and churn risk to identify segments with higher observed churn.

The project uses **Python** for data preparation and analysis and **Streamlit** for the interactive dashboard.

---

## 🎯 Objectives

- Analyze customer churn across different segments.
- Clean and prepare the banking dataset.
- Create demographic, financial, engagement, and value-based segments.
- Analyze churn across geography, age, tenure, credit score, balance, and engagement.
- Develop a customer risk segmentation framework.
- Analyze churn-associated financial exposure.
- Identify high-value and high-risk customer segments.
- Build an interactive Streamlit dashboard.

---

## 📊 Dataset

The dataset contains **10,000 banking customer records**.

### Key Features

| Feature | Description |
|---|---|
| CustomerId | Unique customer identifier |
| CreditScore | Customer credit score |
| Geography | Customer country |
| Age | Customer age |
| Tenure | Years with the bank |
| Balance | Account balance |
| NumOfProducts | Number of banking products |
| HasCrCard | Credit card ownership |
| IsActiveMember | Customer activity status |
| EstimatedSalary | Estimated salary |
| Exited | Churn indicator |

`Exited = 0` → Retained  
`Exited = 1` → Churned

---

## 🧹 Data Preparation

The project follows these stages:

**Raw Dataset → Data Cleaning → Feature Engineering → Risk Segmentation → Churn Analysis → Dashboard**

### Engineered Features

- Age Group
- Credit Score Band
- Tenure Group
- Balance Segment
- Customer Value
- Engagement Status
- Risk Score
- Churn Risk Segment

Final datasets:

- `Cleaned_Bank_Churn.csv`
- `Bank_Churn_Feature_Engineered.csv`
- `Bank_Churn_Risk_Segmented.csv`

---

## 👥 Customer Segmentation

Customers are segmented based on:

- **Age:** `<30`, `30-45`, `46-60`, `60+`
- **Credit Score:** Low, Medium, High
- **Tenure:** New, Mid-term, Long-term
- **Balance:** Zero-balance, Low-balance, High-balance
- **Customer Value:** Regular Value, High Value
- **Engagement:** Active, Inactive

---

## 🎯 Churn Risk Analysis

A calculated `RiskScore` is used to classify customers into:

- Low Risk
- Moderate Risk
- High Risk
- Critical Risk

The analysis examines churn rates and churn-associated balance across these risk segments.

A **Critical Risk + High Value** segment is also analyzed to understand customer retention exposure.

> These are observations from the dataset and are not machine-learning churn predictions.

---

## 📈 Churn Analysis

Churn is analyzed across:

- Geography
- Age
- Gender
- Credit Score
- Balance
- Tenure
- Customer Value
- Engagement
- Number of Products

---

## 📊 Streamlit Dashboard

The interactive dashboard includes:

### 📊 Overview
- Executive KPIs
- Churn distribution
- Geography-wise churn
- Dynamic insights

### 🌍 Demographics
- Age × Geography
- Age × Engagement
- Tenure
- Credit Score
- Balance Segment

### 🎯 Risk Analysis
- Risk segmentation
- Churn-associated balance
- Risk summary
- Critical Risk + High Value analysis

### 💰 Customer Value
- High-value customer KPIs
- High-value churn analysis
- Customer Value × Risk analysis

### 🔎 Customer Explorer
- Individual customer profile
- Financial and banking information
- Engagement and product details
- Risk assessment
- Customer table
- CSV download

### Filters

- Geography
- Age Group
- Engagement Status
- Customer Value

---

## 🛠️ Technologies

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Jupyter Notebook
- Git / GitHub

---

## 📁 Project Structure

```text
Customer Segmentation and Churn Analysis/
│
├── Dataset/
│   ├── Bank_Churn.csv
│   ├── Cleaned_Bank_Churn.csv
│   ├── Bank_Churn_Feature_Engineered.csv
│   └── Bank_Churn_Risk_Segmented.csv
│
├── Images/
│   ├── overview.png
│   ├── Risk Analysis.png
│   ├── Priority segment.png
│   └── Customer explorer.png
│
├── Notebooks/
│   └── Bank_Churn_Analysis.ipynb
│
├── Streamlit/
│   ├── app.py
│   └── requirements.txt
│
├── Reports/
├── .gitignore
└── README.md
🚀 How to Run
1. Clone the Repository
git clone https://github.com/Sriharidonka/customer-segmentation-churn-analysis.git
cd "Customer Segmentation and Churn Analysis/Streamlit"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py

The dashboard will open at:

http://localhost:8501

👨‍💻 Author

Srihari Donka

B.Tech — Artificial Intelligence & Data Science
SRKR Engineering College