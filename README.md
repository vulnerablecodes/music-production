# Vintage Military Radio — FIELD / CIPHER Chrome

**v1.0.13** · Eight stereo tape effects by **Tropix R!X Crazy Jungle Sounds**.

![Animated showcase of all eight effects](media/vintage-military-radio-eight-effects.gif)

v1.0.13 test package prepared; release publication pending device test. · [MP4 showcase](media/vintage-military-radio-eight-effects.mp4)

Original olive canvas and polished chrome artwork, ivory keys, amber indicators and animated reels. Speed, Saturation, Mute, Reverse, Warble, Lo-Fi, Brake and Stutter operate independently. Select an effect title to show its settings; its ivory ON/OFF switch enables or disables it; HOLD changes latching/momentary behavior. NOISE and MIX use horizontal faders. Cipher barrels are decorative. The silent animation demonstrates UI assets, not a recording from MPC hardware.

## Installation and the Effects tab

Use MPC OS 3.10.1 or newer with Enhancements and External Plugin Support enabled. Extract the installer for your architecture and copy the entire `Vintage Military Radio` folder directly into `VST2 Plugins` at the drive root.

Keep one installed copy of each plugin UID across connected drives. Remove earlier copies of the radio design installed under its old name. **Fully restart MPC after copying**, then select it from an audio track/program/mixer **insert FX** slot and the Effects / External Plugins browser.

Vintage Military Radio uses the distinct UID `VMR8` and binary filenames `vintage-military-radio-arm32.so` / `vintage-military-radio-arm64.so`. Both manifest and binary explicitly identify a stereo effect, with no instrument or MIDI flag. A separately retained local plugin can coexist under its own UID.

## Verification and source

ARM32, ARM64 and native builds completed. SDK validation reports zero errors or warnings; the native host simulator passed 20 checks. Device testing confirms separate effect discovery in v1.0.8. The v1.0.13 short-folder skin lookup remains pending physical MPC testing.

The source-and-both-architectures release includes the SDK framework/tools, generated skins, source, verification logs and revision history. Its project is under `Source/mpc-plugin-builder-sdk/plugins/Vintage Military Radio`. Use the SDK build tools to build native, run `make_chrome_skin.py`, then build all targets and run `release.py`. This repository keeps the editable project source and master artwork; generated installable assets are in the release.



## v1.0.13 controls and animation fixes

The chrome/canvas layout and enlarged circuit panel are retained. All eight effects now use metal toggle switches: UP = ON, DOWN = OFF, with state labels and amber lamps. Nameplates select the circuit's Rotor Settings independently of its enable state.

Noise, Mix, Bypass and reel sprite frames now exactly match their native control sizes, fixing clipping caused by MPC drawing sprites without scaling. Noise/Mix frames are 320x42, Bypass 225x48, and reel frames 64x64.

Animation uses a host-notified UI worker, with a normal motor rate when Speed is off. Native no-audio testing confirms continuous frame updates, bypass, suspend/resume and clean worker teardown. Audio simulation passed 20 checks, SDK validation reports 0 errors/warnings, and 16 mode/HOLD touch-layout scenarios plus all main-screen sprite dimensions pass. Physical MPC confirmation remains pending. No catalog PR submitted.

## v1.0.13 polished switches and native reel controls

All eight effect switches now have larger 66-pixel plates with supersampled reflective chrome levers, collars, dark cast shadows, and amber jewels. Bypass and HOLD share the same finish on 56-pixel plates. UP = ON, DOWN = OFF. The chrome/canvas layout and exact-sized fader frames remain intact.

Reel phase now drives read-only native filmstrip Knob widgets inside mouse-disabled components, with a native Value label subscribing to the same parameter. This replaces Image-only reel bindings that the owner reported were frozen on MPC. Desktop idle/bypass/resume/teardown clock tests pass, but the native repaint change still needs physical MPC confirmation. No new catalog PR submitted.
