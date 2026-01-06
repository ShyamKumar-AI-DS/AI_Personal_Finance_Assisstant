import pandas as pd
import os

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False


class Categorizer:
    def __init__(self, df):
        """
        Initialize with a pandas DataFrame provided by DataLoader.
        Expects columns like 'category', 'amount', 'type'.
        """
        self.df = df
        self._ensure_columns()

    def _ensure_columns(self):
        """
        Simple validation to check effectively required columns exist.
        """
        required_cols = ['category', 'amount', 'type']
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"DataFrame missing required column: {col}")

    def categorize_data(self):
        """
        Separates data into Income and Expense DataFrames.
        Returns:
            income_df (pd.DataFrame): Rows where Type is 'Income'
            expense_df (pd.DataFrame): Rows where Type is 'Expense'
        """
        income_df = self.df[self.df['type'].str.title() == 'Income'].copy()
        expense_df = self.df[self.df['type'].str.title() == 'Expense'].copy()
        return income_df, expense_df

    def get_summary(self):
        """
        Generates a summary dictionary of financial health.
        """
        income_df, expense_df = self.categorize_data()
        
        total_income = income_df['amount'].sum()
        total_expense = expense_df['amount'].sum()
        net_savings = total_income - total_expense
        
        # Group by category
        income_by_category = income_df.groupby('category')['amount'].sum().to_dict()
        expense_by_category = expense_df.groupby('category')['amount'].sum().to_dict()
        
        summary = {
            "Total Income": total_income,
            "Total Expense": total_expense,
            "Net Savings": net_savings,
            "Income Breakdown": income_by_category,
            "Expense Breakdown": expense_by_category
        }
        return summary

    def visualize_expenses(self, output_path=None):
        """
        Creates a pie chart of expenses by category.
        If output_path is provided, saves the image there.
        """
        if not VISUALIZATION_AVAILABLE:
            print("Visualization libraries (matplotlib, seaborn) not installed. Skipping expense visualization.")
            return

        _, expense_df = self.categorize_data()
        if expense_df.empty:
            print("No expenses to visualize.")
            return

        expense_summary = expense_df.groupby('category')['amount'].sum()
        
        plt.figure(figsize=(10, 6))
        # Using seaborn color palette for better aesthetics
        colors = sns.color_palette('pastel')[0:len(expense_summary)]
        
        plt.pie(expense_summary, labels=expense_summary.index, autopct='%1.1f%%', startangle=140, colors=colors)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Expense Distribution by Category')
        
        if output_path:
            plt.savefig(output_path)
            print(f"Expense chart saved to {output_path}")
            plt.close()
        else:
            plt.show()

    def visualize_income(self, output_path=None):
        """
        Creates a bar chart of income by category.
        """
        if not VISUALIZATION_AVAILABLE:
            print("Visualization libraries (matplotlib, seaborn) not installed. Skipping income visualization.")
            return

        income_df, _ = self.categorize_data()
        if income_df.empty:
            print("No income to visualize.")
            return

        income_summary = income_df.groupby('category')['amount'].sum()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=income_summary.index, y=income_summary.values, hue=income_summary.index, palette='viridis', legend=False)
        plt.title('Income Sources by Category')
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.xticks(rotation=45)
        
        if output_path:
            plt.tight_layout()
            plt.savefig(output_path)
            print(f"Income chart saved to {output_path}")
            plt.close()
        else:
            plt.show()
