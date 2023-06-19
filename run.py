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


print("_____------Welcome To Product Marketers------_____ \n")
print("Enter the name of the product you sell.")
print("Example Phones, courses, cars etc.\n")
product = input("Product:")
print(f"How much have you been ivesting to advertise {product}")
print("per week on Facebook, Youtube, Instagram and Tiktok?")
while True:
    budget = input("Budget: $")
    print("\n")
    if budget.isdigit():
        break
    else:
        print(f"The Budget must be an interger.")
# Here we assum that the budget is shared equally amon the social
# media platforms. We also assum that the cost per click is $2
investment_per_platform = float(budget)/4
clicks = int(investment_per_platform / 2)
print(f"Therefore, you have been investing ${investment_per_platform} weekly")
print(f"on each advertising platform. About {clicks} clicks.\n")

def get_average_sales():
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
        if (validate_sales_count(average_sales_values)):
            print("Thank you! Building a marketing strategy now...")
            print(f"Sale values provided for the platforms")
            print(f"facebook, youtube, Instagram and TikTok respectively")
            print(f"{average_sales_values}\n")
        average_sales_made = [int(value) for value in average_sales_values]
        return average_sales_made

def validate_sales_count(sales_data):
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
    diff = [clicks - int(value) for value in data]
    diff_btw_clicks_sales_sheet.append_row(diff)
    print(f"Difference between click and sales data is {diff}")
    print("Uploaded to the diff btw clicks and sales worksheet successfully.\n")
    return diff


def market_strategy(diff, clicks, investment):
    """
    Calculate how much should be invested on each social media platform.
    Calculations are based on the differences between clicks and sales to 
    know which platform is best for a particular product. Invest $5 in
    the worst performance case just to keep are advertising page running
    """
    print(f"Calculating a better strategy to invest ${budget}.")
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
    print(f"To make more {product} sales, Invest as instructed below")
    print("for Facebook, Youtube, Instagram and TikTok respectively")
    print(data)
    return data

def validate_strategy(strategy, sales):
    sum_tobe_invested = 0
    expected_total_sales = 0
    multiplier = []
    expected_sales_with_strategy = []
    for i in range(1, 5):
        sum_tobe_invested += strategy[i]
        
        if strategy[i] > investment_per_platform:
            change = strategy[i]/investment_per_platform
            multiplier.append(change)
            sales[i-1] = sales[i-1] * change
            expected_sales_with_strategy.append(sales[i-1])
             
        elif strategy[i] == investment_per_platform:
            change = 1
            multiplier.append(change)
            sales[i-1] = sales[i-1] * change
            expected_sales_with_strategy.append(sales[i-1])
            
        else:
            change = investment_per_platform / strategy[i]
            multiplier.append(change)
            sales[i-1] = sales[i-1] / change
            expected_sales_with_strategy.append(sales[i-1])
            
    print(f"New sum to be invested is ${sum_tobe_invested}\n")
    
    print(f"Expected sales: {expected_sales_with_strategy}")

    print(multiplier)
    
    for sales in expected_sales_with_strategy:
        expected_total_sales += sales
    return expected_total_sales    
    




average_sales = get_average_sales()
update_average_sales_worksheet(average_sales)
diff_btw_sales_clicks = update_diff_btw_clicks_and_sales(average_sales, clicks)
new_invest = market_strategy(diff_btw_sales_clicks, clicks, investment_per_platform )
investment_per_product = update_investment_strategy_worksheet(new_invest, product)
#new_investments = [int(invest) for invest in investment_per_product]
#print(f"To make more {product} sales, Invest as instructed below")
#print("for Facebook, Youtube, Instagram and TikTok respectively")
#print(investment_per_product)
total_expected_sales = validate_strategy(investment_per_product, average_sales)
print(f"Total expected sales {total_expected_sales}")