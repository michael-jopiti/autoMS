from src.utils import argv
from src.analysis.ms_analysis import analyze
import sys, time, pyfiglet

def main():
    """
    Available inputs:

    Mandatory:
        - `-i` : Input file or directory
        - `-o` : Output file or directory

    Optional:
        - `-sum` : Provides a summary output in the terminal
        - `-a` : Specifies the analysis type, with options 'median' or 'mean'
        - `-stat` : Prints descriptive statistics, with options for output in 'console' or 'file'
        - `-mz` : Outputs m/z intensities
        - `-3d` : Generates a 3D plot of the entire chromatogram
    """
        
    print(pyfiglet.figlet_format("autoMS"))

    # Parse arguments
    if len(sys.argv) < 2:
        print("No inputs provided, please run with -h or read the documentation :D")
        return 1
    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        print(main.__doc__)
        return 0
    
    start_time = time.time()

    argvs = argv.argv_parser(sys.argv)

    # Start analysis
    analyze(argvs)

    end_time = time.time() - start_time
    print(f"\nComplete analysis elapsed: {end_time:.4f} seconds")
    return 0

if __name__ == "__main__":
    main()
