---
name: design-import
description: Imports design prints (exported HTML, images, specs) into the repo byte-identical, records checksums, and lists screens where the build drifted from the print.
---

Copy each print byte-identical. Check the byte size against the source. Mismatch: retry once, then stop.
Record a sha256 per print.
Compare print and build: list each screen that drifted, with the print line.
