# Surf Scrap - `surf-scrap-hp`

**surf-scrap-hp** is a Python package that allows you to extract surf conditions  
from **surf-report.com** and save them into a CSV file for further analysis or dashboard creation.

This package was developed as part of a data analysis project to help surf
schools identify the best moments to practice surfing during the week.

[![PyPI version](https://badge.fury.io/py/surf-scrap-hp.svg)](https://badge.fury.io/py/surf-scrap-hp)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
---

## Features

- Scrapes surf conditions from surf-report.com
- Works with multiple surf spots (Lacanau, Carcans, Moliets, etc.)
- Extracts:
  - Day
  - Hour
  - Wave size
  - Wind speed (km/h)
  - Wind direction
- Saves the data as a CSV file
- Returns a pandas DataFrame for immediate use
- Simple API with **one main function**

---

## Installation

Install the package from PyPI:


```bash
pip install surf-scrap-hp
```
---

## Quick Start

```python
from surf_scrap import scrape_surf_report

scrape_surf_report(
    "https://www.surf-report.com/meteo-surf/carcans-plage-s1013.html",
    "carcans.csv"
)
```
After execution, a file `carcans.csv` will be created in your working directory. You can change the name `carcans.csv` to an other one.
---

## Function Documentation

`scrape_surf_report(url, output_csv)`

Scrapes surf conditions from a surf-report.com page and saves the data to a CSV file.

***Parameters:***

| ***Name***   |***Type***| ***Description***                     |
| ------------ | ---------| --------------------------------------|
| `url`        | `str`    | URL of the surf-report page           |
| `output_csv` | `str`    | Path where the CSV file will be saved |

***Returns***

- `pandas.DataFrame` containing the extracted surf conditions.

---

## Output Data Format

The generated CSV file contains the following columns:

| ***Column***       | ***Description***        |
| ------------------ | ------------------------ |
| Day                | Day of the forecast      |
| Hour               | Time of the forecast     |
| Wave_size_m        | Wave size range (meters) |
| Wind_speed_km_h    | Wind speed (km/h)        |
| Wind_direction     | Wind direction           |

---

## Notes & Limitations

- The package relies on the current HTML structure of surf-report.com.
- If the website structure changes, the scraper may require updates.
- This project is intended for educational and analytical purposes.

## Dependencies

- Python ≥ 3.12
- requests
- beautifulsoup4
- pandas

All dependencies are automatically installed via `pip`.


## Licence

This project is licensed under the MIT License.
You are free to use, modify, and distribute it.

---

## Useful Links
 PyPI : [https://pypi.org/project/surf-scrap-hp/](https://pypi.org/project/surf-scrap-hp/)

## Authors

- MISSONGO Aimé Blanchard
- Hippolyte SODJINOU



