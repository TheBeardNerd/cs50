#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <cs50.h>


int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // open forensic image file
    char *pics = argv[1];
    FILE *inptr = fopen(pics, "rb");

    // Check if input file opens
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", pics);
        return 2;
    }

    // initialize variables
    char filename[10];
    unsigned char buffer[512];
    int count = 0;

    // initialize jpeg file
    FILE *jpeg = NULL;

    // read infile by block, 512 bits at a time
    while (fread(buffer, 1, 512, inptr))
    {
        // determine the beginning of a jpeg file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpeg == NULL)
            {
                // increments jpeg filenames by one when a new buffer is found
                sprintf(filename, "%.3i.jpg", count);

                jpeg = fopen(filename, "wb");

                fwrite(buffer, 1, 512, jpeg);

                count++;
            }
            else
            {
                // close previous jpeg file
                fclose(jpeg);

                // begins new jpeg file
                // increments jpeg filenames by one when a new buffer is found
                sprintf(filename, "%.3i.jpg", count);

                jpeg = fopen(filename, "wb");

                fwrite(buffer, 1, 512, jpeg);

                count++;
            }
        }
        else
        {
            // determines the EOF and writes last jpeg to file
            if (jpeg != 0)
            {
                fwrite(buffer, 1, 512, jpeg);
            }
        }
    }

    // close outfile
    fclose(jpeg);

    // close infile
    fclose(inptr);

    // success!
    return 0;
}
