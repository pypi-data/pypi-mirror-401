import pathlib

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert


def powcompress(signal, exponent):
    """Power law compression (MATLAB: powcompress)"""
    return np.power(np.abs(signal), exponent)


def dbzero(signal):
    """Convert to dB scale relative to max value"""
    signal_abs = np.abs(signal)
    signal_max = np.max(signal_abs)
    if signal_max == 0:
        return 20 * np.log10(signal_abs + 1e-10)
    return 20 * np.log10(signal_abs / signal_max + 1e-10)


def sizeOfFile(filepath):
    """Get file size in bytes"""
    return pathlib.Path(filepath).stat().st_size


def readGenoutSlice(filepath, time_indices, ncoordsout, idx_coords):
    """Read ultrasound data from binary file
    filepath: path to genout.dat
    time_indices: array of time indices to read
    ncoordsout: total number of coordinates
    idx_coords: indices of coordinates to extract (typically transducer indices)

    Returns: [n_time, n_selected_coords] array
    """
    nRun = len(time_indices)
    n_selected = len(idx_coords)

    pxducer = np.zeros((nRun, n_selected), dtype=np.float32)

    with pathlib.Path(filepath).open("rb") as f:
        for t_idx, t in enumerate(time_indices):
            # Seek to the correct position (4 bytes per float)
            f.seek(t * ncoordsout * 4)
            # Read all coordinates at this time step
            data = np.fromfile(f, dtype=np.float32, count=ncoordsout)
            # Extract selected coordinates
            pxducer[t_idx, :] = data[idx_coords]

    return pxducer


def focusProfile(fcen, xducercoords, speed_scaled):
    """Calculate delay profile for focusing
    fcen: [lateral_idx, depth_idx] focus center
    xducercoords: [n_elements, 3] transducer coordinates
    speed_scaled: speed of sound in scaled units (dT/dY * c0)

    Returns: delay profile (indices to add to time dimension)
    """
    n_elements = xducercoords.shape[0]
    fcen_pos = np.array([fcen[0], fcen[1]])  # Focus center position

    # Distance from each transducer to focus point
    distances = np.linalg.norm(xducercoords[:, :2] - fcen_pos, axis=1)

    # Convert distances to time delays (samples)
    dd = distances / speed_scaled

    return dd


# ============================================================================
# MAIN BEAMFORMING LOOP
# ============================================================================

# Parameters (SET THESE BASED ON YOUR SETUP)
lambda_val = 1.0  # Wavelength
nY = 100  # Number of y points
dY = 1.0  # Y spacing
wX = 100.0  # Width in X
dtheta = 1.0  # Angular spacing (degrees)
nangles = 11  # Number of angles
c0 = 1540.0  # Speed of sound (m/s)
dT = 1e-6  # Time step
fnumber = 1  # F-number for focusing

# Create depth and lateral position arrays
deps = np.arange(1e-3, nY * dY, lambda_val / 8)
lats = np.arange(-wX / 2, wX / 2 + lambda_val / 8, lambda_val / 8)

# Initialize beamformer output
bm = np.zeros((len(lats), len(deps), nangles))

# Figure handles for interactive plotting
fig1 = plt.figure(figsize=(10, 8))
fig2 = plt.figure(figsize=(10, 8))
fig3 = plt.figure(figsize=(10, 8))

# Read initial data to find synchronization peak
base_dir = "/kulm/scratch/lesion"
n_init = round(nangles / 2)
outdir = f"{base_dir}{n_init}/"

