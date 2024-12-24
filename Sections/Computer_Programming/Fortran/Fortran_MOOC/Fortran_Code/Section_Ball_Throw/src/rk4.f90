module rk4_mod
    use, intrinsic :: iso_fortran_env, only : DP => real64, int32
    use :: f_mod, only : f
    
    implicit none

    public :: rk4, rk4vec

contains

  !*******************************************************************************
  subroutine rk4 ( t0, u0, dt, u )
  !*******************************************************************************
  !
  !! RK4 takes one Runge-Kutta step for a scalar ODE.
  !
  !  Discussion:
  !
  !    It is assumed that an initial value problem, of the form
  !
  !      du/dt = f ( t, u )
  !      u(t0) = u0
  !
  !    is being solved.
  !
  !    If the user can supply current values of t, u, a stepsize dt, and a
  !    function to evaluate the derivative, this function can compute the
  !    fourth-order Runge Kutta estimate to the solution at time t+dt.
  !
  !  Licensing:
  !
  !    This code is distributed under the GNU LGPL license. 
  !
  !  Modified:
  !
  !    31 January 2012
  !    19 December 2024
  !
  !  Author(s):
  !
  !    John Burkardt
  !    Modified by Mark Khusid with ChatGPT 4o (OpenAI)
  !
  !  Parameters:
  !
  !    Input, real ( kind = 8 ) T0, the current time.
  !
  !    Input, real ( kind = 8 ) U0, the solution estimate at the current time.
  !
  !    Input, real ( kind = 8 ) DT, the time step.
  !
  !    Input, external F, a subroutine of the form 
  !      subroutine f ( t, u, uprime ) 
  !    which evaluates the derivative uprime given the time T and
  !    solution vector U.
  !
  !    Output, real ( kind = 8 ) U, the fourth-order Runge-Kutta solution 
  !    estimate at time T0+DT.
  !
    implicit none

    ! Current time
    real ( kind = DP ), intent(in) :: t0 

    ! Initial state vector at time t0
    real ( kind = DP ), dimension(:), intent(in) :: u0 

    ! Time step
    real ( kind = DP ), intent(in) :: dt

    ! Output argument: updated state vector at time t0 + dt
    real ( kind = DP ), dimension(:), intent(out) :: u

    ! Local variables

    integer :: m

    ! Derivative estimates at different stages of the Runge-Kutta method
    real ( kind = DP ), dimension(:), allocatable :: f0, f1, f2, f3

    ! Intermediate state vectors at different stages of the Runge-Kutta method
    real ( kind = DP ), dimension(:), allocatable :: u1, u2, u3

    ! Intermediate times at different stages of the Runge-Kutta method
    real ( kind = DP ) :: t1, t2, t3

    ! Get the size of the state vector
    m = size(u0)

    ! Allocate memory for the derivative estimates and intermediate state vectors
    allocate(f0(m), f1(m), f2(m), f3(m))
    allocate(u1(m), u2(m), u3(m))

    ! Step 1: Evaluate the derivative at the initial time and state
    call f ( t0, m, u0, f0 )

    ! Step 2: Compute the intermediate state and derivative at the midpoint 1 of the interval
    t1 = t0 + dt / 2.0_DP
    u1 = u0 + dt * f0 / 2.0_DP
    call f ( t1, m, u1, f1 )

    ! Step 3: Compute the intermediate state and derivative at the midpoint 2 of the interval
    t2 = t0 + dt / 2.0_DP
    u2 = u0 + dt * f1 / 2.0_DP
    call f ( t2, m, u2, f2 )

    ! Step 4: Compute the intermediate state and derivative at the end of the interval  
    t3 = t0 + dt
    u3 = u0 + dt * f2
    call f ( t3, m, u3, f3 )

    ! Step 5: Combine the four estimates to update the solution at t0 + dt
    u = u0 + (dt / 6.0_DP) * ( f0 + 2.0_DP * f1 + 2.0_DP * f2 + f3 )

    ! Deallocate the temporary arrays
    deallocate(f0, f1, f2, f3)
    deallocate(u1, u2, u3)

  end subroutine rk4
  !*******************************************************************************

  !*******************************************************************************
  subroutine rk4vec ( t0, m, u0, dt, f, u )
  !*****************************************************************************80
  !
  !! RK4VEC takes one Runge-Kutta step for a vector ODE.
  !
  !  Discussion:
  !
  !    Thanks to Dante Bolatti for correcting the final function call to:
  !      call f ( t3, m, u3, f3 )
  !    18 August 2016.
  !
  !  Licensing:
  !
  !    This code is distributed under the GNU LGPL license. 
  !
  !  Modified:
  !
  !    18 August 2016
  !    19 December 2024
  !
  !  Author(s):
  !
  !    John Burkardt
  !    Modified by Mark Khusid with ChatGPT 4o (OpenAI)
  !
  !  Parameters:
  !
  !    Input, real ( kind = 8 ) T0, the current time.
  !
  !    Input, integer ( kind = 4 ) M, the dimension of the system.
  !
  !    Input, real ( kind = 8 ) U0(M), the solution estimate at the current time.
  !
  !    Input, real ( kind = 8 ) DT, the time step.
  !
  !    Input, external F, a subroutine of the form 
  !      subroutine f ( t, m, u, uprime ) 
  !    which evaluates the derivative UPRIME(1:M) given the time T and
  !    solution vector U(1:M).
  !
  !    Output, real ( kind = 8 ) U(M), the fourth-order Runge-Kutta solution 
  !    estimate at time T0+DT.
  !
    implicit none

    interface
      subroutine f ( t, m, u, uprime )
        use, intrinsic :: iso_fortran_env, only : DP => real64, int32
        real ( kind = DP ), intent(in) :: t
        integer ( kind = int32 ), intent(in) :: m
        real ( kind = DP ), dimension(m), intent(in) :: u
        real ( kind = DP ), dimension(m), intent(out) :: uprime
      end subroutine f
    end interface
    
    ! Input arguments
    ! Current time
    real ( kind = DP ), intent(in) :: t0 

    ! Dimension of the system
    integer ( kind = int32 ), intent(in) :: m
    
    ! Initial state vector at time t0
    real ( kind = DP ), dimension(m), intent(in) :: u0

    ! Time step
    real ( kind = DP ), intent(in) :: dt

    ! Output argument: updated state vector at time t0 + dt
    real ( kind = DP ), dimension(m), intent(out) :: u

    ! Local variables
    ! Derivative estimates at different stages of the Runge-Kutta method
    real ( kind = DP ), dimension(m) :: f0, f1, f2, f3

    ! Intermediate state vectors at different stages of the Runge-Kutta method
    real ( kind = DP ), dimension(m) :: u1, u2, u3

    ! Intermediate times at different stages of the Runge-Kutta method
    real ( kind = DP ) :: t1, t2, t3

  !  Get four sample values of the derivative.
    ! Step 1: Evaluate the derivative at the initial time and state
    call f ( t0, m, u0, f0 )

    ! Step 2: Compute the intermediate state and derivative at the midpoint 1 of the interval
    t1 = t0 + dt / 2.0_DP
    u1 = u0 + dt * f0 / 2.0_DP
    call f ( t1, m, u1, f1 )

    ! Step 3: Compute the intermediate state and derivative at the midpoint 2 of the interval
    t2 = t0 + dt / 2.0_DP
    u2 = u0 + dt * f1 / 2.0_DP
    call f ( t2, m, u2, f2 )

    ! Step 4: Compute the intermediate state and derivative at the end of the interval
    t3 = t0 + dt
    u3 = u0 + dt * f2
    call f ( t3, m, u3, f3 )
  !
  !  Combine them to estimate the solution U at time T1.
  ! Step 5: Combine the four estimates to update the solution at t0 + dt
    u = u0 + ( dt / 6.0_DP ) * ( f0 + 2.0_DP * f1 + 2.0_DP * f2 + f3 )

  end subroutine rk4vec
  !*******************************************************************************

end module rk4_mod