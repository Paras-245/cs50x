#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");



    float L = ((float)count_letters(text) / (float)count_words(text)) * 100;
    float S = ((float)count_sentences(text) / (float)count_words(text)) * 100;

    int index = round(0.0588 * L - 0.296 * S - 15.8);


    if (index > 16)
    {
        printf("Grade 16+\n");
    }

    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }

    else
    {
        printf("Grade %i\n", index);
    }
    return 0;

}
























int count_letters(string text)
{

    int letters = 0;
    int len = strlen(text);
    for (int i = 0 ; i < len ; i++)
    {
        if (text[i] >= 65 && text[i] <= 122)
        {
            letters++;

        }
    }
    return letters;
}

int count_words(string text)
{
    int words = 1;

    int len = strlen(text);
    for (int i = 0 ; i < len ; i++)
    {
        if (text[i] == 32)
        {
            words++;
        }


    }


    return words;
}


int count_sentences(string text)
{

    int sentences = 0;
    int len = strlen(text);
    for (int i = 0 ; i < len ; i++)
    {
        if (text[i] == 33 || text[i] == 63 || text[i] == 46)
        {
            sentences++;

        }
    }
    return sentences;

}