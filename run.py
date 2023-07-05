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
        print(Fore.YELLOW + "Hit Enter key to return to main Menu")
        key = input("Return to Menu? \n")
        if key == "":
            main()
            break
        else:
            print("Invalid input! \n")
            pass


def menu_select():
    """
    User selects a menu item by inputting a number that corresponds
    to what part of the application the user want to use.
    """
    menu_item = input(Fore.YELLOW + "Enter Menu Number: \n")
    if menu_item == "0":
        instructions()
    elif menu_item == "1" or menu_item == "2" or menu_item == "3":
        pass
    else:
        print(Fore.WHITE + "Please enter a valid menu item. \n")
        menu_select()
    return menu_item


def product_info(menu):
    """
    Checks product if it is already in worksheet.
    If yes it prints the investment ratio
    If no it proceeds to create a strategy.
    Also asks if you want to delete then follows the instrction.
    """
    strategies = SHEET.worksheet('investment_strategy')
    product_name = strategies.col_values(1)
    print(Fore.WHITE + "Enter the name of the product you have been selling.")
    if menu == "2" or menu == "3":
        print(Fore.GREEN + f"Example: \n{product_name}.\n")
    else:
        pass
    while True:
        prod = input(Fore.YELLOW + "Product Name:\n")
        if len(prod) != 0:
            break
        else:
            print(Fore.WHITE + "Please enter a product name.")
    if prod in product_name:
        row_no = product_name.index(prod) + 1
        investment_ratio = strategies.row_values(row_no)
        print(Fore.GREEN + f"The product {prod} is in the worksheet with,")
        print(Fore.GREEN + f"Investment ratio: {investment_ratio}")
        print("\n")
        if menu == "3":
            print(Fore.WHITE + "Hit enter to delete or input other key for menu")
            delete = input(Fore.RED + "Delete? \n")
            if delete == "":
                print(f"Do you really want to delete {prod}?")
                print("Input 'YES' to confirm, & any other thing to cancel")
                confirm_delete = input("Confirm delete?\n")
                if confirm_delete == "YES":
                    strategies.delete_rows(row_no)
                    print(f"{prod} has been deleted from investment sheet")
                    main()
                else:
                    print(f"{prod} has not been deleted. Investment still valid!")
                    main()
            else:
                main()
        else:
            goto_menu()        
    else:
        if menu == "1":
            pass
        elif menu == "2":
            print(Fore.RED + f"\n{prod} is not in worksheet")
            print(f"Do you want to create an investment strategy for {prod}?")
            print(f"Hit enter to create new strategy or input any key for menu")
            create = input("Add product to investment worksheet?\n")
            if create == "":
                pass
            else:
                main()
        else:
            print(f"You can't delete {prod}. It does not exist in worksheet.\n")
            goto_menu()
        print(Fore.WHITE + f"How much have you been ivesting to advertise {prod}")
        print(Fore.WHITE + "per week on Facebook, Youtube, Instagram and Tiktok?")
        while True:
            budget = input(Fore.YELLOW + "Budget: $\n")
            if budget.isdigit():
                break
            else:
                print(Fore.WHITE + "The Budget must be an interger.")
        p_investment = float(budget)/4
        clicks = int(p_investment / 2)
        return clicks, p_investment, budget, prod


def get_average_sales(clicks):
    """
    Get average number of sales made on each platform
    Sales can not be more than clicks.
    """
    while True:
        print(Fore.WHITE + f"What is the average number of sales you make")
        print(Fore.WHITE + f"on each of the following platforms every week?\n")
        print(f"* No: of sales must be less or equal No: of clicks({clicks})")
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
    Validate the values user inputs as average sales to make
    sure that they are integers and sales is less than clicks
    """
    try:
        [int(sale) for sale in sales_data]
        for sale in sales_data:
            if int(sale) > clicks:
                raise ValueError(
                    Fore.WHITE + f"Input '{sale}' for sales is not correct."
                    f"Number of sales can't be more than number of clicks. \n"
                )
    except ValueError as e:
        print(Fore.WHITE + f"Invalid data: {e}")
        print("Enter Integer values for sales made")
        return False
    return True


def update_average_sales_worksheet(sales_data):
    """
    Update the averages sales work sheet
    with the sales values the user provided
    """
    average_sales_sheet = SHEET.worksheet('average_sales')
    average_sales_sheet.append_row(sales_data)


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
    Calculations are based on the differences between clicks and sales
    to know which platform is best for the particular product. Invest $5 in
    the worst performance case just to keep the advertising page running
    """
    investment_ratio = []
    sum_of_ratio = 0
    s_investment = []
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
        s_investment.append((int(budget)/sum_of_ratio) * investment_ratio[i])
        calculated_strategy = [int(value) for value in s_investment]
    return calculated_strategy


