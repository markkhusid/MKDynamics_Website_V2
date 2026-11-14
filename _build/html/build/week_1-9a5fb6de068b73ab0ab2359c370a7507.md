# Week 1 — Collect and clean

The Falcon 9 table comes from two saved sources. One is a static copy of the SpaceX API response. The other is the Wikipedia snapshot of [List of Falcon 9 and Falcon Heavy launches](https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922) from 8 June 2021.

The API table is filtered to Falcon 9. Missing payload masses are filled with the mean of that column. The exported file, [`dataset_part_1.csv`](https://github.com/markkhusid/Applied_Data_Science_Capstone/blob/master/Week_1_Introduction/Lab_1_Collecting_the_Data/dataset_part_1.csv), has 90 Falcon 9 flights and no missing payload mass. The Wikipedia table is saved as `spacex_web_scraped.csv` in the same repository.

```python
import pandas as pd

launches = pd.read_csv("dataset_part_1.csv")
falcon9 = launches.loc[launches["BoosterVersion"].eq("Falcon 9")].copy()
falcon9["PayloadMass"] = falcon9["PayloadMass"].fillna(falcon9["PayloadMass"].mean())
```

That file is already the result of those two lines: every `BoosterVersion` is Falcon 9, and `PayloadMass` has no missing values.

## Landing label

The wrangling result is [`dataset_part_2.csv`](https://github.com/markkhusid/Applied_Data_Science_Capstone/blob/master/Week_1_Introduction/Lab_3_Data_Wrangling/dataset_part_2.csv). The notebook that shares that folder is a second copy of the web-scraping lab, so the counts below are computed from the CSV.

The table has 90 Falcon 9 flights and 18 columns. `Class` is 1 when `Outcome` records a landing (`True ASDS`, `True RTLS`, or `True Ocean`) and 0 otherwise. Sixty flights are class 1. The class mean is 0.667.

```python
import pandas as pd

flights = pd.read_csv("dataset_part_2.csv")
landed = {"True ASDS", "True RTLS", "True Ocean"}
flights["Class"] = flights["Outcome"].isin(landed).astype(int)
flights["Year"] = pd.to_datetime(flights["Date"]).dt.year

landing_count = int(flights["Class"].sum())
landing_rate = flights["Class"].mean()

by_site = (
    flights.groupby("LaunchSite")["Class"]
    .agg(flights="count", landings="sum", rate="mean")
    .round(3)
)
by_orbit = (
    flights.groupby("Orbit")["Class"]
    .agg(flights="count", landings="sum", rate="mean")
    .round(3)
)
by_outcome = flights.groupby("Outcome").size()
by_year = (
    flights.groupby("Year")["Class"]
    .agg(flights="count", rate="mean")
    .round(3)
)
```

`landing_count` is 60 and `landing_rate` is 0.667. The four tables below are `by_site`, `by_orbit`, `by_outcome`, and `by_year`. Rates are rounded to three decimals. Years with no flights, including 2011, do not appear.

## Launch sites

| Launch site | Flights | Landings | Landing rate |
| --- | ---: | ---: | ---: |
| CCAFS SLC 40 | 55 | 33 | 0.600 |
| KSC LC 39A | 22 | 17 | 0.773 |
| VAFB SLC 4E | 13 | 10 | 0.769 |

KSC LC-39A and VAFB SLC-4E land more often than CCAFS SLC 40. KSC is 17 of 22. VAFB is 10 of 13. CCAFS is 33 of 55.

## Orbits

| Orbit | Flights | Landings | Landing rate |
| --- | ---: | ---: | ---: |
| SSO | 5 | 5 | 1.000 |
| ES-L1 | 1 | 1 | 1.000 |
| GEO | 1 | 1 | 1.000 |
| HEO | 1 | 1 | 1.000 |
| VLEO | 14 | 12 | 0.857 |
| LEO | 7 | 5 | 0.714 |
| PO | 9 | 6 | 0.667 |
| MEO | 3 | 2 | 0.667 |
| ISS | 21 | 13 | 0.619 |
| GTO | 27 | 14 | 0.519 |
| SO | 1 | 0 | 0.000 |

SSO is 5 of 5. GTO, the largest group, is 14 of 27. ES-L1, GEO, HEO, and SO are one flight each.

## Outcomes

| Outcome | Flights |
| --- | ---: |
| True ASDS | 41 |
| None None | 19 |
| True RTLS | 14 |
| False ASDS | 6 |
| True Ocean | 5 |
| False Ocean | 2 |
| None ASDS | 2 |
| False RTLS | 1 |

The successful landings are True ASDS (41), True RTLS (14), and True Ocean (5).

## Landing rate by year

| Year | Flights | Landing rate |
| --- | ---: | ---: |
| 2010 | 1 | 0.000 |
| 2012 | 1 | 0.000 |
| 2013 | 3 | 0.000 |
| 2014 | 6 | 0.333 |
| 2015 | 6 | 0.333 |
| 2016 | 8 | 0.625 |
| 2017 | 18 | 0.833 |
| 2018 | 18 | 0.611 |
| 2019 | 10 | 0.900 |
| 2020 | 19 | 0.842 |

The rate is 0 in 2010, 2012, and 2013. There is no 2011 row. In 2019 the rate is 0.90 (9 of 10) and in 2020 it is 0.84 (16 of 19).
