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

'''def plot_transactions(df):
    df.set_index('Date', inplace= True)

    income_df = df[df['Category'] == 'Income'].resample("D").sum().reindex(df.index,fill_value=0)
    expense_df = df[df['Category'] == 'Expense'].resample("D").sum().reindex(df.index,fill_value=0)
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df['Amount'], label='Income',color='g')
    plt.plot(expense_df.index, expense_df['Amount'], label='Expense', color='r')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income Expenses Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
'''

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
            #if input('Do you want to see a plot(Y/N): ').upper() == 'Y':
            #    plot_transactions(df)
        elif choice == '3':
            print('Exiting...')
            break
        else:
            print('Invalid Choice. Enter 1,2, or 3.')

if __name__ == '__main__':
    main()