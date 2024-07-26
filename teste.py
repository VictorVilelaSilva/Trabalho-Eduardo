import sys
from parte1 import *
from classTokens import *

diretorio = 'listas/lista1/EXS1.pas'
lista = analisadorLexico(diretorio)

def main():
    l=[]
    print(lista)
    consome(Tokens.PROGRAM.value)
    consome(Tokens.TKN_VARIAVEIS.value)
    consome(Tokens.TKN_PONTOEVIRGULA.value)
    l.extend(declarations())
    consome(Tokens.BEGIN.value)
    l.extend(stmtList())
    consome(Tokens.END.value)
    consome(Tokens.TKN_PONTO.value)
    print('CÓDIGO COMPILADO COM SUCESSO')


def declarations():
    l = []
    consome(Tokens.VAR.value)
    l.extend(declaration())
    restoDeclaration()
    return l
    

def declaration():
    l=[]
    l.extend(listaIdent())
    consome(Tokens.TKN_DOISPONTOS.value)
    tipo = typeFuncao()
    
    for i in range(len(l)):
        a1 = l[i][0]
        a2 = l[i][1]
        l[i] = (a1, a2, tipo, None)
    consome(Tokens.TKN_PONTOEVIRGULA.value)
    return l
    

def listaIdent():
    l=[]
    l.append(("=", lista[0][1],None,None))
    consome(Tokens.TKN_VARIAVEIS.value)
    l.extend(restoIdentList())
    return l
    

def restoIdentList():
    l=[]
    if Tokens.TKN_VIRGULA.value == lista[0][0]:
        consome(Tokens.TKN_VIRGULA.value)
        l.append(("=", lista[0][1],None,None))
        consome(Tokens.TKN_VARIAVEIS.value)
        l.extend(restoIdentList())
        return l
    # OU VAZIO
    else:
        return l
    

def restoDeclaration():
    if Tokens.TKN_VARIAVEIS.value == lista[0][0]:
        declaration()
        restoDeclaration()
    # OU VAZIO
    else:
        return

def typeFuncao():
    if Tokens.INTEGER.value == lista[0][0]:
        a = 0
        (consome(Tokens.INTEGER.value))
        return a
    # OU
    elif Tokens.REAL.value == lista[0][0]:
        a = 0.0
        (consome(Tokens.REAL.value))
        return a
    # OU
    elif Tokens.STRING.value == lista[0][0]:
        a = ''
        (consome(Tokens.STRING.value))
        return a
    else:      
        print('ERRO, ESPERAVA TOKEN ' + str(encontrar_nome_por_valor(Tokens.INTEGER.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.REAL.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.STRING.value)) + ' TEMOS TOKEN ' + str(encontrar_nome_por_valor(lista[0][0])))
        print('Linha ' + str(lista[0][2]) + ' Coluna ' + str(lista[0][3]))
        exit()

# ------------------------------------------------
# INSTRUÇÕES DOS PROGRAMAS

def bloco():
    consome(Tokens.BEGIN.value)
    stmtList()
    consome(Tokens.END.value)
    consome(Tokens.TKN_PONTOEVIRGULA.value)
    
def stmtList():
    if Tokens.FOR.value == lista[0][0] or Tokens.READ.value == lista[0][0] or Tokens.WRITE.value == lista[0][0] or Tokens.WHILE.value == lista[0][0] or Tokens.TKN_VARIAVEIS.value == lista[0][0] or Tokens.IF.value == lista[0][0] or Tokens.BEGIN.value == lista[0][0] or Tokens.BREAK.value == lista[0][0] or Tokens.CONTINUE.value == lista[0][0] or Tokens.TKN_PONTOEVIRGULA.value == lista[0][0]:
        stmt()
        stmtList()
    # OU VAZIO
    else:
        return

def stmt():
    l=[]
    if Tokens.FOR.value == lista[0][0]:
        l.extend(forStmt())
    # OU
    elif Tokens.READ.value == lista[0][0] or Tokens.WRITE.value == lista[0][0]:
        ioStmt()

    # OU
    elif Tokens.WHILE.value == lista[0][0]:
        whileStmt()

    # OU
    elif Tokens.TKN_VARIAVEIS.value == lista[0][0]:
        atrib()
        consome(Tokens.TKN_PONTOEVIRGULA.value)

    # OU
    elif Tokens.IF.value == lista[0][0]:
        ifStmt()

    # OU
    elif Tokens.BEGIN.value == lista[0][0]:
        bloco()

    # OU
    elif Tokens.BREAK.value == lista[0][0]:
        consome(Tokens.BREAK.value)
        consome(Tokens.TKN_PONTOEVIRGULA.value)

    # OU
    elif Tokens.CONTINUE.value == lista[0][0]:
        consome(Tokens.CONTINUE.value)
        consome(Tokens.TKN_PONTOEVIRGULA.value)

    # OU
    elif Tokens.TKN_PONTOEVIRGULA.value == lista[0][0]:
        consome(Tokens.TKN_PONTOEVIRGULA.value)
        
    else:      
        print('ERRO, ESPERAVA TOKEN ' + str(encontrar_nome_por_valor(Tokens.FOR.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.READ.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.WRITE.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.WHILE.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.TKN_VARIAVEIS.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.IF.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.BEGIN.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.BREAK.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.CONTINUE.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.TKN_PONTOEVIRGULA.value)) + ' TEMOS TOKEN ' + str(encontrar_nome_por_valor(lista[0][0])))
        print('Linha ' + str(lista[0][2]) + ' Coluna ' + str(lista[0][3]))
        exit()


