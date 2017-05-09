# -*- coding:utf8 -*-

MAX_COUNT = 1024


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


global inFile,outFile,errFile,varFile,proFile
global Input,kind,pToken,pChar,lineNum,varCount,proCount
global var
global pro
global currentVar
global currentPro
inFile = None # 输入文件句柄
outFile = None # 输出文件句柄
errFile = None # 错误文件句柄
varFile = None # 变量文件句柄
proFile = None # 过程文件句柄
Input = [] # 输入文件每一行的符号，标识符等
kind = [] # 每一行的数字，即符号类别
pToken = 0 # 指向当前输入符号
pChar = 0 # 指向当前输入符号中的当前字符
lineNum = 1 # 当前行号
varCount = 0
proCount = 0
var = [0 for i in xrange(MAX_COUNT)] # 存放变量名表项数组
pro = [0 for i in xrange(MAX_COUNT)] # 存放过程名表项数组
currentVar = None # 存放当前变量的信息, class varRecord
currentPro = proRecord("","",0,0,0,0,-1,0) # 存放当前过程的信息，class proRecord


# 初始化处理 kind,Input
def init():
	global inFile,outFile,errFile,varFile,proFile
	global kind,Input
	inFilename = "d:/test.dyd"
	outFilename = "d:/test.dys"
	errFilename = "d:/test.err"
	varFilename = "d:/test.var"
	proFilename = "d:/test.pro"
	inFile = open(inFilename,'r')
	outFile = open(outFilename,'w')
	errFile = open(errFilename,'w')
	varFile = open(varFilename,'w')
	proFile = open(proFilename,'w')
	for line in inFile.readlines():
		divide = line.strip().replace("  "," ").split(' ')
		kind.append(divide[1])
		Input.append(divide[0])
	A()


def nextToken():
	global pToken,Input,lineNum
	pToken += 1
	if Input[pToken] == "EOF":
		return True
	while Input[pToken] == "EOLN":
		pToken += 1
		lineNum += 1
	return False


def judgeSt(string,array,stnum,hasVal):
	global pToken,Input,kind
	if Input[pToken] == string:
		nextToken()
	else:
		error(4,string)
		flag = 0
		for i in xrange(stnum):
			if Input[pToken] == array[i]:
				flag = 1
		if hasVal is True:
			if kind[pToken] == 10:
				flag = 1
		if flag == 0:
			nextToken()


def getNextToken():
	global pToken
	tnext = pToken + 1
	while Input[tnext] == "EOLN":
		tnext += 1
	return tnext


def isVarExist(vnam,vpro,vkind):
	global varCount,var,proCount,pro
	for i in xrange(varCount):
		if var[i].vname == vnam and var[i].vproc == vpro and vkind == var[i].vkind:
			return True
	for j in xrange(proCount):
		if pro[j].pname == vnam:
			return True
	return False


def isProExist(pnam):
	global varCount,var,pro,proCount
	for i in xrange(varCount):
		if var[j].vname == pnam:
			return True
	for j in xrange(proCount):
		if pro[i].pname == pnam:
			return True
	return False


def error(errNum,symbol = None):
	global errFile,lineNum,Input,pToken
	if errNum == 1:
		errFile.write("***LINE:" + str(lineNum) + "  " + Input[pToken] + "标记符未定义\n")
	elif errNum == 2:
		errFile.write("***LINE:" + str(lineNum) + "  " + Input[pToken] + "标记符重定义\n")
	elif errNum == 3:
		errFile.write("***LINE:" + str(lineNum) + "  " + Input[pToken] + "执行语句不能识别\n")
	elif errNum == 4:
		errFile.write("***LINE:" + str(lineNum) + "  " + Input[pToken] + "缺少符号" + symbol + "\n")
	elif errNum == 5:
		errFile.write("***LINE:" + str(lineNum) + "  函数参数" + Input[pToken] + "未定义\n")


def final():
	global inFile,outFile,errFile,varFile,proFile
	global varCount,var,pro,proCount
	for i in xrange(varCount):
		if var[i].vkind:
			kind = 1
		else:
			kind = 0
		vtype = " "
		if var[i].vtype == "integer":
			vtype = "integer"
		formater = "%16s %16s %d %s %d %d\n" % (var[i].vname, var[i].vproc, kind, vtype, var[i].vlev, var[i].vadr)
		varFile.write(formater)
	for i in xrange(proCount):
		ptype = " "
		if pro[i].ptype == "integer":
			ptype = "integer"
		formater = "%16s %s %d %d %d\n" % (pro[i].pname, ptype, pro[i].plev, pro[i].fadr, pro[i].ladr)
		proFile.write(formater)
	inFile.seek(0,0)
	for line in inFile.readlines():
		outFile.write(line)
	inFile.close()
	outFile.close()
	errFile.close()
	varFile.close()
	proFile.close()


# A：程序			A->B
# B：分程序			B->begin C;M end
# C：说明与句表		C->DC'
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
def A():
	B()
	final()


def B():
	global Input,pToken
	judgeSt("begin","integer",1,False)
	C()
	judgeSt(";",["if","read","write"],3,True)
	M()
	if Input[pToken] == "end":
		nextToken()
	else:
		error(4,"end")


def C():
	D()
	C_()


def C_():
	global Input,pToken
	if Input[pToken] == ";" and Input[getNextToken()] == "integer":
		nextToken()
		D()
		C_()
	else:
		if Input[pToken] == "integer":
			error(4,";")
			D()
			C_()


def D():
	global Input,pToken
	if Input[pToken+1] == "function":
		J()
	else:
		E()


