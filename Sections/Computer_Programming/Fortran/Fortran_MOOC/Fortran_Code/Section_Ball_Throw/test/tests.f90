
// Correctly performs single RK4 integration step for a simple ODE system
subroutine test_rk4vec_simple_ode_system()
  use rk4_mod
  use iso_fortran_env, only: int32, DP => real64
  implicit none

  real(DP) :: t0, dt
  integer(int32) :: m
  real(DP), allocatable :: u0(:), u(:)
  real(DP), parameter :: TOL = 1.0e-10_DP

  ! Initialize test case for simple harmonic oscillator: dy/dt = -y
  m = 1
  t0 = 0.0_DP
  dt = 0.1_DP
  
  allocate(u0(m), u(m))
  u0(1) = 1.0_DP

  ! Call RK4 integrator
  call rk4vec(t0, m, u0, dt, simple_ode, u)

  ! Compare with analytical solution y(t) = exp(-t)
  ! At t = 0.1, y ≈ 0.9048374180359595
  call assert_near(u(1), 0.9048374180359595_DP, TOL, "RK4 step matches analytical solution")

  deallocate(u0, u)

  contains
    subroutine simple_ode(t, m, y, dydt)
      real(DP), intent(in) :: t
      integer(int32), intent(in) :: m  
      real(DP), intent(in) :: y(m)
      real(DP), intent(out) :: dydt(m)
      dydt(1) = -y(1)
    end subroutine simple_ode

end subroutine test_rk4vec_simple_ode_system

    // Handles zero time step (dt = 0)
subroutine test_rk4vec_zero_timestep()
  use rk4_mod
  use iso_fortran_env, only: int32, DP => real64
  implicit none

  real(DP) :: t0, dt
  integer(int32) :: m
  real(DP), allocatable :: u0(:), u(:)
  real(DP), parameter :: TOL = 1.0e-10_DP

  ! Initialize test case
  m = 2
  t0 = 1.0_DP
  dt = 0.0_DP
  
  allocate(u0(m), u(m))
  u0 = [1.0_DP, 2.0_DP]

  ! Call RK4 integrator with zero time step
  call rk4vec(t0, m, u0, dt, dummy_ode, u)

  ! For dt=0, output should equal input
  call assert_near(u(1), u0(1), TOL, "First component unchanged for dt=0")
  call assert_near(u(2), u0(2), TOL, "Second component unchanged for dt=0")

  deallocate(u0, u)

  contains
    subroutine dummy_ode(t, m, y, dydt)
      real(DP), intent(in) :: t
      integer(int32), intent(in) :: m
      real(DP), intent(in) :: y(m)
      real(DP), intent(out) :: dydt(m)
      dydt = [1.0_DP, 1.0_DP]  ! Values don't matter for dt=0
    end subroutine dummy_ode

end subroutine test_rk4vec_zero_timestep