# ----------------------------------------------------------------------------
# DESCRIÇÃO AS INSTRUCOES

def forStmt():
    l=[]
    consome(Tokens.FOR.value)
    a2 = lista[0][1]
    l.extend(atrib())
    consome(Tokens.TO.value)
    endFor()
    consome(Tokens.DO.value)
    stmt() 

def endFor():
    if Tokens.TKN_VARIAVEIS.value == lista[0][0]:
        consome(Tokens.TKN_VARIAVEIS.value)

    # OU
    elif Tokens.TKN_INT.value == lista[0][0]:
        consome(Tokens.TKN_INT.value)
    else:      
        print('ERRO, ESPERAVA TOKEN ' + str(encontrar_nome_por_valor(Tokens.TKN_VARIAVEIS.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.TKN_INT.value)) + ' TEMOS TOKEN ' + str(encontrar_nome_por_valor(lista[0][0])))
        print('Linha ' + str(lista[0][2]) + ' Coluna ' + str(lista[0][3]))
        exit()

def ioStmt():
    l=[]
    if Tokens.READ.value == lista[0][0]:
        consome(Tokens.READ.value)
        consome(Tokens.TKN_ABREPARENTESE.value)
        l.append(("call", "scan", lista[0][1], None))
        consome(Tokens.TKN_VARIAVEIS.value)
        consome(Tokens.TKN_FECHAPARENTESE.value)
        consome(Tokens.TKN_PONTOEVIRGULA.value)
    # OU
    elif Tokens.WRITE.value == lista[0][0]:
        consome(Tokens.WRITE.value)
        consome(Tokens.TKN_ABREPARENTESE.value)
        l.append(("call", "print", lista[0][1], None))
        outList()
        consome(Tokens.TKN_FECHAPARENTESE.value)
        consome(Tokens.TKN_PONTOEVIRGULA.value)
        
    else:      
        print('ERRO, ESPERAVA TOKEN ' + str(encontrar_nome_por_valor(Tokens.READ.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.WRITE.value)) + ' TEMOS TOKEN ' + str(encontrar_nome_por_valor(lista[0][0])))
        print('Linha ' + str(lista[0][2]) + ' Coluna ' + str(lista[0][3]))
        exit()
    return l

def outList():
    out()
    restoOutList()
    
def restoOutList():
    if Tokens.TKN_VIRGULA.value == lista[0][0]:
        consome(Tokens.TKN_VIRGULA.value)
        outList()
    #OU VAZIO
    else:
        return
    
def out():
    if Tokens.TKN_STRING.value == lista[0][0]:
        consome(Tokens.TKN_STRING.value)
    # OU
    elif Tokens.TKN_VARIAVEIS.value == lista[0][0]:
        consome(Tokens.TKN_VARIAVEIS.value)
    # OU
    elif Tokens.TKN_INT.value == lista[0][0]:
        consome(Tokens.TKN_INT.value)
    # OU
    elif Tokens.TKN_FLOAT.value == lista[0][0]:
        consome(Tokens.TKN_FLOAT.value)
        
    else:      
        print('ERRO, ESPERAVA TOKEN ' + str(encontrar_nome_por_valor(Tokens.TKN_STRING.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.TKN_VARIAVEIS.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.TKN_INT.value)) + ' ou ' + str(encontrar_nome_por_valor(Tokens.TKN_FLOAT.value)) +' TEMOS TOKEN ' + str(encontrar_nome_por_valor(lista[0][0])))
        print('Linha ' + str(lista[0][2]) + ' Coluna ' + str(lista[0][3]))
        exit()

def whileStmt():
    consome(Tokens.WHILE.value)
    expr()
    consome(Tokens.DO.value)
    stmt()

def ifStmt():
    consome(Tokens.IF.value)
    expr()
    consome(Tokens.THEN.value)
    stmt()
    elsePart()
    

def elsePart():
    if Tokens.ELSE.value == lista[0][0]:
        consome(Tokens.ELSE.value)
        stmt()
    # OU
    # VAZIO
    else:
        return
# ------------------------------------------------------------------------
# expressoes

def atrib():
    l=[]
    consome(Tokens.TKN_VARIAVEIS.value)
    a1 = lista[0][1]
    consome(Tokens.TKN_ATRIBUICAO.value)

    l.extend(expr())

