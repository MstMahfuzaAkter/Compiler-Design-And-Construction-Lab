%{
#include<stdio.h>
%}

%%
"is"|"am"|"are"|"was"|"were"|"be"|"been"|"being" {
    printf("To Be Verb : %s\n",yytext);
}

.|\n ;
%%

int yywrap(){ return 1; }

int main()
{
    yylex();
    return 0;
}
