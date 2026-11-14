# Vintage Military Radio release requirements

User-required policy for every future release:
- Maintain revisions.txt with the newest version entry at the top. Never erase prior entries.
- Record every change, timestamp with timezone, validation performed and material limits.
- Put the current manifest version first. Use exact recorded timestamps; label estimates honestly.
- Include revisions.txt at the distribution ZIP root and inside the installable plugin folder.
- Retain releaseHistory: revisions.txt in plugin.json. The bundled SDK tools/package.py enforces the history/version/order checks and embeds the file.
- Use release.py for the full deliverable; it also includes source, previews, test logs and SHA256SUMS.txt.
- A packaging-only/documentation-only repack retains the plugin version and adds a timestamped repack note to the top version entry. DSP/UI/binary changes bump the patch version.
- Preserve plugin UID and existing parameter IDs/order. Run appropriate build/audio/UI checks for code changes. Do not claim physical MPC validation without device evidence.
