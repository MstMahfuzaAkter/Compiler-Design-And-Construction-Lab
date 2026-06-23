%{
#include<stdio.h>
int count=0;
%}

%%

"auto"|"break"|"case"|"char"|"const"|"continue"|"default"|"do"|"double"|"else"|"enum"|"extern"|"float"|"for"|"goto"|"if"|"int"|"long"|"register"|"return"|"short"|"signed"|"sizeof"|"static"|"struct"|"switch"|"typedef"|"union"|"unsigned"|"void"|"volatile"|"while" ;

[a-zA-Z_][a-zA-Z0-9_]* {
    count++;
    printf("Identifier : %s\n", yytext);
}

.|\n ;

%%

int yywrap()
{
    return 1;
}

int main()
{
    yylex();

    printf("\nTotal Identifiers = %d\n", count);

    return 0;
}
