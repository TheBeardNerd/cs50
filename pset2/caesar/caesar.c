#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// initializes program with a command line argument
int main(int argc, string argv[])
{
    // checks that the argument is valid
    if (argc != 2)
    {
        printf("Invalid Entry, use only one non-negative integer: %s\n", argv[0]);
        return 1;
    }

    // executes program if argument is valid
    else
    {
        // initialize variables
        // converts string to integer
        int key = atoi(argv[1]);

        char letter;

        // prompts user for plain text
        string text = get_string("plaintext: ");

        printf("ciphertext: ");

        // iterates through each letter in string to print cypher text
        for (int count = 0, length = strlen(text); count < length; count++)
        {
            // checks for uppercase letters
            if (isalpha(text[count]) && isupper(text[count]))
            {
                letter = ((((text[count] + key) - 65) % 26) + 65);
                printf("%c", letter);
            }
            // checks for lowercase letters
            else if (isalpha(text[count]) && islower(text[count]))
            {
                letter = ((((text[count] + key) - 97) % 26) + 97);
                printf("%c", letter);
            }
            // prints whatever else is in the string
            else
            {
                printf("%c", text[count]);
            }
        }
        // prints new line after cypher text
        printf("\n");
        return 0;
    }
}