import streamlit as st
import pandas as pd
import os
import sys

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from loader import DataLoader
from analytics import FinancialAnalyzer
from advisor import FinancialAdvisor

import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="AI Personal Finance Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
        font-family: 'Inter', sans-serif;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 AI Personal Finance Assistant")
st.markdown("### Analyzing your finances with RAG + OpenAI + AI Agents")

# Sidebar for file upload
st.sidebar.header("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=['csv', 'xlsx'])

st.sidebar.markdown("---")
st.sidebar.header("Download Sample Data")
dataset_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Datasets")
if os.path.exists(dataset_dir):
    # Specific files requested
    target_files = [
        "Personal_Finance_Data_1.xlsx", 
        "Personal_Finance_Data_3.csv", 
        "Personal_Finance_Data_2.csv"
    ]
    sample_files = [f for f in os.listdir(dataset_dir) if f in target_files]
    for filename in sorted(sample_files):
        file_path = os.path.join(dataset_dir, filename)
        with open(file_path, "rb") as f:
            st.sidebar.download_button(
                label=f"📥 {filename}",
                data=f,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if filename.endswith(".xlsx") else "text/csv"
            )

# Use default dataset if no file uploaded
if uploaded_file is None:
    st.info("👆Showing demo data for now. Upload your own financial data to get started.")
    # Load demo data
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        dataset_path = os.path.join(base_dir, "../Datasets/Personal_Finance_Dataset.xlsx")
        loader = DataLoader()
        # DataLoader expects a path, so we use it directly.
        df = loader.run_pipeline(dataset_path)
    except Exception as e:
        st.error(f"Could not load demo data: {e}")
        st.stop()
else:
    # Handle File Upload
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # We need to clean/normalize this uploaded DF similar to DataLoader
        # For simplicity, let's reinstantiate DataLoader methods manually or update DataLoader to accept DF
        # Re-using DataLoader logic by mocking it or calling methods
        loader = DataLoader()
        df = loader.clean_column_names(df)
        df = loader.remove_duplicates(df)
        # Assuming standard column names exist or user maps them.
        # For this prototype, we assume format matches.
        df = loader.parse_dates(df, date_col='date') 
        # df = loader.standardize_amounts(df, amount_col='amount')
        
    except Exception as e:
        st.error(f"Error processing file: {e}")
        st.stop()

# Initialize Analyzer
analyzer = FinancialAnalyzer(df)
report = analyzer.generate_full_report()
totals = report['Totals']

# --- Dashboard Layout ---

# 1. Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Income", f"${totals['Total Income']:,.2f}")
with col2:
    st.metric("Total Expenses", f"${totals['Total Expenses']:,.2f}")
with col3:
    net = totals['Net Savings']
    color = "normal" if net >= 0 else "inverse"
    st.metric("Net Debt", f"${net:,.2f}", delta_color=color)
with col4:
    st.metric("Avg Monthly Debt", f"${report['Monthly Average Savings']:,.2f}")

st.divider()

# 2. Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Expense Breakdown")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    expenses = pd.Series(report['Category Totals'])
    # Sort and limit
    expenses = expenses.sort_values(ascending=False).head(10)
    sns.barplot(x=expenses.values, y=expenses.index, ax=ax1, palette="viridis")
    ax1.set_xlabel("Amount")
    ax1.set_ylabel("Category")
    ax1.set_title("Top 10 Expense Categories")
    st.pyplot(fig1)

with col_chart2:
    st.subheader("Monthly Trends")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    trends = analyzer.get_monthly_trends()
    sns.lineplot(data=trends[['Income', 'Expense']], ax=ax2, markers=True)
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Amount")
    ax2.set_title("Monthly Income vs. Expenses")
    st.pyplot(fig2)

st.divider()

# 3. Insights Section
st.subheader("⚠️ Risk Analysis")

# Overspending
with st.expander("Overspending Alerts", expanded=True):
    overspending = report['Overspending Alerts (Latest Month)']
    if overspending:
        for cat, data in overspending.items():
            st.error(f"{cat}: ${data['current']:.0f} (Avg: ${data['average']:.0f}) \n\n(+{data['pct_over']:.1f}%)")
    else:
        st.success("Spending is within average limits.")

# # Recurrent
# with st.expander("Recurrent Charges", expanded=True):
#     recurrent = report['Recurrent Charges']
#     if recurrent:
#         for item in recurrent:
#             st.write(f"** {item['description']} **: ${item['amount']:.0f} ({item['estimated_interval']})")
#     else:
#         st.write("No recurring subscriptions detected.") 

st.divider()

st.subheader("🤖 AI Financial Advisor")
st.caption("Powered by OpenAI & RAG Knowledge Base")

if st.button("Generate Personalized Financial Plan"):
    with st.spinner("Analyzing spending patterns and retrieving expert strategies..."):
        try:
            # Instantiate Advisor with the CURRENT dataframe
            advisor = FinancialAdvisor(df=df)
            advice = advisor.get_advice()
            st.markdown(advice)
        except Exception as e:
            st.error(f"AI Error: {e}")
else:
    st.info("Click the button to generate a detailed financial plan based on your data.")
