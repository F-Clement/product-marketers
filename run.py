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

def introduction():
    """
    Welcome to the program and presents a menu for user to select
    action the want to take
    """
    while True:
        print("_____------Welcome To Product Marketers------_____ \n")

        print(f"Product marketers proveds an investment strategy for")
        print(f"advertising a product on four social media platforms")
        print(f"namely Facebook, Youtube, Instagram and TikTok\n")

        print(f"What Do You Want To Do?\n \n")

        print(f"1 - Find investment strategy for a new product\n")
        print(f"2 - Check investment strategy for existing products\n")

        print(f"Enter '1' to get investment strategy new products and 2 for old products\n")

        menu_item = input("Enter Menu Number: ")


        if menu_item == "1":
            pass
            break
        elif menu_item == "2":
            check_existing_product_strategy()
            break
        else:
            print("Please enter a valid menu item")
        return True    


def basic_info():
    while True:
        product = input("Product:")
        print("\n")
        if len(product) != 0:
            break
        else:
            print("Please enter a product name.")
    print(f"How much have you been ivesting to advertise {product}")
    print("per week on Facebook, Youtube, Instagram and Tiktok?")
    while True:
        budget = input("Budget: $")
        print("\n")
        if budget.isdigit():
            break
        else:
            print(f"The Budget must be an interger.")
    # Here we assum that the budget is shared equally among the social
    # media platforms. We also assum that the cost per click is $2
    platform_investment = float(budget)/4
    clicks = int(platform_investment/ 2)
    print(f"Therefore, you have been investing ${platform_investment} weekly")
    print(f"on each advertising platform. About {clicks} clicks.\n")
    return clicks, platform_investment, budget, product

def get_average_sales(clicks):
    """
    Get average number of sales made on each platform 
    """
    while True:
        print(f"What is the average number of sales you make")
        print(f"on each of the following platforms every week?\n")
        facebook = input("Facebook:")
        youtube = input("Youtube:")
        instagram = input("Instagram:")
        tiktok = input("TikTok:")
        print("\n")
        average_sales_values = [facebook, youtube, instagram, tiktok]
        if (validate_sales_count(average_sales_values, clicks)):
            print("Thank you! Building a marketing strategy now...")
            print(f"Sale values provided for the platforms")
            print(f"facebook, youtube, Instagram and TikTok respectively")
            print(f"{average_sales_values}\n")
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
                    f"The input '{sale}' for sales is not correct."
                    f"Number of Sales cannot be more than Number of clicks. \n"
                )
    except ValueError as e:
        print(f"Invalid data: {e} Please enter Integer values for sales made")
        return False
    return True

def update_average_sales_worksheet(sales_data):
    """
    Update the averages sales work sheet
    with the sales values the user provided
    """
    print(f"Adding sales values you provided to average sales work sheet..")
    average_sales_sheet = SHEET.worksheet('average_sales')
    average_sales_sheet.append_row(sales_data)
    print(f"Average sales values uploaded to worksheet successfully.\n")

def update_diff_btw_clicks_and_sales(data, click):
    """
    Calculate the difference between sales and clicks for each platform
    and update our diff_btw_clics_sales worksheet
    """
    print(f"We calculate the difference between clicks")
    print("and sales and add to diff_btw_clicks_sales worksheet")
    diff_btw_clicks_sales_sheet = SHEET.worksheet('diff_btw_clicks_and_sales')
    diff = [click - int(value) for value in data]
    diff_btw_clicks_sales_sheet.append_row(diff)
    print(f"Difference between click and sales data is {diff}")
    print("Uploaded to the diff btw clicks and sales worksheet successfully.\n")
    return diff


def market_strategy(diff, clicks, investment, budget):
    """
    Calculate how much should be invested on each social media platform.
    Calculations are based on the differences between clicks and sales to 
    know which platform is best for a particular product. Invest $5 in
    the worst performance case just to keep are advertising page running
    """
    print(f"Calculating a better strategy to invest .")
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
    print(f"To make more {product} sales, Invest as instructed below.\n")
    print(f"[{product}, Facebook, Youtube, Instagram, TikTok] : {data}")
    return data

def validate_strategy(strategy, sales, platform_investment):
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
            
    print(f"New sum to be invested is ${sum_tobe_invested}")
    print(f"Expected sales: {expected_sales}")

    for sales in expected_sales:
        expected_total_sales += sales
    print(f"Expected total sales: {expected_total_sales}")
    return expected_total_sales  

def check_existing_product_strategy():
    print("Enter product name")
    prod = input("Product Name: ")
    strategies = SHEET.worksheet('investment_strategy')
    product_name = strategies.col_values(1)
    if prod in product_name:
        row_no = product_name.index(prod) + 1
        investment_ratio = strategies.row_values(row_no )
        print(investment_ratio)
    else:
        print(f"Strategy for {prod} not found")
    


def main():
    introduction()
    print("Enter the name of the product you have been selling.")
    print("Example Phones, courses, cars, jewelries etc.\n")
    clicks, platform_investment, budget, product = basic_info()
    average_sales = get_average_sales(clicks)
    update_average_sales_worksheet(average_sales)
    diff_btw_sales_clicks = update_diff_btw_clicks_and_sales(average_sales, clicks)
    new_invest = market_strategy(diff_btw_sales_clicks, clicks, platform_investment, budget )
    investment_per_product = update_investment_strategy_worksheet(new_invest, product)
    validate_strategy(investment_per_product, average_sales, platform_investment)
    

main()
