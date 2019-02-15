import sys


def caesar():

    # checks for correct argument
    while True:
        if len(sys.argv) != 2:
            print("Usage:", sys.argv[0], "integer")
            exit(1)
        else:
            break

    # converts user key from char input to integer
    key = int(sys.argv[1])

    # prompts user for plaintext to be cyphered
    text = input("plaintext: ")

    # prints 'ciphertext: ' in preparation for obscured text
    print("ciphertext: ", end="")

    # iterates through each letter in string to print cypher text
    for count in range(0, len(text)):
        # checks for alphabetic characters
        if text[count].isalpha():
            # prints uppercase characters
            if text[count].isupper():
                print("{}".format(chr(65 + (ord(text[count]) - 65 + key) % 26)), end="")
            # prints lowercase characters
            elif text[count].islower():
                print("{}".format(chr(97 + (ord(text[count]) - 97 + key) % 26)), end="")
        # prints whatever else is in the string
        else:
            print("{}".format(text[count]), end="")
    # prints new line after cypher text
    print("")
    return 0


if __name__ == "__main__":
    caesar()