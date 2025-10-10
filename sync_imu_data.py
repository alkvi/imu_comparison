import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.interpolate import interp1d

def set_xvalues(polygon, x0, x1):
    _ndarray = polygon.get_xy()
    _ndarray[:, 0] = [x0, x0, x1, x1, x0]
    polygon.set_xy(_ndarray)

# def update(val):
#     new_lag = lag_slider.val
#     for i in range(0, len(stim_polygons)):
#         poly = stim_polygons[i]
#         onset = onsets[i]
#         duration = durations[i]
#         set_xvalues(poly, onset+new_lag, onset+new_lag+duration)
#     fig.canvas.draw_idle()

if __name__ == "__main__":

    # Where all the data is stored
    pq_file = "data/apdm/apdm_subj1_outside_imu_data.parquet"
    csv_file = "data/actigraph/actigraph_subj1_outside/data_acc.csv"

    fs_opal = 128
    fs_actigraph = 30

    imu_data = pd.read_parquet(pq_file)
    imu_subject = list(imu_data.columns)[0].split("/")[0]

    # Get acc data for session
    session = "test"
    seek_column = session + "/LUMBAR/Accelerometer"
    acc_data = imu_data.filter(regex=seek_column).to_numpy()
    print("Using pq file " + pq_file)
    print(imu_data.head())

    # Actigraph acc
    actigraph_data = pd.read_csv(csv_file)
    actigraph_acc = actigraph_data[['Accelerometer X', 'Accelerometer Y', 'Accelerometer Z']].to_numpy()

    # Create time axes
    t_actigraph = np.arange(0, len(actigraph_acc)) / fs_actigraph
    t_opal = np.arange(0, len(acc_data)) / fs_opal

    #Plot in two subplots
    fig, axs = plt.subplots(2, 1, figsize=(14, 8), sharex=False)
    axs[0].plot(t_opal, acc_data[:, 0], label='Opal X')
    axs[0].set_title('Opal Accelerometer')
    axs[0].set_ylabel('Acceleration (g)')
    axs[0].legend()
    axs[1].plot(t_actigraph, actigraph_acc[:, 0], label='ActiGraph X', color='orange')
    axs[1].set_title('ActiGraph Accelerometer')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Acceleration (g)')
    axs[1].legend()
    plt.tight_layout()
    plt.show()

    # Interpolate ActiGraph to Opal's time base
    interp_func = interp1d(t_actigraph, actigraph_acc[:, 0], kind='linear', fill_value="extrapolate")
    actigraph_resampled = interp_func(t_opal)

    # Slider
    best_lag = 0
    def update(val):
        new_lag = int(lag_slider.val * fs_opal)
        line_acti.set_ydata(np.roll(actigraph_resampled, new_lag))
        fig.canvas.draw_idle()

    fig, ax = plt.subplots(figsize=(14, 6))
    plt.subplots_adjust(left=0.25, bottom=0.25)
    line_opal, = ax.plot(t_opal, acc_data[:, 0], label='Opal')
    line_acti, = ax.plot(t_opal, np.roll(actigraph_resampled, best_lag), label='ActiGraph')
    ax.legend()

    lag_seconds = 0
    lim_low = -300
    lim_high = 300
    slider_axis = plt.axes([0.25, 0.1, 0.65, 0.03])
    lag_slider = Slider(slider_axis, 'Lag (s)', lim_low, lim_high, valinit=lag_seconds, valstep=1)
    lag_slider.on_changed(update)
    plt.show()

    final_lag = lag_slider.val
    print(f"Lag is: {final_lag}")

    # Now trim the file to specified start point
    lag_samples = fs_actigraph * np.abs(final_lag)
    actigraph_data_trimmed = actigraph_data.iloc[lag_samples:]
    actigraph_data_trimmed.to_csv(csv_file.replace(".csv", "_trimmed.csv"), index=False)
