import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_rental_per_day_df(days_df):
    rental_per_day_df = days_df.query(str("dteday >= '2011-01-01' and dteday < '2012-12-31'"))
    return rental_per_day_df

def create_registered_user_df(days_df):
    registered_df = days_df.groupby(by="dteday").agg({
        "registered": "sum"
    })
    registered_df = registered_df.reset_index()
    
    return registered_df

def create_casual_user_df(days_df):
    casual_df = days_df.groupby(by="dteday").agg({
        "casual": "sum"
    })
    casual_df = casual_df.reset_index()

    return casual_df

days_df = pd.read_csv("dashboard/cleaned_day.csv")
hours_df = pd.read_csv("dashboard/cleaned_hour.csv")

datetime_columns = ["dteday"]

days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hours = hours_df["dteday"].min()
max_date_hours = hours_df["dteday"].max()

with st.sidebar:
    st.image("image.jpg")

    start_date, end_date = st.date_input(
        label="Range of Time",
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

new_days_df = days_df[(days_df["dteday"] >= str(start_date)) & (days_df["dteday"] <= str(end_date))]
new_hours_df = hours_df[(hours_df["dteday"] >= str(start_date)) & (hours_df["dteday"] <= str(end_date))]

rental_per_day_df = create_rental_per_day_df(new_days_df)
registered_df = create_registered_user_df(new_days_df)
casual_df = create_casual_user_df(new_days_df)

print(casual_df)

st.header('Simple Bike Sharing Dashboard 🚲')

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = rental_per_day_df.count_cr.sum()
    st.metric("Total Rents", value=total_rentals)

with col2:
    total_registered = registered_df.registered.sum()
    st.metric("Total Registered Users", value=total_registered)

with col3:
    total_casual = casual_df.casual.sum()
    st.metric("Total Casual Users", value=total_casual)

st.subheader("Comparison of bicycle rentals on holidays compared to weekdays")

fig, ax = plt.subplots(figsize=(18, 9))

sns.barplot(
    y="count_cr",
    x="workingday",
    data=days_df.sort_values(by="workingday"),
    palette="tab10",
    ax=ax
)

ax.set_title("One of Week", loc="center", fontsize=20)
ax.set_ylabel("count_cr")
ax.set_xlabel("workingday")
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=16)

st.pyplot(fig)

st.subheader("Year-on-year trend of increasing or decreasing bicycle rentals")

fig, ax = plt.subplots(figsize=(18, 9))
ax.plot(
    days_df["dteday"],
    days_df["count_cr"],
)

ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15)
st.pyplot(fig)