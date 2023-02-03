import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales data figures from user
    """
    while True:
        print("Please enter sales data from last market")
        print("Data should be six numbers, separated by commas")
        print("Example: 10, 20, 30, 40, 50, 60")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try block, converts all of the string valus into integers
    Raises ValueError if strings cannot be converted into integers
     or if there are not exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values must be entered, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid Data: {e}, please try again")
        return False

    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating Sales Data")
    salesworksheet = SHEET.worksheet('sales')
    salesworksheet.append_row(data)
    print("Sales worksheet updated")


def calculate_surplus_data(sales_row):
    """
    Compares sales with stock values and calculates surplus for each type.

    The surplus is defined as the sales figures subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extras made after stock runs out
    """
    print("Calculating surplus data: ")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)


def main():
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print("Welcome to Love Sandwiches Data Automation")
main()
