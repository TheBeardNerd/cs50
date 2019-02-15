#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize f infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // resizing factor
    float factor = atof(argv[1]);

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // save width and height to int variables
    int new_wide = bi.biWidth;
    int new_tall = bi.biHeight;
    // original file's padding
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // new file header info times factor
    bi.biWidth *= factor;
    bi.biHeight *= factor;
    // padding for outfile
    int new_pad = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // update header info for outfile
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + new_pad) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // allocate memory to store output into rows
    RGBTRIPLE *rows = malloc(bi.biWidth * sizeof(RGBTRIPLE));

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(new_tall); i < biHeight; i++)
    {
        // counter initialized to zero
        int count = 0;

        // iterate over pixels in scanline
        for (int j = 0; j < new_wide; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // for loop to write RGB triple by pixel into rows
            for (int pixel = 0; pixel < factor; pixel++)
            {
                rows[count] = triple;
                count++;
            }
        }
        // skip over any padding
        fseek(inptr, padding, SEEK_CUR);

        // write rows of RGB triple to outfile
        for (int vert = 0; vert < factor; vert++)
        {
            // write RGB triple to outfile
            fwrite(rows, sizeof(RGBTRIPLE), bi.biWidth, outptr);

            // then add padding to outfile
            for (int k = 0; k < new_pad; k++)
            {
                fputc(0x00, outptr);
            }
        }

    }
    // free malloc *rows
    free(rows);

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}