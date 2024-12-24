module f_mod
    use, intrinsic :: iso_fortran_env, only : DP => real64, int32
    use :: vector_indices_mod, only : X_IDX, Y_IDX, VX_IDX, VY_IDX
    implicit none

    private
    public :: f

    contains

        !*******************************************************************************
        subroutine f(t, m, u, uprime)
            implicit none
            real(kind=DP), intent(in) :: t ! Time
            integer(kind=int32), intent(in) :: m ! Number of equations
            real(kind=DP), dimension(m), intent(in) :: u ! State vector
            real(kind=DP), dimension(m), intent(out) :: uprime ! Derivative of the state vector

            ! Declare local variables for the components of the state vector
            real(kind=DP) :: X, Y, VX, VY

            ! Extract state vector components
            X  = u(X_IDX)   ! Position in the x-direction
            Y  = u(Y_IDX)   ! Position in the y-direction
            VX = u(VX_IDX)  ! Velocity in the x-direction
            VY = u(VY_IDX)  ! Velocity in the y-direction

            ! Compute the derivatives (primes)
            uprime(X_IDX)  = VX        ! Derivative of position in x is velocity in x
            uprime(Y_IDX)  = VY        ! Derivative of position in y is velocity in y
            uprime(VX_IDX) = 0.0_DP    ! No acceleration in x (ignoring air resistance)
            uprime(VY_IDX) = -9.81_DP  ! Acceleration in y due to gravity

        end subroutine f
        !*******************************************************************************
        
end module f_mod