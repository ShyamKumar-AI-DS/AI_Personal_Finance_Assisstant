import os
import sys
from dotenv import load_dotenv
from groq import Groq

# Add src to path if running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from loader import DataLoader
from analytics import FinancialAnalyzer
from rag import BudgetRAG

load_dotenv()

class FinancialAdvisor:
    def __init__(self, df=None):
        # Initialize Components
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.rag = BudgetRAG()
        
        # Load Data
        if df is not None:
            self.df = df
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            dataset_path = os.path.join(base_dir, "../Datasets/Personal_Finance_Data_1.xlsx")
            loader = DataLoader()
            self.df = loader.run_pipeline(dataset_path)
            
        self.analyzer = FinancialAnalyzer(self.df)

    def generate_prompt(self, analysis, context_strategies):
        """
        Constructs the detailed prompt for the LLM.
        """
        totals = analysis['Totals']
        overspending = analysis['Overspending Alerts (Latest Month)']
        
        # Format Overspending text
        overspending_text = "No significant overspending."
        if overspending:
            items = []
            for cat, data in overspending.items():
                items.append(f"- {cat}: Current ${data['current']:.0f} (Avg ${data['average']:.0f}) -> +{data['pct_over']:.1f}% higher")
            overspending_text = "\n".join(items)

        # Context from RAG
        strategies_text = "\n".join([f"- {s}" for s in context_strategies])

        prompt = f"""
        You are an expert AI Financial Advisor. Your goal is to analyze the user's financial situation and provide actionable, personalized advice based on proven budgeting strategies.

        ### 1. USER FINANCIAL OVERVIEW
        - Total Income: ${totals['Total Income']:,.2f}
        - Total Expenses: ${totals['Total Expenses']:,.2f}
        - Net Savings: ${totals['Net Savings']:,.2f} (Deficit if negative)
        
        ### 2. CRITICAL ALERTS (OVERSPENDING)
        {overspending_text}

        ### 3. PROVEN BUDGETING STRATEGIES (Reference these in your advice)
        {strategies_text}

        ### 4. YOUR TASK
        Based on the data above, provide a comprehensive financial plan:
        
        **A. Executive Summary**
        Briefly assess the user's financial health (Healthy, At Risk, or Critical) and explain in simple terms. Be clear and direct but empathetic.

        **B. Immediate Action Items**
        In bullet list 3 specific actions the user must take this week to stop the bleeding. Focus on the overspending categories.

        **C. Strategic Budgeting Plan**
        In bullet list propose a specific strategy from the provided list (e.g., 50/30/20 or Zero-Based) that fits this user's situation. Explain WHY.

        **D. Savings Roadmap**
        Tabulate and calculate if they can become positive next month by cutting the 'Recoverable Waste' mentioned in the overspending section.

        **E. Habit Building**
        In bullet list suggest one simple daily or weekly habit to improve financial discipline.

        Keep the tone professional, encouraging, and highly actionable.
        """
        return prompt

    def get_advice(self):
        print("Running Financial Analysis...")
        report = self.analyzer.generate_full_report()
        
        print("Retrieving Relevant Budgeting Strategies...")
        # Construct a query based on the analysis
        query = "How to fix overspending and save money debt"
        if report['Totals']['Net Savings'] < 0:
            query = "strategies for getting out of debt and stopping overspending"
        
        context_strategies = self.rag.retrieve(query, k=5)
        
        print("Generating AI Advice...")
        prompt = self.generate_prompt(report, context_strategies)
        
        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful financial advisor and strict financial coach."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
<<<<<<< HEAD
            model="openai/gpt-oss-20b", 
=======
            model="llama-3.3-70b-versatile", 
>>>>>>> 14c6bee1708ed71972a8b6bc0e42e8f6321da319
            temperature=0.2,
        )
        
        return completion.choices[0].message.content

if __name__ == "__main__":
    advisor = FinancialAdvisor()
    advice = advisor.get_advice()
    
    print("\n" + "="*50)
    print("AI FINANCIAL ADVISOR REPORT")
    print("="*50 + "\n")
    print(advice)
