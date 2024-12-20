program ball_throw
    use, intrinsic :: iso_fortran_env, only : DP => real64, int32
    use :: rk4_mod, only  : rk4vec
    implicit none
    integer, parameter :: NR_EQS = 4
    integer, parameter :: MAX_STEPS = 10000
    real(kind=DP), parameter :: DELTA_T = 0.01_DP
    real(kind=DP) :: t
    real(kind=DP), dimension(NR_EQS) :: u, u_new
    integer :: step

! State vector indices
    integer, parameter :: X_IDX = 1
    integer, parameter :: Y_IDX = 2
    integer, parameter :: VX_IDX = 3
    integer, parameter :: VY_IDX = 4

    step = 0
    t = 0.0_DP
    u(X_IDX) = 0.0_DP
    u(Y_IDX) = 0.0_DP
    u(VX_IDX) = 5.0_DP
    u(VY_IDX) = 5.0_DP
    print *, step, t, u(X_IDX), u(Y_IDX), u(VX_IDX), u(VY_IDX)

    do step = 1, MAX_STEPS
        call rk4vec(t, NR_EQS, u, DELTA_T, u_new)
        t = t + DELTA_T
        u = u_new
        if (u(Y_IDX) < 0.0_DP) exit
        print *, step, t, u(X_IDX), u(Y_IDX), u(VX_IDX), u(VY_IDX)
    end do

contains
    subroutine rhs(t, n, u, u_prime)
        implicit none
        real(kind=DP), intent(in) :: t
        integer(kind=INT32), intent(in) :: n
        real(kind=DP), dimension(n), intent(in) :: u
        real(kind=DP), dimension(n), intent(out) :: u_prime

        u_prime(X_IDX) = u(VX_IDX)
        u_prime(Y_IDX) = u(VY_IDX)
        u_prime(VX_IDX) = 0.0_DP
        u_prime(VY_IDX) = -9.81_DP
    end subroutine rhs

end program ball_throw
