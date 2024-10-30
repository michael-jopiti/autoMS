from utils import argv, ms_analysis
import sys, time, pyfiglet

def  main():
    print(pyfiglet.figlet_format("autoMS"))

    start_time = time.time()

    # parse argvs (check availability, print parsed/pruned, return available)
    argvs = argv.argv_parser(sys.argv)

    ms_analysis.analyze(argvs)    

    end_time = time.time() - start_time
    print(f"\nAnalysis concluded in: {end_time:.4f} seconds")
    return 0


if __name__ == "__main__":
    main()