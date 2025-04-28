import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from millify import millify
st.set_page_config(page_title="Cars Dashboard 🚗", layout="wide")

@st.cache_data
def read():
    return pd.read_csv(r"../cars-project/tree/master/datasets/EDa.csv")

# 🧠 New: Cache the scatter figure creation
@st.cache_data
def create_scatter_plot(df, x, y, color=None, size=None):
    fig = px.scatter(df, x=x, y=y, color=color, size=size)
    return fig

# Read data
df = read()

# Dashboard Title
st.title("cars dashboard 🚗")

# Button to show sample data
btn = st.button("show sample of data")
if btn:
    st.dataframe(df.sample(5))

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("total sales", millify(df['price'].sum()))
with col2:
    st.metric("mean sales", millify(df['price'].mean()))
with col3:
    st.metric("average sales", millify((df['price'].max() - df['price'].min())))

# Visualization Section
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 5 Car Sale", divider="gray")
    top5carSales = df.CarName.value_counts().head(5).reset_index()
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(top5carSales, x='CarName', y='count', hue='count')
    plt.title('Top 5 Car sale', fontsize=16)
    plt.xlabel('Car Name', fontsize=14)
    plt.ylabel('count', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Carbody vs Price", divider="gray")
    top5carPrice = df.groupby('carbody')['price'].mean().sort_values(ascending=False).reset_index()
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=top5carPrice, x='carbody', y='price', palette='viridis')
    plt.title('Carbody Prices', fontsize=16)
    plt.xlabel('carbody', fontsize=14)
    plt.ylabel('Price ($)', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Top 5 Car Prices", divider="gray")
    top5carPrice = df.groupby('CarName')['price'].max().sort_values(ascending=False).head(5).reset_index()
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=top5carPrice, x='CarName', y='price', palette='viridis')
    plt.title('Top 5 Car Prices', fontsize=16)
    plt.xlabel('Car Name', fontsize=14)
    plt.ylabel('Price ($)', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Fueltype vs Price")
    top5carPrice = df.groupby('fueltype')['price'].mean().sort_values(ascending=False).reset_index()
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=top5carPrice, x='fueltype', y='price', palette='viridis')
    plt.title('Fueltype Prices', fontsize=16)
    plt.xlabel('fueltype', fontsize=14)
    plt.ylabel('Price ($)', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)

# Dynamic scatter plot
clonum = df.select_dtypes(include='number').columns.tolist()
category = df.select_dtypes(include='object').columns.tolist()

col1, col2, col3, col4 = st.columns(4)
with col1:
    x = st.selectbox("x axis", [None] + clonum, index=0)
with col2:
    y = st.selectbox("y axis", [None] + clonum, index=0)
with col3:
    color = st.selectbox("filter by", [None] + category, index=0)
with col4:
    size = st.selectbox("size", [None] + clonum, index=0)

# Now use the cached scatter plot creation
if x is not None and y is not None:
    fig = create_scatter_plot(df, x, y, color=color, size=size)
    st.plotly_chart(fig)
else:
    st.info("Please select both X and Y axes to generate the scatter plot.")