def expr():

    return orFuncao()

def orFuncao():
    
    andFuncao()
    restoOr()

def restoOr():
    if Tokens.OR.value == lista[0][0]:
        consome(Tokens.OR.value)
        andFuncao()
        restoOr()
    # OU
    # VAZIO
    else:
        return

def andFuncao():
    notFuncao()
    restoAnd()

def restoAnd():
    if Tokens.AND.value == lista[0][0]:
        consome(Tokens.AND.value)
        notFuncao()
        restoAnd()
    # OU
    # VAZIO
    else:
        return


def notFuncao():
    if Tokens.NOT.value == lista[0][0]:
        consome(Tokens.NOT.value)
        notFuncao()
    # OU
    else:
        rel()
        
        

def rel():
    addFuncao()
    restoRel()

def restoRel():
    if Tokens.TKN_IGUALDADE.value == lista[0][0]:
        consome(Tokens.TKN_IGUALDADE.value)
        addFuncao()
    # OU
    elif Tokens.TKN_MAIORMENOR.value == lista[0][0]:
        consome(Tokens.TKN_MAIORMENOR.value)
        addFuncao()
    # OU
    elif Tokens.TKN_MENOR.value == lista[0][0]:
        consome(Tokens.TKN_MENOR.value)
        addFuncao()
    # OU
    elif Tokens.TKN_MENORIGUAL.value == lista[0][0]:
        consome(Tokens.TKN_MENORIGUAL.value)
        addFuncao()

    # OU
    elif Tokens.TKN_MAIOR.value == lista[0][0]:
        consome(Tokens.TKN_MAIOR.value)
        addFuncao()
    # OU
    elif Tokens.TKN_MAIORIGUAL.value == lista[0][0]:
        consome(Tokens.TKN_MAIORIGUAL.value)
        addFuncao()
    # OU
    # VAZIO
    else:
        return


def addFuncao():
    mult()
    restoAdd()

def restoAdd():
    if Tokens.TKN_ADICAO.value == lista[0][0]:
        consome(Tokens.TKN_ADICAO.value)
        mult()
        restoAdd()
    # OU
    elif Tokens.TKN_SUBTRACAO.value == lista[0][0]:
        consome(Tokens.TKN_SUBTRACAO.value)
        mult()
        restoAdd()

    # OU
    # VAZIO
    else:
        return


def mult():
    uno()
    restoMult()

def restoMult():
    if Tokens.TKN_MULTIPLICACAO.value == lista[0][0]:
        consome(Tokens.TKN_MULTIPLICACAO.value)
        uno()
        restoMult()
    # OU
    elif Tokens.TKN_DIVISAO.value == lista[0][0]:
        consome(Tokens.TKN_DIVISAO.value)
        uno()
        restoMult()
    # OU
    elif Tokens.MOD.value == lista[0][0]:
        consome(Tokens.MOD.value)
        uno()
        restoMult()
    # OU
    elif Tokens.DIV.value == lista[0][0]:
        consome(Tokens.DIV.value)
        uno()
        restoMult()
    # OU
    # VAZIO
    else:
        return


def uno():
    if Tokens.TKN_ADICAO.value == lista[0][0]:
        consome(Tokens.TKN_ADICAO.value)
        uno()
    # OU
    elif Tokens.TKN_SUBTRACAO.value == lista[0][0]:
        consome(Tokens.TKN_SUBTRACAO.value)
        uno()
    # OU
    else:
        fator()


def fator():
    if Tokens.TKN_INT.value == lista[0][0]:
        consome(Tokens.TKN_INT.value)
        
    elif Tokens.TKN_FLOAT.value == lista[0][0]:
        consome(Tokens.TKN_FLOAT.value)

    elif Tokens.TKN_VARIAVEIS.value == lista[0][0]:
        consome(Tokens.TKN_VARIAVEIS.value)
        
    elif Tokens.TKN_ABREPARENTESE.value == lista[0][0]:
        consome(Tokens.TKN_ABREPARENTESE.value)
        expr()
        consome(Tokens.TKN_FECHAPARENTESE.value)
            
    elif Tokens.TKN_STRING.value == lista[0][0]:
        consome(Tokens.TKN_STRING.value)
        



# CADA CONSOME DA UM POP NA LISTA
def consome(token_consumido):
    if lista[0][0] == token_consumido:
            lista.pop(0)
            return
    else:      
        print('ERRO, ESPERAVA TOKEN ' + str(encontrar_nome_por_valor(token_consumido)) + ' TEMOS TOKEN ' + str(encontrar_nome_por_valor(lista[0][0])))
        print('Linha ' + str(lista[0][2]) + ' Coluna ' + str(lista[0][3]))
        exit()

def encontrar_nome_por_valor(valor):
    for token in Tokens:
        if token.value == valor:
            return token.name
main()