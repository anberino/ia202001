"""
  AO PREENCHER ESSE CABECALHO COM O MEU NOME E O MEU NUMERO USP,
  DECLARO QUE SOU A UNICA PESSOA AUTORA E RESPONSAVEL POR ESSE PROGRAMA.
  TODAS AS PARTES ORIGINAIS DESSE EXERCICIO PROGRAMA (EP) FORAM
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUCOES
  DESSE EP E, PORTANTO, NAO CONSTITUEM ATO DE DESONESTIDADE ACADEMICA,
  FALTA DE ETICA OU PLAGIO.
  DECLARO TAMBEM QUE SOU A PESSOA RESPONSAVEL POR TODAS AS COPIAS
  DESSE PROGRAMA E QUE NAO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUICAO. ESTOU CIENTE QUE OS CASOS DE PLAGIO E
  DESONESTIDADE ACADEMICA SERAO TRATADOS SEGUNDO OS CRITERIOS
  DIVULGADOS NA PAGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NAO SERAO CORRIGIDOS E,
  AINDA ASSIM, PODERAO SER PUNIDOS POR DESONESTIDADE ACADEMICA.

  Nome : Gabriel Sarti Massukado
  NUSP : 10284177

  Referencias: Com excecao das rotinas fornecidas no enunciado
  e em sala de aula, caso voce tenha utilizado alguma referencia,
  liste-as abaixo para que o seu programa nao seja considerado
  plagio ou irregular.

  Exemplo:
  - O algoritmo Quicksort foi baseado em:
  https://pt.wikipedia.org/wiki/Quicksort
  http://www.ime.usp.br/~pf/algoritmos/aulas/quick.html
"""

import util

############################################################
# Part 1: Segmentation problem under a unigram model

class SegmentationProblem(util.Problem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state):
        """ Metodo que implementa verificacao de estado """
        return True

    def initialState(self):
        """ Metodo que implementa retorno da posicao inicial """
        return ("", self.query) # [palavras separadas, letras que faltam]

    def actions(self, state):
        """ Metodo que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        actions = []

        for i in range(len(state[1])+1): #olha pras letras que faltam
            actions.append(i)

        return actions


    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        add, rest = state[1][:action], state[1][action:]

        newState = (state[0] + " " + add, rest)

        return newState


    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        if state[1] == "":
            return True
        
        return False

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """

        newWord = state[1][:action]
        
        cost = self.unigramCost(newWord)

        return cost


def segmentWords(query, unigramCost): #unigramCost é uma funcao de custo

    if len(query) == 0:
        return ''
    
    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)

    problem = SegmentationProblem(query, unigramCost)

    goal = util.uniformCostSearch(problem)

    return goal.state[0][1:]

    # END_YOUR_CODE

############################################################
# Part 2: Vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.Problem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills
        self.queryWords.insert(0, util.SENTENCE_BEGIN)

    def isState(self, state):
        """ Metodo  que implementa verificacao de estado """
        return True

    def initialState(self):
        """ Metodo  que implementa retorno da posicao inicial """
        
        return ("", tuple(self.queryWords), "") #frase sendo montada (frase), palavras que faltam (words), palavra pra comparar (ref)

    def actions(self, state):
        """ Metodo  que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        
        actions = []



        if state[2] == "":
            fills1 = self.getFills(state[1][0])
            fills2 = self.getFills(state[1][1])
        else:
            fills1 = {state[2]}
            fills2 = self.getFills(state[1][0])
        
        for i in fills1:
            for j in fills2:
                actions.append([i, j])

        return actions

    def getFills(self, fillable):
        fills = self.possibleFills(fillable)
        if len(fills) < 1:
            return {fillable}
        
        return fills


    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        
        if state[2] == "":
            frase = state[0] + " " + str(action[0])
            ref = str(action[0])
        else:
            frase = state[0] + " " + str(action[1])
            ref = str(action[1])

        words = list(state[1])

        if len(words) > 1:
            words = words[1:]
        else:
            words = []

        words = tuple(words)

        newState = (frase, words, ref)

        return newState

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        return len(state[1]) < 1

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        cost = self.bigramCost(action[0], action[1])
        return cost




def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)

    if len(queryWords) == 0:
        return ''
    
    problem = VowelInsertionProblem(queryWords, bigramCost, possibleFills)

    goal = util.uniformCostSearch(problem)

    return goal.state[0][9:]
    # END_YOUR_CODE

############################################################


def getRealCosts(corpus='corpus.txt'):

    """ Retorna as funcoes de custo unigrama, bigrama e possiveis fills obtidas a partir do corpus."""
    
    _realUnigramCost, _realBigramCost, _possibleFills = None, None, None
    if _realUnigramCost is None:
        print('Training language cost functions [corpus: '+ corpus+']... ')
        
        _realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
        _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')

        print('Done!')

    return _realUnigramCost, _realBigramCost, _possibleFills

def main():
    """ Voce pode/deve editar o main() para testar melhor sua implementacao.

    A titulo de exemplo, incluimos apenas algumas chamadas simples para
    lhe dar uma ideia de como instanciar e chamar suas funcoes.
    Descomente as linhas que julgar conveniente ou crie seus proprios testes.
    """
    unigramCost, bigramCost, possibleFills  =  getRealCosts()
    
    resulSegment = segmentWords('believeinyourselfhavefaithinyourabilities', unigramCost)
    print(resulSegment)

    resultInsert = insertVowels('smtms ltr bcms nvr'.split(), bigramCost, possibleFills)
    print(resultInsert)

if __name__ == '__main__':
    main()
