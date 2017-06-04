#include<stdio.h>
#include<string.h>
#include <ctype.h>
#include <stdlib.h>
#define MAX_COUNT 1024

/*types是支持类型的集合*/
typedef enum{ integer } types;
/*记录变量信息的结构体*/
typedef struct {
	char vname[17];
	char vproc[17];
	bool vkind; //1(0—变量、1—形参)
	types vtype;
	int vlev; //变量层次
	int vadr; //相对位置
} varRecord;
/*记录过程信息的结构体*/
typedef struct{
	char pname[17];
	types ptype;
	int plev;
	int varNum;
	int fadr; //第一个变量在变量表中的位置
	int ladr; //最后一个变量在变量表中的位置
	int parameter;  //当前函数变量的位置
	bool parameterIsDefined;
} proRecord;

FILE* inFile;//输入文件句柄
FILE* outFile;//输出文件句柄
FILE* errFile;//错误文件句柄
FILE* varFile;//变量文件句柄
FILE* proFile;//过程文件句柄
char input[MAX_COUNT][17]; //输入文件每一行的符号，标识符等
int kind[MAX_COUNT];//每一行的数字，即符号类别
int inputCount;//输入符号的数量
int pToken;//指向当前输入符号
int pChar;//指向当前输入符号中的当前字符
int lineNum;//当前行号
int varCount;
int proCount;
varRecord var[MAX_COUNT];//存放变量名表项数组
proRecord pro[MAX_COUNT];//存放过程名表项数组
varRecord currentVar;//存放当前变量的信息
proRecord currentPro;//存放当前过程的信息
//初始化,读入token表
bool init(){
	char inFilename[MAX_COUNT] = "d:\\test.dyd";
	char outFilename[MAX_COUNT] = "d:\\test.dys";
	char errFilename[MAX_COUNT] = "d:\\test.err";
	char varFilename[MAX_COUNT] = "d:\\test.var";
	char proFilename[MAX_COUNT] = "d:\\test.pro";
	if((inFile=fopen(inFilename,"r"))&&(outFile=fopen(outFilename,"w"))&&(errFile=fopen(errFilename,"w"))
	&&(varFile=fopen(varFilename,"w"))&&(proFile=fopen(proFilename,"w"))){
		inputCount=0;
		proCount=0;
		varCount=0;
		pToken=0;
		pChar=0;
		lineNum=1;
		currentPro.plev=0;
		currentPro.parameter=-1;
		currentPro.varNum=0;
		strcpy(currentPro.pname,"");
		while(!feof(inFile)){
			char stringLine[MAX_COUNT];
			if(fgets(stringLine,MAX_COUNT,inFile)){
				char line[20]="";
				strncpy(line,stringLine,19);          //input文件的每一行是这样的 "   begin 1     " ,我们要做的是把这两个东西割开并存在两个数组里
				char *kindString=strrchr(line,' '); //空格最后一次出现的位置
				kind[inputCount]=atoi(kindString+1);

				char string[17]="";
				strncpy(string,stringLine,16);
				char *firstString=strrchr(string,' '); //空格最后一次出现的位置
				strcpy(input[inputCount],firstString+1);
				inputCount++;
			}
		}
		return true;
	}else{
		fclose(inFile);
		fclose(outFile);
		fclose(errFile);
		fclose(varFile);
		fclose(proFile);
		return false;
	}
}
void final(){                          //将结构体里存的数据写入到指定文件中
	for(int i=0;i<varCount;i++){
		int kind=var[i].vkind?1:0;
		char vtype[10]=" ";
		if(var[i].vtype == integer){
			strcpy(vtype,"integer");
		}else{
			strcpy(vtype," ");
		}
		fprintf(varFile,"%16s %16s %d %s %d %d\n", var[i].vname, var[i].vproc, kind, vtype, var[i].vlev, var[i].vadr);
	}
	for(int i=0;i<proCount;i++){
		char type[10]=" ";
		if(pro[i].ptype == integer){
			strcpy(type,"integer");
		}else{
			strcpy(type," ");
		}
		fprintf(proFile,"%16s %s %d %d %d\n", pro[i].pname, type, pro[i].plev, pro[i].fadr, pro[i].ladr);
	}
	if (fseek(inFile, 0, 0) == 0)
	{
		while (!feof(inFile)){
			fputc(fgetc(inFile), outFile);
		}
	}
}
//1 标记符未定义  2 标记符重定义  3  执行语句不能识别
//4  缺少符号     5  函数参数未定义
void error(int errNum,const char* symbol){
	switch(errNum){
		case 1:
			fprintf(errFile, "***LINE:%d  symbol %s undefined\n",lineNum,input[pToken]);
			break;
		case 2:
			fprintf(errFile, "***LINE:%d  symbol %s re-defined\n",lineNum,input[pToken]);
			break;
		case 3:
			fprintf(errFile, "***LINE:%d  can not execute %s\n",lineNum,input[pToken]);
			break;
		case 4:
			fprintf(errFile, "***LINE:%d  near %s lack of %s\n",lineNum,input[pToken],symbol);
			break;
		case 5:
			fprintf(errFile, "***LINE:%d  function param not defined\n",lineNum);
			break;
		case 6:
			fprintf(errFile, "***LINE:%d  lack of symbol\n",lineNum);
			break;
		default:
			break;
	}
	fclose(inFile);
	fclose(outFile);
	fclose(errFile);
	fclose(varFile);
	fclose(proFile);
	exit(0);
}
bool nextToken(){
	pToken++;
	if(strcmp(input[pToken],"EOF")==0){
		return true;
	}
	while(strcmp(input[pToken],"EOLN")==0){
		pToken++;
		lineNum++;
	}
	return false;
}
bool isVarExist(char *vnam,char *vpro,bool vkind){
	for(int i=0;i<varCount;i++){
		if((strcmp(var[i].vname,vnam)==0)&&(strcmp(var[i].vproc,vpro)==0)&&(vkind==var[i].vkind)){
			return true;
		}
	}
	for(int i=0;i<proCount;i++){
		if(strcmp(pro[i].pname,vnam)==0){
			return true;
		}
	}
	return false;
}
bool isProExist(char *pnam){
	for(int i=0;i<varCount;i++){
		if(strcmp(var[i].vname,pnam)==0){
			return true;
		}
	}
	for(int i=0;i<proCount;i++){
		if(strcmp(pro[i].pname,pnam)==0){
			return true;
		}
	}
	return false;
}
int getNextToken(){         //不改变pToken的值，提前读
	int tnext=pToken+1;
	while(strcmp(input[tnext],"EOLN")==0){
		tnext++;
	}
	return tnext;
}
void A();
void B();
void C();
void C_();
void D();
void E();
void F();
void G();
void J();
void K();
void L();
void M();
void M_();
void N();
void O();
void P();
void Q();
void R();
void R_();
void S();
void S_();
void T();
void U();
void W();
void X();
void Y();
void Z();
int main(){
	if(init()){

		A();
		final();
	}
}
//判断当前非终结符是否正确，并且预判一位,
//参数分别是：要判断的终结符，当前终结符后面的终结符，后面终结符（除去变量）的个数，是否有变量
void judgeSt(const char *string,const char array[][20],int stnum,bool hasVar){
	if(strcmp(input[pToken],string)==0){
		nextToken();
	}else{
		error(4,string);
		int flag=0;
		for(int i=0;i<stnum;i++){
			if(strcmp(input[pToken],array[i])==0){
				flag=1;
			}
		}
		if(hasVar){
			if(kind[pToken]==10){
				flag=1;
			}
		}
		if(flag==0){
			nextToken();
		}
	}
}
// A：程序	A->B
void A()
{
	B();
}
// B：分程序	B->begin C（说明语句表）;M（执行语句表） end
void B()
{
	char tmp[1][20]={"integer"}; // 说明语句只能是integer xx
	judgeSt("begin",tmp,1,false); // begin后是否匹配到integer,nextToken取到integer
	C(); // 匹配说明语句
	char tmp1[3][20]={"if","read","write"};
	judgeSt(";",tmp1,3,true);
	M();

	if(strcmp(input[pToken],"end")==0){
		nextToken();
	}
	else{
		error(4,"end");
	}
}
// C：说明语句表	C->DC'
void C()
{
	D(); // 说明语句
	C_();
}
// C'->;DC'|ε 递归匹配说明语句
void C_()
{
	// 如果匹配到分号并且下一个字符还是integer这种说明语句，去取下一个字符
	if(strcmp(input[pToken],";")==0&&strcmp(input[getNextToken()],"integer")==0){
		nextToken();
		D();
		C_();
	}
	// 如果开头不是分号，而是integer，就会报缺少分号错
	else{
		if(strcmp(input[pToken],"integer")==0){
			error(4,";");
			D();
			C_();
		}
	}
}
// 匹配说明语句
void D()
{
	// 预判一位，是否是函数声明 integer function
	if(strcmp(input[pToken+1],"function") == 0)
	{
		J();
	}else{
		// 变量声明 integer k
		E();
	}
}
// 匹配变量说明
void E()
{
	if (strcmp(input[pToken], "integer") == 0)
	{
		nextToken();
	}
	else //缺少integer错
	{
		error(4, "integer");
		//if (kind[pToken] != 10)
		//{
			nextToken();
		//}
	}
	strcpy(currentVar.vname,input[pToken]);
	strcpy(currentVar.vproc,currentPro.pname);
	if(strcmp(input[pToken], input[currentPro.parameter]) == 0){
		currentPro.parameterIsDefined=true;
		currentVar.vkind=true;
	}else{
		currentVar.vkind=false;
	}
	currentVar.vadr=varCount;
	currentVar.vlev=currentPro.plev;
	currentVar.vtype=integer;
	if (isVarExist(input[pToken], currentPro.pname, currentVar.vkind))//如果存在变量
	{
		// 变量已存在，符号重定义
		error(2,NULL);
	}
	else
	{
		//函数表中信息增加
		if(currentPro.varNum==0){
			currentPro.fadr=currentVar.vadr;
		}
		currentPro.ladr=currentVar.vadr;
		currentPro.varNum++;
		//变量表新增一条变量信息
		var[varCount]=currentVar;
		varCount++;
	}
	F();
}
void F()
{
	G();
}
void G()
{
	// 如果是标识符
	if(kind[pToken]==10){
		nextToken();
	}else{
		error(6,NULL);//缺少标识符
	}
}
// 函数说明
void J()
{
	proRecord backup=currentPro; // 先保存主程序
	char tmp[1][20]={"function"};
	judgeSt("integer",tmp,1,false);

	char tmp1[1][20]={" "};
	judgeSt("function",tmp1,0,true);

	strcpy(currentPro.pname,input[pToken]);
	currentPro.varNum=0;
	currentPro.ptype=integer;
	currentPro.parameterIsDefined=false;
	currentPro.plev++;
	if(isProExist(currentPro.pname)){
		error(2,NULL); //过程已经定义
	}
	G(); // 匹配标识符
	char tmp2[1][20]={" "};
	judgeSt("(",tmp2,0,true); // 匹配左括号

	currentPro.parameter=pToken;
	K(); // 匹配参数，其实就是标识符
	char tmp3[1][20]={" "};
	judgeSt(")",tmp3,0,true); // 匹配右括号

	char tmp4[1][20]={"begin"}; // 看看是不是;begin
	judgeSt(";",tmp4,1,false);
	L(); // 匹配函数体
	currentPro=backup;
}
void K()
{
	F();
}
void L()
{
	char tmp[1][20]={"integer"};
	judgeSt("begin",tmp,1,false); // 看看begin后是不是integer
	C();
	if(!currentPro.parameterIsDefined){
		error(5,input[currentPro.parameter]);//函数括号里的参数没有在函数体中定义
	}
	pro[proCount]=currentPro;
	proCount++;
	char tmp1[3][20]={"if","read","write"};
	judgeSt(";",tmp1,3,true); // 看是不是分号，不是的话看是不是if/read/write

	M();
	char tmp2[2][20]={";","end"};
	judgeSt("end",tmp2,2,false);
}
// 执行语句表
void M()
{
	N(); // 执行语句
	M_();
}
void M_()
{
	// 如果是分号，则继续匹配
	if(strcmp(input[pToken],";") == 0){
		nextToken();
		N();
		M_();
	}else{
		// 不是end且不是EOF,报缺少分号
		if(strcmp(input[pToken], "end") != 0&&strcmp(input[pToken], "EOF") != 0){
			error(4,";");
			N();
			M_();
		}
	}
}
void N()
{
	if(strcmp(input[pToken], "read") == 0){
		O();
	}else if(strcmp(input[pToken], "write") == 0){
		P();
	}else if(kind[pToken]==10){
		Q(); // 匹配赋值
	}else if(strcmp(input[pToken], "if") == 0){
		W();
	}else{
		error(3,NULL); // 执行语句不能识别
		nextToken();
	}
}
// read
void O()
{
	char tmp[1][20]={"("};
	judgeSt("read",tmp,1,false);//匹配read
	char tmp1[1][20]={" "};
	judgeSt("(",tmp1,0,true);//匹配左括号

	if(!isVarExist(input[pToken],currentPro.pname,false)&&!isVarExist(input[pToken],currentPro.pname,true)){
		error(1,NULL); // 形参实参都不存在，报标记符未定义错
	}
	F();
	char tmp2[2][20]={";","end"};
	judgeSt(")",tmp2,2,false);

}
// write
void P()
{
	char tmp[1][20]={"("};
	judgeSt("write",tmp,1,false);

	char tmp1[1][20]={" "};
	judgeSt("(",tmp1,0,true);
	if(!isVarExist(input[pToken],currentPro.pname,false)&&!isVarExist(input[pToken],currentPro.pname,true)&&kind[pToken] == 10){
		error(1,NULL);
	}
	F();
	char tmp2[2][20]={";","end"};
	judgeSt(")",tmp2,2,false);
}
// 赋值语句
void Q()
{
	if(!isVarExist(input[pToken],currentPro.pname,false)&&!isVarExist(input[pToken],currentPro.pname,true)&& !isProExist(input[pToken])){
		error(1,NULL);
	}
	F();
	if(strcmp(input[pToken], ":=") == 0){
		nextToken();
	}else{
		error(4,":=");
		if(kind[pToken]!=10&&kind[pToken]!=11){
			nextToken();
		}
	}
	R();
}
// 算术表达式
void R()
{
	S(); // 匹配项
	R_();
}
// 匹配-
void R_()
{
	if(strcmp(input[pToken], "-") == 0){
		nextToken();
		S();
		R_();
	}
	/*else{
		if(kind[pToken]==10||kind[pToken]==11){
			S();
			R_();
		}
	}*/
}
void S()
{
	T();
	S_();
}
// 匹配*
void S_()
{
	if(strcmp(input[pToken], "*") == 0){
		nextToken();
		T();
		S_();
	}
	/*else{
		if(kind[pToken]==10||kind[pToken]==11){
			T();
			S_();
		}
	}*/
}
void T()
{
	// 常数
	if(kind[pToken]==11){
		U();
	}
	// 函数调用
	else if (strcmp(input[pToken+1], "(") == 0)
	{
		Z();
	}
	// 变量
	else
	{
		if(!isVarExist(input[pToken],currentPro.pname,true)&&!isVarExist(input[pToken],currentPro.pname,false)){
			error(1,NULL);
		}
		F();
	}
}
void U()
{
	if (kind[pToken] == 11){
		nextToken();
	}
}
// 条件语句
void W()
{
	if(strcmp(input[pToken], "if") == 0){
		nextToken();
	}else{
		error(4,"if");
		if(kind[pToken]!=11&&kind[pToken]!=10){
			nextToken();
		}
	}
	X();
	char tmp[3][20]={"if","read","write"};
	judgeSt("then",tmp,3,true);

	N();
	char tmp1[3][20]={"if","read","write"};
	judgeSt("else",tmp1,3,true);
	N();
}
void X()
{
	R();
	Y();
	R();
}
void Y()
{
	if((strcmp(input[pToken], "<") == 0)||(strcmp(input[pToken], "<=") == 0)||(strcmp(input[pToken], ">") == 0)||(strcmp(input[pToken], ">=") == 0)||(strcmp(input[pToken], "=") == 0)||(strcmp(input[pToken], "<>") == 0)){
		nextToken();
	}
    else{
   		error(4,"关系运算符");
		if(kind[pToken]!=11&&kind[pToken]!=10){
			nextToken();
		}
	}
}
// 匹配函数调用
void Z()
{
	if(!isProExist(input[pToken])){
		error(1,NULL);
	}
	G();// 标识符
	if(strcmp(input[pToken], "(") == 0){
		nextToken();
	}else{
		error(4,"(");
		if(kind[pToken]!=10&&kind[pToken]!=11){
			nextToken();
		}
	}
	R();
	char tmp[4][20]={"-","*",";","end"};
	judgeSt(")",tmp,4,false);
}
