# fplotlib: Pure Fortran Plotting, Animations, TeX Math, and Scientific Reports

## Announcement

On November 26, 2026, Ondřej Čertík announced **fplotlib**, a pure Fortran library for high-quality 2D and 3D plotting, animations, TeX-style math rendering, and scientific report generation.

From the announcement:

> Your Fortran code can solve differential equations, simulate the evolution of the universe and the quantum realm. Surely it can draw a decent plot? Let’s say goodbye to slow and fragile glue scripts!

## Key Features

- **Pure Fortran** — No external dependencies. All rendering, fonts, and typesetting are self-contained.
- **Matplotlib-style API** adapted for Fortran.
- **Plot types**: plot, scatter, bar, hist, contour, quiver, imshow, polar, and 3D surfaces/wireframes.
- **Animations**: Frame-by-frame support, export to GIF or APNG.
- **Backends**: SVG, PNG, PDF, EPS, GIF, APNG.
- **TeX Math**: Built-in typesetting engine with embedded Lato and Lete Sans Math fonts. Supports inline and display equations, justified paragraphs, and hyphenation.
- **Scientific Reports**: Generate multi-page MyST Markdown reports (PDF/SVG/PNG/EPS) with embedded plots, tables, and cross-references.

## Example

```fortran
use fplotlib
call plot(x, sin(x), "b-", lw=2.0_dp, label="$\\sin(x)$")
call title("Trigonometric functions")
call xlabel("$x$")
call ylabel("$y$")
call savefig("out.svg")
```

## Resources

- Discourse announcement: [fortran-lang Discourse](https://fortran-lang.discourse.group/t/announcing-fplotlib-pure-fortran-plotting-animations-tex-math-and-scientific-reports/11339)
- GitHub repository: [fortran-lang/fplotlib](https://github.com/fortran-lang/fplotlib)
- Documentation and gallery: [fplotlib.fortran-lang.org](https://fplotlib.fortran-lang.org/)

Installation via fpm:

```toml
[dependencies]
fplotlib = { git = "https://github.com/fortran-lang/fplotlib" }
```

## Notebooks

::::{grid} 2 2 2 2

:::{grid-item-card}
:link: fplotlib_demo.ipynb

fplotlib demo in Jupyter
^^^
```{image} demo_subplots.svg
:alt: Two fplotlib panels, a damped sine above a damped cosine
:height: 300
```
:::

:::{grid-item-card}
:link: fplotlib_animation_demo.ipynb

fplotlib Animations Demo in Jupyter
^^^
```{image} mobius.png
:alt: Rotating Möbius strip drawn by fplotlib
:height: 300
```
:::

::::

## Notes

This page was added to document the release of fplotlib, a significant addition to the modern Fortran ecosystem for scientific computing and visualization.
