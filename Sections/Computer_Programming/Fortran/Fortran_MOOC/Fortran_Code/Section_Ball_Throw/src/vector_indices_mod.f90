module vector_indices_mod
    ! This module defines the indices for the state vector components
    implicit none

    private

    public :: X_IDX, Y_IDX, VX_IDX, VY_IDX

    integer, parameter :: X_IDX = 1
    integer, parameter :: Y_IDX = 2
    integer, parameter :: VX_IDX = 3
    integer, parameter :: VY_IDX = 4

end module vector_indices_mod