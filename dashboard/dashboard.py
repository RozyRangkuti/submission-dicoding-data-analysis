# Import Semua Packages/Library yang Digunakan

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import urllib
import matplotlib.image as mpimg
import streamlit as st
from func import DataAnalyzer, BrazilMapPlotter

sns.set_theme(style='darkgrid')

# main dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_data = pd.read_csv("dashboard/main_data.csv")
all_data.sort_values(by="order_approved_at", inplace=True)
all_data.reset_index(inplace=True)

# Geolocation dataset
geolocation = pd.read_csv("geolocation.csv")
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_data[col] = pd.to_datetime(all_data[col])

min_date = all_data["order_approved_at"].min()
max_date = all_data["order_approved_at"].max()

# sidebar
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("logo3.png", width=200)
    with col3:
        st.write(' ')

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
# Main
main_df = all_data[(all_data["order_approved_at"] >= str(start_date)) &
                    (all_data["order_approved_at"] <= str(end_date))]


function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)

sum_order_items_df = function.create_sum_order_items_df()
product_price_df = function.create_product_price_df()
monthly_orders_df = function.create_monthly_orders_df()
review_score, common_score = function.review_score_df()
                    
# title
st.header('Brazil E-Commerce Analysis Data')

# Add text or descriptions
st.write("**This is a dashboard for analyzing Brazil E-Commerce public dataset.**")

# Sum Order Items
st.subheader("Sum Order Items")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

colors = ["#008000", "#808080", "#808080", "#808080", "#808080"]

sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Most sold products", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.sort_values(by="products", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Least sold product", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("Most and least sold products", fontsize=20)
st.pyplot(fig)


# Product Price
st.subheader("E-Commerce Product Price")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

colors = ["#008000", "#808080", "#808080", "#808080", "#808080"]

sns.barplot(x="price", y="product_category_name_english", data=product_price_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Most expensive product", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="price", y="product_category_name_english", data=product_price_df.sort_values(by="price", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Cheapest product", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("The most expensive and cheapest products in e-commerce", fontsize=20)
st.pyplot(fig)


# Monthly Orders (2018)
st.subheader("Monthly Orders (2018)")

total_order = monthly_orders_df["order_count"].sum()
st.markdown(f"Total Order: **{total_order}**")
    
# plt.figure(figsize=(10, 5))
fig, ax = plt.subplots(figsize=(12, 6))
plt.plot(
    monthly_orders_df["order_approved_at"],
    monthly_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#008000"
)
plt.title("Number of Orders per Month (2018)", loc="center", fontsize=20)
plt.xticks(fontsize=10, rotation=25)
plt.yticks(fontsize=10)
st.pyplot(fig)


# Review Score
st.subheader("Review Score")
col1, col2 = st.columns(2)

with col1:
    avg_review_score = review_score.mean()
    st.markdown(f"Average Review Score: **{avg_review_score:.2f}**")

with col2:
    most_common_review_score = review_score.value_counts().index[0]
    st.markdown(f"Most Common Review Score: **{most_common_review_score}**")
    
fig, ax = plt.subplots(figsize=(10, 5))
colors = sns.color_palette("crest", len(review_score))

sns.barplot(x=review_score.index,
            y=review_score.values,
            order=review_score.index,
            palette=colors
            )

plt.title("Rating by customers", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.xticks(fontsize=12)

# Adding labels above each bar
for i, v in enumerate(review_score.values):
    ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=12, color='black')

st.pyplot(fig)


# Customer Demographic
st.subheader("Geolocation")

map_plot.plot()

with st.expander("See Explanation"):
    st.write("According to the graph that has been created, there are more customers in the southeast and south. Other information, there are more customers in cities that are capitals (São Paulo, Rio de Janeiro, Porto Alegre, and others).")
        
st.caption("Copyright (C) Muhammad Rozy Syahputra 2024")
