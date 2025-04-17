import pandas as pd
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description

class CSV:
    dateFormat = "%d-%m-%Y"
    csv_file = "FinanceData.csv"
    Columns=["Date","Amount","Category","Description"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.Columns)
            df.to_csv(cls.csv_file, index=False)
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        with open(cls.csv_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.Columns)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.csv_file)
        df['Date'] = pd.to_datetime(df["Date"], format=CSV.dateFormat)
        start_date = datetime.strptime(start_date,CSV.dateFormat)
        end_date = datetime.strptime(end_date,CSV.dateFormat)
        
        mask = (df['Date'] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(f'Transactions from {start_date.strftime(CSV.dateFormat)} to {end_date.strftime(CSV.dateFormat)}')
            print(filtered_df.to_string(index=False, formatters={'Date':lambda x: x.strftime(CSV.dateFormat)}))

        total_income = filtered_df[filtered_df['Category']=='Income']['Amount'].sum()
        total_expense = filtered_df[filtered_df['Category']=='Expense']['Amount'].sum()
        net_income = total_income - total_expense
        print('\nSummary:')
        print(f'Total Income: ${total_income:.2f}')
        print(f'Total Expense: ${total_expense:.2f}')
        if net_income < 0:
            print(f'Net Loss: ${net_income:.2f}')
        else:
            print(f'Net Income: ${net_income:.2f}')
        
        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of transaction or press enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    plot_df = df.copy()
    
    plot_df['Date'] = pd.to_datetime(plot_df['Date'])
    
    plot_df.set_index('Date', inplace=True)
    
    income_df = plot_df[plot_df['Category'] == 'Income']
    expense_df = plot_df[plot_df['Category'] == 'Expense']
    
    income_by_date = income_df.groupby(income_df.index.date)['Amount'].sum()
    expense_by_date = expense_df.groupby(expense_df.index.date)['Amount'].sum()
    
    income_by_date.index = pd.to_datetime(income_by_date.index)
    expense_by_date.index = pd.to_datetime(expense_by_date.index)
    
    income_by_date = income_by_date.sort_index()
    expense_by_date = expense_by_date.sort_index()
    
    plt.figure(figsize=(12, 6))
    plt.plot(income_by_date.index, income_by_date.values, 'g-', marker='o', label='Income')
    plt.plot(expense_by_date.index, expense_by_date.values, 'r-', marker='o', label='Expense')
    
    plt.xlabel('Date')
    plt.ylabel('Amount ($)')
    plt.title('Income vs Expenses Over Time')
    plt.legend()
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()

def main():
    while True:
        print('\n1. Add new Transaction\n2. View transactions and summary within a date range\n3. Exit')
        choice = input('Enter your choice (1-3): ')

        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date('Enter the start date (dd-mm-yyyy): ')
            end_date =  get_date('Enter the end date (dd-mm-yyyy): ')
            df = CSV.get_transactions(start_date, end_date)
            if input('Do you want to see a plot(Y/N): ').upper() == 'Y':
                print("Preparing to display plot...")
                plot_transactions(df)
        elif choice == '3':
            print('Exiting...')
            break
        else:
            print('Invalid Choice. Enter 1,2, or 3.')

if __name__ == '__main__':
    main()

