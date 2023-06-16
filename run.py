# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('product_marketers')


print("_____----------Welcome To Product Marketers----------_____ \n")
print("Enter the name of the product you sell. Example Phones, courses, cars etc.")
product = input("Produt:")
print(f"How much have you been ivesting to advertise {product} on Facebook, Youtube,Instagram and Tiktok?")
while True:
    budget = input("Budget: $")
    if budget.isdigit():
        break
    else:
        print(f"The Budget must be an interger.")
investment_per_platform = float(budget)/4
clicks = int(investment_per_platform / 2)
print(f"So you have been investing {investment_per_platform}€ on each advertising platform. Thus approximately {clicks} clicks per week.\n")

def get_average_sales():
    """
    Get average number of sales made on each platform
    """
    while True:
        print(f"What is the average number of sales you make on each of the platforms?")
        facebook = input("Facebook:")
        youtube = input("Youtube:")
        instagram = input("Instagram:")
        tiktok = input("TikTok:")
        average_sales = [facebook, youtube, instagram, tiktok]
        if(validate_sales_count(average_sales)):
        
            print("Thank you! Let's build a marketing strategy based on the data you have provided.")
            return average_sales

def validate_sales_count(sales_data):
    try:
        [int(sale) for sale in sales_data]
        for sale in sales_data:
            if int(sale) > clicks:
                raise ValueError(
                    f"The input '{sale}' for sales is not correct. Number of Sales cannot be more than Number of clicks. \n"
                )
    except ValueError as e:
        print(f"Invalid data: {e} Please enter Integer values for sales made")
        return False
    return True

def update_average_sales_worksheet(sales_data):
    """
    Update the averages sales work sheet with the sales values the user provided
    """
    print(f"Adding sales values you provided to average sales work sheet......")
    average_sales_sheet = SHEET.worksheet('average_sales')
    average_sales_sheet.append_row(sales_data)
    print(f"Average sales values uploaded successfully to average sales worksheet.")

def update_diff_btw_clicks_and_sales(data, click):
    """
    Update our diff_btw_clics_sales worksheet
    Data to update comes from subtracting number of sales from number of clicks for each platform
    """
    print(f"We calculate the difference between click and sales and add to diff_btw_clicks_sales worksheet")
    diff_btw_clicks_sales_sheet = SHEET.worksheet('diff_btw_clicks_and_sales')
    diff = [clicks - int(value) for value in data]
    diff_btw_clicks_sales_sheet.append_row(diff)
    print(f"This Data {diff} was uploaded successfully\n")

sales = get_average_sales()
average_sales = [int(sale) for sale in sales]
print(f"Sale values provided for the platforms facebook, youtube, Instagram and TikTok respectively\n{average_sales}\n")
update_average_sales_worksheet(average_sales)
update_diff_btw_clicks_and_sales(average_sales, clicks)