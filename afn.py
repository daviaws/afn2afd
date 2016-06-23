import funcs
from datetime import datetime
from copy import deepcopy

#RETURN CODES
STATE_ALREADY_EXISTS        = 'State Already Exists'
STATE_DONT_EXISTS           = 'State Dont Exists'
NEXT_STATE_DONT_EXISTS      = 'New State Dont Exists'
INITIAL_STATE_NOT_ASSIGNED  = 'Initial State Not Assigned'
OK                          =  'OK'
ACCEPTED                    =  'Entry Accepted'
REJECTED                    =  'Entry Rejected'

#EPSILON
EPSILON = 'eps'

class AF():
    
    def __init__(self, name, automataTable=None, initialState=None, finalStates=None):
        
        self.name = name
        if automataTable:
            self.automataTable = automataTable
        else:
            self.automataTable = {}
        if initialState:
            self.initialState = initialState
        else:
            self.initialState = None
        if finalStates:
            self.finalStates = finalStates
        else:
            self.finalStates = set()
    
    def setInitialState(self, state):
        if state in self.automataTable:
            self.initialState = state
            return OK
        return STATE_DONT_EXISTS
    
    def addFinalState(self, state):
        if state in self.automataTable:
            self.finalStates.add(state)
            return OK
        return STATE_DONT_EXISTS
    
    def addState(self, state):
        if not state in self.automataTable:
            self.automataTable[state] = {}
            return OK
        return STATE_ALREADY_EXISTS
            
    def addTransition(self, state, character, newState):
        if state in self.automataTable:
            if newState in self.automataTable:
                transitions = self.automataTable[state]
                if character in transitions:
                    transitions[character].append(newState)
                else:
                    transitions[character] = [newState]
                return OK
            return NEXT_STATE_DONT_EXISTS    
        return STATE_DONT_EXISTS
    
    def epsTable(self):
        '''
        Retorna tabela de EPISOLON transicoes em ultimo grau de transitividade
        '''
        epsTransitions = {}
        for state in self.automataTable:
            epsTransitions[state] = set([state])
            if EPSILON in self.automataTable[state]:
                epsTransitions[state].update(self.automataTable[state][EPSILON])
                newEpsTransitions = set(epsTransitions[state])
                while 1:
                    for epsState in epsTransitions[state]:
                        if EPSILON in self.automataTable[epsState]:
                            newEpsTransitions.update(self.automataTable[epsState][EPSILON])
                    if epsTransitions[state] != newEpsTransitions:
                        epsTransitions[state] = set(newEpsTransitions)
                    else:
                        break
        return epsTransitions

    def run(self, entry):
        '''
        Roda string de entrada no automato atual
        Retornos:
        Falta estado inicial = 'Initial State Not Assigned''
        Entrada aceita = 'Entry Accepted'
        Entrada rejeitada = 'Entry Rejected'
        '''
        if self.initialState:
            begin = datetime.now()
            epsTransitions = self.epsTable()
            state = epsTransitions[self.initialState]
            for character in entry:
                newState = set()
                print(list(state))
                for q in state:
                    if character in self.automataTable[q]:
                        for transitionState in self.automataTable[q][character]:
                            newTransitions = epsTransitions[transitionState]
                            newState.update(newTransitions)
                state = newState
            end = datetime.now()
            total = end - begin
            print('Ran in {} seconds'.format(total))
            if state.intersection(self.finalStates):
                return ACCEPTED
            return REJECTED
        return INITIAL_STATE_NOT_ASSIGNED
    
    def convert(self):
        '''
        Retorna novo automato em formato Deterministico
        '''
        if self.initialState:
            epsTransitions = self.epsTable()
            
            newName = 'afd.{}'.format(self.name)
            newInitialState = tuple(sorted(epsTransitions[self.initialState]))
            newAutomataTable = {}
            newFinalStates = set()
            
            for newState in funcs.powerset(list(self.automataTable.keys())):
                newState = tuple(sorted(newState))
                newAutomataTable[newState] = {}
                for q in newState:
                    if q in self.finalStates:
                        newFinalStates.add(newState)
                    for transition in self.automataTable[q]:
                        if transition == EPSILON:
                            continue
                        if not transition in newAutomataTable[newState]:
                            newAutomataTable[newState][transition] = set()
                        transitionStates = self.automataTable[q][transition]
                        for transitionState in transitionStates:
                            epsTransitionStates = epsTransitions[transitionState]
                            newAutomataTable[newState][transition].update(epsTransitionStates)
                for transition in newAutomataTable[newState]:
                    conversionTuple = tuple(sorted(newAutomataTable[newState][transition]))
                    conversionSet = set()
                    conversionSet.add(conversionTuple)
                    newAutomataTable[newState][transition] = conversionSet

            return AF(newName, newAutomataTable, newInitialState, newFinalStates)

        return INITIAL_STATE_NOT_ASSIGNED
    

    def removeUnusedStates(self):
        if self.initialState:
            used = set(self.initialState)
            newStates = [self.initialState]
            epsTransitions = self.epsTable()

            newName = 'opt.{}'.format(self.name)
            newAutomataTable = self.copyRecipe()
            newInitialState = self.initialState
            newFinalStates = self.getFinalStates()

            while newStates:
                checkState = newStates.pop()
                for epState in epsTransitions[checkState]:
                    if not epState in used:
                        used.add(epState)
                        newStates.append(epState)
                for character in self.automataTable[checkState]:
                    for targetState in self.automataTable[checkState][character]:
                        if not targetState in used:
                            used.add(targetState)
                            newStates.append(targetState)
            
            toDelete = set(newAutomataTable)
            toDelete.difference_update(used)
            toDelete.add(tuple())
            if toDelete:
                for state in toDelete:
                    del newAutomataTable[state]
                    if state in newFinalStates:
                        newFinalStates.remove(state)

            return AF(newName, newAutomataTable, newInitialState, newFinalStates)
        return INITIAL_STATE_NOT_ASSIGNED

    def copyRecipe(self):
        '''
        Retorna copia de tabela do automato
        '''
        return deepcopy(self.automataTable)

    def getStates(self):
        '''
        Retorna conjunto de estados do automato
        '''
        return set(self.automataTable.keys())
    
    def getInitialState(self):
        '''
        Retorna conjunto de estados do automato
        '''
        return self.initialState

    def getFinalStates(self):
        '''
        Retorna conjunto de estados do automato
        '''
        return set(self.finalStates)

    def getEdges(self):
        '''
        Retorna dict de transições -> { (q1, q2) : [simbol1, simbol2] }
        '''
        edges = {}
        for source in self.automataTable:
            for transition in self.automataTable[source]:
                for target in self.automataTable[source][transition]:
                    key = (source, target)
                    if not key in edges:
                        edges[key] = []    
                    edges[key].append(transition)

        print('Printing the edges: {}'.format(edges))
        return edges

    def __repr__(self):
        attr = self.__dict__
        name = self.__dict__['name']
        return "{}: {}".format(name, str(attr))

