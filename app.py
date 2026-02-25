import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="2026 Habit Tracker", layout="wide")

# Custom CSS to make it look modern
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    # Load your specific file
    df = pd.read_csv("Habittracker 2026.xlsx - Feb.csv")
    
    # Identify habit columns (Everything except Day and Month)
    # We assume 'Day' is your first column based on your request
    all_cols = df.columns.tolist()
    non_habit_cols = ['Day', 'Month', 'Date'] # Columns to ignore for math
    habits = [c for c in all_cols if c not in non_habit_cols]
    
    # Convert Checkbox/True-False to 1 and 0
    for habit in habits:
        df[habit] = df[habit].apply(lambda x: 1 if x is True or str(x).upper() == 'TRUE' or x == 1 else 0)
    
    return df, habits

try:
    df, habit_list = load_data()

    st.title("🚀 2026 Habit Performance")
    
    # --- Sidebar ---
    st.sidebar.header("Dashboard Settings")
    # If your file has multiple months, this lets you switch
    if 'Month' in df.columns:
        month_filter = st.sidebar.selectbox("Select Month", df['Month'].unique())
        display_df = df[df['Month'] == month_filter]
    else:
        display_df = df
        month_filter = "Current Month"

    selected_habits = st.sidebar.multiselect("Filter Habits", habit_list, default=habit_list[:3])

    # --- Top Metrics ---
    st.subheader(f"Summary for {month_filter}")
    m_cols = st.columns(len(selected_habits))
    for i, habit in enumerate(selected_habits):
        count = display_df[habit].sum()
        total = len(display_df)
        percent = (count / total) * 100
        m_cols[i].metric(label=habit, value=f"{count}/{total}", delta=f"{percent:.0f}% Done")

    # --- The 1-31 Trend Visual ---
    st.markdown("---")
    st.subheader("Daily Completion Trend (Day 1 - 31)")
    
    # Prepare data for Line Chart
    plot_df = display_df.melt(id_vars=['Day'], value_vars=selected_habits, 
                              var_name='Habit', value_name='Completed')
    
    fig = px.line(plot_df, x='Day', y='Completed', color='Habit',
                  markers=True, 
                  line_shape="hv", # This makes it a "Step" chart (On/Off)
                  range_y=[-0.1, 1.1],
                  color_discrete_sequence=px.colors.qualitative.Prism)

    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        yaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['❌ Missed', '✅ Done']),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Heatmap View ---
    st.subheader("Completion Heatmap")
    heat_df = display_df.set_index('Day')[selected_habits].T
    fig_heat = px.imshow(heat_df, 
                         color_continuous_scale='Greens',
                         labels=dict(x="Day of Month", y="Habit", color="Status"))
    st.plotly_chart(fig_heat, use_container_width=True)

except Exception as e:
    st.error(f"Waiting for data... Ensure your CSV is named 'Habittracker 2026.xlsx - Feb.csv' in GitHub.")
    st.exception(e)
