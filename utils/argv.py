available_argvs = {"-o": "Output file is: ", 
                   "-i": "Input file is: "}

def argv_parser(argvs):
    ''' parse argvs, returns dictionary of available parsed argvs -> parsed = {flag: input} '''
    # remove first element of list because it's program name
    argvs = argvs[1:]

    # key = flag
    # item = input
    # every even item is a flag if argv[0] is removed from original sys.argv()
    dict_argvs = {}
    for index, element in enumerate(argvs):
        if index % 2 == 0 or index == 0:
            dict_argvs[argvs[index]] = argvs[index + 1]

    parsed, pruned = check_parsed(dict_argvs)
    print_parsed(parsed, pruned)
    return parsed


def check_parsed(argvs):
    ''' Check availability of parsed argvs, returns parsed, pruned'''

    parsed = {}
    pruned = {}

    for item in argvs.keys():
        if item in available_argvs:
            parsed[item] = argvs[item]
        else:
            pruned[item] = argvs[item]

    return parsed, pruned

def print_parsed(parsed, pruned):
    ''' After availabilty of parsed argvs, print to console the treated inputs'''

    if len(parsed) > 0:
        print(f"Inputs parsed [{len(parsed)}]: ")
        for item in parsed:
            print(f"\t{available_argvs[item]} {parsed[item]}")
        
    if len(pruned) > 0:
        print(f"\n Inputs pruned [{len(pruned)}]:")
        for item in pruned:
            print(f"\t{item} {pruned[item]}")