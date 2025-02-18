from datetime import datetime
categories = {'I':'Income','E':'Expense'}

def get_date(prompt, allow_default=False):
    dateStr = input(prompt)
    dateFormat = "%d-%m-%Y"
    if allow_default and not dateStr:
        return datetime.today().strftime(dateFormat)
    else:
        try:
            validDate = datetime.strptime(dateStr,dateFormat)
            return validDate.strftime(dateFormat)
        except ValueError:
            print("Invalid Date Format. Please enter in dd-mm-yyyy format.")
            return get_date(prompt, allow_default)
        
def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative, non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category('I' for Income or 'E' for Expense): ").upper()
    if category in categories:
        return categories[category]
    print("Invalid Category. Please enter 'I' for Income or 'E' for Expense")
    return get_category()

def get_description():
    return input("Enter a description(optional): ")