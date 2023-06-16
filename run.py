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

print(f"Great! How much have you been ivesting to advertise {product} on Facebook, Youtube,Instagram and Tiktok?")
budget = input("Budget: $")

investment_per_platform = float(budget)/4
clicks = int(investment_per_platform / 2)
print(f"So you have been investing {investment_per_platform}€ on each advertising platform. Thus approximately {clicks} clicks per week.\n")

def get_average_sales():
    """
    Get number of sales made on each platform
    """
    print(f"What is the average number of sales you make on each of the platforms?")
    facebook = input("Facebook:")
    youtube = input("Youtube:")
    instagram = input("Instagram:")
    tiktok = input("TikTok:")
    average_sales = [facebook, youtube, instagram, tiktok]
    
    validate_sales_count(average_sales)

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

get_average_sales()