def update_investment_strategy_worksheet(data, product):
    """
    Add particular product to the calculated investment sheet then
    upload the calculated values from market_strategy function
    """
    investment_strategy_sheet = SHEET.worksheet('investment_strategy')
    data.insert(0, product)
    investment_strategy_sheet.append_row(data)
    print(Fore.WHITE + f"To make more {product} sales, use strategy below.")
    print(Fore.WHITE + f"[{product}, Facebook, Youtube, Instagram, TikTok]")
    print(f"{data}\n")
    return data


def validate_strategy(strategy, sales, p_investment):
    """
    Verify that calculated investment strategy works better
    by calculating the expected sales and money invested
    """
    sum_tobe_invested = 0
    expected_sales_with_strategy = []
    expected_total_sales = 0
    for i in range(1, 5):
        sum_tobe_invested += strategy[i]
        if strategy[i] > p_investment:
            change = strategy[i]/p_investment
            sales[i-1] = sales[i-1] * change
            expected_sales_with_strategy.append(sales[i-1])
        elif strategy[i] == p_investment:
            change = 1
            sales[i-1] = sales[i-1] * change
            expected_sales_with_strategy.append(sales[i-1])
        else:
            change = p_investment / strategy[i]
            sales[i-1] = sales[i-1] / change
            expected_sales_with_strategy.append(sales[i-1])
    expected_sales = [int(sale) for sale in expected_sales_with_strategy]
    print(Fore.GREEN + f"New sum to be invested is ${sum_tobe_invested}")
    print(Fore.GREEN + f"Expected sales: {expected_sales}")
    for sales in expected_sales:
        expected_total_sales += sales
    print(Fore.GREEN + f"Expected total sales: {expected_total_sales}\n\n")
    goto_menu()


def instructions():
    print(Fore.WHITE + "===== A SIMPLE GUIDE ======\n")
    print("1 - What has been assumed")
    print("  * All users market on Youtube, Facebook, Instagram & Tiktok.")
    print("  * The cost per click (cpc) on the various platforms is $2. ")
    print("  * User used to divide budget equally among the platforms.")
    print("\n")
    print("2 - Number of sales can't exceed number of clicks on each media.\n")
    print("3 - Reading prompts carefully will help improve user experience.\n")
    goto_menu()


def main():
    """
    Use print statements to welcome user and present a menu to select
    a part of the application they want to use. Also include all other
    functions.
    """
    print("\n")
    print(Fore.BLUE + "_____----Welcome To Product Marketers----_____ \n")
    print(Fore.WHITE + "______________________________________________\n")
    print("Product marketers is an application that generates an investment")
    print("strategy for advertising a product on four popular social media")
    print("platforms namely Facebook, Youtube, Instagram and TikTok. It uses")
    print("previous experience to guide you on how to divide your budget")
    print("across these social media platforms.\n")
    print(f"Input a menu item number and hit Enter :)\n \n")
    print("0 - A simple guide\n")
    print(f"1 - Find investment strategy for a new product\n")
    print(f"2 - Check investment strategy for existing products\n")
    print(f"3 - Delete investment strategy for existing product\n")
    menu = menu_select()
    clicks, p_investment, budget, product = product_info(menu)
    average_sales = get_average_sales(clicks)
    update_average_sales_worksheet(average_sales)
    clicks_sales = update_diff_btw_clicks_and_sales(average_sales, clicks)
    new_invest = market_strategy(clicks_sales, clicks, p_investment, budget)
    investments = update_investment_strategy_worksheet(new_invest, product)
    validate_strategy(investments, average_sales, p_investment)


main()
