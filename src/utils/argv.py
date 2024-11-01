available_argvs = {"-o": "Output: ", 
                   "-i": "Input: ",
                   "-sum": "Print summary per file: ",
                   "-a": "Analysis type: ",
                   "-stat": "Descriptive statistics on: ",
                   "-rt": "Plot RT's intensities: ",
                   "-mz": "Plot m/z's intensities: ",
                   "-3d": "3D plot of m/z, RT and intensities: ",
                   "-ms": "MS level: "}

boolean_argvs = ["-sum", "-stat", "-mz", "-rt", "-3d"]


def argv_parser(argvs):
    ''' parse argvs, returns dictionary of available parsed argvs -> parsed = {flag: input} '''
    # remove first element of list because it's program's name
    argvs = argvs[1:]

    # key = flag
    # item = input
    # every even item is a flag if argv[0] is removed from original sys.argv()
    
    # Define baseline argvs with default, if user provides something, baseline will be overwritten
    dict_argvs = {"-sum": False,
                  "-stat": False,
                  "-mz": False,
                  "-rt": False,
                  "-3d": False,
                  "-a": "median"}
    
    for index, element in enumerate(argvs):
        if '-' in element:
            if element in boolean_argvs:
                dict_argvs[argvs[index]] = True
            else:
                dict_argvs[argvs[index]] = argvs[index + 1]

    parsed, pruned = check_parsed(dict_argvs)
    print_parsed(parsed, pruned)
    return parsed


def check_parsed(argvs):
    ''' Check availability of parsed argvs, returns parsed, pruned'''

    parsed = {}
    pruned = {}

    for item in argvs.keys():
        # Default False or Empty do not need to be printed
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
            if parsed[item]:
                print(f"\t{available_argvs[item]} {parsed[item]}")
        
    if len(pruned) > 0:
        print(f"\n Inputs pruned [{len(pruned)}]:")
        for item in pruned:
            print(f"\t{item} {pruned[item]}")


def str_to_bool(s):
    return s.lower() in ('true', '1', 't', 'y', 'yes')