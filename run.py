import gspread
import openpyxl
import colorama
from colorama import Fore
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

def goto_menu():
    """
    Get user to menu after finishing a task to avoid function
    continously running even without user requesting
    """
    while True:
        print(Fore.WHITE + "Enter '1' to return to main Menu")
        key = input("Return to Menu? \n")
        if key == "1":
            main()
            break
        else:
            pass

def menu_select():
    """
    User selects a menu item by inputting a number that corresponds
    to what part of the application the user want to use.
    """
    menu_item = input(Fore.YELLOW + "Enter Menu Number: \n")
    if menu_item == "1":
        pass
    elif menu_item == "2":
        product_info()
    elif menu_item == "3":
        product_info()
    else:
        print(Fore.WHITE + "Please enter a valid menu item. \n")
        menu_select()


def product_info():
    """
    Checks product if it is already in worksheet.
    If yes it prints the investment ratio
    If no it proceeds to create a strategy.
    Also asks if you want to delete then follows the instrction.
    """
    print(Fore.WHITE + "Enter the name of the product you have been selling.")
    print(Fore.WHITE + "Example Phones, courses, cars, jewelries etc.\n")
    while True:
        prod = input(Fore.YELLOW + "Product Name:\n")
        if len(prod) != 0:
            break
        else:
            print(Fore.WHITE + "Please enter a product name.")
    strategies = SHEET.worksheet('investment_strategy')
    product_name = strategies.col_values(1)
    if prod in product_name:
        
        row_no = product_name.index(prod) + 1
        investment_ratio = strategies.row_values(row_no )
        print(Fore.GREEN + f"The product {prod} is in the worksheet with,")
        print(Fore.GREEN + f"Investment ratio: {investment_ratio}")
        print("\n")
        print(Fore.WHITE + "Enter '1' to delete and any other key to go back to menu")
        delete = input(Fore.RED + "Delete? \n")
        if delete == '1':
            strategies.delete_rows(row_no)
            print(f"{prod} has been deleted from investment sheet")
        else:
            main()
    else:
        print(Fore.WHITE + f"'{prod}' is not in worksheet.")
        print(Fore.WHITE + f"Let's create a strategy for {prod}\n")

    print(Fore.WHITE + f"How much have you been ivesting to advertise {prod}")
    print(Fore.WHITE + "per week on Facebook, Youtube, Instagram and Tiktok?")
    while True:
        budget = input(Fore.YELLOW + "Budget: $\n")
        if budget.isdigit():
            break
        else:
            print(Fore.WHITE + "The Budget must be an interger.")
    platform_investment = float(budget)/4
    clicks = int(platform_investment/ 2)
    return clicks, platform_investment, budget, product      


def get_average_sales(clicks):
    """
    Get average number of sales made on each platform 
    Sales can not be more than clicks.
    """
    while True:
        print(Fore.WHITE + f"What is the average number of sales you make")
        print(Fore.WHITE + f"on each of the following platforms every week?\n")
        facebook = input(Fore.YELLOW + "Facebook:\n")
        youtube = input(Fore.YELLOW + "Youtube:\n")
        instagram = input(Fore.YELLOW + "Instagram:\n")
        tiktok = input(Fore.YELLOW + "TikTok:\n")
        print("\n")
        average_sales_values = [facebook, youtube, instagram, tiktok]
        if (validate_sales_count(average_sales_values, clicks)):
            break
    average_sales_made = [int(value) for value in average_sales_values]
    return average_sales_made

def validate_sales_count(sales_data, clicks):
    """
    Validate the values use inputs as average sales to make sure 
    that they are integers and sales is less than clicks
    """
    try:
        [int(sale) for sale in sales_data]
        for sale in sales_data:
            if int(sale) > clicks:
                raise ValueError(
                    Fore.WHITE + f"The input '{sale}' for sales is not correct."
                    f"Number of Sales cannot be more than Number of clicks. \n"
                )
    except ValueError as e:
        print(Fore.WHITE + f"Invalid data: {e} Please enter Integer values for sales made")
        return False
    return True

def update_average_sales_worksheet(sales_data):
    """
    Update the averages sales work sheet
    with the sales values the user provided
    """
    average_sales_sheet = SHEET.worksheet('average_sales')
    average_sales_sheet.append_row(sales_data)
    print(Fore.WHITE + f"Average sales values uploaded to worksheet successfully.\n")

