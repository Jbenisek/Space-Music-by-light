import soundfile as sf
import numpy as np
from scipy import signal

# Load stretched, redshifted signal
data, sr = sf.read("stretched_15s_am.wav")

# Downsample 10× to match original time length
downsampled = signal.resample_poly(data, up=1, down=10)

# Demodulate AM: Envelope detection
envelope = np.abs(signal.hilbert(downsampled))

# Light noise filtering
sos = signal.butter(4, 0.1, 'lowpass', output='sos')
filtered = signal.sosfilt(sos, envelope)

# Normalize
filtered -= np.mean(filtered)
filtered /= np.max(np.abs(filtered))

# Save at correct sample rate
sf.write("reconstructed_cleaned.wav", filtered, 44100)

print("✅ Fully corrected file saved as: reconstructed_cleaned.wav")
