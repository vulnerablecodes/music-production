# Crazy Cassette 88 — v1.0.5

**Manufacturer: Tropix R!X Crazy Jungle Sounds**  
Original stereo cassette performance effect for MPC standalone. Built with the official inMusic MPC Plugin Builder SDK at commit `febd2ca5bd9eb16c4a412837196e145566bc981b`.

This is a compiled hardware-test release, not an AIR product. Original code and graphics approximate the requested Fly Tape II feature categories; proprietary algorithms, sounds, factory presets, branding and artwork are not included. Sonic equivalence is not claimed.

## v1.0.5 — Explicit host notifications for moving reels

The XL user reports that v1.0.4 changes the reel image only when controls are tapped. Neither the earlier parameter-only approach nor the native animated-image flag supplied continuous redraws on that device. This build uses the reporting strategy described in OpenMPC's wrapper: a normal-priority background thread changes Reel Phase and sends `audioMasterAutomate` for that parameter. It avoids `audioMasterUpdateDisplay`, which that project reports can rebuild the screen, close menus and interfere with Q-Link interactions. These host calls are never made from the audio callback.

Both 64-frame reel images now follow explicitly reported cached parameter values. The worker uses a monotonic clock (up to 25 checks per second) and the selected 1/4, 1/2, 3/4 or 9/10 ratio. It runs when SPEED is engaged with Bypass OFF, including pad audition without PLAY. Reverse changes direction. Brake slows the visual motor using the current tempo and selected original duration until it stops. SPEED off or Bypass on freezes it. Host-level insert OFF is external to the plugin's own Bypass control, so do not use animation alone as proof that audio is passing through the insert.

Look for **v1.0.5 • LIVE REELS** and a small **UI nnn** counter below it. With Speed enabled and hands off the controls, the counter and highlighted reel marker should advance. The counter wraps at 999. If the counter or reels remain frozen, report which one; this readout is a diagnostic, not a guarantee of host repaint behavior.

A real-time-paced cached-host test now checks continuous updates without screen taps at all four ratios, rejects notifications from the audio thread, checks no screen-rebuild requests, and checks worker join/no callbacks after close. The worker test also passed ASan/UBSan (LSan disabled for this tracing environment). Speed audio and native SDK host/state/audio checks pass; both ARM binaries validate. This is stronger test coverage of the reporting path, but it does not replace physical MPC XL validation. The audio signal equations are unchanged; the audio-thread UI phase publication was removed to avoid competing with the notifier.

Notification strategy reference (MIT): https://github.com/open-mpc/mpc-vst-plugins/blob/59fb2e8a9c3531270fda00c43e0236fefd893589/wrapper/vst2_wrap.c (DISPLAY_REV_NO_UPDATE / rev_scan / rev_thread). The original thread/phase implementation here is written against the inMusic SDK. See LICENSE-OpenMPC.txt for reference-project attribution. Worker callbacks can have host-specific behavior; the phase control remains non-automatable and absent from Q-Link mappings.

## v1.0.4 — Native-clock animation repair

The user confirmed that the four Speed audio settings work on the XL, but the v1.0.3 reels remain static. This build replaces the displayed parameter-driven reel animation with native `Image` film strips using `animated: true`. The visible reels no longer depend on audio phase notifications, polling of parameter 27, or the transport PLAY flag.

All eight forward/reverse sequences have 400 frames. The four speed choices contain 5, 10, 15 and 18 full revolutions per cycle: the exact relative 1/4, 1/2, 3/4 and 9/10 motor rates. Absolute rotation speed depends on the MPC UI animation clock; it is not calibrated to a physical cassette. Both reels select the same speed/direction. Frame pixel-angle tests verify these ratios and continuous loop closure.

Motion starts when Speed is engaged with Bypass OFF and Brake OFF, even if you are auditioning pads with the sequencer stopped. Speed OFF, Bypass ON or Brake ON shows stationary reels. Brake freezes the native animation immediately rather than showing the audio slowdown curve. Reverse selects backwards animation. These display rules replace the earlier v1.0.3 transport-stop behavior; a native UI timer cannot be claimed to track audio position sample-for-sample.

Audio DSP is unchanged from v1.0.3 except version metadata. The old non-automatable Reel Phase parameter remains at index 27 for compatibility but is not used by the displayed reels. Host/audio/state validation, native animation bindings and frame geometry checks passed; physical XL native-timer display behavior still needs the next on-device test. Look for **v1.0.4 • ANIMATION FIX**.

## v1.0.3 — Speed-dependent reel motion

