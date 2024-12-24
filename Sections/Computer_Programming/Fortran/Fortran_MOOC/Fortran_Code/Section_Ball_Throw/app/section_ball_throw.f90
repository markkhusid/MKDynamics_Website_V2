program ball_throw
    use, intrinsic :: iso_fortran_env, only : DP => real64, int32
    use :: f_mod, only : f
    use :: rk4_mod, only  : rk4vec
    use :: vector_indices_mod, only : X_IDX, Y_IDX, VX_IDX, VY_IDX
    implicit none
    integer, parameter :: NR_EQS = 4
    integer, parameter :: MAX_STEPS = 10000
    real(kind=DP), parameter :: DELTA_T = 0.01_DP
    real(kind=DP) :: t
    real(kind=DP), dimension(NR_EQS) :: u, u_new
    integer :: step

    step = 0
    t = 0.0_DP
    u(X_IDX) = 0.0_DP
    u(Y_IDX) = 0.0_DP
    u(VX_IDX) = 5.0_DP
    u(VY_IDX) = 5.0_DP
    print *, step, t, u(X_IDX), u(Y_IDX), u(VX_IDX), u(VY_IDX)

    do step = 1, MAX_STEPS
        call rk4vec(t, NR_EQS, u, DELTA_T, f, u_new)
        t = t + DELTA_T
        u = u_new
        if (u(Y_IDX) < 0.0_DP) exit
        print *, step, t, u(X_IDX), u(Y_IDX), u(VX_IDX), u(VY_IDX)
    end do

end program ball_throw
