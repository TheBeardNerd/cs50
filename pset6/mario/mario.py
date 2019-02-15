def mario():

    while True:
        try:
            # gets input from user and checks it for errors
            height = int(input("Welcome to Mario World: How many levels of bricks between 0 and 23?\n"))
            # checks if input is between 0 and 23
            if height < 0 or height > 23:
                print("Please enter a number between 0 and 23\n")
                continue
        # checks if input is a number
        except ValueError:
            print("I'm not sure what you mean...\n")
            continue
        else:
            break

    # loop for new rows
    for new_row in range(height):

        # loop for spaces
        for space in range(height - new_row - 1):
            print(" ", end="")

        # prints left pyramid
        for octothorpe in range(new_row + 1):
            print("#", end="")

        # creates 2 space gap between pyramids
        print("  ", end="")

        # prints right pyramid
        for blocks in range(new_row + 1):
            print("#", end="")

        print()


if __name__ == "__main__":

    mario()
