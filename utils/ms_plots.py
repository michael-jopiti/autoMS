import os
import pymzml
import matplotlib.pyplot as plt


def plot_raw_peaks(run, output_file="plot.png"):
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
        import numpy as np
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