# Reference alignment — v1.0.5

Reference: AIR/MSXII Fly Tape II User Guide v1.1, Operation. Manufacturer identity and artwork remain original to Tropix R!X Crazy Jungle Sounds.

| Control | Implemented behavior |
|---|---|
| Mode names | Select one of eight cassette views and expose its settings, without changing enable switches. |
| Large mode pads | Engage eight independent effects; separate LEDs display enable state. |
| Hold | ON latches pads; OFF uses touch-release reset. Multiple effect enables may coexist. |
| Speed | Four displayed rates: 1/2, 1/4, 3/4, 9/10. |
| Saturation | Amp, Boost, Drive selectors; original DSP with additional Drive amount. |
| Mute | Wet-path cut, smoothed to avoid clicks. At partial Mix the dry signal remains. |
| Reverse | Buffered backwards chunks; additional Reverse Size setting on CHARACTR/EXTRAS. |
| Warble | Seven numbered selectors, increasing depth coefficients; wow/flutter plus random drift. |
| Lo-Fi | Eight numbered selectors; eight original degradation recipes. |
| Brake | Four numbered selectors; original beat-based stopping durations. |
| Stutter | 1/2, 1/4, 1/4T, 1/8, 1/8T, 1/16, 1/32, 1/64. A rate selection takes effect during engagement. |
| Noise / Mix | Independent wet-path hiss level and dry/processed balance, both 0–100%. |
| Bypass | Smoothed return to unity dry audio while input continues. |
| Automation | All 27 user controls exposed to the SDK host and restored by project state. |

## Explicit limits

The manual documents control functions, not the proprietary DSP coefficients, tape models, exact brake durations, latency, signal-chain ordering or per-preset algorithms. Those audio details are original approximations. This package includes neither original-product DSP nor its graphics, factory sounds or desktop formats.

Repeat Wear is an original added control to fulfill the requested gradually worn repeats. The manual does not establish progressive degradation as a Fly Tape II behavior. Setting Wear to 0 disables this addition.

The layout uses original cassette graphics following the supplied reference positions and color families. Reel motion now follows the audio motor phase. Exact wear patterns from the reference are not reproduced. Mute/Reverse use status icons; additional size/amount controls remain on the editing pages.

Hardware gesture behavior, multitouch stacking, Q-Link focus/feel, project automation in MPC OS, and actual XL CPU performance remain unverified until physical testing. Desktop host automation/state/audio and SDK structural validation are tested; they cannot certify on-device behavior. Native insert effects do not receive pad MIDI through this SDK.

The original walkthrough URL could not be fetched; validation uses the official manual and user-provided screenshots rather than an audiovisual comparison.

Speed UI repair in v1.0.2: native bitmap captions replace overlay Labels, four visible Speed choices reordered to 1/4, 1/2, 3/4, 9/10 without changing saved indices. See SPEED-TEST.txt.

v1.0.3 adds two 64-frame reel overlays driven by non-automatable phase telemetry at index 27. Speed scales their motion; Reverse reverses direction; Brake and stopped transport stop the animation. All behavior needs physical XL display verification.

v1.0.4 supersedes the displayed v1.0.3 telemetry approach with native animated images. Speed audio works per user XL confirmation. Absolute animation clock rate is host-defined; displayed reel ratios are exact relative proportions. Playback-stop synchronization and a visible Brake deceleration curve are not implemented by this native-clock fallback. Physical animation retest remains required.

v1.0.5 supersedes both previous repaint assumptions. A normal-priority worker explicitly reports phase value changes via the SDK host callback. Skin images follow that cached value; no automatic Image animation or recurring full-screen rebuild request is used. The native UI repaint result still requires an XL test.
