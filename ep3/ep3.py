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

import math
import random
from collections import defaultdict
import util


# **********************************************************
# **            PART 01 Modeling BlackJack                **
# **********************************************************


class BlackjackMDP(util.MDP):
    """
    The BlackjackMDP class is a subclass of MDP that models the BlackJack game as a MDP
    """
    def __init__(self, valores_cartas, multiplicidade, limiar, custo_espiada):
        """
        valores_cartas: list of integers (face values for each card included in the deck)
        multiplicidade: single integer representing the number of cards with each face value
        limiar: maximum number of points (i.e. sum of card values in hand) before going bust
        custo_espiada: how much it costs to peek at the next card
        """
        self.valores_cartas = valores_cartas
        self.multiplicidade = multiplicidade
        self.limiar = limiar
        self.custo_espiada = custo_espiada

    def startState(self):
        """
         Return the start state.
         Each state is a tuple with 3 elements:
           -- The first element of the tuple is the sum of the cards in the player's hand.
           -- If the player's last action was to peek, the second element is the index
              (not the face value) of the next card that will be drawn; otherwise, the
              second element is None.
           -- The third element is a tuple giving counts for each of the cards remaining
              in the deck, or None if the deck is empty or the game is over (e.g. when
              the user quits or goes bust).
        """
        return (0, None, (self.multiplicidade,) * len(self.valores_cartas))

    def actions(self, state):
        """
        Return set of actions possible from |state|.
        You do not must to modify this function.
        """
        return ['Pegar', 'Espiar', 'Sair']

    def succAndProbReward(self, state, action):
        """
        Given a |state| and |action|, return a list of (newState, prob, reward) tuples
        corresponding to the states reachable from |state| when taking |action|.
        A few reminders:
         * Indicate a terminal state (after quitting, busting, or running out of cards)
           by setting the deck to None.
         * If |state| is an end state, you should return an empty list [].
         * When the probability is 0 for a transition to a particular new state,
           don't include that state in the list returned by succAndProbReward.
        """
        # BEGIN_YOUR_CODE

        hand = state[0] #state[0][0]
        peek = state[1] #state[0][1]
        deck = state[2] #state[0][2]

        # print("minha mão é ") #TEST
        # print(hand) #TEST
        # print("meu peek é") #TEST
        # print(peek) #TEST
        # print("meu deck é") #TEST
        # print(deck) #TEST

        #primeiro, ver a condicao de parada
        if deck == None:
            #print("ENTREI NO DECK NONE") #TEST
            return []

        #se ele nao parou, vamos ver como esta o deck
        #ver o numero de cartas que faltam no deck e "quais sao"
        decksize = 0
        possible = 0

        for card in deck:
            if card > 0:
                possible = possible+1
            decksize = decksize+card

        # print("meu deck tem %d cartas de %d tipos" % (decksize, possible)) #TEST

        #se nao tem mais cartas no deck, hora de sair e receber meu reward
        if action == 'Sair':
            # print("ENTREI NO ACTION SAIR") #TEST
            return [((hand, None, None), 1, hand)]

        #nada pra parar aconteceu, hora de ver estados pra retornar
        states = []
        
        #colocar os estados possiveis caso ele queira pegar
        if action == "Pegar":
            # print("HORA DE PEGAR CARTINHAS") #TEST
            prize = 0 #premio por pegar cartas
            if peek == None:
                # print("NAO TEM PEEK") #TEST
                #pega aleatoriamente
                i = 0 #contador do indice
                for card in deck:
                    #so tem chance de pegar cartas que nao sao 0 (prob > 0)
                    if card > 0:
                        # edita o deck para tirar a carta
                        value = self.valores_cartas[i] #valor da carta nesse indice
                        # print(deck) #TEST
                        # print("estou pegando  do deck a carta de indice %d, cujo naipe é %d com card = %d" % (i, value, card)) #TEST
                        new_deck = list(deck)
                        new_deck[i] = new_deck[i]-1
                        new_deck = tuple(new_deck)
                        if hand+value > self.limiar: #extinguir o deck caso o limiar estoure
                            new_deck = None
                        if decksize-1 == 0: #fugir caso pegue a ultima carta
                            new_deck = None
                            prize = hand+value
                        states.append(((hand+value, peek, new_deck), card/decksize, prize))
                    i = i+1
                    # print("oi eu sou o i = %d" % i) #TEST
            else:
                #pega a carta que espiou
                new_deck = list(deck)
                new_deck[peek] = new_deck[peek]-1
                new_deck = tuple(new_deck)
                states.append(((hand+self.valores_cartas[peek], None, new_deck), 1, prize))

            return states

        if action == "Espiar":
            if peek == None:
                #só pode fazer o peek se não tiver peekado antes
                i = 0
                for card in deck:
                    if card > 0:
                        states.append(((hand, i, deck), 1/possible, -self.custo_espiada))
                    i = i+1
            else:
                return []
            return states

        return states

        # END_YOUR_CODE

    def discount(self):
        """
        Return the descount  that is 1
        """
        return 1

