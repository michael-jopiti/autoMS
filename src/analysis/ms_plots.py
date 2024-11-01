import os
import pymzml
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_mz_rt(run, output_file="plot_m/z_RetentionTime.png"):
    ''' Plot intensities against RT'''
    # Initialize lists for retention times and intensities
    retention_times = []
    intensities = []

    # Get the peaks from the Total Ion Chromatogram (TIC)
    tic_peaks = run["TIC"].peaks()

    # Check if there are any peaks in the TIC
    if tic_peaks is not None and len(tic_peaks) > 0:  # Check for None and length
        for peak in tic_peaks:
            # Ensure peak has the expected structure
            if len(peak) == 2:  # Ensure there are two values to unpack
                retention_times.append(peak[0])  # RT
                intensities.append(peak[1])       # Intensity
            else:
                print(f"Unexpected peak format: {peak}")

    # Check if we have data to plot
    if retention_times and intensities:
        # Convert intensities to a NumPy array for easier processing
        intensities_np = np.array(intensities)

        # Calculate median intensity
        median_intensity = np.median(intensities_np)

        # Create a scatter plot
        plt.figure(figsize=(12, 8))

        # Plot points below median in red and above median in blue
        below_median = intensities_np < median_intensity
        plt.scatter(np.array(retention_times)[below_median], intensities_np[below_median], color='red', s=1, alpha=0.5, label='Below Median')
        plt.scatter(np.array(retention_times)[~below_median], intensities_np[~below_median], color='blue', s=1, alpha=0.5, label='Above Median')

        # Customize plot
        plt.title(f"All peaks raw from {run.info['file_name']}")
        plt.xlabel('RT [minutes]')
        plt.ylabel('Intensity')
        plt.legend()
        plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight') 
        plt.close()
    else:
        print("No peaks found in the TIC to plot.")

    
def plot_mz_intensity(run, output_file="plot_m/z_intensities_peaks.png"):
    ''' Plot every m/z and intensities per spectrum '''

    # Create the output directory path by removing the .png extension
    output_dir = output_file.rsplit(".", 1)[0]
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

    p = pymzml.plot.Factory()

    for spectrum in run:
        if spectrum.ms_level == 2:  # Filter by MS level if needed
            p.new_plot()  # Initialize new plot for each spectrum

            # Add peaks to the plot with a specific style and color
            p.add(spectrum.peaks("centroided"), color=(0, 0, 0), style="sticks", name="peaks")

            # Define output filename for each spectrum plot within the new directory
            spectrum_filename = f"{os.path.basename(output_dir)}_{spectrum.ID}.html"
            output_path = os.path.join(output_dir, spectrum_filename)

            # Save the plot with custom layout settings
            p.save(
                filename=output_path,
                layout={
                    "xaxis": {
                        "ticks": 'outside',
                        "ticklen": 2,
                        "tickwidth": 0.25,
                        "showgrid": False,
                        "linecolor": 'black',
                    },
                    "yaxis": {
                        "ticks": 'outside',
                        "ticklen": 2,
                        "tickwidth": 0.25,
                        "showgrid": False,
                        "linecolor": 'black',
                    },
                    "plot_bgcolor": 'rgba(255, 255, 255, 0)',
                    "paper_bgcolor": 'rgba(255, 255, 255, 0)',
                },
            )
            print(f"Plotted file: {output_path}")



def plot_3d(run, output_file):
    ''' Plot 3D plots with X: m/z (MS2), Y: retention time, Z: intensity'''

    # Filter for MS2 spectra
    spectra = [spectrum for spectrum in run if spectrum.ms_level == 2]

    # Prepare data lists
    mz_values = []           # To store m/z values
    retention_times = []     # To store retention times
    intensities = []         # To store intensities

    # Collect data from each spectrum
    for spectrum in spectra:
        for mz, intensity in spectrum.highest_peaks(len(spectrum.peaks('centroided'))):  # Assuming highest_peaks returns [(m/z, intensity), ...]
            mz_values.append(mz)
            retention_times.append(spectrum.scan_time_in_minutes())  # Assuming scan_time_in_minutes() returns time in minutes
            intensities.append(intensity)

    # Check for missing data
    if not mz_values or not retention_times or not intensities:
        print("No data available for plotting.")
        return

    # Create a 3D plot
    fig = plt.figure(figsize=(10, 7))  # Set figure size
    ax = fig.add_subplot(111, projection='3d')

    # Plotting with plasma color map, inverting intensity for color
    sc = ax.scatter(mz_values, retention_times, intensities, c=[-i for i in intensities], cmap='plasma', marker='o', s=60, alpha=0.7, edgecolor='none')

    # Add color bar
    cbar = plt.colorbar(sc)
    cbar.set_label('Intensity (inverted)', fontsize=12)
    cbar.ax.tick_params(labelsize=10)

    # Labeling the axes
    ax.set_xlabel('m/z', fontsize=14)
    ax.set_ylabel('RT (min)', fontsize=14)
    ax.set_zlabel('Intensity', fontsize=14)

    # Set viewing angle
    ax.view_init(elev=30, azim=210)  # Adjust elevation and azimuth

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.6)

    # Improve axis limits if needed
    ax.set_xlim([min(mz_values), max(mz_values)])
    ax.set_ylim([min(retention_times), max(retention_times)])
    ax.set_zlim([0, max(intensities) * 1.1])  # Slightly higher limit for aesthetics

    # Save the plot to a file
    plt.tight_layout()  # Adjust layout to fit labels
    plt.savefig(output_file)
    plt.close()  # Close the plot to free up memory

    print(f"\n\n\t3D Plot saved as {output_file}")