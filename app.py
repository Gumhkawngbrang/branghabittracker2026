import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="2026 Habit Tracker", layout="wide")
st.title("📈 My Annual Habit Trends")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_excel("habit_data.xlsx")
    # Convert checkboxes (True/False) to 1/0 for charting
    df.iloc[:, 3:] = df.iloc[:, 3:].astype(int) 
    return df

df = load_data()

# 2. Sidebar Filter for Month
month = st.sidebar.selectbox("Select Month", df['Month'].unique())
filtered_df = df[df['Month'] == month]

# 3. Monthly Trend Visual
st.subheader(f"Daily Performance for {month}")
# Unpivot data for the chart
df_melted = filtered_df.melt(id_vars=['Day'], value_vars=['Gym', 'Reading'], 
                             var_name='Habit', value_name='Status')

fig = px.line(df_melted, x='Day', y='Status', color='Habit', 
              range_x=[1, 31], range_y=[-0.1, 1.1],
              title="Daily Completion (1 = Done, 0 = Missed)")
st.plotly_chart(fig, use_container_width=True)

# 4. Total Success Rate
st.subheader("Monthly Consistency")
success_rate = filtered_df[['Gym', 'Reading']].mean() * 100
st.bar_chart(success_rate)
