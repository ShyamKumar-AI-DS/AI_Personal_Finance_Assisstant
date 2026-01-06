# 💰 AI Personal Finance Agent

An intelligent financial assistant that analyzes your personal transaction data, detects spending patterns, and uses Retrieval-Augmented Generation (RAG) to provide actionable, expert financial advice.

## 📋 Project Overview

This project is designed to bridge the gap between raw financial data and personalized financial coaching. By combining traditional data analytics with Generative AI, the system not only tells you *what* you spent but *how* to improve your financial health based on proven budgeting strategies (e.g., 50/30/20 rule, Zero-Based Budgeting).

## 🏗️ Architecture

The system follows a modular architecture separating data processing, analysis, knowledge retrieval, and the user interface.
![alt text](<Datasets/Flow Diagram.png>)

## 🚀 Project Phases

### Phase 1: Data Ingestion & Preprocessing (`loader.py`)
*   **Objective**: Create a robust pipeline to handle messy user data.
*   **Features**:
    *   Supports `.csv` and `.xlsx` formats.
    *   Standardizes column names (snake_case).
    *   Parses dates and normalizes numerical amounts.
    *   Removes duplicates to ensure data integrity.

### Phase 2: Financial Analytics Engine (`analytics.py` & `categorizer.py`)
*   **Objective**: Extract meaningful insights from the cleaned data.
*   **Features**:
    *   **Trend Analysis**: Monthly income vs. expense tracking.
    *   **Subscription Detection**: Identifies recurring charges based on amount and frequency (e.g., Netflix, Gym).
    *   **Overspending Alerts**: Flags categories where current spending exceeds the historical average by a threshold (default 1.2x).
    *   **Categorization**: Splits data into Income and Expense streams for visualization.

### Phase 3: RAG Knowledge Base (`rag.py`)
*   **Objective**: Equip the AI with expert financial knowledge.
*   **Implementation**:
    *   **Embeddings**: Uses `SentenceTransformer` (`all-MiniLM-L6-v2`) to convert text into vector embeddings.
    *   **Vector Store**: Uses `ChromaDB` to store and retrieve budgeting guidelines.
    *   **Retrieval**: Fetches relevant financial strategies based on the user's specific financial situation (e.g., "debt reduction" strategies if savings are negative).

### Phase 4: AI Advisor Agent (`advisor.py`)
*   **Objective**: Synthesize data and knowledge into human-readable advice.
*   **Workflow**:
    1.  Receives the structured report from the Analytics Engine.
    2.  Queries the RAG system for relevant context.
    3.  Constructs a detailed prompt containing the user's financial health, alerts, and retrieved strategies.
    4.  Calls the LLM (via Groq) to generate a personalized "Executive Summary" and "Action Plan".

### Phase 5: User Interface (`app.py`)
*   **Objective**: Provide an interactive dashboard for the user.
*   **Tech Stack**: Streamlit.
*   **Features**:
    *   File uploader.
    *   Interactive metric cards (Income, Expense, Savings).
    *   Charts (Expense Breakdown, Monthly Trends).
    *   "Generate Plan" button to trigger the AI Advisor.

## 📂 File Structure

| File | Description |
|------|-------------|
| `src/app.py` | Main entry point. Streamlit dashboard application. |
| `src/loader.py` | Handles file loading, cleaning, and normalization. |
| `src/analytics.py` | Core logic for calculating totals, trends, and alerts. |
| `src/categorizer.py` | Helper for categorization and generating chart data. |
| `src/rag.py` | Manages the Vector Database and document retrieval. |
| `src/advisor.py` | Orchestrates the analysis and LLM interaction. |
| `src/budget_guidelines.py` | (Optional) Source text data for the RAG knowledge base. |

## 🛠️ Setup & Installation

1.  **Clone the repository**:
    ```bash
    git clone <repo_url>
    cd Personal_finance_analyser
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Key libraries: `streamlit`, `pandas`, `chromadb`, `sentence-transformers`, `groq`, `python-dotenv`, `matplotlib`, `seaborn`.*

3.  **Environment Configuration**:
    Create a `.env` file in the root directory and add your API key:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

4.  **Run the Application**:
    ```bash
    streamlit run src/app.py
    ```

## 💡 Usage Flow

1.  **Launch App**: Open the localhost URL provided by Streamlit.
2.  **Upload Data**: Upload your bank statement (CSV/Excel).
    *   *Note: Ensure columns like 'Date', 'Description', 'Category', 'Amount', and 'Type' exist.*
3.  **View Dashboard**: Explore the automatic breakdown of your finances.
4.  **Get Advice**: Click **"Generate Personalized Financial Plan"**.
    *   The AI will analyze your overspending.
    *   It will retrieve specific strategies (e.g., "Snowball Method" for debt).
    *   It will output a formatted plan with immediate action items.

## 🔮 Future Improvements

*   **Multi-Modal Input**: Support for uploading images of receipts.
*   **Forecasting**: Use time-series models to predict future balances.
*   **Goal Tracking**: Allow users to set specific savings goals within the UI."# AI_Personal_Finance_Assisstant" 