try:
    ncoordsout = 64  # Total number of output coordinates (ADJUST AS NEEDED)
    nRun = sizeOfFile(f"{outdir}genout.dat") // (4 * ncoordsout)

    # For now, assuming you have transducer coordinates
    # Replace with your actual coordinate loading
    outcoords = np.random.randn(ncoordsout, 3)  # Placeholder
    idxducer = np.where(outcoords[:, 2] == 1)[0]
    xducercoords = outcoords[idxducer, :]

    # Read initial transducer data
    pxducer = readGenoutSlice(f"{outdir}genout.dat", np.arange(nRun), ncoordsout, idxducer)

    # Display raw data
    ax3 = fig3.add_subplot(111)
    ax3.imshow(powcompress(pxducer, 1 / 4), aspect="auto", cmap="gray")
    ax3.set_title("Raw Transducer Data")

    # Find synchronization peak
    px = pxducer[:, pxducer.shape[1] // 2]
    analytic_signal = hilbert(px)
    idt0 = np.argmax(np.abs(analytic_signal))

    print(f"Synchronization index: {idt0}")

    # Main beamforming loop over angles
    for n in range(nangles):
        theta = (n - (nangles + 1) / 2) * dtheta * np.pi / 180  # Convert to radians

        print(f"Processing angle {n + 1}/{nangles}: theta = {np.degrees(theta):.2f}°")

        # Read data for this angle
        outdir = f"{base_dir}{n}/"
        nRun = sizeOfFile(f"{outdir}genout.dat") // (4 * ncoordsout)
        pxducer = readGenoutSlice(f"{outdir}genout.dat", np.arange(nRun), ncoordsout, idxducer)

        # Update figure 3 with current angle data
        ax3.clear()
        ax3.imshow(powcompress(pxducer, 1 / 4), aspect="auto", cmap="gray")
        ax3.set_title(f"Transducer Data - Angle {n}")
        plt.pause(0.01)

        # Delay-and-sum beamforming for each lateral/depth position
        idps = {}  # Store indices for each pixel

        for ii in range(len(lats)):
            lat = lats[ii]

            for jj in range(len(deps)):
                dep = deps[jj]

                # Focus center calculation
                fcen = np.array([lat / dY + np.mean(xducercoords[:, 0]), dep / dY])

                # Select elements within F-number
                max_dist = fcen[1] / fnumber
                idx_elements = np.where(np.abs(xducercoords[:, 0] - fcen[0]) <= max_dist)[0]

                if len(idx_elements) == 0:
                    idps[ii, jj] = np.array([], dtype=int)
                    continue

                # Calculate focus delays
                speed_scaled = dT / dY * c0
                dd = focusProfile(fcen, xducercoords[idx_elements, :], speed_scaled)

                # Calculate time index (propagation delay)
                idt = idt0 + round(2 * dep / c0 / dT)

                # Calculate linear indices into flattened pxducer array
                # idp = (element_idx) * nRun + time_idx
                idp = (idx_elements * nRun) + (idt + np.round(dd)).astype(int)

                # Filter valid indices
                valid = (idp > 0) & (idp < nRun * len(idxducer))
                idps[ii, jj] = idp[valid]

        # Sum over selected indices for each pixel
        for ii in range(len(lats)):
            for jj in range(len(deps)):
                if len(idps[ii, jj]) > 0:
                    # Flatten pxducer for indexing
                    pxducer_flat = pxducer.T.flatten()
                    bm[ii, jj, n] = np.sum(pxducer_flat[idps[ii, jj]])

        # Display beamformed image for current angle
        ax1 = fig1.add_subplot(111)
        ax1.clear()
        beamdata_single = dbzero(np.abs(hilbert(bm[:, :, n].T)))
        im1 = ax1.imshow(
            beamdata_single,
            extent=[lats[0], lats[-1], deps[-1], deps[0]],
            cmap="gray",
            vmin=-50,
            vmax=0,
            aspect="auto",
        )
        ax1.set_xlabel("Lateral Position (mm)")
        ax1.set_ylabel("Depth (mm)")
        ax1.set_title(f"Beamformed Image - Angle {n}")
        plt.colorbar(im1, ax=ax1, label="dB")
        plt.pause(0.01)

        # Display accumulated average image
        ax2 = fig2.add_subplot(111)
        ax2.clear()
        beamdata_avg = dbzero(np.abs(hilbert(np.mean(bm[:, :, : n + 1], axis=2).T)))
        im2 = ax2.imshow(
            beamdata_avg,
            extent=[lats[0], lats[-1], deps[-1], deps[0]],
            cmap="gray",
            vmin=-50,
            vmax=0,
            aspect="auto",
        )
        ax2.set_xlabel("Lateral Position (mm)")
        ax2.set_ylabel("Depth (mm)")
        ax2.set_title(f"Averaged Beamformed Image (n=1:{n + 1})")
        plt.colorbar(im2, ax=ax2, label="dB")
        plt.pause(0.01)

    plt.show()

except FileNotFoundError as e:
    print(f"Error: {e}")
    print(f"Could not find data files in {base_dir}")
