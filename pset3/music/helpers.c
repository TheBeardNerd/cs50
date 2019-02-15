// Helper functions for music
#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    // TODO
    // declare variables
    int x = atoi(&fraction[0]);
    int y = atoi(&fraction[2]);
    // calculates length of note
    int duration = (x * 8) / y;

    return duration;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    // TODO
    // declare variables
    int count;
    int length = strlen(note);
    int base_note = 0;
    double hertz;
    int octave = note[strlen(note) - 1];

    // for loop iterates through length of given string
    for (count = 0; count < length; count++)
    {

        // determines the note
        switch (note[0])
        {
            case 'A':
                base_note = 0;
                break;

            case 'B':
                base_note = 2;
                break;

            case 'C':
                base_note = -9;
                break;

            case 'D':
                base_note = -7;
                break;

            case 'E':
                base_note = -5;
                break;

            case 'F':
                base_note = -4;
                break;

            case 'G':
                base_note = -2;
                break;
        }

        // determines the incedental (if there is one)
        if (note[1] == '#')
        {
            base_note += 1;
        }
        else if (note[1] == 'b')
        {
            base_note -= 1;
        }

        // determines the octave
        switch (octave)
        {

            case '1':
                base_note -= 36;
                break;

            case '2':
                base_note -= 24;
                break;

            case '3':
                base_note -= 12;
                break;

            case '4':
                base_note += 0;
                break;

            case '5':
                base_note += 12;
                break;

            case '6':
                base_note += 24;
                break;

            case '7':
                base_note += 36;
                break;
        }
    }

    // calculates frequency
    hertz = pow(2, base_note / 12.0) * 440;

    int frequency = round(hertz);

    return frequency;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    // determines whether a line is blank indicating a rest

    int rest = strcmp(s, "");

    if (rest == 0)
    {
        return true;
    }
    else;
    {
        return false;
    }

}
