import json
import re
from typing import List
from functions import  is_integer, is_float, errorCatch, handleTokensAritimeticos, handleTokensSimbolos, handleTokensLogicos, obter_valor_simbolo, errorCatchStringComentario
from enum import Enum

#####################################Analisador Léxico (Pascal)################################
# percorre o arquivo e retorna os tokens

# padrao = r'([a-zA-Z][a-zA-Z0-9_]*|<>|=|:=|>=|<=|<|>|:|[\d.]+|[a-zA-Z0-9]+| |\S)' #Gabriel
padrao = r'(\d+[a-zA-Z_][a-zA-Z0-9_]*|[a-zA-Z_][a-zA-Z0-9_]*|<>|=|:=|>=|<=|<|>|:|[\d.]+| |\S)' #Victor

def getTokens(pascalExerciseContent: str) -> List[dict]:

    intRegex = r'^[0-9]+$'
    floatRegex = r'[0-9]+\.[0-9]+'
    variableRegex = r'[a-zA-Z][a-zA-Z0-9_]*'
    # variableRegex = r'^[a-zA-Z][a-zA-Z0-9]*$'

    lista = []
    tokensAritimeticos = []
    tokensLogicosRelacionaisAtri = []
    palavrasReservadas = []
    tokensSimbolos = []
    variaveis = []
    stringsArray = []
    inteirosArray = []
    comentariosArray = []
    floatsArray = []
    string = ""
    
    
    linha = 0
    coluna = 0
    linhaString = 0
    stringStart = 0
    linhaComentario = 0
    colunaComentario = 0

    modoString = False
    dentroComentario = False

    for line in pascalExerciseContent.split('\n'):
        linha += 1
        coluna = 1

        # verifica se a linha é um comentário
        tempLine = line.lstrip()

        if (modoString):
            errorCatchStringComentario(linhaString, stringStart, actualLine)

        if(tempLine.startswith('//')):
            coluna = coluna+2
            
            continue

        # percorre a linha por palavra
        for word in re.findall(padrao, line):
           
            # if not line.startswith(word) and not word.isspace(): 
            if(word == ' '):
                coluna = coluna+1
                continue
            #faz com que ocorra uma espaco entre as palavras da string
            if(modoString):
                string += " "
                
            # verifica se a palavra é uma palavra reservada
            if (word in palavrasReservadasRegras) and not modoString and not dentroComentario:
                lista.append([obter_valor_simbolo(word),word,linha,coluna])
                coluna += (len(word))
                continue

            elif (is_float(word)):
                simbolo = 'tkn_float'
                lista.append([obter_valor_simbolo(simbolo), word,linha,coluna])
                coluna += (len(word))
                continue
            
            elif (is_integer(word)):
                simbolo = 'tkn_int'
                lista.append([obter_valor_simbolo(simbolo), word,linha,coluna])
                coluna += (len(word))
                continue
            
            
            # verifica se a palavra não é uma palavra reservada e é uma variável
            elif (word not in palavrasReservadasRegras) and (word not in tokensLogicosRelacionaisAtriRegras)and (re.fullmatch(variableRegex, word) and not modoString and not dentroComentario):

                simbolo = 'tkn_variaveis'
                lista.append([obter_valor_simbolo(simbolo),word,linha,coluna])
                coluna += (len(word))
                continue

            # verifica se a palavra é um tokensLogicosRelacionaisAtri
            elif (word in tokensLogicosRelacionaisAtriRegras) and not modoString and not dentroComentario:
                simbolo = handleTokensLogicos(word)
                lista.append([obter_valor_simbolo(simbolo),word,linha,coluna])
                coluna += (len(word))
                continue
            
            # verifica se o caractere é um tokensAritimeticos
            elif (word in tokensAritimeticosRegras) and not modoString and not dentroComentario:
                simbolo = handleTokensAritimeticos(word)
                lista.append([obter_valor_simbolo(simbolo),word,linha,coluna])
                coluna += (len(word))
                continue
            # verifica se o caractere é um tokenSimbolo
            elif(word in tokensSimbolosRegras) and not modoString and not dentroComentario:
                simbolo = handleTokensSimbolos(word)

                lista.append([obter_valor_simbolo(simbolo),word,linha,coluna])
                coluna += (len(word))
                continue
            
            # percorre a palavra por caractere
            for caractere in word:
                coluna += 1
                # verifica se esta no modo string
                if modoString:
                    string+=caractere
                    if caractere == "'":
                        modoString = False
                        stringsArray.append(['tkn_string',string[:-1],linha,stringStart])
                        simbolo = 'tkn_string'
                        lista.append([obter_valor_simbolo(simbolo),string[:-1],linha,stringStart])
                        string = ""
                    continue  
               
                # verifica se o caractere é um espaço
                if (caractere == r'\s'):
                    variableBuilder = "" 
                    continue

                # verifica se o caractere é um string
                elif caractere == "'" and not dentroComentario:
                    stringStart = coluna
                    linhaString = linha
                    actualLine = line
                    modoString = True
                    continue
                
                # ativa o modo de comentario
                elif (caractere == '{') and not modoString and not dentroComentario:
                    dentroComentario = True
                    linhaComentario = linha
                    colunaComentario = coluna
                    lineComentario = line
                    textoComentario = caractere  # Inicia o texto do comentário com '{'
                    
                    continue
            
                # Se estiver dentro de um comentário, acumula o texto
                elif dentroComentario:
                    textoComentario += caractere  # Acumula texto do comentário
                    
                    if caractere == '}':
                        dentroComentario = False
                        # Adiciona o comentário acumulado ao array
                        textoComentario = ""  # Reinicia para o próximo comentário
                    continue

                else:
                    errorCatch(linha, line, word) 
    if(dentroComentario):
        errorCatchStringComentario(linhaComentario, colunaComentario, lineComentario)        
            

    tokensDict = {
        'tokensAritimeticos': tokensAritimeticos,
        'tokensLogicosRelacionaisAtri' : tokensLogicosRelacionaisAtri,
        'palavrasReservadas' : palavrasReservadas,
        'tokensSimbolos' : tokensSimbolos,
        'variaveis' : variaveis,
        'strings' : stringsArray,
        'inteiros' : inteirosArray,
        'floats' : floatsArray,
        'comentarios' : comentariosArray
    }
    return tokensDict, lista


tokensAritimeticosRegras: List[str] = [
    '+',
    '-',
    '*',
    '/'
]

tokensLogicosRelacionaisAtriRegras: List[str]  = [
    '<>',
    '>',
    '>=',
    '<',
    '<=',
    ':=',
    '=' 
]

palavrasReservadasRegras: List[str] = [
    'program',	
    'var',
    'integer',
    'real',
    'string',
    'begin',
    'boolean',
    'end',
    'for',
    'to',
    'while',
    'do',
    'breal',
    'continue',
    'if',
    'else',
    'then',
    'write',
    'read',
    'mod',
    'div',
    'or',
    'and',
    'not',
]

tokensSimbolosRegras: List[str] = [
    ';',
    ',',
    '.',
    ':',
    '(',
    ')',
]

  
def analisadorLexico(arquivo):
    # Abre o arquivo informado como argumento
    try:
        with open(arquivo, 'r') as pascalExercise:
            pascalExerciseContent = pascalExercise.read()
        
        tokenDict, lista = getTokens(pascalExerciseContent)

        resultadoJson = json.dumps(lista)
        with open('resultado.json', 'w') as criarArquivo:
            criarArquivo.write(resultadoJson)

        return lista


            
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")

