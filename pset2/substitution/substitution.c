#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    if (strlen(argv[1]) != 26)

    {
        printf("Key must contain 26 characters.\n");
        return 1;

    }
    int sum = 0;
    string key = argv[1];
    int key_len = strlen(key);

    for (int i = 0  ; i < key_len ; i++)
    {
        if (isalpha(key[i]) == 0)
        {
            printf("Usage: ./substitution key\n");
            return 1;

        }
        sum = sum + toupper(key[i]);

    }

    if (sum != 2015)
    {
        printf("Usage: ./substitution key\n");
        return 1;

    }



    string text = get_string("plaintext: ");
    int text_len = strlen(text);

    printf("ciphertext: ");

    for (int j = 0; j < text_len ; j++)
    {
        if (islower(text[j]))
        {
            printf("%c", tolower(key[(text[j] - 97)]));

        }
        else if (isupper(text[j]))
        {
            printf("%c", toupper(key[text[j] - 65]));
        }
        else
        {
            printf("%c", text[j]);
        }



    }

    printf("\n");












}