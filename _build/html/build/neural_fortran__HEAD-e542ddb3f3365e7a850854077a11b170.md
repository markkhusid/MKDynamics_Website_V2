# Neural Fortran

Created with Grok Build

Source code by [Milan Curcic](https://github.com/milancurcic) and the neural-fortran contributors, from the [neural-fortran](https://github.com/modern-fortran/neural-fortran) repository. The library is released under the MIT license. Copyright (c) 2018-2025 neural-fortran contributors.

## Introduction

These pages use Fortran for neural networks through [neural-fortran](https://github.com/modern-fortran/neural-fortran). The library can train with data-based parallelism, and it can read a Keras HDF5 file through its Keras bridge.

The cards below, other than the sine-wave tutorial, are the programs in the repository directory `example/`. Each program is copied unchanged. The page shows the source, an `fpm.toml` that depends on the git repository, the fpm 0.10.1 release build from commit `357e63d`, and the saved run from this machine. The sine-wave card is the longer CSV tutorial already in this section. It is not a second copy of `example/sine.f90`.

::::{grid} 2 2 2 2

:::{grid-item-card}
:link: Section_Examples_Sine_Wave.ipynb

Training a Neural Network to Fit a Sine Wave
^^^
```{image} images/sine_wave_NN.png
:height: 200
```
:::

:::{grid-item-card}
:link: Section_Examples_Simple.ipynb

A Small Dense Network
^^^
```{image} images/nf_simple.png
:height: 200
```
:::

:::{grid-item-card}
:link: Section_Examples_Network_Parameters.ipynb

Reading Layer Weights
^^^
```{image} images/nf_network_parameters.png
:height: 200
```
:::

:::{grid-item-card}
:link: Section_Examples_Get_Set.ipynb

Copying Network Parameters
^^^
```{image} images/nf_get_set.png
:height: 200
```
:::

:::{grid-item-card}
:link: Section_Examples_Merge.ipynb

Merging Two Networks
^^^
```{image} images/nf_merge.png
:height: 200
```
:::

:::{grid-item-card}
:link: Section_Examples_Mha.ipynb

Self-Attention
^^^
```{image} images/nf_mha_simple.png
:height: 200
```
:::

:::{grid-item-card}
:link: Section_Examples_Quadratic.ipynb

Eleven Optimizers on a Quadratic
^^^
```{image} images/nf_quadratic.png
:height: 200
```
:::

:::{grid-item-card}
:link: Section_Examples_Dense_Mnist.ipynb

Dense Network on MNIST
^^^
```{image} images/nf_dense_mnist.png
:height: 200
```
:::

:::{grid-item-card}
:link: Section_Examples_Cnn_Mnist.ipynb

Convolutional Network on MNIST
^^^
```{image} images/nf_cnn_mnist.png
:height: 200
```
:::

:::{grid-item-card}
:link: Section_Examples_Cnn_Mnist_1d.ipynb

Locally Connected Network on MNIST
^^^
```{image} images/nf_cnn_mnist_1d.png
:height: 200
```
:::

::::
