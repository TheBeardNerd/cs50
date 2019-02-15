def cash():

    while True:
        try:
            # gets change owed to user and checks it for errors
            change = float(input("Change owed: "))
            # checks if input is greater than 0.0
            if change < 0.0:
                print("Please enter change owed.\n")
                continue
        # checks if input is a number
        except ValueError:
            print("I'm not sure what you mean...\n")
            continue
        else:
            break

    # takes floating point input and converts and
    # rounds it for more accurate counting
    change = change * 100
    change = int(round(change))

    # initializes number of coins to return to user
    coins = 0

    # checks for quarters
    while change >= 25:
        change = change - 25
        coins += 1

    # checks for dimes
    while change >= 10:
        change = change - 10
        coins += 1

    # checks for nickels
    while change >= 5:
        change = change - 5
        coins += 1

    # checks for pennies
    while change >= 1:
        change = change - 1
        coins += 1

    print("Fewest coins possible:", coins)


if __name__ == "__main__":
    cash()