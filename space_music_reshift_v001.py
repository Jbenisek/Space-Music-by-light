# Space Music Redshift Processor
# Requirements: install necessary libraries
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import numpy as np
    import soundfile as sf
    from scipy import signal
except ImportError:
    install("numpy")
    install("soundfile")
    install("scipy")
    import numpy as np
    import soundfile as sf
    from scipy import signal

# Load original signal
input_file = "original_15s_am.wav"
data, sr = sf.read(input_file)

# Stretch factor to simulate cosmic redshift
stretch_factor = 10
stretched = signal.resample(data, int(len(data) * stretch_factor))

# Add space-like noise
noise = np.random.normal(0, 0.02, len(stretched))
stretched_noisy = stretched + noise

# Save redshifted signal
output_file = "stretched_15s_am.wav"
sf.write(output_file, stretched_noisy, int(sr / stretch_factor))

print(f"✅ Done. Redshifted signal saved to: {output_file}")
