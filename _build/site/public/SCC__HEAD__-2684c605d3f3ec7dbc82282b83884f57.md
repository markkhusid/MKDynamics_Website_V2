# Supercomputing Crash Course

```{image} images/NERSC_CCS.png
:height: 300
```

## Introduction

From the [NERSC website](https://www.nersc.gov/news-and-events/calendar-of-events/hpc-crash-course-jun2025):

>"This hybrid training, as part of the 2025 Berkeley Lab Computational Sciences Summer Student Program, is also open to NERSC, ALCF, LANL, OLCF, and TACC users. This training is geared towards novice parallel programmers."


In these sections, we will adapt the Fortran code that NERSC uses to teach about parallel programming and high performance computing.  In the course, NERSC has a collection of programs called the Darts-Suite.  In the Darts-Suite, Pi is computed using a Monte-Carlo method by counting the number of randomly selected points that fall within a circle of unit length.

In these sections, we will compute Pi using various methods, include serial, using OpenMP, MPI, and various combinations of these.

Course code can be found at the following Github link:

https://github.com/NERSC/crash-course-supercomputing

## Table of Contents 
::::{grid} 2 2 2 2

:::{grid-item-card}
:link: Computing_Pi_Serial/Computing_Pi_Serial.ipynb

Computing Pi Serial
^^^
```{image} images/NERSC_CCS.png
:height: 300
```
:::

::::
