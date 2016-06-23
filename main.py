import afn
import config

#NEED TO CONFIG
name = 'meuAutomatoBonitinho'
inPath = 'teste1AfndAfd.in'
outPath = 'teste1AfndAfd.out'

automataTable, start, finals = config.loadAutomata(inPath)
firstAutomata = afn.AF(name, automataTable=automataTable, initialState=start, finalStates=finals)
newAutomata = firstAutomata.convert()
newOptmized = newAutomata.removeUnusedStates()

print()
print('Origin - %s' % firstAutomata)
print()
print('Target - %s' % newAutomata)
print()
print('Optimized - %s' % newOptmized)
print()

optmizedRecipe = newOptmized.copyRecipe()
optimizedStart = newOptmized.getInitialState()
optimizedFinals = newOptmized.getFinalStates()
config.saveAutomata(optmizedRecipe, optimizedStart, optimizedFinals, outPath)