#include<stdio.h>
#include<cs50.h>
int main()
{
    string name = get_string("What is your name? \n");
    //getting name from user
    printf("hello, %s \n", name);
    return 0;
}