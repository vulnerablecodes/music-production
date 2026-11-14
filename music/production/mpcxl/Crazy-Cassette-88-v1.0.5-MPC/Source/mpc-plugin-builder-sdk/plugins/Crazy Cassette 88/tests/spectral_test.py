"""Run after dsp_test; verify four varispeed settings on a 440 Hz input."""
from pathlib import Path
import numpy as np
p = Path(__file__).resolve().parents[1] / "build"
for mode, target in [(-1,440),(0,220),(1,110),(2,330),(3,396)]:
    x = np.fromfile(p / f"speed-{mode}.f32", dtype=np.float32)[44100:]
    spectrum = abs(np.fft.rfft(x * np.hanning(len(x))))
    frequency = np.fft.rfftfreq(len(x), 1/44100)
    peak = frequency[spectrum.argmax()]
    assert abs(peak-target) < 10, (mode, peak, target)
    print(f"PASS mode {mode}: {peak:.2f} Hz, nominal {target} Hz (granular approximation)")
