# TODO
def cal_quarters(money):
    quarters = 0

    while money >= 25:
        quarters = quarters + 1
        money = money - 25

    return quarters


def cal_dimes(money):
    dimes = 0
    while money >= 10:

        dimes = dimes + 1
        money = money - 10

    return dimes


def cal_nickels(money):
    nickels = 0
    while money >= 5:

        money = money - 5
        nickels = nickels + 1

    return nickels


def cal_pennies(money):
    pennies = 0
    while money >= 1:

        money = money - 1
        pennies = pennies + 1

    return pennies


def main():
    from cs50 import get_float

    while True:
        money = get_float("Change Owed: ")
        if money > 0:
            break

    money = int(money * 100)

    # calculating quarters and updating money
    quarters = cal_quarters(money)
    money = money - (quarters * 25)
    # calculating dimes
    dimes = cal_dimes(money)
    money = money - (dimes * 10)
    # calculating nickels
    nickels = cal_nickels(money)
    money = money - (nickels * 5)
    # calculating pennies
    pennies = cal_pennies(money)
    money = money - (pennies * 1)
    coins = quarters + dimes + nickels + pennies
    print(coins)


if __name__ == "__main__":
    main()