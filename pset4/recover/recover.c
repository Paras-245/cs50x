#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    FILE *raw = fopen(argv[1], "r");
    if (raw == NULL)
    {
        printf("File can't be opened!\n");
        return 1;
    }
    typedef uint8_t BYTE;
    BYTE buffer[512];
    int jpegn = 0;
    int fjpeg = 0;
    FILE *img ;

    while (fread(buffer, 512, 1, raw))
    {


        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (fjpeg == 0)
            {
                fjpeg = 1;
            }
            else
            {
                fclose(img);
            }
            char name[9];

            sprintf(name, "%03i.jpg", jpegn);
            img = fopen(name, "a");
            fwrite(buffer, sizeof(buffer), 1, img);

            jpegn++;

        }

        else if (fjpeg == 1)
        {
            fwrite(buffer, sizeof(buffer), 1, img);

        }
    }
    fclose(img);
    fclose(raw);


}























