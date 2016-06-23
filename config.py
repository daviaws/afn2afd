def loadAutomata(path):
    f = open(path)
    f = f.read()
    f = f.lower()
    f = f.split('\n')
    
    #Decode header
    tmp = []
    header = f[0]
    header = header.split('|')
    for line in header:
        element = line.strip()
        if element:
            tmp.append(element)
    header = tmp

    #Decode body
    tmp = []
    body = f[1:]
    start = None
    finals = set()
    for line in body:
        if line:
            tmp2 = []
            splittedLine = line.split('|')
            for item in splittedLine:
                item = item.strip()
                if item:
                    if ',' in item:
                        item = item.split(',')
                        tmp3 = []
                        for i in item:
                            tmp3.append(i.strip())
                        item = sorted(tmp3)
                        tmp2.append(item)
                    else:
                        s = False
                        f = False
                        if '*' in item:
                            item = item[:-1]
                            f = True
                        if '--' in item:
                            item = item[2:]
                            s = True
                        if s:
                            start = item
                        if f:
                            finals.add(item)
                        tmp2.append([item])
            tmp.append(tmp2)
    body = tmp

    tableLength = len(header)
    automataTable = {}
    for line in body:
        source = line[0][0]
        automataTable[source] = {}
        source = automataTable[source]
        for x in range(tableLength):
            character = header[x]
            target = []
            for item in line[x+1]:
                if item != '-':
                    target.append(item)
            source[character] = target

    return (automataTable, start, finals)

def saveAutomata(recipe, start, finals, path):
    firstCol = 'state'
    spaces = 30
    f = open(path, 'w')

    states = recipe.keys()
        
    alphabet = set()
    for state in states:
        for character in recipe[state]:
            alphabet.add(character)
    alphabet = sorted(list(alphabet))

    #Header
    line = '{}'.format(firstCol).center(spaces)
    line += '|'
    for item in alphabet:
        line += '{}'.format(item).center(spaces)
        line += '|'
    line += '\n'

    f.write(line)

    #Body
    for state in states:
        strstate = str(state)
        if start in state:
            strstate = '--' + strstate
        if state in finals:
            strstate = strstate + '*'
        line = '{}'.format(state).center(spaces)
        line += '|'
        for character in alphabet:
            if isinstance(recipe[state][character], set):
                target = str(recipe[state][character])[1:-1]
            else:
                target = str(recipe[state][character])
            if target == '()':
                target = '-'

            line += '{}'.format(target).center(spaces)
            line += '|'
        line += '\n'
        f.write(line)

    f.close()