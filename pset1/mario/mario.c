#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // initializes variables
    int height;
    int space;
    int hash;

    // prompts user for number of bricks between 0 and 23
    do
    {
        height = get_int("Welcome to Mario World: How many levels of bricks between 0 and 23?\n");
    }
    while (height <= -1 || height >= 24);

    // loop making new rows
    for (int new_row = 0; new_row < height; new_row++)
    {
        // loop for spaces
        for (space = (height - new_row) - 1; space > 0; space--)
        {
            printf(" ");
        }
        // prints first pyramid
        for (hash = 0; hash < new_row + 1; hash++)
        {
            printf("#");
        }
        // prints two space gap between pyramids
        for (space = 0; space + 2; space--)
        {
            printf(" ");
        }
        // prints second pyramid
        for (hash = 0; hash < (new_row + 1); hash++)
        {
            printf("#");
        }
        printf("\n");
    }
}