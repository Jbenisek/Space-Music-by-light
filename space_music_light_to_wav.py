import subprocess
import sys

# Auto-install missing packages
def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# Ensure required packages are available
try:
    import os
    import numpy as np
    import soundfile as sf
    from astropy.io import fits
    import h5py
except ImportError:
    install("numpy")
    install("soundfile")
    install("astropy")
    install("h5py")
    import os
    import numpy as np
    import soundfile as sf
    from astropy.io import fits
    import h5py

# WAV output sample rate
sample_rate = 44100

# Create output directory
output_dir = "converted_wav"
os.makedirs(output_dir, exist_ok=True)

# Scan and convert .fits and .h5 files
for filename in os.listdir('.'):
    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    try:
        if ext == '.fits':
            with fits.open(filename) as hdul:
                data = hdul[0].data
                if data is None:
                    print(f"[SKIP] {filename} has no data")
                    continue
                data = data.flatten()
                data -= np.mean(data)
                data /= np.max(np.abs(data))
                data_int16 = np.int16(data * 32767)
                sf.write(os.path.join(output_dir, f"{name}.wav"), data_int16, sample_rate)
                print(f"[OK] Converted {filename}")

        elif ext == '.h5':
            with h5py.File(filename, 'r') as h5file:
                for key in h5file.keys():
                    dataset = h5file[key][()]
                    if dataset.ndim > 1:
                        dataset = dataset.flatten()
                    dataset -= np.mean(dataset)
                    dataset /= np.max(np.abs(dataset))
                    data_int16 = np.int16(dataset * 32767)
                    out_path = os.path.join(output_dir, f"{name}_{key}.wav")
                    sf.write(out_path, data_int16, sample_rate)
                    print(f"[OK] Converted {filename} [{key}]")

    except Exception as e:
        print(f"[ERR] Failed to process {filename}: {e}")
