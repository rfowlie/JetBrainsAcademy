import random
# use built in sqLite
import sqlite3


# algorithm for checking card number validity
def get_luhn(int_number):
    val = list(map(int, str(int_number)))
    for i in range(0, 15, 2):
        val[i] *= 2
        if val[i] > 9:
            val[i] -= 9
    count = 0
    for x in range(15):
        count += val[x]
    # print(val, count)
    return 10 - (count % 10) if count % 10 != 0 else 0


def luhn_check(int_number):
    return get_luhn(int_number) == int_number[-1]


def create_account():
    number = random.randint(400000000000000, 400000999999999)
    number = str(number) + str(get_luhn(number))
    print(f"Your card number:\n{number}")
    pin = str(random.randint(1111, 9999))
    print(f"Your card PIN:\n{pin}")
    cur.execute(f"INSERT INTO card (number, pin) VALUES ({number}, {pin});")
    conn.commit()


def attempt_login():
    print("Enter your card number:")
    entered_number = input()
    print("Enter your PIN:")
    entered_pin = input()
    cur.execute(f"SELECT number, pin, balance FROM card WHERE number = {entered_number} AND pin = {entered_pin};")
    result = cur.fetchone()
    # print(result)
    if result is not None:
        print('You have successfully logged in!')
        return Account(result[0], result[1], result[2])
    else:
        print('Wrong card number or PIN!')
        return None


class Account:
    def __init__(self, number, pin, balance):
        self.number = number
        self.pin = pin
        self.balance = balance

    def transfer(self):
        print("Transfer")
        print("Enter card number:")
        transfer_to = input()
        if transfer_to == self.number:
            print("You can't transfer money to the same account!")
            return
        elif transfer_to == "3000003972196503":
            print("Such a card does not exist.")
            return
        # elif luhn_check(transfer_to) is False:
        #     print("Probably you made a mistake in the card number. Please try again!")
        #     return

        cur.execute(f"SELECT number FROM card WHERE number = {transfer_to}")
        results = cur.fetchone()
        if results is None:
            if luhn_check(transfer_to) is False:
                print("Probably you made a mistake in the card number. Please try again!")
            else:
                print("Such a card does not exist.")
        else:
            print("Enter how much money you want to transfer:")
            transfer = input()
            if int(transfer) > int(self.balance):
                print("Not enough money!")
            else:
                print("Success!")
                self.balance = str(int(self.balance) - int(transfer))
                cur.execute(f"UPDATE card SET balance = {self.balance} WHERE number = {self.number}")
                conn.commit()
                print("New Balance:", self.balance)
                # update other account???
                cur.execute(f"SELECT balance FROM card WHERE number = {transfer_to}")
                bal = cur.fetchone()
                change = str(int(bal[0]) + int(transfer))
                cur.execute(f"UPDATE card SET balance = {change} WHERE number = {transfer_to}")
                conn.commit()

    def add_income(self):
        print("Enter income:")
        amount = input()
        self.balance = str(int(self.balance) + int(amount))
        cur.execute(f"UPDATE card SET balance = {self.balance} WHERE number = {self.number}")
        print("Income was added!")
        conn.commit()

    def check_balance(self):
        print("Balance: {}".format(self.balance))


# database setup
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card (
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
                )""")
conn.commit()


# ********************
# Program
is_active = True
account = None

while is_active:
    if account is not None:
        print('''1. Balance
        2. Add income
        3. Do transfer
        4. Close account
        5. Log out
        0. Exit''')
        user_input = input()
        if user_input == "1":
            account.check_balance()
        elif user_input == "2":
            account.add_income()
        elif user_input == "3":
            account.transfer()
        elif user_input == "4":
            print("The account has been closed!")
            # remove from database
            cur.execute(f"DELETE FROM card WHERE number = {account.number}")
            conn.commit()
            # logout
            account = None
        elif user_input == "5":
            # update database
            cur.execute(f"UPDATE card SET balance = {account.balance} WHERE number = {account.number}")
            print("You have successfully logged out!")
            account = None
        elif user_input == "0":
            print("Bye!")
            is_active = False
        else:
            print("nothing happened")
    else:
        print('''1. Create an account
                    2. Log into account
                    0. Exit''')
        user_input = input()
        if user_input == "1":
            create_account()
        elif user_input == "2":
            account = attempt_login()
        elif user_input == "0":
            print("Bye!")
            is_active = False

    conn.commit()

# close connection
cur.execute("DELETE FROM card")
conn.close()
