# Superstore Sales Analytics

An interactive sales & profit dashboard built with Streamlit, Pandas and Plotly over the public "Sample - Superstore" retail dataset (9,994 US orders, 2014-2017).

**Live app:** _add your Streamlit Community Cloud URL here after deploying_

## Features

- KPI tiles: Total Sales, Total Profit, Profit Margin, Orders
- Sidebar filters: Year, Region, Category, Segment
- Sales mix by category
- Monthly sales trend
- Sales & profit by region
- Profit by sub-category (flags which sub-categories are unprofitable despite high sales)
- Top 10 products by sales

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy for free (Streamlit Community Cloud)

1. Push this folder to a public GitHub repo (include `app.py`, `requirements.txt`, `superstore.csv`)
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub
3. "New app" → pick the repo → main file path `app.py` → Deploy
4. You'll get a permanent `https://<something>.streamlit.app` URL

## Data

Public "Sample - Superstore" dataset — the standard dataset used to learn BI/analytics tools. Not real company data.
