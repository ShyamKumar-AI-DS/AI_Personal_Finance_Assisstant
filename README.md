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
| **Language** | Python 3.9+ |
| **Interface** | Streamlit |
| **LLM Inference** | Groq (Llama models) |
| **Embeddings** | SentenceTransformers (`all-MiniLM-L6-v2`) |
| **Vector Store** | ChromaDB |
| **Data Handling** | Pandas, Openpyxl |

---

## 🏗️ Architecture

The system is built with a modular approach to ensure scalability and easy debugging.

> [!TIP]
> The separation of the **Analytics Engine** from the **AI Advisor** ensures the LLM receives structured, factual data, reducing potential hallucinations.

<img width="800" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/fa0ac895-4074-41a1-bc39-8e5d47584e45" />

---

## 🚀 Project Phases

### 1. Data Ingestion (`loader.py`)
Creates a robust pipeline to handle messy user data:
* Standardizes column names to `snake_case`.
* Parses dates and normalizes numerical amounts.
* Removes duplicates to ensure data integrity.

### 2. Analytics Engine (`analytics.py` & `categorizer.py`)
Extracts meaningful insights:
* **Trend Analysis**: Tracking the "burn rate" and savings ratio across months.
* **Overspending Alerts**: Flags categories exceeding 1.2x historical averages.

### 3. RAG Knowledge Base (`rag.py`)
Equips the AI with expert knowledge:
* **Vector Search**: Uses `ChromaDB` to fetch specific strategies (e.g., "Debt Snowball") based on the user's current financial situation.

### 4. AI Advisor Agent (`advisor.py`)
The "brain" of the operation. It synthesizes the analytics report and RAG context into a human-readable action plan using **Groq**.

---

## 📂 File Structure

```bash
├── src/
│   ├── app.py           # Streamlit Dashboard UI
│   ├── loader.py        # Data cleaning & normalization
│   ├── analytics.py     # Financial logic & trend detection
│   ├── categorizer.py   # Chart data generation
│   ├── rag.py           # Vector DB & retrieval logic
│   └── advisor.py       # LLM orchestration
├── .env                 # API Keys (Git ignored)
└── requirements.txt     # Project dependencies

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
## Outputs
<img width="940" height="487" alt="image" src="https://github.com/user-attachments/assets/62699b13-8645-470c-83bb-9b4151893aec" />
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
*   **Goal Tracking**: Allow users to set specific savings goals within the UI."# AI_Personal_Finance_Assisstant" 
