# MONTHLY EXPENSES
### Video demo: <https://youtu.be/6EVmLEZQEgU>
### Description:

My project is a web-based application using JavaScript, Python and SQL that allows the user to keep track of they're monthly expenses in a chosen month and year.


## LAYOUT

The file "layout.html" contains the basic layout of the pages that is a body with a navbar in the header, that shows different information
whether the user is logged in or not, and an empty main part.


## INDEX

The file "index.html" contains the home page of the web application, it's where the user is redirected when it logs in or when it clicks on "Monthly Expenses" whilst logged in.

This page contains a form with two select tags, one to select a month and the other to select a year, and one button to submit the form. Once the form is submited to "/" at "app.py"
 via POST.

The index() function will check if user selected both month and year, if not, it will return to index.html passing a errorMsg, the current year and expenses=None as parameter.
If both were selected then it goes on to get the data from "users.db".
    First it selects all from the expenses table where the user_id is the id of the user current logged in and the month and year is equal to the month and year selected in the form.
    Then it selects all from the user_history table where the user_id is the id of the user current logged in and the date is equal to f"month/year" where month and year were selected 
    in the form. 

After that, it checks if the user has any income or expense registered into that date on the databse.
    If not it will return to index.html passing a errorMsg, the current year and expenses=None as parameter.
    Else it will get the data from user_history and divide the expense amount into types of expenses.
Then it gets the % value of each expense_items compared to the total spent and pass it as a list to "index.html".

The POST return of the index() function renders the template of "index.html" and passes as parameters (expenses, year, selected_year, month, income, spending) that contains 
respectively (a list containing the % value of each expense_items compared to the total spent on the month, the current year, year selected from the user, month selected from 
the user, total income of the month, total spending of the month).


## REGISTER

The file "register.html" contains the register page of the web application.

It contains a form in wich the user should input an username, password and confirmation password.
Once the form is submitted to "/register" at "app.py" via POST the register() function will check if user filled all fields, if not it will return to "register.html" passing 
a errorMsg as parameter.
It will also check if the username isn't already taken, by checking the users table at "users.db", and if the password and confirmation match, if so then it generates a hash password and 
registers the username and hash at the users table, if not then return to "register.html" passing a errorMsg as parameter.

The POST return of the register() function redirects to "/login" wich gets "login.html".


## LOGIN

The file "login.html" contains the login page of the web application.

It contains a form in which the user should input an username and password.
Once the form is submitted to "/login" at "app.py" via POST the login() function will check if the username and password were submitted, if not it will return to "login.html" 
passing a errorMsg as parameter.

If both were submitted then it gets all information from users table were username is igual to the username typed. 
If didn't found any information in users table with that username or if the password was invalid the function will return to "login.html" passing a errorMsg as parameter.
If found username and password corrects then session["user_id"] receives the id from this user and the user logs in.

The POST return of the login() function redirects to "/" wich gets "index.html" .


## RESET

The file "reset.html" contains a page where the user can reset his account settings, deleting all history and expenses.

The page contains a form in which the user is asked if he wants to reset his account. If he clicks "NO" then he is redirected to "/",
if he clicks "YES" then the form is submitted to "/reset" at "app.py" via POST.

The reset() function will delete all information from the expenses and user_history tables where the user_id is igual to the id of the user who is currently logged in.
Then it redirects to "/".


## INCOME

The file "income.html" contains a page where the user can add an income.

It contains a form in which the user should select a month, an year, a type of income and input an amount of the income. The form is submitted to "/income" at "app.py" via POST 
when the user clicks the "Add income" button.

The add_income() function will check if the user filled all the fields, else it returns to "income.html" passing a errorMsg and the current year as parameters.
Then it checks if the amount is a valid number (float number higher then 0), else it returns to "income.html" passing a errorMsg and the current year as parameters.

If user filled all the fields and the information is valid, the function will then select all information from expenses table where user_id is the id of user currently 
logged in and the month and year are equal to the month and year submitted via form. If there's no information then it inserts this income amount to the database. Else it will get the 
current income amount and add to the amount the user inputted and update the information on the database.
After that it will insert this information into the user_history table.
Then it redirects to "/".


## SPENDING

The file "spending.html" contains a page where the user can add an expense.

It contains a form in which the user should select a month, an year, a type of expense and input the name of the item, the price the unity and the amount of items.
The form is submitted to "/spending" at "app.py" via POST when the user clicks the "Add expense" button.

The spending() function contains a list of expenses, that are shown when the user is selecting a type of expense.
The function will check if the user filled all fields. If not then it returns to "spending.html" passing a errorMsg, the current year and the expenses list as parameters.
Then it checks if the information given by the user is valid. If not then it returns to "spending.html" passing a errorMsg, the current year and the expenses list as parameters.

Else, the function will then select all information from expenses table where user_id is the id of the user currently logged in and the month and year are equal to the month and year submitted
via form. If there's no information then it inserts this spending amount to the database. Else it will get the current spending amount and add to the amount the user inputted and 
update the information on the database.
After that it will insert this information into the user_history table.
Then it redirects to "/".


## helpers.py

The file "helpers.py" contains two functions. 
The function login_required(f) decorate routes to check login and the function usd(value) formats a number value to USD.

