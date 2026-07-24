# Network Recon Toolkit

Small Python toolkit for authorized host checks: reachability, TCP port scan, optional banner grab, JSON report.

**Use only on systems you own or have written permission to test.**

## Features

- Host reachability check
- Port scanning (single ports or ranges)
- Light banner grab (HTTP/SSH-style)
- JSON report output
- Requires an explicit authorization flag before scanning

## Requirements

- Python 3.10+

## Usage

```bash
python3 recon.py --target 127.0.0.1 --ports 22,80,443,8080 --i-own-this-target
python3 recon.py --target 127.0.0.1 --ports 20-25,80 --out report.json --i-own-this-target
```

Without `--i-own-this-target` the tool exits and does not scan.

## Layout

```
recon.py
modules/
  discovery.py
  ports.py
  report.py
example_report.json
```

## Notes

Unauthorized scanning may be illegal depending on jurisdiction. Keep scope tight and document authorization in your own notes.
