from utils import argv, ms_analysis
import sys, time, pyfiglet

def main():
    print(pyfiglet.figlet_format("autoMS"))

    start_time = time.time()

    # parse argvs (check availability, print parsed/pruned, return available)
    if len(sys.argv) < 2:
        print("No inputs provided, please run with -h or read the documentation :D")
        return 1
    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        argv.help()
        return 1
    
    argvs = argv.argv_parser(sys.argv)

    ms_analysis.analyze(argvs)    

    end_time = time.time() - start_time
    print(f"\nAnalysis concluded in: {end_time:.4f} seconds")
    return 0


if __name__ == "__main__":
    main()