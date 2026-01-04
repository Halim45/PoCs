### Summary

This is a PoC malicious `.deb` for [Feather](https://github.com/khcrysalis/Feather) that takes advantage of [a tar slip in extracting tweaks](https://github.com/khcrysalis/Feather/pull/561) (unvalidated tar entry paths) to overwrite Feather's DB, `Feather.sqlite`, making the app crash on run (CoreData hits a fatalError when loading the corrupted store).

### Use
Only for educational purposes. Test with the the [`.deb`](https://github.com/jacobprezant/PoCs/releases/tag/1.0) or with the [script](https://github.com/jacobprezant/PoCs/blob/main/feather_tar_slip/create_poc_deb.py). Overwrite occurs after signing *any* `.ipa` with the malicious `.deb` added as a tweak. Current PoC exploits [`Decompression.swift`](https://github.com/khcrysalis/Feather/blob/cf804fa0566ad73ad04ae2c8abe2287ef3302e18/Feather/Utilities/ARDecompression/Decompression.swift), and a simpler but larger alternate PoC would be possible with [`TweakHandler.swift`](https://github.com/khcrysalis/Feather/blob/cf804fa0566ad73ad04ae2c8abe2287ef3302e18/Feather/Utilities/Handlers/TweakHandler.swift) (AR member filenames). Either gives arbitrary write.

The path traversal in [`DownloadManager.swift`](https://github.com/khcrysalis/Feather/blob/cf804fa0566ad73ad04ae2c8abe2287ef3302e18/Feather/Backend/Observable/DownloadManager.swift) is also *seemingly* exploitable for arbitrary write with a malicious repo, but it's sanitized with `URLSession`. This is also *seemingly* exploitable during the export of a `.ipa` in [`ArchiveHandler.swift`](https://github.com/khcrysalis/Feather/blob/cf804fa0566ad73ad04ae2c8abe2287ef3302e18/Feather/Utilities/Handlers/ArchiveHandler.swift), but ArchiveHandler appends `_{version}_{timestamp}.ipa`.

**This will wreck your Feather.** The only fix is to delete and reinstall Feather.

#### Patched in [`cf804fa`](https://github.com/khcrysalis/Feather/commit/cf804fa0566ad73ad04ae2c8abe2287ef3302e18)

### Credit
Jacob Prezant
