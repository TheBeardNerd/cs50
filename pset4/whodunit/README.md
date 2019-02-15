# Questions

## What's `stdint.h`?

##### *stdint.h provides typedefs that specify exact-width integer types, with allowed values for each type.*

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

##### *Unsigned integers to give access to larger integer type numbers.*

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

##### *BYTE = 1 byte*
##### *DWORD = 4 bytes*
##### *LONG = 4 bytes*
##### *WORD = 2 bytes*

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

##### *424D*

## What's the difference between `bfSize` and `biSize`?

##### *bfSize is the size of the whole bitmap file. biSize is only BITMAPINFOHEADER and is a constant value equalling 40.*

## What does it mean if `biHeight` is negative?

##### *The bitmap is top-down starting at the top left corner.*

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

##### *biBitCount*

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

##### *There is nothing to read in the file.*

## Why is the third argument to `fread` always `1` in our code?

##### *It only needs to read 1 struct.*

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

##### *Padding would be 3.*

## What does `fseek` do?

##### *Sets the file position.*

## What is `SEEK_CUR`?

##### *Current position in file.*

## Whodunit?

## _**`It was Professor Plum with the candlestick in the library!`**_