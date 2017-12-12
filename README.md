# Pascal Compiler

注意：该实现版本一次只判一个错

```c
/**********文法产生式如下**********
A：程序				A->B
B：分程序			B->begin C;M end
C：说明与句表		C->DC'
C'->;DC'|ε
D：说明语句			D->E|J
E：变量说明			E->integer F
F：变量				F->G
G：标识符			G->HG'
G'->HG'|IG'|ε
H：字母				H->a|...|z|A|...|Z
I：数字				I->0|1|...|9
J：函数说明			J->integer function G(K);L
K：参数				K->F
L：函数体			L->begin C;M end
M：执行语句表		M->NM'
M'->;NM'|ε
N：执行语句			N->O|P|Q|W
O：读语句			O->read(F)
P：写语句			P->write(F)
Q：赋值语句			Q->F:=R
R：算术表达式		R->SR'
R'->-SR'|ε
S：项				S->TS'
S'->*TS'|ε
T：因子				T->F|U|Z
U：常数				U->V
V：无符号整数		V->IV'
V'->IV'|ε
W：条件语句			W->if X then N else N
X：条件表达式		X->RYR
Y：关系运算符		Y-><|<=|>|>=|=|<>
Z：函数调用			Z->G(R)
**********************************/
```