Both cassette reels now use 64-frame film strips bound to audio-engine phase telemetry. With SPEED engaged, their nominal motion is 0.225, 0.45, 0.675 and 0.81 revolutions per second for 1/4, 1/2, 3/4 and 9/10 respectively. These are illustrative relative motor speeds, not calibrated measurements of a physical cassette. With SPEED off, motion returns to 0.9 revolutions/sec. Bypass shows normal-speed motion; Reverse changes direction and Brake progressively stops it. A valid stopped host transport freezes motion. If no transport information is available, audio callback time drives animation.

The new Reel Phase parameter is appended at index 27, is not automatable and is updated once per audio block without GUI notifications, allocation, locks or I/O. The skin follows it directly rather than using the fixed-rate animated-image option. Its saved phase is incidental display state and has no effect on audio. The other 27 parameter IDs/indices and controls are retained.

Motor-rate/direction/stop tests passed; both image bindings and the normal host/state/audio checks passed. Display polling and frame redraw on a physical XL remain unverified until your next test. The GIF is an illustrative rendering of the shipped assets, not a hardware recording. Look for **v1.0.3 • SPEED + REELS** after replacing the folder and fully restarting.

## v1.0.2 — Speed-first repair

The XL photos showed blank captions in v1.0.1. Fixed the main interface by baking Speed fractions, mode names, all variation-button captions and HOLD into the actual button bitmaps. Those touch targets no longer have text Label overlays. The upstream SDK report https://github.com/inmusic-software/mpc-plugin-builder-sdk/pull/5 documents the hidden-label/touch-interception behavior; this build avoids it rather than relying on an unmerged SDK patch.

Speed's four buttons run **1/4, 1/2, 3/4, 9/10 from top to bottom**, using diagonal fractions. Their saved parameter indices remain 1, 0, 2, 3 respectively; previous presets keep their meanings. Inactive LEDs are black. A visible **v1.0.2 • SPEED FIX** badge below the brand identifies the new skin after a restart.

A continuous 1 kHz signal measured 250, 500, 750 and 900 Hz after live selections in that order, with Speed kept enabled. Caption pixels and clear touch bounds were checked; native host tests passed 20/20 and ARM validation passed with zero warnings. The audio algorithms are unchanged in this focused UI repair; no claim of new hardware validation is made. The CHARACTR/EXTRAS editing-page layout is not the target of this Speed repair. Re-test the four Speed controls on the XL before working through other features.

See SPEED-TEST.txt for the short on-device test.

## Install on MPC XL

1. Extract this ZIP on your computer.
2. At the root of a USB drive or SD card accessible to your MPC, create a folder named **VST2 Plugins**.
3. Copy the entire **Tropix R!X Crazy Jungle Sounds - VST - Crazy Cassette 88** folder into it. Preserve its contents and folder name; do not copy only the .so file.
4. Run **MPC OS 3.10.1 or later**. Enable **Preferences → Enhancements (Beta) → Enable Enhancements** and **External Plugin Support**.
5. Connect the drive and restart/rescan as required by MPC OS. In a track's insert-effect selector, look under **External Plugins** for **Crazy Cassette 88**.
6. Play audio through that track. Start with the Clean preset, Mix 100%, Noise 0%, and modest monitoring level. Toggle SAT or WARBLE to check processing.
7. Test Hold, all effects, tempo changes, automation, and saving/reloading your project before using it in a live set. Test multiple instances to establish the XL CPU budget.

The package includes both **ARM64** (MPC XL) and **ARM32** binaries. Compatibility on other supported MPC models is intended through the SDK, but no physical MPC was available for validation. If your installed OS does not expose External Plugin Support, this package cannot be loaded through this SDK's supported route.

## Performance screen

Eight original cassette designs follow the reference layout and color families: cyan Speed, yellow Saturation, white Mute, green Reverse, orange Warble, blue Lo-Fi, red Brake and purple Stutter. Tap a mode NAME to select its cassette and left-hand sub-controls; use the LARGE PAD BELOW it to engage that effect. LEDs reflect the eight independent enable states. A selected view does not enable an effect. **PERFORM** is the live screen; **CHARACTR** and **EXTRAS** contain the additional controls.

- **Hold ON**: effect buttons latch; tap again to release.
- **Hold OFF**: touch-and-release effect controls use the SDK's `ResetOnGestureEnd` handle. Lift your finger to return that effect to OFF. This interaction requires physical MPC verification. A momentary press on a currently active effect first toggles it off; release leaves it off.
- All 27 user controls are exposed for host automation and saved in project state. The SDK does not expose dedicated pad MIDI triggering to insert effects; these are touchscreen buttons and Q-Link/automation controls.
- Q-Links 1–8 on PERFORM control Speed, Saturation, Mute, Reverse, Warble, Lo-Fi, Brake, Stutter. 9–16 control Noise, Mix, Mode View, Hold, Output, Drive, Warble Depth, Bypass. Other MPC models may bank these controls differently. Momentary release applies to touch gestures, not automatically to physical Q-Link movements.

## Eight independent effects

