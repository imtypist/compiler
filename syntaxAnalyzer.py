# -*- coding:utf8 -*-
import globalVar as g


# 初始化处理 kind,inputChar
def init():
	inFilename = "./syntaxInput/test.dyd"
	outFilename = "./syntaxOutput/test.dys"
	errFilename = "./syntaxOutput/test.err"
	varFilename = "./syntaxOutput/test.var"
	proFilename = "./syntaxOutput/test.pro"
	g.inFile = open(inFilename,'r')
	g.outFile = open(outFilename,'w')
	g.errFile = open(errFilename,'w')
	g.varFile = open(varFilename,'w')
	g.proFile = open(proFilename,'w')
	for line in g.inFile.readlines():
		divide = line.strip().replace("  "," ").split(' ')
		g.kind.append(divide[1])
		g.inputChar.append(divide[0])
		g.inputCount += 1


def final():
	for i in xrange(g.varCount):
		if g.var[i].vkind:
			vkind = 1
		else:
			vkind = 0
		vtype = ""
		if g.var[i].vtype == "integer":
			vtype = "integer"
		formater = "%16s %16s %d %s %d %d\n" % (g.var[i].vname, g.var[i].vproc, vkind, vtype, g.var[i].vlev, g.var[i].vadr)
		g.varFile.write(formater)
	for i in xrange(g.proCount):
		ptype = ""
		if g.pro[i].ptype == "integer":
			ptype = "integer"
		formater = "%16s %s %d %d %d\n" % (g.pro[i].pname, ptype, g.pro[i].plev, g.pro[i].fadr, g.pro[i].ladr)
		g.proFile.write(formater)
	g.inFile.seek(0,0)
	for line in g.inFile.readlines():
		g.outFile.write(line)
	g.inFile.close()
	g.outFile.close()
	g.errFile.close()
	g.varFile.close()
	g.proFile.close()


def error(errNum,symbol = None):
	if errNum == 1:
		g.errFile.write("***LINE:" + str(g.lineNum) + "  " + g.inputChar[g.pToken] + "符号无定义\n")
	elif errNum == 2:
		g.errFile.write("***LINE:" + str(g.lineNum) + "  " + g.inputChar[g.pToken] + "符号重定义\n")
	elif errNum == 3:
		g.errFile.write("***LINE:" + str(g.lineNum) + "  " + g.inputChar[g.pToken] + "处不能匹配执行语句\n")
	elif errNum == 4:
		g.errFile.write("***LINE:" + str(g.lineNum) + "  " + g.inputChar[g.pToken] + "处缺少" + symbol + "\n")
	elif errNum == 5:
		g.errFile.write("***LINE:" + str(g.lineNum) + "  缺少形参" + g.inputChar[g.pToken] + "的声明\n")


def nextToken():
	g.pToken += 1
	if g.inputChar[g.pToken] == "EOF":
		return True
	while g.inputChar[g.pToken] == "EOLN":
		g.pToken += 1
		g.lineNum += 1
	return False


def isVarExist(vname,vpro,vkind):
	for i in xrange(g.varCount):
		if (g.var[i].vname == vname) and (g.var[i].vproc == vpro) and (vkind == g.var[i].vkind):
			return True
	for j in xrange(g.proCount):
		if g.pro[j].pname == vname:
			return True
	return False


def isProExist(vname):
	for i in xrange(g.varCount):
		if g.var[j].vname == vname:
			return True
	for j in xrange(g.proCount):
		if g.pro[i].pname == vname:
			return True
	return False


def getNextToken():
	tnext = pToken + 1
	while g.inputChar[tnext] == "EOLN":
		tnext += 1
	return tnext


def judgeSt(string,array,hasVal):
	if g.inputChar[g.pToken] == string:
		nextToken()
	else:
		error(4,string) # NO_SIGN_ERR
		flag = 0
		for el in array:
			if g.inputChar[g.pToken] == el:
				flag = 1
		if hasVal is True:
			if g.kind[g.pToken] == 10:
				flag = 1
		if flag == 0:
			nextToken()


def A():
	B()


def B():
	judgeSt("begin",["integer"],False)
	C()
	judgeSt(";",["integer","read","write"],True)
	M()
	if g.inputChar[g.pToken] == "end":
		nextToken()
	else:
		error(4,"end") # NO_SIGN_ERR


def C():
	D()
	C_()


def C_():
	if (g.inputChar[g.pToken] == ";") and (g.inputChar[getNextToken()] == "integer"):
		nextToken()
		D()
		C_()
	else:
		if g.inputChar[g.pToken] == "integer":
			error(4,";") # NO_SIGN_ERR
			D()
			C_()


def D():
	if g.inputChar[g.pToken+1] == "function":
		J()
	else:
		E()


def E():
	if g.inputChar[g.pToken] == "integer":
		nextToken()
	else:
		error(4,"integer")
		nextToken()
	g.currentVar = g.varRecord(g.inputChar[g.pToken],g.currentPro.pname,True,"integer",g.currentPro.plev,g.varCount)
	if g.inputChar[g.pToken] == g.inputChar[g.currentPro.parameter]:
		g.currentPro.parameterIsDefined = True
	else:
		g.currentVar.vkind = False
	if isVarExist(g.inputChar[g.pToken],g.currentPro.pname,g.currentVar.vkind) is True:
		error(2) # SIGN_REDEFINED_ERR
	else:
		if g.currentPro.varNum == 0:
			g.currentPro.fadr = g.currentVar.vadr
		g.currentPro.ladr = g.currentVar.vadr
		g.currentPro.varNum += 1
		g.var.append(g.currentVar);
		g.varCount += 1
	F()


