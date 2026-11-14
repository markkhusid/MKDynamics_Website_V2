# Week 2 — Exploratory analysis

The SQL queries read `Spacex.csv` (101 rows). The plots read the 90-flight wrangling table and the same run writes `dataset_part_3.csv` for the models in week 4.

## SQL results

`Spacex.csv` loads into SQLite under the column names in the file, including `PAYLOAD_MASS__KG_` and `Landing _Outcome`.

```python
import sqlite3
import pandas as pd

launches = pd.read_csv("Spacex.csv")
con = sqlite3.connect(":memory:")
launches.to_sql("SPACEXTBL", con, index=False)
```

Distinct launch sites are CCAFS LC-40, VAFB SLC-4E, KSC LC-39A, and CCAFS SLC-40.

```sql
SELECT DISTINCT Launch_Site
FROM SPACEXTBL;
```

NASA (CRS) payloads sum to 45,596 kg.

```sql
SELECT SUM(PAYLOAD_MASS__KG_) AS total_kg
FROM SPACEXTBL
WHERE Customer = 'NASA (CRS)';
```

The average payload on boosters whose version starts with `F9 v1.1` is 2,534.7 kg.

```sql
SELECT ROUND(AVG(PAYLOAD_MASS__KG_), 1) AS avg_kg
FROM SPACEXTBL
WHERE Booster_Version LIKE 'F9 v1.1%';
```

`Date` is stored as text in day-month-year order, so `MIN(Date)` for `Success (ground pad)` returns the string `01-05-2017`. Read as calendar dates, the earliest successful ground-pad landing in `Spacex.csv` is 22 December 2015.

```sql
SELECT MIN(Date) AS earliest_text
FROM SPACEXTBL
WHERE "Landing _Outcome" = 'Success (ground pad)';
```

Drone-ship landings with payload from 4,000 kg to 6,000 kg are F9 FT B1022 (4,696 kg), F9 FT B1026 (4,600 kg), F9 FT B1021.2 (5,300 kg), and F9 FT B1031.2 (5,200 kg).

```sql
SELECT Booster_Version, PAYLOAD_MASS__KG_
FROM SPACEXTBL
WHERE "Landing _Outcome" = 'Success (drone ship)'
  AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000;
```

Mission outcomes are 99 Success, 1 Failure (in flight), and 1 Success (payload status unclear). One success row is stored as `Success` with a trailing space, so a raw `GROUP BY` splits the 99 into 98 and 1. `TRIM` puts them back together.

```sql
SELECT TRIM(Mission_Outcome) AS mission_outcome, COUNT(*) AS flights
FROM SPACEXTBL
GROUP BY TRIM(Mission_Outcome);
```

The maximum payload is 15,600 kg, on twelve B5 boosters: B1048.4, B1049.4, B1051.3, B1056.4, B1048.5, B1051.4, B1049.5, B1060.2, B1058.3, B1051.6, B1060.3, and B1049.7.

```sql
SELECT Booster_Version, PAYLOAD_MASS__KG_
FROM SPACEXTBL
WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);
```

Drone-ship landing failures in 2015 are 10 January, F9 v1.1 B1012, CCAFS LC-40, and 14 April, F9 v1.1 B1015, CCAFS LC-40. The month is characters 4–5 of the text date, and the year is characters 7–10.

```sql
SELECT Date, Booster_Version, Launch_Site
FROM SPACEXTBL
WHERE substr(Date, 7, 4) = '2015'
  AND "Landing _Outcome" = 'Failure (drone ship)';
```

From 2010 through 2017 the file has 12 successful drone-ship landings and 8 successful ground-pad landings.

```sql
SELECT "Landing _Outcome", COUNT(*) AS landings
FROM SPACEXTBL
WHERE substr(Date, 7, 4) BETWEEN '2010' AND '2017'
  AND "Landing _Outcome" LIKE 'Success%'
GROUP BY "Landing _Outcome"
ORDER BY landings DESC;
```

Selecting a month and a year in that grouped query, without aggregating them, returns one row from each group: April 2016 for the drone-ship rows and December 2015 for the ground-pad rows.

## Plots

Class 0 is blue and class 1 is orange. The year chart is also on the [section page](../applied_data_science_capstone.md).

```python
import pandas as pd
import seaborn as sns

flights = pd.read_csv("dataset_part_2.csv")
flights["Year"] = pd.to_datetime(flights["Date"]).dt.year

sns.catplot(data=flights, x="FlightNumber", y="LaunchSite", hue="Class", aspect=3)
sns.catplot(data=flights, x="PayloadMass", y="LaunchSite", hue="Class", aspect=3)
orbit_rate = flights.groupby("Orbit")["Class"].mean()
sns.barplot(x=orbit_rate.index, y=orbit_rate.to_numpy())
sns.catplot(data=flights, x="FlightNumber", y="Orbit", hue="Class", aspect=3)
sns.catplot(data=flights, x="PayloadMass", y="Orbit", hue="Class", aspect=3)
year_rate = flights.groupby("Year")["Class"].mean()
sns.lineplot(x=year_rate.index, y=year_rate.to_numpy())
```

The feature file for week 4 is the dummy columns only. `dataset_part_3.csv` has 90 rows and 72 columns, one column for each orbit, launch site, landing pad, and booster serial. The numeric columns stay in `dataset_part_2.csv`.

```python
import pandas as pd

flights = pd.read_csv("dataset_part_2.csv")
features = pd.get_dummies(
    flights[["Orbit", "LaunchSite", "LandingPad", "Serial"]]
)
```

```{figure} ../images/launch_site_vs_flight.png
:alt: Flight number against launch site, colored by landing class.
:align: center
:class: clickable-figure

Flight number against launch site. Early CCAFS flights are mostly class 0, and later flights at CCAFS, VAFB, and KSC are mostly class 1.
```

```{figure} ../images/launch_site_vs_payload.png
:alt: Payload mass against launch site, colored by landing class.
:align: center
:class: clickable-figure

Payload mass against launch site. Most flights are under about 8,000 kg, and the sparse points above that mass are mostly class 1, including a CCAFS cluster near 15,600 kg.
```

```{figure} ../images/success_vs_orbit.png
:alt: Average landing success rate by orbit type.
:align: center
:class: clickable-figure

Landing rate by orbit. ES-L1, GEO, HEO, and SSO sit at 1.0, with SSO on five flights and the others on one, while SO sits at 0 and GTO is near one half.
```

```{figure} ../images/orbit_vs_flight.png
:alt: Flight number against orbit, colored by landing class.
:align: center
:class: clickable-figure

Flight number against orbit. LEO, ISS, PO, and GTO run from the early flights, while VLEO, MEO, GEO, and SO appear only later, and the later VLEO flights are mostly class 1.
```

```{figure} ../images/orbit_vs_payload.png
:alt: Payload mass against orbit, colored by landing class.
:align: center
:class: clickable-figure

Payload mass against orbit. GTO sits in a mixed band from about 2,500 kg to 8,000 kg, and VLEO is the heavy orbit, mostly class 1 from about 9,000 kg to 16,000 kg.
```

```{figure} ../images/success_rate_vs_year.png
:alt: Landing success rate of Falcon 9 flights by year.
:align: center
:class: clickable-figure

Landing rate by year. The rate is 0 in 2010, 2012, and 2013, then rises, with 2019 at 0.90 (9 of 10) and 2020 at 0.84 (16 of 19).
```
