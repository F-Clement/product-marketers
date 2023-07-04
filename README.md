# Product Marketers

Live URL: [Product Marketers](https://product-marketers-65388db1c310.herokuapp.com/)

Product marketers is designed to improve investment strategies for social media marketing companies or individuals who frequently advertise products on social media platforms like Facebook, Youtube, Instagram and Tiktok. Users will be able to improve investment strategy for each product and understand that some products sell better on some platforms than others. In case a new user sells thesame product as an old user, the new user is able to get an investment strategy and start his/her marketing immediatly with the strategy. Thus starting above average and saving some money. A user is also able to delete a product-investment strategy. It is assumed that before using this application, the user usually divides his budget into four equal halves for the different platforms. We also assume that the cost per click here is $2. This application is designed in Python and runs through a terminal.

## Project Goals

### User Goals
- The user wants to improve social media sales of a product by better investing the budget he has and not just dividing the budget equally accross four social media platforms.
- The user also wants to be able to check investment strategies for already registered products and also able to delete some product investment strategies from a saved word sheet.

### Site Owner Goals
- The site owner through the application, wants to collect data from user then then analyse and provide that data with an investment strategy for social media marketing.
- The site owner also wants to provide new users with the ability to get existing investment strategies if they sell same products like old users.

## Design
Lucid Chart was used to design the flow of this program. It runs through a terminal so the display is thesame on every device.

## Existing Features
- Start Menu

Once the user runs the program an ordered menu will be displayed. This menu shows the various things that a user can do with this application. By selecting one of the and hitting enter the user will then get the required results.


## Testing
- In the table below we present a couple of actions, expected out comes and resutls.

<table>
<tr>
<th>Action</td>
<th>Expected Results</td>
<th>Actual Results</td>
</tr>
<tr>
<td>Hit enter without selecting a menu item or enter a menu item that is invalid and hit enter</td>
<td>User is notified that the input is invalid and given another chance to enter a menu item</td>
<td>Pass</td>
</tr>
<tr>
<td>Enter menu number 0 and hit enter key</td>
<td>A simple guide on how the application works is displayed</td>
<td>Pass</td>
</tr>
<tr>
<td>Enter menu number 1 and hit enter key </td>
<td>Application prompts user to enter a product name, budget, and previous average sales. Then calculates and displays investment strategy for that product.</td>
<td>Pass</td>
</tr>
<tr>
<td>User selects menu 1 and enters a product name that already exist.</td>
<td>The application finds the investment strategy for that product and displays to the user then ask if they want to delete.</td>
<td>Pass</td>
</tr>
<tr>
<td>Enter menu number 2 and hits enter.</td>
<td>Application prompts user to enter a product name, then finds the investment strategy from the investment strategy worksheet and displays it</td>
<td>Pass</td>
</tr>
<tr>
<td>User selects menu number 2 and enters a product that does not exist in the investment strategy worksheet</td>
<td>Application tells user that the product does not exist in works sheet the proposes to create a new investment strategy for the product</td>
<td>Pass</td>
</tr>
<tr>
<td>Enter menu number 3 and hit enter</td>
<td>Application prompts user to enter a product name, and then searches for that product for investment strategy worksheet, then displays the investment strategy before asking user to confirm delete.</td>
<td>Pass</td>
</tr>
<tr>
<td>User selects menu number 3 and enters a product that does not exist in investment strategy worksheet</td>
<td>Applications tell the user the product does not exist and proposes to create and investment strategy for the corresponding product</td>
<td>Pass</td>
</tr>
<tr>
<td>User hits enter without typing anything when application request for product name.</td>
<td>Application ask user to enter a valid product name which could be anything except for and empty data</td>
<td>Pass</td>
</tr>
<tr>
<td>User enters a string when prompt to enter budget</td>
<td>Application rejects invalid data and asks user to enter a number</td>
<td>Pass</td>
</tr>
<tr>
<td>User enters an invalid data for at least one of the social media platforms when asked to enter number of sales.</td>
<td>Application treats it as invalid data and askes user to reenter the number of sales for the four different platforms</td>
<td>Pass</td>
</tr>
</table>