| Effect | Variations / operation |
|---|---|
| Speed | 1/2, 1/4, 3/4, 9/10. Dual overlapping variable-delay read heads create pitch-lowering varispeed with granular tape artifacts. |
| Saturation | Boost (soft clipping), Amp (asymmetric coloration), Drive (strong symmetric distortion). Drive 0–100%. |
| Mute | Smoothed wet-path cut; use Mix 100% for full silence. |
| Reverse | Backward chunks of already received audio; sizes 1/8, 1/4, 1/2, 1 bar. Edge fades reduce chunk clicks. |
| Warble | Numbered buttons 1–7 select increasing modulation-depth combinations with wow, flutter and randomized drift; continuous Depth control. |
| Lo-Fi | Dust, Cassette, Narrow, 8-bit, 6-bit, 4-bit, Broken, Telephone. Bandwidth reduction, sample-rate/bit-depth reduction, light hiss and periodic dropout combinations. |
| Brake | Decelerates buffered audio to silence over 1/8, 1/2, 1, or 2 quarter-note beats. Release/re-engage to retrigger. |
| Stutter | Frozen rhythmic repeats: 1/2, 1/4, 1/4T, 1/8, 1/8T, 1/16, 1/32, 1/64. Captures preceding audio; original adjustable repeat wear progressively filters/quantizes repeats. |

Note fractions for reverse and stutter use whole-note notation: 1/4 = one quarter-note beat. Brake labels explicitly specify quarter-note beats. At 120 BPM one beat is 500 ms. With no valid host tempo, synchronization falls back to 120 BPM. Reverse and stutter lengths are captured on engagement or size selection; selecting another size restarts the segment immediately. Retrigger to apply a new host tempo without a size change. Brake duration follows the current tempo while braking. Lo-Fi preset names describe this plugin's original algorithms, not measured original-product presets.

## Controls

| Index | Parameter | Range/default |
|---|---|---|
| 0 | Output | −24 to +6 dB, default 0 dB |
| 1 | Noise | Independent hiss level 0–100%, default 0 |
| 2 | Mix | Linear wet/dry 0–100%, default 100 |
| 3 | Bypass | Default off; smoothed unity dry bypass |
| 4 | Hold | Default on; controls touch latch/momentary behavior |
| 5–12 | Eight enable switches | All off by default; separate automatable switches |
| 13 | Tape Speed | Four rates; default 1/2 |
| 14 | Sat Type | Boost / Amp / Drive |
| 15 | Warble Type | Seven variations |
| 16 | Lo-Fi Type | Eight variations |
| 17 | Brake Time | Four durations; default 1 beat |
| 18 | Stutter Rate | Eight documented divisions + hidden legacy 1/16T; default 1/16 |
| 19 | Drive | 0–100%, default 35 |
| 20 | Warble Depth | 0–100%, default 40 |
| 21 | Reverse Size | Four sizes; default 1/4 |
| 22 | Tone | Wet-path low-pass 500–20,000 Hz, default 18,000 Hz |
| 23 | Hiss Tone | Hiss low-pass 800–16,000 Hz, default 7,500 Hz |
| 24 | Edge Fade | Reverse/stutter boundary fade 1–20 ms, default 4 ms |
| 25 | Mode View | Eight cassette/sub-control panels; independent of enable switches |
| 26 | Repeat Wear | 0–100%, default 10; progressive filtering/bit reduction of stutter repeats |

Signal order is fixed: Speed → Reverse → Brake → Stutter → Warble → Saturation → Lo-Fi → Hiss → Mute → Tone/DC removal → Mix → Output. Bypass returns the original dry input at unity. At Mix 0%, hiss is absent. Lo-Fi adds a very small internal texture in addition to independent Noise. Tone and DC removal affect the wet path even with all eight effects disabled; use Mix 0% or Bypass for transparent dry output.

## Eight presets

Clean, Dusty Deck, Half Speed, Quarter Dream, Jungle Crunch, Reverse Dub, Flutter Reel, Stutter 16. A newly loaded stutter preset needs preceding input audio in its history: turn STUTTER off, play audio, then engage it. Saving a project preserves parameters, not the transient tape-buffer audio.

## Implementation limits and test status

