#include <stdio.h>
#include <string>
#include <stdlib.h>
#include <iostream>
using namespace std;
#define ILLEGAL_CHAR 0
#define ERROR_OPERATOR 1

string key[9] = {"begin","end","integer","if","then","else","function","read","write"};
int lexAnalyze(FILE* fp);
int getnbc(char ch);
int isDigit(char ch);
int isLetter(char ch);
int isKey(string arr);
void retract(FILE* fp);
void formatOutput(FILE* res,int code);
void formatOutput(FILE* res,int code,string arr);
void error(int code,int line,FILE* err);

int main(){
    FILE *fp = fopen("D:\\lex.pas","r");
    if(fp == NULL) return 1;
    lexAnalyze(fp);
    fclose(fp);
    return 0;
}

int lexAnalyze(FILE* fp){
    char ch;
    FILE *res = fopen("D:\\result.dyd","w+");
    if(res == NULL) return 1;
    FILE *err = fopen("D:\\result.err","w+");
    if(err == NULL) return 1;
    int line = 1;
    while((ch = fgetc(fp)) != EOF){
        string arr = "";
        if(ch == '\n'){
            formatOutput(res,24);
            line++;
            continue;
        }
        if(getnbc(ch)) continue;
        switch(ch){
        case 'a':
        case 'b':
        case 'c':
        case 'd':
        case 'e':
        case 'f':
        case 'g':
        case 'h':
        case 'i':
        case 'j':
        case 'k':
        case 'l':
        case 'm':
        case 'n':
        case 'o':
        case 'p':
        case 'q':
        case 'r':
        case 's':
        case 't':
        case 'u':
        case 'v':
        case 'w':
        case 'x':
        case 'y':
        case 'z':
        case 'A':
        case 'B':
        case 'C':
        case 'D':
        case 'E':
        case 'F':
        case 'G':
        case 'H':
        case 'I':
        case 'J':
        case 'K':
        case 'L':
        case 'M':
        case 'N':
        case 'O':
        case 'P':
        case 'Q':
        case 'R':
        case 'S':
        case 'T':
        case 'U':
        case 'V':
        case 'W':
        case 'X':
        case 'Y':
        case 'Z':
            while(isDigit(ch) || isLetter(ch)){
                arr += ch;
                if((ch = fgetc(fp)) == EOF)
                    break;
            }
            if(ch != EOF)
                retract(fp);
            int num;
            num = isKey(arr);
            if(num == 9){
                formatOutput(res,10,arr);
            }else{
                formatOutput(res,num+1);
            }
            break;
        case '0':
        case '1':
        case '2':
        case '3':
        case '4':
        case '5':
        case '6':
        case '7':
        case '8':
        case '9':
            while(isDigit(ch)){
                arr += ch;
                if((ch = fgetc(fp)) == EOF)
                    break;
            }
            if(ch != EOF)
                retract(fp);
            formatOutput(res,11,arr);
            break;
        case '<':
            arr += ch;
            if((ch = fgetc(fp)) == '='){
                arr += ch;
                formatOutput(res,14);
            }else if(ch == '>'){
                arr += ch;
                formatOutput(res,13);
            }else{
                retract(fp);
                formatOutput(res,15);
            }
            break;
        case '>':
            arr += ch;
            if((ch = fgetc(fp)) == '='){
                arr += ch;
                formatOutput(res,16);
            }else{
                retract(fp);
                formatOutput(res,17);
            }
            break;
        case ':':
            arr += ch;
            if((ch = fgetc(fp)) == '='){
                arr += ch;
                formatOutput(res,20);
            }else{
                retract(fp);
                error(ERROR_OPERATOR,line,err);
            }
            break;
        case ';':
            arr += ch;
            formatOutput(res,23);
            break;
        case '=':
            arr += ch;
            formatOutput(res,12);
            break;
        case '-':
            arr += ch;
            formatOutput(res,18);
            break;
        case '*':
            arr += ch;
            formatOutput(res,19);
            break;
        case '(':
            arr += ch;
            formatOutput(res,21);
            break;
        case ')':
            arr += ch;
            formatOutput(res,22);
            break;
        default:
            error(ILLEGAL_CHAR,line,err);
            break;
        }
    }
    formatOutput(res,25);
    fclose(res);
    fclose(err);
    return 0;
}

int getnbc(char ch){
    if(ch == ' ' || ch == '\t' || ch == '\r')
        return 1;
    else
        return 0;
}

int isDigit(char ch){
    if(ch >= '0' && ch <= '9')
        return 1;
    else
        return 0;
}

int isLetter(char ch){
    if((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z'))
        return 1;
    else
        return 0;
}

int isKey(string arr){
    int i;
    for(i = 0;i < 9;i++){
        if(arr.compare(key[i]) == 0)
            break;
    }
    return i;
}

void retract(FILE* fp){
    fseek(fp,-1L,SEEK_CUR);
}

void formatOutput(FILE* res,int code){
    if(code >= 1 && code <= 9){
        fprintf(res,"%16s %2d\n",key[code-1].c_str(),code);
    }else if(code >= 12 && code <= 25){
        switch(code){
        case 12:
            fprintf(res,"%16s %2d\n","=",code);
            break;
        case 13:
            fprintf(res,"%16s %2d\n","<>",code);
            break;
        case 14:
            fprintf(res,"%16s %2d\n","<=",code);
            break;
        case 15:
            fprintf(res,"%16s %2d\n","<",code);
            break;
        case 16:
            fprintf(res,"%16s %2d\n",">=",code);
            break;
        case 17:
            fprintf(res,"%16s %2d\n",">",code);
            break;
        case 18:
            fprintf(res,"%16s %2d\n","-",code);
            break;
        case 19:
            fprintf(res,"%16s %2d\n","*",code);
            break;
        case 20:
            fprintf(res,"%16s %2d\n",":=",code);
            break;
        case 21:
            fprintf(res,"%16s %2d\n","(",code);
            break;
        case 22:
            fprintf(res,"%16s %2d\n",")",code);
            break;
        case 23:
            fprintf(res,"%16s %2d\n",";",code);
            break;
        case 24:
            fprintf(res,"%16s %2d\n","EOLN",code);
            break;
        case 25:
            fprintf(res,"%16s %2d","EOF",code);
            break;
        }
    }
}

void formatOutput(FILE* res,int code,string arr){
    if(code == 10 || code == 11){
        fprintf(res,"%16s %2d\n",arr.c_str(),code);
    }
}

void error(int code,int line,FILE* err){
    switch(code){
    case 0:
        fprintf(err,"***LINE:%d  illegal character\n",line);
        break;
    case 1:
        fprintf(err,"***LINE:%d  operator ':' error\n",line);
        break;
    }
}
