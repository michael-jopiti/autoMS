import os, pymzml
from datetime import datetime
from ..utils.loading import loading_bar
from ..utils.print import print_table

def analyze(argvs):
    ''' Before true analysis, sanity check of input/output and respective dispatch depending if dir or file'''

    # Manage inputs
    # distinguish between single file or directory
    if os.path.isfile(argvs['-i']):
        if check_output_file(argvs['-o']):
            analyze_file(argvs['-i'], argvs)
        return 1
    elif os.path.isdir(argvs['-i']):
        if check_output_dir(argvs['-o']):
            analyze_dir(argvs['-i'], argvs)
        return 1
    else:
        print("-i input is not a file nor a directory")
        return 1


def analyze_file(file_path, argvs, multiple=False):
    ''' Perform analysis on a single mzML file, given user inputs '''
    try:
        run = pymzml.run.Reader(file_path)  # Read mzML file

        if argvs['-sum']:
            if multiple:
               return summarize(run, multiple=True)
            else: 
                summarize(run)

        # if '-ms' in argvs.keys():
        #     run = analysis_type.ms_trim(run, argvs['-ms'])

        if argvs['-rt']:
            output_file = os.path.join(argvs['-o'], f"{os.path.basename(file_path).replace('.mzML', '_peaks.png')}")
            ms_plots.plot_mz_rt(run, output_file)

        if argvs['-mz']:
            output_file = os.path.join(argvs['-o'], f"{os.path.basename(file_path).replace('.mzML', '_peaks.png')}")
            ms_plots.plot_mz_intensity(run, output_file)

        # if argvs['-3d']:
        #     output_file = os.path.join(argvs['-o'], f"{os.path.basename(file_path).replace('.mzML', '_3d.png')}") 
        #     ms_plots.plot_3d(run, output_file)

        if argvs['-stat']:
            print("\t\tTODO: implement basic descriptive statistics")

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"Error analyzing file {file_path}: {e}")

def analyze_dir(dir_path, argvs):
    ''' Get all files from provided directory and redirect them into analyze_file()'''

    files = os.listdir(dir_path)

    if len(files) < 1:
        print(f"Directory is empty")
        return
    
    mzml_files = [file for file in files if file.endswith('.mzML')]  # Only process mzML files
    total_files = len(mzml_files)

    if total_files < 1:
        print("No .mzML files found in the directory.")
        return
    
    print(f"\nSummarizing {total_files} files:")
    
    analyzed = []
    loading_bar(0, total_files)

    for i, file in enumerate(mzml_files):
        global current_file  # Declare a global variable to hold the current file name
        current_file = file  # Set the current file name
        
        # Analyze the file
        analyzed.append(analyze_file(os.path.join(dir_path, file), argvs, multiple=True))
        
        # Update loading bar after analyzing each file
        loading_bar(i + 1, total_files)

    print_table(analyzed[0].keys(), [list(result.values()) for result in analyzed])

    return 0

def summarize(run, multiple=False):
    ''' Print summary from analyzed mzML file'''
    # spin_thread = spin.start()

    specs = {
        "file_name": run.info['file_name'],
        "start_time": datetime.strptime(run.info['start_time'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d @ %H:%M:%S"),
        "spectra": run.info['spectrum_count'],
        "ms1_spectra": len([spec for spec in run if spec.ms_level == 1]),
        "ms2_spectra": len([spec for spec in run if spec.ms_level == 2]),
        "ms1_percentage": f"{(len([spec for spec in run if spec.ms_level == 1]) / int(run.info['spectrum_count']) * 100):.2f}",
        "ms2_percentage": f"{(len([spec for spec in run if spec.ms_level == 2]) / int(run.info['spectrum_count']) * 100):.2f}"
    }

    # spin.stop(spin_thread)
    if multiple:
        return specs
    else:
        print(f"\tSummary for file: {specs['file_name']}\n\t\tStart time: {specs['start_time']}\
              \n\t\tSpectra found: {specs['spectra']}\
              \n\t\t\tMS1 spectra represent {specs['ms1_percentage']:.2f}% ({specs['ms1_spectra']}/{specs['spectra']})\
              \n\t\t\tMS2 represent {specs['ms2_percentage']:.2f}% ({specs['ms2_spectra']}/{specs['spectra']})\n")


def check_output_file(argv):
    ''' Boolean return if argv is file '''
    if os.path.isfile(argv):
        return True
    print("Error: provided output is not a file (not matching input type)")

def check_output_dir(argv):
    ''' Boolean return if argv is directory'''
    if os.path.isdir(argv):
        return True
    print("Error: provided output is not a directory (not matching input type)")
