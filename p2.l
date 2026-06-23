%{
#include<stdio.h>

int chars=0, words=0, lines=0;
%}

%%
\n      { lines++; chars++; }
[ \t]+  { chars += yyleng; }
[^ \t\n]+ { words++; chars += yyleng; }
%%

int yywrap(){ return 1; }

int main()
{
    yylex();

    printf("Characters = %d\n", chars);
    printf("Words = %d\n", words);
    printf("Lines = %d\n", lines);

    return 0;
}
