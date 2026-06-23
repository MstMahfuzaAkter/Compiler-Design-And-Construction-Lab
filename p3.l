%{
#include<stdio.h>
%}

%%
[+-]?[0-9]+ {
    printf("Integer : %s\n",yytext);
}

[+-]?[0-9]+"."[0-9]+ {
    printf("Float : %s\n",yytext);
}

[+-]?[0-9]+(\.[0-9]+)?[eE][+-]?[0-9]+ {
    printf("Exponential : %s\n",yytext);
}

[+-]?[0-9]+(\.[0-9]+)?[+-][0-9]+(\.[0-9]+)?i {
    printf("Complex : %s\n",yytext);
}

.|\n ;
%%

int yywrap(){ return 1; }

int main()
{
    yylex();
    return 0;
}
