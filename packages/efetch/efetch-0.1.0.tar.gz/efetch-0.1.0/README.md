# efetch (POC 7)
Modernized Python system information tool.

## Modifications
- **Python 3 Compatibility:** Full migration of `print` statements and core logic to Python 3.13.
- **Relative Import Fixes:** Standardized all internal module imports for Python 3 compliance.
- **Kali Linux Detection:** Prioritized detection via `kali-undercover` and `/etc/os-release`.
- **Dragon ASCII Art:** Integrated custom Kali Linux dragon artwork with dynamic coloring.
- **System Metric Fixes:** Restored RAM and Disk usage reporting for Unix/Linux platforms.
- **Encoding Fixes:** Added explicit decoding for subprocess outputs to handle byte-strings.
