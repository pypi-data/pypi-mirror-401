# Timesat

> **License Notice**
>
> **TIMESAT is proprietary software.**
> It is freely available for **non-commercial scientific research,
> academic teaching, and personal use only**.
>
> **Commercial use requires a separate written agreement with the authors.**
>
> See the `LICENSE` and `NOTICE` files for full terms.

---

**Timesat** provides Python bindings for the [TIMESAT](https://github.com/TIMESAT) algorithms — a suite of routines for analyzing time-series of satellite remote sensing data.  
This package wraps the original **Fortran-based TIMESAT core** into a modern Python interface for convenient use in data analysis and research workflows.

---

## Features

- Native Python bindings for the **TIMESAT Fortran core**
- Cross-platform precompiled binaries (macOS Intel & ARM, Linux, Windows)
- Supports **Python 3.10–3.12**
- Compatible with **NumPy ≥ 2.0**
- Provides high performance through the compiled Fortran backend
- Simple API for fitting and extracting vegetation metrics from time-series data

---

## Installation

You can install the latest release directly from PyPI:

```bash
pip install timesat
```

> **Note**
>
> TIMESAT is proprietary software licensed for **non-commercial research,
> academic teaching, and personal use only**.
> Commercial use requires a separate written agreement.

---

## Version log

## 4.2.1 – License Change

Starting from version 4.2.1, TIMESAT is licensed under the
TIMESAT Research License.

This software is now licensed for non-commercial scientific research,
academic teaching, and personal use only.

Commercial use requires a separate written agreement with the authors.

Versions prior to v4.2.1 remain available under their original license.

### 4.1.12 – Debugged Windows parallel processing

### 4.1.11 – Added parallel processing

### 4.1.10 – Improved NoData Handling
Pixels whose land-cover class is not included in the SETTINGS table now receive a proper NoData value instead of zero.

### 4.1.9 – Performance release
- Build system updated to compile the Fortran core with high-optimization for improved runtime performance.
- Minor internal clean-ups to keep behaviour consistent across platforms.
- Note: Due to more aggressive optimization, very small floating-point differences (round-off level) may occur compared to earlier versions.

### 4.1.8 – Bugfixes and QA improvements
- **Fixed:** Issue related to handling of negative slopes in the time-series processing.
- **Added:** Switch for VPP (vegetation peak/phenology) calculation to give users more control over how metrics are derived.
- **Added:** `yfitqa` output for basic quality assessment of the fitted time-series.

---

## License
SPDX-License-Identifier: LicenseRef-Proprietary-TIMESAT-Research-Only

TIMESAT is proprietary software licensed under the
TIMESAT Research License.

It is freely available for non-commercial scientific research,
academic teaching, and personal use.

Commercial use is not permitted under this license and requires
a separate written agreement with the authors.

See the LICENSE file for the full license text.

---

## Citation

If you use **TIMESAT** in your research, please cite the corresponding release on Zenodo:

> Cai, Z., Eklundh, L., & Jönsson, P. (2025). *TIMESAT4:  is a software package for analysing time-series of satellite sensor data* (Version 4.1.x) [Computer software]. Zenodo.   
> [https://doi.org/10.5281/zenodo.17369757](https://doi.org/10.5281/zenodo.17369757)

If you use the underlying TIMESAT algorithms, please also cite the
relevant TIMESAT publications listed in the official repository.

---

## Contact and Licensing Inquiries

For licensing questions, including commercial use, please contact:

**Dr. Zhanzhang Cai**
Department of Physical Geography and Ecosystem Science
Lund University, Sweden
Email: zhanzhang.cai@mgeo.lu.se

https://www.nateko.lu.se

---

## Acknowledgments

- [TIMESAT](https://www.nateko.lu.se/TIMESAT) — Original analysis framework for satellite time-series data.  
- This project acknowledges the Swedish National Space Agency (SNSA), the European Environment Agency (EEA), and the European Space Agency (ESA) for their support and for providing access to satellite data and related resources that made this software possible.

---