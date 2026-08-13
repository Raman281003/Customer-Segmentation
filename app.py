import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="European Banking - Customer Churn Analytics",
    page_icon="🏦",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_excel(
        "Internship Project.xlsx",
        sheet_name="European_Bank (1)"
    )

df = load_data()

st.title("🏦 Customer Segmentation & Churn Pattern Analytics")
st.caption("European Banking | Data-driven customer churn analysis")

# Sidebar filters
st.sidebar.header("Filters")

geographies = sorted(df["Geography"].dropna().unique().tolist())
selected_geo = st.sidebar.multiselect(
    "Geography",
    geographies,
    default=geographies
)

genders = sorted(df["Gender"].dropna().unique().tolist())
selected_gender = st.sidebar.multiselect(
    "Gender",
    genders,
    default=genders
)

churn_options = sorted(df["Churn Status"].dropna().unique().tolist())
selected_churn = st.sidebar.multiselect(
    "Churn Status",
    churn_options,
    default=churn_options
)

filtered = df[
    df["Geography"].isin(selected_geo)
    & df["Gender"].isin(selected_gender)
    & df["Churn Status"].isin(selected_churn)
].copy()

# KPI calculations
total_customers = len(filtered)
churned_customers = int((filtered["Exited"] == 1).sum())
retained_customers = total_customers - churned_customers
churn_rate = (churned_customers / total_customers * 100) if total_customers else 0
avg_balance = filtered["Balance"].mean() if total_customers else 0
avg_salary = filtered["EstimatedSalary"].mean() if total_customers else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Customers", f"{total_customers:,}")
c2.metric("Churned Customers", f"{churned_customers:,}")
c3.metric("Retention Customers", f"{retained_customers:,}")
c4.metric("Churn Rate", f"{churn_rate:.1f}%")
c5.metric("Avg. Balance", f"€{avg_balance:,.0f}")

st.divider()

# Charts row 1
left, right = st.columns(2)

with left:
    geo = (
        filtered.groupby("Geography", as_index=False)
        .agg(Customers=("CustomerId", "count"),
             Churned=("Exited", "sum"))
    )
    geo["Churn Rate %"] = geo["Churned"] / geo["Customers"] * 100
    fig = px.bar(
        geo,
        x="Geography",
        y="Churn Rate %",
        text="Churn Rate %",
        title="Churn Rate by Geography"
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with right:
    age = (
        filtered.groupby("Age Group", as_index=False)
        .agg(Customers=("CustomerId", "count"),
             Churned=("Exited", "sum"))
    )
    age["Churn Rate %"] = age["Churned"] / age["Customers"] * 100
    fig = px.bar(
        age,
        x="Age Group",
        y="Churn Rate %",
        text="Churn Rate %",
        title="Churn Rate by Age Group"
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# Charts row 2
left, right = st.columns(2)

with left:
    active = (
        filtered.groupby("IsActiveMember", as_index=False)
        .agg(Customers=("CustomerId", "count"),
             Churned=("Exited", "sum"))
    )
    active["Member Status"] = active["IsActiveMember"].map(
        {0: "Inactive Member", 1: "Active Member"}
    )
    active["Churn Rate %"] = active["Churned"] / active["Customers"] * 100
    fig = px.bar(
        active,
        x="Member Status",
        y="Churn Rate %",
        text="Churn Rate %",
        title="Churn Rate: Active vs Inactive Members"
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with right:
    products = (
        filtered.groupby("NumOfProducts", as_index=False)
        .agg(Customers=("CustomerId", "count"),
             Churned=("Exited", "sum"))
    )
    products["Churn Rate %"] = products["Churned"] / products["Customers"] * 100
    fig = px.bar(
        products,
        x="NumOfProducts",
        y="Churn Rate %",
        text="Churn Rate %",
        title="Churn Rate by Number of Products"
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# Customer value segment
segment = (
    filtered.groupby("Customer Value Segment", as_index=False)
    .agg(Customers=("CustomerId", "count"),
         Churned=("Exited", "sum"))
)
segment["Churn Rate %"] = segment["Churned"] / segment["Customers"] * 100

fig = px.bar(
    segment,
    x="Customer Value Segment",
    y="Churn Rate %",
    text="Churn Rate %",
    title="Churn Rate by Customer Value Segment"
)
fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# Detailed data
st.subheader("Customer Data")
st.dataframe(filtered, use_container_width=True, height=350)

# Download filtered data
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Filtered Data",
    data=csv,
    file_name="filtered_customer_data.csv",
    mime="text/csv"
)
