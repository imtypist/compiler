# -*- coding:utf8 -*-

# SIGN_UNDEFINED_ERR = 1
# SIGN_REDEFINED_ERR = 2
# SIGN_EXECUTE_ERR = 3
# NO_SIGN_ERR = 4
# NO_PARA_ERR = 5

def struct(*name):
    """ 装饰器函数
        用途：用于在类定义中，自动设置self.value = value
    """
    def decorator(func):
        def wrapper(*args, **kw):
            for i in range(len(name)):
                setattr(args[0], name[i], args[i+1])
            return func(*args, **kw)
        return wrapper
    return decorator


# 记录变量信息
class varRecord(object):
	""" 
		vkind(0-变量 1-形参)
		vlev(变量层次)
		vadr(相对位置) 
	"""
	@struct('vname','vproc','vkind','vtype','vlev','vadr')
	def __init__(self, *all_value):
		pass


# 记录过程信息
class proRecord(object):
	"""
		fadr(第一个变量在变量表中的位置)
		ladr(最后一个变量在变量表中的位置)
		parameter(当前函数变量的位置)
	"""
	@struct('pname','ptype','plev','varNum','fadr','ladr','parameter','parameterIsDefined')
	def __init__(self, *all_value):
		pass


# **********文法产生式如下************
# A：程序			A->B
# B：分程序			B->begin C;M end
# C：说明语句表		C->DC'
# C'->;DC'|ε
# D：说明语句		D->E|J
# E：变量说明		E->integer F
# F：变量			F->G
# G：标识符			G->HG'
# G'->HG'|IG'|ε
# H：字母			H->a|...|z|A|...|Z
# I：数字			I->0|1|...|9
# J：函数说明		J->integer function G(K);L
# K：参数			K->F
# L：函数体			L->begin C;M end
# M：执行语句表		M->NM'
# M'->;NM'|ε
# N：执行语句		N->O|P|Q|W
# O：读语句			O->read(F)
# P：写语句			P->write(F)
# Q：赋值语句		Q->F:=R
# R：算术表达式		R->SR'
# R'->-SR'|ε
# S：项				S->TS'
# S'->*TS'|ε
# T：因子			T->F|U|Z
# U：常数			U->V
# V：无符号整数		V->IV'
# V'->IV'|ε
# W：条件语句		W->if X then N else N
# X：条件表达式		X->RYR
# Y：关系运算符		Y-><|<=|>|>=|=|<>
# Z：函数调用		Z->G(R)


inputChar = [] # 输入dyd文件每一行的符号，标识符等
kind = [] # dyd每一行的数字，即符号类别
inputCount = 0 #输入符号的数量
pToken = 0 # 指向当前输入符号
pChar = 0 # 指向当前输入符号中的当前字符

currentVar = 0 # 存放当前变量的信息, class varRecord
currentPro = proRecord("","",0,0,0,0,-1,0) # 存放当前过程的信息，class proRecord

lineNum = 1 # 当前行号

var = [] # 存放变量名表项数组
pro = [] # 存放过程名表项数组

varCount = 0 # 变量的数量
proCount = 0 # 过程的数量

inFile = 0 # 输入文件句柄
outFile = 0 # 输出文件句柄
errFile = 0 # 错误文件句柄
varFile = 0 # 变量文件句柄
proFile = 0 # 过程文件句柄