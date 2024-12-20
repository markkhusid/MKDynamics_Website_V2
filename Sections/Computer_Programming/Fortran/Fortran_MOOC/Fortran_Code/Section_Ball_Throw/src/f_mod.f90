module f_mod
    use, intrinsic :: iso_fortran_env, only : DP => real64, int32
    implicit none

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
            X = u(1)   ! Position in the x-direction
            Y = u(2)   ! Position in the y-direction
            VX = u(3)  ! Velocity in the x-direction
            VY = u(4)  ! Velocity in the y-direction

            ! Compute the derivatives (primes)
            uprime(1) = VX        ! Derivative of position in x is velocity in x
            uprime(2) = VY        ! Derivative of position in y is velocity in y
            uprime(3) = 0.0_DP    ! No acceleration in x (ignoring air resistance)
            uprime(4) = -9.81_DP  ! Acceleration in y due to gravity

        end subroutine f
        !*******************************************************************************
        
end module f_mod