- No hardware test has been performed. Touch layout, gesture-release behavior, Q-Link focus rectangles, actual CPU consumption, and host project automation must be checked on the XL.
- Native SDK host-sim passed 20 checks with zero warnings/failures at 44.1 kHz / 128 frames; an additional run passed at 48 kHz / 32 frames with transport playing. Logs are in Verification.
- Direct DSP tests cover 44.1/48/96 kHz; 32/127/128/511/512-frame blocks; every effect plus all effects stacked; finite/bounded output under setting changes; exact dry/bypass; stereo in-place processing; stop/mute behavior. Address/undefined-behavior sanitizer tests also passed. LeakSanitizer cannot run under this environment’s tracing; leak detection was disabled for that run.
- Both ARM binaries passed SDK validation, including architecture, entry point, identity, dependencies, GLIBC, UI handles/assets and skin versions. Compilation is not an on-device compatibility certification.
- Varispeed is a real-time granular approximation with pitch shift and periodic coloration, not offline stretching or transparent pitch-preserving time stretch. Spectral peaks can differ slightly from mathematical target ratios due to the overlapping windows.
- Reverse needs received history and repeats backwards chunks. Stutter freezes a preceding chunk. Empty startup history is silence; this is expected. Edge fades can make very short stutters sound gated.
- Brake durations, Warble and Lo-Fi variations are original choices where exact manufacturer settings/algorithms are unavailable. Warble combines deterministic wow/flutter with smoothed pseudo-random drift; it is not a measured cassette model.
- Saturation is not oversampled and can alias at aggressive drive. There is no limiter; manage Output to avoid clipping. Continuous controls and effect enables are smoothed; changing discrete character modes can produce intentional discontinuities.
- About 14 MiB of delay storage per instance at 44.1/48 kHz (larger at higher rates). No allocation, locks, logging or I/O inside process().
- MPC package only. No AU, VST3, macOS or Windows desktop build is included. A native Linux VST2 test binary is retained in the source test environment, not in the installation folder.

## v1.0.1 changes and reference alignment

The official **Fly Tape II User Guide v1.1**, Operation (desktop and standalone), is the control-layout/behavior reference. See `REFERENCE-ALIGNMENT.md` for the implemented settings and remaining approximation limits. The linked YouTube walkthrough could not be fetched in this environment; no claim is made to have watched or compared its audio.

All eight effects and global controls are available with no activation/trial restrictions. The Clean preset starts the eight enables OFF so it passes audio instead of immediately muting or stopping it. Turn on the effects you want to use; multiple effects can be enabled together.

Existing UID and the first 25 parameter IDs/indices are retained. Mode View and Repeat Wear are appended. The old 1/16-triplet stutter remains at its previous plain-value index for project-chunk compatibility; the correct 1/4-triplet is appended and shown on the performance panel. The host-visible Stutter Rate list therefore has nine entries, eight of which are on the main panel. **Existing normalized Stutter Rate automation may need re-recording because the host range changed from eight to nine choices.**

New tests verify all 36 documented settings affect audio, view selection does not alter enables/audio, and all displayed variation buttons, cassette frames, global faders, LEDs and both Hold branches are bound. Previews are generated from the actual assets and layout, not photographs or screenshots of MPC hardware.

## Rebuild

The Source folder includes the SDK snapshot and plugin source, original skin assets/generator, tests and licensing. From `Source/mpc-plugin-builder-sdk`:

```
python3 tools/build.py "plugins/Crazy Cassette 88"
.sdk-tools/host_sim "plugins/Crazy Cassette 88/build/native/crazy-cassette-88.so" test --seconds 4
python3 tools/package.py "plugins/Crazy Cassette 88"
```

The SDK fetches Zig if needed. Existing `skins/` builds without Pillow. To redraw the artwork, install Pillow and adjust the system font path in `make_skin.py` for your OS, then run it after a native build. The UI generator preserves required duplicate JSON overlay version keys: do not normalize TUI.json with a conventional JSON serializer. Direct tests can be compiled from the plugin directory using `c++ -std=c++17 -O2 -I../../framework tests/dsp_test.cpp -o build/dsp_test` and run there.

## Credits / license / references

Original DSP and graphics: Tropix R!X Crazy Jungle Sounds, MIT. SDK/framework/UI kit: Copyright © 2026 inMusic Brands, Inc., MIT; full license included. No proprietary product binaries, firmware or Steinberg SDK assets are used. Names mentioned for compatibility/comparison belong to their respective owners; no affiliation or endorsement is claimed.

- SDK: https://github.com/inmusic-software/mpc-plugin-builder-sdk
- Feature reference: https://www.airmusictech.com/effects/fly-tape-ii/
- Feature reference: https://support.akaipro.com/en/support/solutions/articles/69000872907-fly-tape-ii-walkthrough-and-faq

Official manual: https://cdn.inmusicbrands.com/Software/SI03/FLYTAPEII/Fly%20Tape%20II%20-%20User%20Guide%20-%20v1.1.pdf

## Release history policy

`revisions.txt` contains the full timestamped history, newest version first. It ships at the ZIP root and inside the plugin folder. `AGENTS.md` makes this a standing project requirement; `releaseHistory` in plugin.json and the bundled packager reject missing, stale or incorrectly ordered history. Use the included `release.py` for the full deliverable. This documentation-only v1.0.3 repack retains the existing binaries.
