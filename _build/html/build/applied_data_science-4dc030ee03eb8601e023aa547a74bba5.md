# Applied Data Science Capstone

Created with Grok Build

This section is the capstone from the IBM Data Science Professional Certificate. The repository is [Applied_Data_Science_Capstone](https://github.com/markkhusid/Applied_Data_Science_Capstone). The question is whether a Falcon 9 first stage will land. The course material puts a Falcon 9 launch at 65 million dollars and other providers at upwards of 165 million dollars, and it ties much of that gap to reuse of the first stage.

The certificate is on the [Coursera certificates](../About_Me/Certificates/certificates_coursera.md) page. The slide deck is [ds-capstone-coursera_Mark_Khusid.pdf](https://github.com/markkhusid/Applied_Data_Science_Capstone/blob/master/ds-capstone-coursera_Mark_Khusid.pdf) (3 December 2022).

```{figure} images/success_rate_vs_year.png
:name: capstone-success-by-year
:alt: Landing success rate of Falcon 9 flights by year, from the exploratory analysis.
:align: center
:class: clickable-figure

Landing success rate by year in the wrangling table of 90 Falcon 9 flights. The rate is 0 in 2010, 2012, and 2013, then rises. In 2019 it is 0.90 (9 of 10) and in 2020 it is 0.84 (16 of 19).
```

## Weeks

::::{grid} 2 2 2 2

:::{grid-item-card}
:link: Week_1_Introduction/week_1.md

Week 1 — Collect and clean
^^^
```{image} images/success_vs_orbit.png
:height: 180
:align: center
```
The SpaceX API and the Wikipedia launch table, then a landing label on 90 Falcon 9 flights.
:::

:::{grid-item-card}
:link: Week_2_Exploratory_Data_Analysis/week_2.md

Week 2 — Exploratory analysis
^^^
```{image} images/success_rate_vs_year.png
:height: 180
:align: center
```
SQL queries on the Wikipedia table, and the six landing-rate plots.
:::

:::{grid-item-card}
:link: Week_3_Interactive_Visual_Analytics/week_3.md

Week 3 — Maps and dashboard
^^^
```{image} images/dash_all_sites.png
:height: 180
:align: center
```
Distances from CCAFS SLC-40, and a Plotly Dash board of 56 flights.
:::

:::{grid-item-card}
:link: Week_4_Predictive_Analysis/week_4.md

Week 4 — Classification
^^^
```{image} images/test_accuracy.png
:height: 180
:align: center
```
Logistic regression, a support vector machine, a decision tree, and k-nearest neighbors.
:::

:::{grid-item-card}
:link: Week_5_Presentation/presentation.md

Week 5 — Presentation
^^^
```{image} images/presentation_title.png
:height: 180
:align: center
```
The December 2022 slide deck and the scores from the saved model run.
:::

::::