def update_diff_btw_clicks_and_sales(data, click):
    """
    Calculate the difference between sales and clicks for each platform
    and update our diff_btw_clics_sales worksheet
    """
    diff_btw_clicks_sales_sheet = SHEET.worksheet('diff_btw_clicks_and_sales')
    diff = [click - int(value) for value in data]
    diff_btw_clicks_sales_sheet.append_row(diff)
    return diff

def market_strategy(diff, clicks, investment, budget):
    """
    Calculate how much should be invested on each social media platform.
    Calculations are based on the differences between clicks and sales to 
    know which platform is best for a particular product. Invest $5 in
    the worst performance case just to keep are advertising page running
    """
    investment_ratio = []
    sum_of_ratio = 0
    strategised_investment = []
    for value in diff:
        if value < clicks * 0.2:
            sum_to_invest = int(investment * 2)
            investment_ratio.append(sum_to_invest)
        elif value < clicks * 0.5:
            sum_to_invest = int(investment * 1.5)
            investment_ratio.append(sum_to_invest)
        elif value < clicks * 0.7:
            sum_to_invest = int(investment/2)
            investment_ratio.append(sum_to_invest)
        elif value < clicks * 0.9:
            sum_to_invest = int(investment/3)
            investment_ratio.append(sum_to_invest)
        else:
            sum_to_invest = 5
            investment_ratio.append(sum_to_invest)
    for amount in investment_ratio:
        sum_of_ratio += int(amount)
    for i in range(0, 4):
        strategised_investment.append((int(budget)/sum_of_ratio) * investment_ratio[i])
        calculated_strategy = [int(value) for value in strategised_investment]
    return calculated_strategy

def update_investment_strategy_worksheet(data, product):
    """
    Add particular product to the calculated investment sheet then
    upload the calculated values from market_strategy function
    """
    investment_strategy_sheet = SHEET.worksheet('investment_strategy')
    data.insert(0, product)
    investment_strategy_sheet.append_row(data)
    print(Fore.WHITE + f"To make more {product} sales, Invest as instructed below.")
    print(Fore.WHITE + f"[{product}, Facebook, Youtube, Instagram, TikTok] : {data}\n")
    return data

def validate_strategy(strategy, sales, platform_investment):
    """
    Verify that calculated investment strategy works better
    by calculating the expected sales and money invested
    """
    sum_tobe_invested = 0
    expected_sales_with_strategy = []
    expected_total_sales = 0
    for i in range(1, 5):
        sum_tobe_invested += strategy[i]
        if strategy[i] > platform_investment:
            change = strategy[i]/platform_investment
            sales[i-1] = sales[i-1] * change
            expected_sales_with_strategy.append(sales[i-1])
        elif strategy[i] == platform_investment:
            change = 1
            sales[i-1] = sales[i-1] * change
            expected_sales_with_strategy.append(sales[i-1])
        else:
            change = platform_investment / strategy[i]
            sales[i-1] = sales[i-1] / change
            expected_sales_with_strategy.append(sales[i-1])
    expected_sales = [int(sale) for sale in expected_sales_with_strategy ]        
    print(Fore.GREEN + f"New sum to be invested is ${sum_tobe_invested}")
    print(Fore.GREEN + f"Expected sales: {expected_sales}")
    for sales in expected_sales:
        expected_total_sales += sales
    print(Fore.GREEN + f"Expected total sales: {expected_total_sales}\n\n")
    goto_menu()  

def main():
    """
    Use print statements to welcome user and present a menu to select
    a part of the application they want to use. Also include all other 
    functions.
    """
    print("\n")
    print(Fore.BLUE + "_____------Welcome To Product Marketers------_____ \n")
    print(Fore.WHITE +  f"Product marketers is an application that generates investment")
    print(f"strategies for advertising a product on four social media")
    print(f"platforms namely Facebook, Youtube, Instagram and TikTok\n")
    print(f"What Do You Want To Do? (Enter menu item number and hit Enter)\n \n")
    print(f"1 - Find investment strategy for a new product\n")
    print(f"2 - Check investment strategy for existing products\n")
    print(f"3 - Delete investment strategy for existing product\n")
    

    menu_select()
    clicks, platform_investment, budget, product = product_info()
    average_sales = get_average_sales(clicks)
    update_average_sales_worksheet(average_sales)
    diff_btw_sales_clicks = update_diff_btw_clicks_and_sales(average_sales, clicks)
    new_invest = market_strategy(diff_btw_sales_clicks, clicks, platform_investment, budget )
    investment_per_product = update_investment_strategy_worksheet(new_invest, product)
    validate_strategy(investment_per_product, average_sales, platform_investment)
main()