def E():
	global varCount,Input,pToken,currentVar,currentPro,varCount,var
	if Input[pToken] == "integer":
		nextToken()
	else:
		error(4,"integer")
		nextToken()
	currentVar = varRecord(Input[pToken],currentPro.pname,True,"integer",currentPro.plev,varCount)
	if Input[pToken] == Input[currentPro.parameter]:
		currentPro.parameterIsDefined = True
	else:
		currentVar.vkind = False
	if isVarExist(Input[pToken],currentPro.pname,currentVar.vkind) is True:
		error(2)
	else:
		if currentPro.varNum == 0:
			currentPro.fadr = currentVar.vadr
		currentPro.ladr = currentVar.vadr
		currentPro.varNum += 1
		var[varCount] = currentVar
		varCount += 1
	F()


def F():
	G()


def G():
	global kind,pToken
	if kind[pToken] == 10:
		nextToken()


def J():
	global Input,pToken,currentPro
	backup = currentPro
	judgeSt("integer","function",1,False)
	judgeSt("function"," ",0,True)
	currentPro = proRecord(Input[pToken],"integer",backup.plev + 1,0,backup.fadr,backup.ladr,backup.parameter,False)
	if isProExist(currentPro.pname) is True:
		error(2)
	G()
	judgeSt("("," ",0,True)
	currentPro.parameter = pToken
	K()
	judgeSt(")"," ",0,True)
	judgeSt(";","begin",1,False)
	L()
	currentPro = backup


def K():
	F()


def L():
	global pro,proCount,currentPro
	judgeSt("begin","integer",1,False)
	C()
	if currentPro.parameterIsDefined is False:
		error(5,Input[currentPro.parameter])
	pro[proCount] = currentPro
	proCount += 1
	judgeSt(";",["if","read","write"],3,True)
	M()
	judgeSt("end",[";","end"],2,False)


def M():
	N()
	M_()


def M_():
	global Input,pToken
	if Input[pToken] == ";":
		nextToken()
		N()
		M_()
	else:
		if Input[pToken] != "end" and Input[pToken] != "EOF":
			error(4,";")
			N()
			M_()


def N():
	global Input,pToken
	if Input[pToken] == "read":
		O()
	elif Input[pToken] == "write":
		P()
	elif kind[pToken] == 10:
		Q()
	elif Input[pToken] == "if":
		W()
	else:
		error(3)
		nextToken()


def O():
	global Input,pToken,currentPro
	judgeSt("read","(",1,False)
	judgeSt("("," ",0,True)
	if isVarExist(Input[pToken],currentPro.pname,False) is False and isVarExist(Input[pToken],currentPro.pname,True) is False:
		error(1)
	F()
	judgeSt(")",[";","end"],2,False)


def P():
	global Input,pToken,currentPro
	judgeSt("write","(",1,False)
	judgeSt("("," ",0,True)
	if isVarExist(Input[pToken],currentPro.pname,False) is False and isVarExist(Input[pToken],currentPro.pname,True) is False:
		error(1)
	F()
	judgeSt(")",[";","end"],2,False)


def Q():
	global Input,pToken,currentPro,kind
	if isVarExist(Input[pToken],currentPro.pname,False) is False and isVarExist(Input[pToken],currentPro.pname,True) is False and isProExist(Input[pToken]) is False:
		error(1)
	F()
	if Input[pToken] == ":=":
		nextToken()
	else:
		error(4,":=")
		if kind[pToken] != 10 and kind[pToken] != 11:
			nextToken()
	R()


def R():
	S()
	R_()


def R_():
	global Input,pToken,kind
	if Input[pToken] == "-":
		nextToken()
		S()
		R_()
	else:
		if kind[pToken] == 10 or kind[pToken] == 11:
			S()
			R_()


def S():
	T()
	S_()


def S_():
	global Input,pToken,kind
	if Input[pToken] == "*":
		nextToken()
		T()
		S_()
	else:
		if kind[pToken] == 10 or kind[pToken] == 11:
			T()
			S_()


def T():
	global Input,pToken,kind,currentPro
	if kind[pToken] == 11:
		U()
	elif Input[pToken+1] == "(":
		Z()
	else:
		if isVarExist(Input[pToken],currentPro.pname,True) is False and isVarExist(Input[pToken],currentPro.pname,False) is False:
			error(1)
		F()


def U():
	global kind,pToken
	if kind[pToken] == 11:
		nextToken()


def W():
	global Input,pToken,kind
	if Input[pToken] == "if":
		nextToken()
	else:
		error(4,"if")
		if kind[pToken] != 11 and kine[pToken] != 10:
			nextToken()
	X()
	judgeSt("then",["if","read","write"],3,True)
	N()
	judgeSt("else",["if","read","write"],3,True)
	N()


def X():
	R()
	Y()
	R()


def Y():
	global Input,pToken,kind
	if Input[pToken] == "<" or Input[pToken] == "<=" or Input[pToken] == ">" or Input[pToken] == ">=" or Input[pToken] == "=" or Input[pToken] == "<>":
		nextToken()
	else:
		error(4,"关系运算符")
		if kind[pToken] != 11 and kind[pToken] != 10:
			nextToken()


def Z():
	global Input,pToken,kind
	if isProExist(Input[pToken]) is False:
		error(1)
	G()
	if Input[pToken] == "(":
		nextToken()
	else:
		error(4,"(")
		if kind[pToken] != 10 and kind[pToken] != 11:
			nextToken()
	R()
	judgeSt(")",["-","*",";","end"],4,False)


if __name__ == '__main__':
	init()