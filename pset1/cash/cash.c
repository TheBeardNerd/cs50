#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // initialize variables
    int coins = 0;
    float change;

    // prompts user for how much change they are owed
    do
    {
        change = get_float("Change owed:\n");
    }
    while (change < 0);

    // takes floating point input and converts and
    // rounds it for more accurate counting
    change = change * 100;
    change = round(change);

    // loop to detirmine fewest amount of coins necessary for change
    while (change > 0)
    {
        if (change >= 25)
        {
            change = change - 25;
            coins = coins + 1;
        }

        else if (change >= 10)
        {
            change = change - 10;
            coins = coins + 1;
        }

        else if (change >= 5)
        {
            change = change - 5;
            coins = coins + 1;
        }

        else
        {
            change = change - 1;
            coins = coins + 1;
        }
    }
    // prints fewest coins output
    printf("Fewest coins possible: %i\n", coins);
}