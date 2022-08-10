#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]))
        {
            continue;
        }
        else
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }



    int key = atoi(argv[1]);

    if (key < 0)
    {
        return 1;
    }


    string plaintext = get_string("plaintext: ");

    int plainlen = strlen(plaintext);
    printf("ciphertext: ");





    for (int i = 0; i < plainlen ; i++)
    {
        if (isupper(plaintext[i]))
        {
            printf("%c", (((plaintext[i] + key) - 65) % 26) + 65);
        }
        else if (islower(plaintext[i]))
        {
            printf("%c", (((plaintext[i] + key) - 97) % 26) + 97);
        }
        else
        {
            printf("%c", plaintext[i]);

        }

    }

    printf("\n");




    return 0;




}


