# Skybank

#### Video Demo: https://youtu.be/1wmbBZgg91Q

#### Description:

Skybank is a web application which (aka) represents a virtual bank. You can open an account in Skybank with a personal debit card attached to it. You can choose currency of an account, payment system of your card (Visa, Mastercard) and intial deposit. You must provide PIN of your card (possible to change later) and login in the system as well.

Once applied for openning of an account, you recieve "all" the benefits of a real bank: you can transfer some money to other **_valid_** (thanks to credit assignment) AMEX/MASTERCARD/VISA card, top up mobile phone credit and of course replenish your balance with different type of ways (ATM, another card, credit etc.).

The main features of the app are on it`s main page. You can see your card in a way it would look like in real world: the name of the bank, the currency of an account, number of the card (valid and unique for each user), an expiration date (5 years from the month an account was opened), name of card's holder, and type of payment system (svg image). It's also possible to see all of your transactions in transaction section below.

And last but not the least feature is possibility to set monthly payments limit (1000 in the currency of an acoount). It's always on sight, so it`s very handy to track your expenditures. You can't spend more during current month than specified there.

Stack of technologies used:

- HTML
- CSS
- Bootstrap
- JavaScript
- Python
- SQLite
- Flask

## Brief structure of the app and main features:

### Open account

Registration form

1. Name;
2. Last name;
3. Payment system (Visa/Mastercard);
4. Currency of an account (USD, EUR, GBP, UAH, RUB);
5. Initial deposit (min 1000);
6. Login
7. PIN
8. Confirm PIN
9. Agree with terms and conditions

### Sign in

Login form

1. Login
2. PIN

### Main page

#### Card:

- bank`s name, holding
- currency
- number
- expiration date (in 5 years)
- holder`s name
- payment system

#### Monthly payments limit section

- indicator of funds left to spend
- modal window on click, possibility to change the limit

#### Transactions

- time
- source/address
- sum (highlighted in green if in or red if out)

### Top up

- Select source
- Sum

### Money transfer

- address (valid card number)
- sum

### Other payments

- Modal window: top up mobole phone credit

### My account

- Possibility to change PIN

### Log out

- Clear session,
- Redirect to logit

### P.S.

Stylization inspired by Monobank - the most digitilized and convenient bank in Ukraine (at least there)
(https://www.monobank.ua/)
