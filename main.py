import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os
from datetime import datetime

# 1. Setup Folders
for folder in ['data', 'outputs', 'reports']:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 2. Generate Synthetic Data (For Simulation)
def generate_sample_data():
    data = {
        'Date': ['2026-05-01', '2026-05-02', '2026-05-03', '2026-05-04', '2026-05-05'],
        'Category': ['Food', 'Transport', 'Food', 'Education', 'Entertainment'],
        'Amount': [250, 100, 150, 2000, 500],
        'Method': ['bKash', 'Cash', 'Paytm', 'Bank Transfer', 'bKash'],
        'Note': ['Lunch', 'Rickshaw', 'Snacks', 'Course Fee', 'Movie']
    }
    df = pd.DataFrame(data)
    df.to_csv('data/expenses.csv', index=False)
    print("✅ Sample data generated in data/expenses.csv")

# 3. Data Analysis & Visualization
def run_analysis():
    df = pd.read_csv('data/expenses.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Analysis
    total_spend = df['Amount'].sum()
    category_total = df.groupby('Category')['Amount'].sum()
    method_total = df.groupby('Method')['Amount'].sum()

    print(f"\n--- Financial Summary ---")
    print(f"Total Spent: {total_spend}")
    print(f"Top Category: {category_total.idxmax()}")
    
    # Visualization: Category-wise Bar Chart
    plt.figure(figsize=(10,6))
    sns.barplot(x=category_total.index, y=category_total.values, palette='viridis')
    plt.title('Spending by Category')
    plt.ylabel('Amount')
    plt.savefig('outputs/category_bar.png')
    
    # Visualization: Payment Method Pie Chart
    plt.figure(figsize=(8,8))
    plt.pie(method_total.values, labels=method_total.index, autopct='%1.1f%%', startangle=140)
    plt.title('Spending by Payment Method')
    plt.savefig('outputs/method_pie.png')
    
    # Generate Report
    with open('reports/summary.txt', 'w') as f:
        f.write(f"Expense Report - {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"Total Spending: {total_spend}\n")
        f.write(f"Category Breakdown:\n{category_total.to_string()}")

    print("✅ Charts saved in outputs/ and report saved in reports/")

if __name__ == "__main__":
    generate_sample_data()
    run_analysis()