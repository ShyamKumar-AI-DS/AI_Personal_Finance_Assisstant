# 💰 AI Personal Finance Agent

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://groq.com/)
[![VectorDB](https://img.shields.io/badge/VectorDB-ChromaDB-blueviolet.svg)](https://www.trychroma.com/)

An intelligent financial assistant that transforms raw transaction data into actionable, expert financial advice. By leveraging **Retrieval-Augmented Generation (RAG)**, the agent provides personalized coaching based on proven budgeting frameworks like the 50/30/20 rule.

---

## 🌟 Key Features

* 📊 **Automated Ingestion**: Support for `.csv` and `.xlsx` bank statements with automatic cleaning.
* 🔍 **Smart Analytics**: Monthly trend tracking and automated categorization of Income vs. Expenses.
* 🚫 **Subscription Detective**: Automatically identifies recurring charges (Netflix, Gym, etc.).
* 🧠 **RAG-Powered Advice**: Combines your financial data with a knowledge base of expert budgeting strategies.
* 🤖 **AI Executive Summary**: Generates a high-level overview and a step-by-step action plan using LLMs.

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Language** | Python 3.13 |
| **Interface** | Streamlit |
| **LLM Inference** | Groq (OpenAI 20b OSS) |
| **Embeddings** | SentenceTransformers (`all-MiniLM-L6-v2`) |
| **Vector Store** | ChromaDB |
| **Data Handling** | Pandas, Numpy, Openpyxl |

---

## 🏗️ Architecture

The system is built with a modular approach to ensure scalability and easy debugging.

> [!TIP]
> The separation of the **Analytics Engine** from the **AI Advisor** ensures the LLM receives structured, factual data, reducing potential hallucinations.

<img width="800" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/fa0ac895-4074-41a1-bc39-8e5d47584e45" />

---

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
~~~
├── src/
│   ├── app.py           # Streamlit Dashboard UI
│   ├── loader.py        # Data cleaning & normalization
│   ├── analytics.py     # Financial logic & trend detection
│   ├── categorizer.py   # Chart data generation
│   ├── rag.py           # Vector DB & retrieval logic
│   └── advisor.py       # LLM orchestration
├── .env                 # API Keys (Git ignored)
└── requirements.txt     # Project dependencies
~~~

## 🛠️ Setup & Installation

1.  **Clone the repository**:
    ```bash
    git clone <repo_url>
    ```
    cd Personal_finance_analyser


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
## Outputs
#### Dashboard Overview
<img width="940" height="487" alt="image" src="https://github.com/user-attachments/assets/62699b13-8645-470c-83bb-9b4151893aec" />

#### AI Advice Generation
<img width="940" height="354" alt="image" src="https://github.com/user-attachments/assets/0e817525-31e1-4d3b-97e8-548fbdfda070" />


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
*   **Goal Tracking**: Allow users to set specific savings goals within the UI."**AI_Personal_Finance_Assisstant**"

### Developed by Shyam Kumar 🚀
