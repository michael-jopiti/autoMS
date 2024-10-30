import os
import pymzml

def analyze(argvs):
    ''' Perform analysis depending on inputs detected'''

    input_file = None
    input_diretory = None

    if os.path.isfile(argvs['-i']):
        analyze_file(argvs['-i'], argvs)
    elif os.path.isdir(argvs['-i']):
        analyze_dir(argvs['-i'], argvs)
    else:
        print("-i input is not a file nor a directory")
        return 

    output_file = None
    output_directory = None
    if os.path.isfile(argvs['-o']):
        input_file = argvs['-o']
    elif os.path.isdir(argvs['-o']):
        input_diretory = argvs['-o']
    else:
        print("-o input is not a file nor a directory")
        return 

def analyze_file(file, argvs):
    ''' Perform analysis on file, given user inputs '''
    print(f"\nCurrently analyzing {file}")
    print("... Analysis ... ")


def analyze_dir(dir, argvs):
    ''' Get all files from provided directory and redirect them into analyze_file()'''

    if len(os.listdir(dir)) < 1:
        print(f"Directory is empty")

    for file in os.listdir(dir):
        analyze_file(file, argvs)

    return