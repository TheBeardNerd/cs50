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
        printf("Invalid Entry, use only one command line argument: %s\n", argv[0]);
        return 1;
    }
    else;
    {
        // saves command line argument to key string
        string key = argv[1];

        // initialize variables
        int k_tally = 0;
        int t_count = 0;
        int t_len;
        int k_len = strlen(key);

        for (k_tally = 0; k_tally < k_len; k_tally++)
        {
            if (!isalpha(key[k_tally]))
            {
                printf("Invalid Entry, all characters must be letters. %s\n", argv[0]);
                return 1;
            }
        }

        // prompts user for plain text
        string text = get_string("plaintext: ");

        // prints "ciphertext: " to prep for cypher
        printf("ciphertext: ");

        // iterates through each letter in string to print cypher text
        for (k_tally = 0, t_len = strlen(text); t_count < t_len; t_count++)
        {
            int k_value = toupper(key[k_tally % k_len]) - 'A';

            // checks for uppercase letters
            if (isalpha(text[t_count]) && isupper(text[t_count]))
            {
                printf("%c", (((text[t_count] - 'A' + k_value) % 26) + 'A'));
                k_tally++;
            }
            // checks for lowercase letters
            else if (isalpha(text[t_count]) && islower(text[t_count]))
            {
                printf("%c", (((text[t_count] - 'a' + k_value) % 26) + 'a'));
                k_tally++;
            }
            // prints whatever else is in the string
            else if (!isalpha(text[t_count]))
            {
                printf("%c", text[t_count]);
            }
        }
        // prints new line after cypher text
        printf("\n");
        return 0;
    }
}