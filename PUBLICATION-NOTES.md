# Publication status

Source, native skin assets, documentation, verification logs, GIF previews and MP4 are published. Automatic approval review blocked compiled ARM shared libraries and the audio test output. Installer ZIPs contain the held libraries and are also withheld. The library bytes match the original v1.0.5 user package; they are ARM/AArch64 ELF DYN shared libraries.

Pending files:

- `Tropix R!X Crazy Jungle Sounds - VST - Crazy Cassette 88/VST/crazy-cassette-88-arm32.so`
- `Tropix R!X Crazy Jungle Sounds - VST - Crazy Cassette 88/VST/crazy-cassette-88-arm64.so`
- `Verification/host-test-signal.wav`
- `Releases/Crazy-Cassette-88-1.0.5-mpc-armv7.zip`
- `Releases/Crazy-Cassette-88-1.0.5-mpc-aarch64.zip`

Both installer ZIPs passed the OpenMPC catalog checker with nine advisory tall-image warnings each. Gen2 was owner-tested on MPC XL / OS 3.10.1; Gen1 is untested.

After these uploads are allowed, publish a GitHub v1.0.5 release with both ZIPs and submit catalog/plugins/crazy-cassette-88.json to open-mpc/mpc-vst-plugins. No release or catalog PR has been submitted.

The new GIF and MP4 cycle through all eight effect views. They are UI asset previews without audio, not hardware footage. The legacy reel GIF is resized to 640 pixels wide, keeping all 100 frames and timings.
