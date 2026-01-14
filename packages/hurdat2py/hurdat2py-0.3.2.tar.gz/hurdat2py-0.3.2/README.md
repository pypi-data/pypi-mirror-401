# hurdat2py

[![PyPI version](https://img.shields.io/pypi/v/hurdat2py.svg)](https://pypi.org/project/hurdat2py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**hurdat2py** is a modern, researcher-focused Python interface for the NOAA HURDAT2 Hurricane Database. 

Unlike legacy parsers, this library is built from the ground up to integrate seamlessly with the **Pandas** and **Matplotlib** scientific stack. It handles data retrieval, parsing, and caching automatically, allowing researchers to focus on analysis rather than file management.

## Key Features
* **Automatic Data Retrieval:** Automatically downloads and caches the latest HURDAT2 dataset from NOAA.
* **Pandas-Native:** Export storm tracks, seasons, or the entire database to Pandas DataFrames with a single method.
* **Built-in Analytics:** Instant calculation of Accumulated Cyclone Energy (ACE), storm duration, and track distances.
* **Publication-Quality Plotting:** Generate professional track maps and intensity plots with one line of code.
* **Object-Oriented Design:** Intuitive access to storms via `db['Bob', 1991]` or ATCF ID.

## Installation

```bash
pip install hurdat2py
```

## Quick Start

### 1. Initialize the Database
The first time you run this, it will download the latest data from NOAA (~12MB) and save it locally.
```python
import hurdat2py

# Initialize the database
atl = hurdat2py.Hurdat2()

# Check how many storms are in the record
print(f"Loaded {len(atl)} storms from 1851-Present.")
```

### 2. Analyze a Specific Storm
You can access storms by **Name and Year** tuple or by **ATCF ID**.
```python
# Get Hurricane Bob (1991)
bob = atl['Bob', 1991]
# OR: bob = atl['al031991']

# Access properties
print(f"Name: {bob.name}")
print(f"Peak Wind: {bob.peak_wind} kts")
print(f"ACE: {bob.ace}")
print(f"Duration: {bob.duration_hurricane} hours as a hurricane")

# Get raw data (Lat/Lons)
print(bob.lats) 
print(bob.lons)

# Export to Pandas DataFrame
df = bob.to_dataframe()
print(df.head())
```

### 3. Plotting
Create publication-ready visualizations instantly.
```python
# Plot the track on a map
bob.plot()

# Plot the intensity (Wind Speed & Pressure)
bob.plot_intensity()
```

## Advanced Usage

### Season Analysis
Analyze entire hurricane seasons at once.
```python
# Get the 1991 Season
season_1991 = atl[1991]

# Get season statistics
print(f"Total Storms: {len(season_1991)}")
print(f"Total Season ACE: {season_1991.ace}")

# Plot every storm from the season on one map
season_1991.plot()
```

### Ranking Seasons
Find the most active seasons in history.
```python
# Get top 5 seasons by ACE
rankings = atl.rank_seasons_by_ace(descending=True)

for i, season in enumerate(rankings[:5]):
    print(f"Rank {i+1}: {season['year']} (ACE: {season['ace']:.1f})")
```

## Attribution & Data Sources

### Data
This library processes data from the **National Hurricane Center (NHC) HURDAT2 Database**.
* [HURDAT2 Data Format Description](https://www.nhc.noaa.gov/data/hurdat/hurdat2-format-nencpac.pdf)

### Acknowledgements
* **Plotting Style**: The map visualization aesthetic in this package was inspired by the excellent [tropycal](https://tropycal.github.io/tropycal/index.html) library. While `hurdat2py` is a standalone implementation, we aimed to match their clear, publication-ready visual style.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

**Disclaimer**: This package is maintained for personal research and is not an official NOAA product.
