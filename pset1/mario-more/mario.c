#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n = 0;
    while (n < 1 || n > 8)
    {
        n = get_int("Height: ");
    }

    for (int i = 1; i <= n; i++)
    {
        for (int j = n; j >= 1; j--)
        {
            if (j > i)
            {
                printf(" ");
            }

            else
            {
                printf("#");
            }
        }

        printf("  ");

        for (int k = 1; k <= i; k++)
        {

            if (k <= i)
            {
                printf("#");
            }

            else
            {
                printf(" ");
            }

        }

        printf("\n");




    }

}