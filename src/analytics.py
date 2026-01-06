import os
import pandas as pd
import numpy as np
from loader import DataLoader
from categorizer import Categorizer

class FinancialAnalyzer:
    def __init__(self, df):
        self.df = df

        # Custom Rule: 'Other' category is treated as Income source
        if 'category' in self.df.columns and 'type' in self.df.columns:
             self.df.loc[self.df['category'].str.title() == 'Other', 'type'] = 'Income'

        self.income_df = df[df['type'].str.lower() == 'income'].copy()
        self.expense_df = df[df['type'].str.lower() == 'expense'].copy()
        
        # Ensure date is datetime
        if 'date' in self.df.columns and not pd.api.types.is_datetime64_any_dtype(self.df['date']):
             self.df['date'] = pd.to_datetime(self.df['date'])

    def get_basic_totals(self):
        return {
            "Total Income": self.income_df['amount'].sum(),
            "Total Expenses": self.expense_df['amount'].sum(),
            "Net Savings": self.income_df['amount'].sum() - self.expense_df['amount'].sum()
        }

    def get_category_totals(self):
        return self.expense_df.groupby('category')['amount'].sum().to_dict()

    def get_monthly_trends(self):
        """
        Resamples data by month to show trends.
        """
        # Ensure index is datetime for resampling
        temp_income = self.income_df.set_index('date')
        temp_expense = self.expense_df.set_index('date')
        
        monthly_income = temp_income.resample('ME')['amount'].sum() # 'ME' is Month End (pandas 2.x)
        monthly_expense = temp_expense.resample('ME')['amount'].sum()
        
        # Combine into a DataFrame
        trends = pd.DataFrame({
            'Income': monthly_income,
            'Expense': monthly_expense
        }).fillna(0)
        
        trends['Savings'] = trends['Income'] - trends['Expense']
        return trends

    def detect_recurrent_charges(self, min_occurences=3):
        """
        Detects recurring expenses based on description and amount similarity.
        """
        # Group by description and amount (rounded to avoid small discrepancies)
        self.expense_df['amount_rounded'] = self.expense_df['amount'].round(0)
        
        group = self.expense_df.groupby(['transaction_description', 'amount_rounded']).size().reset_index(name='count')
        recurrent = group[group['count'] >= min_occurences]
        
        # Get details
        results = []
        for _, row in recurrent.iterrows():
            matches = self.expense_df[
                (self.expense_df['transaction_description'] == row['transaction_description']) & 
                (self.expense_df['amount_rounded'] == row['amount_rounded'])
            ]
            avg_days_diff = matches['date'].sort_values().diff().dt.days.mean()
            
            # If it happens roughly every 28-31 days, it's likely a monthly subscription
            interval = "Irregular"
            if 28 <= avg_days_diff <= 32:
                 interval = "Monthly"
            
            results.append({
                "description": row['transaction_description'],
                "amount": row['amount_rounded'],
                "frequency": row['count'],
                "estimated_interval": interval
            })
            
        return pd.DataFrame(results)

    def check_overspending(self, threshold_factor=1.2):
        """
        Flags categories where the latest month's spending is significantly higher than the average.
        """
        if self.expense_df.empty:
            return {}

        # 1. Calculate Monthly Spending per Category
        temp_df = self.expense_df.copy()
        temp_df['month'] = temp_df['date'].dt.to_period('M')
        
        monthly_cat_spend = temp_df.groupby(['category', 'month'])['amount'].sum().reset_index()
        
        # 2. Calculate Average per Category (excluding latest month to avoid skewing?)
        # Let's just use all-time average for simplicity
        avg_spend = monthly_cat_spend.groupby('category')['amount'].mean()
        
        # 3. Check Latest Month
        latest_month = temp_df['month'].max()
        latest_spend = monthly_cat_spend[monthly_cat_spend['month'] == latest_month].set_index('category')['amount']
        
        overspending = {}
        for cat in latest_spend.index:
            avg = avg_spend.get(cat, 0)
            current = latest_spend[cat]
            if current > (avg * threshold_factor):
                overspending[cat] = {
                    "current": current,
                    "average": avg,
                    "pct_over": ((current - avg) / avg) * 100 if avg > 0 else 100
                }
        return overspending

    def calculate_savings_potential(self):
        """
        Simple potential: Net Savings + Waste (Overspending).
        """
        totals = self.get_basic_totals()
        overspending = self.check_overspending()
        
        recoverable_waste = sum([item['current'] - item['average'] for item in overspending.values()])
        
        return {
            "Current Net Savings": totals['Net Savings'],
            "Recoverable Waste (Overspending)": recoverable_waste,
            "Potential Monthly Savings": totals['Net Savings'] + recoverable_waste 
            # Note: This adds 'waste' (which is monthly) to Total Net Savings (which is global). 
            # Ideally should be monthly. Let's adjust to Monthly Average.
        }
    
    def generate_full_report(self):
        trends = self.get_monthly_trends()
        avg_monthly_savings = trends['Savings'].mean()
        
        return {
            "Totals": self.get_basic_totals(),
            "Monthly Average Savings": avg_monthly_savings,
            "Recurrent Charges": self.detect_recurrent_charges().to_dict('records'),
            "Overspending Alerts (Latest Month)": self.check_overspending(),
            "Category Totals": self.get_category_totals()
        }

# def main():
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     dataset_path = os.path.join(base_dir, "../../Datasets/Personal_Finance_Data_1.xlsx")
    
#     print("--- Financial Analysis Engine ---")
#     loader = DataLoader()
#     try:
#         df = loader.run_pipeline(dataset_path)
#     except Exception as e:
#         print(f"Error loading data: {e}")
#         return

#     analyzer = FinancialAnalyzer(df)
#     report = analyzer.generate_full_report()
    
#     print("\n--- 1. Financial Overview ---")
#     totals = report['Totals']
#     print(f"Total Income:   ${totals['Total Income']:,.2f}")
#     print(f"Total Expenses: ${totals['Total Expenses']:,.2f}")
#     print(f"Net Savings:    ${totals['Net Savings']:,.2f}")
#     print(f"Avg Monthly Savings: ${report['Monthly Average Savings']:,.2f}")

#     print("\n--- 2. Recurrent Charges (Subscription Pattern Detection) ---")
#     recurrent = report['Recurrent Charges']
#     if recurrent:
#         print(f"{'Description':<30} | {'Amount':<10} | {'Interval':<10}")
#         print("-" * 55)
#         for item in recurrent:
#             print(f"{item['description']:<30} | ${item['amount']:<9.0f} | {item['estimated_interval']:<10}")
#     else:
#         print("No recurrent charges detected.")

#     print("\n--- 3. Overspending Alerts (Latest Month) ---")
#     overspending = report['Overspending Alerts (Latest Month)']
#     if overspending:
#         for cat, data in overspending.items():
#             print(f"WARNING: {cat}: ${data['current']:.0f} (Avg: ${data['average']:.0f}) -> +{data['pct_over']:.1f}%")
#     else:
#         print("No significant overspending detected.")

#     print("\n--- 4. Savings Potential ---")
#     # Recoverable waste * 12 + current savings (annualized?)
#     # Let's keep it simple
#     waste = sum([item['current'] - item['average'] for item in overspending.values()])
#     print(f"Potential recoverable from overspending: ${waste:.2f}")

# if __name__ == "__main__":
#     main()
