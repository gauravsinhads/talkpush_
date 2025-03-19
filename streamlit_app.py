import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd


# Set page config
st.set_page_config(page_title="Streamlit talkpush Dashboard", layout="wide")


# Cargar los datos desde el archivo CSV
df = pd.read_csv('candidateinf_DEC-MAR.csv')
# Convert DATE_DAY to datetime
df["DATE_DAY"] = pd.to_datetime(df["DATE_DAY"])

# Apply Aggregation based on Selection
#monthly option
df["MONTHLY_"] = df["DATE_DAY"].dt.strftime("%b-%Y")  # Format as Feb-2024
#weekly option
df["WEEKLY_"] = "W_" + (df["DATE_DAY"] + pd.to_timedelta(6 - df["DATE_DAY"].dt.weekday, unit="D")).dt.strftime("%b-%d-%Y")

    
# Filter out rows where talkscore_overall is 0
df_filtered = df[df["TALKSCORE_OVERALL"] > 0]
# FIG1 and FIG1w Aggregate Data
df_avg_overall = df_filtered.groupby("MONTHLY_", as_index=False)["TALKSCORE_OVERALL"].mean()
df_avg_overall_w = df_filtered.groupby("WEEKLY_", as_index=False)["TALKSCORE_OVERALL"].mean()
# Format the values explicitly to 2 decimal places
df_avg_overall["TEXT_LABEL"] = df_avg_overall["TALKSCORE_OVERALL"].apply(lambda x: f"{x:.2f}")
df_avg_overall_w["TEXT_LABEL"] = df_avg_overall_w["TALKSCORE_OVERALL"].apply(lambda x: f"{x:.2f}")

# Convert MONTHLY_ to datetime for proper sorting
df_avg_overall['MONTHLY_'] = pd.to_datetime(df_avg_overall['MONTHLY_'], format='%b-%Y')
df_avg_overall_w['SORT_KEY'] = pd.to_datetime(df_avg_overall_w['WEEKLY_'].str[2:], format='%b-%d-%Y') 

# Sort the DataFrame by MONTHLY_
df_avg_overall = df_avg_overall.sort_values('MONTHLY_')
df_avg_overall_w = df_avg_overall_w.sort_values('SORT_KEY')


# FIG 1: Clustered Column (Talkscore Overall)
fig1 = px.line(df_avg_overall, 
            x="MONTHLY_", 
            y="TALKSCORE_OVERALL",
            markers=True,  # Add points (vertices)
            title="Average Talkscore Overall Over Time",
            labels={"MONTHLY_": "Time", "TALKSCORE_OVERALL": "Avg Talkscore"},
            line_shape="linear",
            text="TEXT_LABEL")  # Use formatted text
    # Update the trace to display the text on the chart
fig1.update_traces(textposition="top center")
      
# FIG 1 w: Clustered Column (Talkscore Overall) WEEKLY
fig1w = px.line(df_avg_overall_w, 
            x="WEEKLY_", y="TALKSCORE_OVERALL",
            markers=True,  # Add points (vertices)
            title="Average Talkscore Overall Over Time",
            labels={"WEEKLY_": "Time", "TALKSCORE_OVERALL": "Avg Talkscore"},
            line_shape="linear",text="TEXT_LABEL")
    # Update the trace to display the text on the chart
fig1w.update_traces(textposition="top center")
# Set up the dashboard
st.title("Streamlit Talkpush Dashboard")
# Input widgets
col = st.columns(2)
# Display Charts
with col[0]:st.plotly_chart(fig1)
with col[1]:st.plotly_chart(fig1w)
