from random import *
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
# cur.execute('''CREATE TABLE card(
# id INTEGER,
# number TEXT,
# pin TEXT,
# balance INTEGER default 0); ''')
conn.commit()

class Card:
    account = {}

    def __init__(self):
        self.card_no = list(cur.execute("SELECT number FROM card"))
        self.pin = list(cur.execute("SELECT pin FROM card"))
        conn.commit()
        self.generate = []

    def creat_account(self):
        while True:
            x = '400000' + str(randrange(0, 999999999)).zfill(9)  # first 15 digit generated
            y = str(check_sum(x))  # last digit generated
            x = x + y  # full card no generated
            z = str(randrange(0, 9999)).zfill(4)
            if x in self.card_no and z in self.pin:
                pass
            else:
                self.card_no.append(x)
                self.pin.append(z)
                self.account = dict(zip(self.card_no, self.pin))
                cur.execute('INSERT INTO card (id,number,pin,balance) VALUES(?,?,?,?)', (len(self.card_no), x, z, 0))
                conn.commit()
                break
        return self.card_no[len(self.card_no) - 1], self.pin[len(self.pin) - 1]

    def login(self):
        print("Enter your card no:")
        n = input()   # card no.
        print('Enter your PIN:')
        m = input()        # pin no
        for row in cur.execute('SELECT number,pin,balance FROM card'):
            if n == row[0] and m == row[1]:
                print('\nYou have successfully logged in!\n')
                while True:                        # login menu
                    print('''1. Balance
2. Add income
3. Do transfer
4. Close account 
5. Logout
0. Exit''')
                    k = int(input())
                    if k == 1:
                        amount = balance(n)
                        print("Balance:",amount)
                    elif k == 2:
                        print("Enter income:")
                        money = int(input())
                        add_income(n, money)
                        print("Income was added!")
                    elif k == 3:
                        transfer(n)

                    elif k == 4:
                        del_acc(n)
                        return
                    elif k == 5:
                        print("\nYou have successfully logged out!")
                        return
                    else:
                        return 0
        else:
            print("\nWrong card number or PIN!\n")


def check_sum(acc_15):    # luhan algorithm to check no is correct or not
    add, digit, count = 0, 0, 1
    for i in acc_15:
        if count % 2 != 0:
            if int(i) * 2 > 9:
                add += int(i) * 2 - 9
            else:
                add += int(i) * 2
        else:
            add += int(i)
        count += 1

    for j in range(10):
        if (add + j) % 10 == 0:
            digit = j
            break
    return digit


def balance(n):
    balance = list(cur.execute(f"SELECT balance FROM card WHERE number = {n}"))[0][0]
    return balance


def add_income(n, money):
    money += int(list(cur.execute(f"SELECT balance FROM card WHERE number = {n}"))[0][0])
    cur.execute(f"UPDATE card SET balance = {money} WHERE number = {n}")
    conn.commit()


def transfer(n):
    print('Enter account no:')
    acc = input()
    print('Enter money')
    digit = check_sum(acc[:15])
    if digit != int(acc[-1]):
        print("Probably you made a mistake in the card number. Please try again!")
    elif not is_exist(acc):
        print("Such a card does not exist.")

    elif acc == n:
        print("You can't transfer money to the same account!")

    else:
        print('Enter money')
        money = int(input())
        if money > balance(n):
            print("Not enough money!")
        else:
            add_income(acc, money)
            rem_income(n, money)
            print("transfer has done successfully!")


def del_acc(n):
    cur.execute(f"DELETE FROM card WHERE number = {n}")
    conn.commit()


def rem_income(n, money):
    amount = balance(n) - money
    cur.execute(f"UPDATE card SET balance = {amount} WHERE number = {n}")
    conn.commit()


def is_exist(acc):
    for row in list(cur.execute("SELECT number FROM card")):
        if row[0] == acc:
            return True
            break
    else:
        return False


new_card = Card()
conn.commit()
while True:
    print('''1. Create account
2. Login in account
0. Exit''')
    n = int(input())
    print()
# creating account
    if n == 1:
        a, b = new_card.creat_account()
        print('Your card has been created')
        print(f"Your card no is:\n{a}\nYour card PIN: \n{b}")
        continue
# logging in account
    elif n == 2:
        n = new_card.login()
# exit
    if n == 0:
        print('bye')
        break


conn.close()