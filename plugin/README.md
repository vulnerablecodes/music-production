# Vintage Military Radio v1.0.14

Eight stereo tape-performance effects with the olive canvas / polished chrome FIELD / CIPHER interface. Vintage Military Radio is a separate plugin identity (VMR8) and can coexist with Crazy Cassette 88 (TW0p).

## Installation and Effects browser

1. Use MPC OS 3.10.1 or newer. Enable Preferences → Enhancements (Beta) → Enable Enhancements and External Plugin Support.
2. Unzip the appropriate package. Copy the complete `Vintage Military Radio` folder directly into `VST2 Plugins` at the drive root; do not nest the ZIP's wrapper directory.
3. Remove stale earlier copies of the *new radio design* installed under Crazy Cassette 88. Keep your original Crazy Cassette folder if desired. Keep one copy of each plugin UID across connected drives to avoid stale/duplicate discovery.
4. Fully restart MPC after copying. Open an audio track/program/mixer insert FX slot, then the Effects browser / External Plugins list; this is an audio effect, not an instrument to create on a Plugin track.
5. If it remains absent, report firmware version, which drive holds the folder, the exact displayed folder name and what happens when selected. Do not modify MPC system files.

The manifest explicitly declares kind=effect, isInstrument=false, two inputs and two outputs. The binary advertises VST effect category and does not set the synth flag. Host tests cannot prove physical MPC browser behavior; device testing is pending.

Select an effect title to show its settings; ENGAGE operates it; HOLD changes latching/momentary behavior. The four cipher barrels are decorative.

Source is built with the inMusic MPC Plugin Builder SDK. To regenerate the skin, build native first, run make_chrome_skin.py, then build all targets. See verification logs and revisions.txt.

The short install folder uses MPC's documented name-only skin lookup fallback. Manufacturer credit remains in metadata. Physical device confirmation is pending.

## Performance workflow
- Tap a chrome effect nameplate to select its Rotor Settings. The amber outline marks the circuit being edited.
- Tap its metal ON/OFF switch to enable or disable that circuit. The switch label and amber LED show its actual state. Selecting a name never disables other effects.
- Adjust readable, matching ivory/chrome setting buttons in the central bay. More parameters remain on CHARACTER/EXTRAS tabs.
- UP is ON and DOWN is OFF. HOLD on latches the circuit switches; HOLD off makes them momentary.
- Noise and Mix use compact horizontal faders below the recorder.
The tape reels use a host-notified UI worker independent of audio processing. Normal tape motion runs with Speed off; Speed/Reverse/Brake affect visual motor motion. It is not a measured transport or audio speed meter. Physical MPC testing of v1.0.14 is pending.

## Chrome switches and reel refresh
Effect switches have larger reflective chrome levers, collars and amber state jewels. UP is ON, DOWN is OFF. Bypass and HOLD use the same finish. Reel phase is displayed through mouse-disabled native filmstrip controls and a native transport value label, to subscribe to MPC parameter refreshes. Desktop clock checks do not prove device repaint behavior; MPC animation testing is pending.

## Vinyl Crackle
The dedicated Vinyl Crackle slider adds procedural record clicks and short filtered crackles independently of tape Noise. Default is 0%. Mix blends the wet signal and Bypass returns the dry signal; Mute also silences crackle. No audio samples or downloads are required.

Radio Static and White Noise have main-page sliders. SOUNDS exposes Tape, Vinyl, Radio, White, Brown and Mains Hum levels plus 50/60 Hz mains selection. All new layers default to zero, follow Mix/Mute/Bypass, and synthesize locally without audio samples. Rotary switch pointers up indicate ON; down indicates OFF.
