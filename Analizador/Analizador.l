%{
#include <stdio.h>
#include <string.h>

int linea = 1;

int esReservada(char palabra[]);

%}

%%

-?[0-9]+\.[0-9]+ {

    printf("Linea %d: Flotante -> %s\n", linea, yytext);

}

-?[0-9]+ {

    printf("Linea %d: Entero -> %s\n", linea, yytext);

}

[a-zA-Z_][a-zA-Z0-9_]* {

    if(esReservada(yytext))
    {
        printf("Linea %d: Palabra reservada -> %s\n", linea, yytext);
    }
    else
    {
        printf("Linea %d: Identificador -> %s\n", linea, yytext);
    }

}

\n {

    linea++;

}

[ \t]+ {

}

. {

}

%%

int esReservada(char palabra[])
{
    if(strcmp(palabra, "BEGIN") == 0)
        return 1;
    else if(strcmp(palabra, "END") == 0)
        return 1;
    else if(strcmp(palabra, "alias") == 0)
        return 1;
    else if(strcmp(palabra, "and") == 0)
        return 1;
    else if(strcmp(palabra, "begin") == 0)
        return 1;
    else if(strcmp(palabra, "break") == 0)
        return 1;
    else if(strcmp(palabra, "case") == 0)
        return 1;
    else if(strcmp(palabra, "class") == 0)
        return 1;
    else if(strcmp(palabra, "def") == 0)
        return 1;
    else if(strcmp(palabra, "do") == 0)
        return 1;
    else if(strcmp(palabra, "else") == 0)
        return 1;
    else if(strcmp(palabra, "elsif") == 0)
        return 1;
    else if(strcmp(palabra, "end") == 0)
        return 1;
    else if(strcmp(palabra, "ensure") == 0)
        return 1;
    else if(strcmp(palabra, "false") == 0)
        return 1;
    else if(strcmp(palabra, "for") == 0)
        return 1;
    else if(strcmp(palabra, "if") == 0)
        return 1;
    else if(strcmp(palabra, "in") == 0)
        return 1;
    else if(strcmp(palabra, "module") == 0)
        return 1;
    else if(strcmp(palabra, "next") == 0)
        return 1;
    else if(strcmp(palabra, "nil") == 0)
        return 1;
    else if(strcmp(palabra, "not") == 0)
        return 1;
    else if(strcmp(palabra, "or") == 0)
        return 1;
    else if(strcmp(palabra, "redo") == 0)
        return 1;
    else if(strcmp(palabra, "rescue") == 0)
        return 1;
    else if(strcmp(palabra, "retry") == 0)
        return 1;
    else if(strcmp(palabra, "return") == 0)
        return 1;
    else if(strcmp(palabra, "self") == 0)
        return 1;
    else if(strcmp(palabra, "super") == 0)
        return 1;
    else if(strcmp(palabra, "then") == 0)
        return 1;
    else if(strcmp(palabra, "true") == 0)
        return 1;
    else if(strcmp(palabra, "undef") == 0)
        return 1;
    else if(strcmp(palabra, "unless") == 0)
        return 1;
    else if(strcmp(palabra, "until") == 0)
        return 1;
    else if(strcmp(palabra, "when") == 0)
        return 1;
    else if(strcmp(palabra, "while") == 0)
        return 1;
    else if(strcmp(palabra, "yield") == 0)
        return 1;
    else if(strcmp(palabra, "__ENCODING__") == 0)
        return 1;
    else if(strcmp(palabra, "__FILE__") == 0)
        return 1;
    else if(strcmp(palabra, "__LINE__") == 0)
        return 1;

    return 0;
}

int main()
{
    yylex();

    return 0;
}