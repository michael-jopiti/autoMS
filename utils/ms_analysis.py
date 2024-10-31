import os
import pymzml
from . import ms_plots
from collections import defaultdict as ddict

def analyze(argvs):
    ''' Perform analysis depending on inputs detected'''

    # Manage inputs
    # distinguish between single file or directory
    if os.path.isfile(argvs['-i']):
        analyze_file(argvs['-i'], argvs)
    elif os.path.isdir(argvs['-i']):
        analyze_dir(argvs['-i'], argvs)
    else:
        print("-i input is not a file nor a directory")
        return 1

    return 0


def analyze_file(file_path, argvs):
    ''' Perform analysis on a single mzML file, given user inputs '''
    try:
        run = pymzml.run.Reader(file_path)  # Read mzML file
        summarize(run)

        # Correct output path
        output_file = os.path.join(argvs['-o'], f"{os.path.basename(file_path).replace('.mzML', '_peaks.png')}")
        ms_plots.plot_raw_peaks(run, output_file)

    except Exception as e:
        print(f"Error analyzing file {file_path}: {e}")


def analyze_dir(dir_path, argvs):
    ''' Get all files from provided directory and redirect them into analyze_file()'''

    files = os.listdir(dir_path)

    if len(files) < 1:
        print(f"Directory is empty")
        return
    
    print(f"\n{len(files)} files found:")

    for file in files:
        if file.endswith('.mzML'):  # Only process mzML files
            analyze_file(os.path.join(dir_path, file), argvs)
        else:
            print(f"Skipping non-mzML file: {file}")
    return


def summarize(run):
    ''' Print summary from analyzed mzML file'''
    print(
        """
    Summary for mzML file:
        {file_name}
    Run was measured on {start_time} using obo version {obo_version}
    File contains {spectrum_count} spectra
        """.format(**run.info)
    )