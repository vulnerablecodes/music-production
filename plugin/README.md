# Vintage Military Radio v1.0.8

Eight stereo tape-performance effects with the olive canvas / polished chrome FIELD / CIPHER interface. Vintage Military Radio is a separate plugin identity (VMR8) and can coexist with Crazy Cassette 88 (TW0p).

## Installation and Effects browser

1. Use MPC OS 3.10.1 or newer. Enable Preferences → Enhancements (Beta) → Enable Enhancements and External Plugin Support.
2. Unzip the appropriate package. Copy the complete `Tropix R!X Crazy Jungle Sounds - VST - Vintage Military Radio` folder directly into `VST2 Plugins` at the drive root; do not nest the ZIP's wrapper directory.
3. Remove stale earlier copies of the *new radio design* installed under Crazy Cassette 88. Keep your original Crazy Cassette folder if desired. Keep one copy of each plugin UID across connected drives to avoid stale/duplicate discovery.
4. Fully restart MPC after copying. Open an audio track/program/mixer insert FX slot, then the Effects browser / External Plugins list; this is an audio effect, not an instrument to create on a Plugin track.
5. If it remains absent, report firmware version, which drive holds the folder, the exact displayed folder name and what happens when selected. Do not modify MPC system files.

The manifest explicitly declares kind=effect, isInstrument=false, two inputs and two outputs. The binary advertises VST effect category and does not set the synth flag. Host tests cannot prove physical MPC browser behavior; device testing is pending.

Select an effect title to show its settings; ENGAGE operates it; HOLD changes latching/momentary behavior. The four cipher barrels are decorative.

Source is built with the inMusic MPC Plugin Builder SDK. To regenerate the skin, build native first, run make_chrome_skin.py, then build all targets. See verification logs and revisions.txt.
