# Week 3 — Maps and dashboard

The map work marks the launch sites and measures how far CCAFS SLC-40 sits from the nearby coast, highway, railway, and Melbourne. The saved distances are 0.87 km to the coastline, 0.60 km to the highway, 1.28 km to the railway, and 51.7 km to Melbourne. The interactive maps stay in the repository.

```python
from math import atan2, cos, radians, sin, sqrt

def kilometers(lat1, lon1, lat2, lon2):
    radius_km = 6373.0
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return radius_km * 2 * atan2(sqrt(a), sqrt(1 - a))

site_lat, site_lon = 28.563197, -80.576820
points = {
    "coastline": (28.56284, -80.56788),
    "highway": (28.56258, -80.57067),
    "railway": (28.57205, -80.58525),
    "Melbourne": (28.10159, -80.64229),
}
distances_km = {
    name: kilometers(site_lat, site_lon, lat, lon)
    for name, (lat, lon) in points.items()
}
```

`distances_km` rounds to 0.874 km, 0.605 km, 1.284 km, and 51.743 km. The figures quoted above are those values to two or three significant digits: 0.87, 0.60, 1.28, and 51.7.

The dashboard is a dropdown of launch sites, a success pie, a payload slider, and a scatter of payload against landing class colored by booster version. The screenshots below are the two views saved on 6 November 2022.

## Dashboard table

`spacex_launch_dash.csv` has 56 flights. A successful landing is `class` 1. Twenty-four flights are class 1.

```python
import pandas as pd

dash = pd.read_csv("spacex_launch_dash.csv")
by_site = (
    dash.groupby("Launch Site")["class"]
    .agg(flights="count", landings="sum", rate="mean")
)
by_site["share_of_landings"] = by_site["landings"] / by_site["landings"].sum()

payload_bins = [0, 2500, 5000, 7500, 10000]
dash["payload_bin"] = pd.cut(
    dash["Payload Mass (kg)"], payload_bins, right=False
)
by_payload = dash.groupby("payload_bin", observed=False)["class"].agg(
    flights="count", rate="mean"
)
by_booster = dash.groupby("Booster Version Category")["class"].agg(
    flights="count", landings="sum", rate="mean"
)
```

`right=False` makes the bins `[0, 2500)`, `[2500, 5000)`, `[5000, 7500)`, and `[7500, 10000)`. Those bins hold 21, 21, 9, and 5 flights. The booster rates use `Booster Version Category`.

| Launch site | Flights | Landings | Landing rate | Share of landings |
| --- | ---: | ---: | ---: | ---: |
| KSC LC-39A | 13 | 10 | 0.769 | 0.417 |
| CCAFS LC-40 | 26 | 7 | 0.269 | 0.292 |
| VAFB SLC-4E | 10 | 4 | 0.400 | 0.167 |
| CCAFS SLC-40 | 7 | 3 | 0.429 | 0.125 |

KSC LC-39A has the most landings and the highest landing rate, 10 of 13. The all-sites pie is the share of those 24 landings: KSC LC-39A 41.7%, CCAFS LC-40 29.2%, VAFB SLC-4E 16.7%, and CCAFS SLC-40 12.5%. The KSC screenshot is the site pie, 10 successes and 3 failures, which is 76.9% and 23.1%.

```{figure} ../images/dash_all_sites.png
:alt: Dashboard pie of successful launches by site, and a payload scatter for all sites.
:align: center
:class: clickable-figure

All sites. The pie is the share of successful landings. The scatter is payload mass against class, colored by booster version, with the slider at 0 to 10,000 kg.
```

```{figure} ../images/dash_ksc.png
:alt: Dashboard filtered to KSC LC-39A, with a 76.9 percent success pie.
:align: center
:class: clickable-figure

KSC LC-39A. Success is 76.9% (10 of 13). The slider in this view runs from about 2,000 kg to 7,000 kg.
```

Payload bins on the same 56 flights:

| Payload (kg) | Flights | Landing rate |
| --- | ---: | ---: |
| 0 to 2,500 | 21 | 0.333 |
| 2,500 to 5,000 | 21 | 0.571 |
| 5,000 to 7,500 | 9 | 0.222 |
| 7,500 to 10,000 | 5 | 0.600 |

Booster version on the same file: FT landed 16 of 24 flights (0.667). B4 landed 6 of 11 (0.545). v1.1 landed 1 of 15 (0.067). v1.0 landed 0 of 5. B5 landed its one flight.

The closing note saved with the dashboard names CCAFS SLC-40 as the highest landing rate. This table puts KSC LC-39A first, at 10 of 13.
