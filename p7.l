%{
#include<stdio.h>
%}

%%
.*"and".*|.*"but".*|.*"or".*|.*"And".*|.*"But".*|.*"Or".* { printf("Compound Sentence\n"); }

.*"because".*|.*"although".*|.*"since".*|.*"Because".*|.*"Although".*|.*"Since".* { printf("Complex Sentence\n"); }

[a-zA-Z0-9]+[ ]+[a-zA-Z0-9]+.*|.*"\."|.*"\!"|.*"\?" { printf("Simple Sentence\n"); }

.* { printf("Not a Valid Sentence\n"); }

\n ;
%%

int yywrap(){ return 1; }

int main()
{
    yylex();
    return 0;
}