# **********************************************************
# **                    PART 02 Value Iteration           **
# **********************************************************

class ValueIteration(util.MDPAlgorithm):
    """ Asynchronous Value iteration algorithm """
    def __init__(self):
        self.pi = {}
        self.V = {}

    def solve(self, mdp, epsilon=0.001):
        """
        Solve the MDP using value iteration.  Your solve() method must set
        - self.V to the dictionary mapping states to optimal values
        - self.pi to the dictionary mapping states to an optimal action
        Note: epsilon is the error tolerance: you should stop value iteration when
        all of the values change by less than epsilon.
        The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
        """
        mdp.computeStates()
        def computeQ(mdp, V, state, action):
            # Return Q(state, action) based on V(state).
            return sum(prob * (reward + mdp.discount() * V[newState]) \
                            for newState, prob, reward in mdp.succAndProbReward(state, action))

        def computeOptimalPolicy(mdp, V):
            # Return the optimal policy given the values V.
            pi = {}
            for state in mdp.states:
                pi[state] = max((computeQ(mdp, V, state, action), action) for action in mdp.actions(state))[1]
            return pi
        V = defaultdict(float)  # state -> value of state
        # Implement the main loop of Asynchronous Value Iteration Here:
        # BEGIN_YOUR_CODE

        solved = False

        while not solved:
            #value iteration yay    
            Vline = defaultdict(lambda: -math.inf)
            for s in mdp.states:
                for a in mdp.actions(s):
                    Q = computeQ(mdp, V, s, a)
                    if Q > Vline[s]:
                        Vline[s] = Q
            solved = True
            for v, vl in zip(V, Vline):
                if abs(V[v]-Vline[vl]) > epsilon:
                    solved = False
            V = {**Vline}
        
        # END_YOUR_CODE

        # Extract the optimal policy now
        pi = computeOptimalPolicy(mdp, V)
        # print("ValueIteration: %d iterations" % numIters)
        self.pi = pi
        self.V = V

# First MDP
MDP1 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=10, custo_espiada=1)

# Second MDP
MDP2 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=15, custo_espiada=1)

def geraMDPxereta():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action for at least 10% of the states.
    """
    # BEGIN_YOUR_CODE
    MDPx = BlackjackMDP(valores_cartas=[5, 10], multiplicidade=4, limiar=15, custo_espiada=1)

    return MDPx
    # END_YOUR_CODE


# **********************************************************
# **                    PART 03 Q-Learning                **
# **********************************************************

class QLearningAlgorithm(util.RLAlgorithm):
    """
    Performs Q-learning.  Read util.RLAlgorithm for more information.
    actions: a function that takes a state and returns a list of actions.
    discount: a number between 0 and 1, which determines the discount factor
    featureExtractor: a function that takes a state and action and returns a
    list of (feature name, feature value) pairs.
    explorationProb: the epsilon value indicating how frequently the policy
    returns a random action
    """
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def getQ(self, state, action):
        """
         Return the Q function associated with the weights and features
        """
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    def getAction(self, state):
        """
        Produce an action given a state, using the epsilon-greedy algorithm: with probability
        |explorationProb|, take a random action.
        """
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    def getStepSize(self):
        """
        Return the step size to update the weights.
        """
        return 1.0 / math.sqrt(self.numIters)

    def incorporateFeedback(self, state, action, reward, newState):
        """
         We will call this function with (s, a, r, s'), which you should use to update |weights|.
         You should update the weights using self.getStepSize(); use
         self.getQ() to compute the current estimate of the parameters.

         HINT: Remember to check if s is a terminal state and s' None.
        """
        # BEGIN_YOUR_CODE
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

def identityFeatureExtractor(state, action):
    """
    Return a single-element list containing a binary (indicator) feature
    for the existence of the (state, action) pair.  Provides no generalization.
    """
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

# Large test case
largeMDP = BlackjackMDP(valores_cartas=[1, 3, 5, 8, 10], multiplicidade=3, limiar=40, custo_espiada=1)

# **********************************************************
# **        PART 03-01 Features for Q-Learning             **
# **********************************************************

def blackjackFeatureExtractor(state, action):
    """
    You should return a list of (feature key, feature value) pairs.
    (See identityFeatureExtractor() above for a simple example.)
    """
    # BEGIN_YOUR_CODE
    raise Exception("Not implemented yet")
    # END_YOUR_CODE