def F():
	G()


def G():
	if g.kind[g.pToken] == 10:
		nextToken()


def J():
	backup = g.currentPro
	judgeSt("integer",["function"],False)
	judgeSt("function",[],True)
	g.currentPro = g.proRecord(g.inputChar[g.pToken],"integer",backup.plev + 1,0,backup.fadr,backup.ladr,backup.parameter,False)
	if isProExist(g.inputChar[g.pToken]) is True:
		error(2)
	G()
	judgeSt("(",[],True)
	g.currentPro.parameter = g.pToken
	K()
	judgeSt(")",[";"],False)
	judgeSt(";",["begin"],False)
	L()
	g.currentPro = backup


def K():
	F()


def L():
	judgeSt("begin",["integer"],False)
	C()
	if g.currentPro.parameterIsDefined is False:
		error(5,g.inputChar[g.currentPro.parameter]) # NO_PARA_ERR
	g.pro.append(g.currentPro)
	g.proCount += 1
	judgeSt(";",["integer","read","write"],True)
	M()
	judgeSt("end",[";","end"],False)


def M():
	N()
	M_()


def M_():
	if g.inputChar[g.pToken] == ";":
		nextToken()
		N()
		M_()
	else:
		if (g.inputChar[g.pToken] != "end") and (g.inputChar[g.pToken] != "EOF"):
			error(4,";") # NO_SIGN_ERR
			N()
			M_()


def N():
	if g.inputChar[g.pToken] == "read":
		O()
	elif g.inputChar[g.pToken] == "write":
		P()
	elif g.kind[g.pToken] == 10:
		Q()
	elif g.inputChar[g.pToken] == "if":
		W()
	else:
		error(3) #SIGN_EXECUTE_ERR
		nextToken()


def O():
	judgeSt("read",["("],False)
	judgeSt("(",[],True)
	if (isVarExist(g.inputChar[g.pToken],g.currentPro.pname,False) is False) and (isVarExist(g.inputChar[g.pToken],g.currentPro.pname,True) is False):
		error(1) #SIGN_UNDEFINED_ERR
	F()
	judgeSt(")",[";","end"],False)


def P():
	judgeSt("write",["("],False)
	judgeSt("(",[],True)
	if (isVarExist(g.inputChar[g.pToken],g.currentPro.pname,False) is False) and (isVarExist(g.inputChar[g.pToken],g.currentPro.pname,True) is False):
		error(1)#SIGN_UNDEFINED_ERR
	F()
	judgeSt(")",[";","end"],False)


def Q():
	if (isVarExist(g.inputChar[g.pToken],g.currentPro.pname,False) is False) and (isVarExist(g.inputChar[g.pToken],g.currentPro.pname,True) is False) and (isProExist(g.inputChar[g.pToken]) is False):
		error(1)
	F()
	if g.inputChar[g.pToken] == ":=":
		nextToken()
	else:
		error(4,":=")
		if (g.kind[g.pToken] != 10) and (g.kind[g.pToken] != 11):
			nextToken()
	R()


def R():
	S()
	R_()


def R_():
	if g.inputChar[g.pToken] == "-":
		nextToken()
		S()
		R_()
	else:
		if (g.kind[g.pToken] == 10) or (g.kind[g.pToken] == 11):
			S()
			R_()


def S():
	T()
	S_()


def S_():
	if g.inputChar[g.pToken] == "*":
		nextToken()
		T()
		S_()
	else:
		if (g.kind[g.pToken] == 10) or (g.kind[g.pToken] == 11):
			T()
			S_()


def T():
	if g.kind[g.pToken] == 11: #常数
		U()
	elif g.inputChar[g.pToken+1] == "(":
		Z()
	else:
		if (isVarExist(g.inputChar[g.pToken],g.currentPro.pname,True) is False) and (isVarExist(g.inputChar[g.pToken],g.currentPro.pname,False) is False):
			error(1)
		F()


def U():
	if g.kind[g.pToken] == 11:
		nextToken()


def W():
	if g.inputChar[g.pToken] == "if":
		nextToken()
	else:
		error(4,"if")
		if (g.kind[g.pToken] != 11) and (g.kind[g.pToken] != 10):
			nextToken()
	X()
	judgeSt("then",["integer","read","write"],True)
	N()
	judgeSt("else",["integer","read","write"],True)
	N()


def X():
	R()
	Y()
	R()


def Y():
	if (g.inputChar[g.pToken] == "<") or (g.inputChar[g.pToken] == "<=") or (g.inputChar[g.pToken] == ">") or (g.inputChar[g.pToken] == ">=") or (g.inputChar[g.pToken] == "=") or (g.inputChar[g.pToken] == "<>"):
		nextToken()
	else:
		error(4,"关系运算符")
		if (g.kind[g.pToken] != 11) and (g.kind[g.pToken] != 10):
			nextToken()


def Z():
	if isProExist(g.inputChar[g.pToken]) is False:
		error(1)
	G()
	if g.inputChar[g.pToken] == "(":
		nextToken()
	else:
		error(4,"(")
		if (g.kind[g.pToken] != 10) and (g.kind[g.pToken] != 11):
			nextToken()
	R()
	judgeSt(")",["-","*",";","end"],False)


if __name__ == '__main__':
	init()
	A()
	final()