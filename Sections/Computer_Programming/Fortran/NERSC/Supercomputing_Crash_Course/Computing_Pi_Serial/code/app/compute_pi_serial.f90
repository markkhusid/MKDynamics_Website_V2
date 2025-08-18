! Compute pi in serial
program compute_pi_serial
  use, intrinsic :: iso_fortran_env, only : DP => REAL64, I8 => INT64
  use lcgenerator_mod,  only : lcgrandom
  use get_nr_iters_mod, only : get_nr_iters
  
  implicit none

  integer(kind=I8) :: num_trials, i = 0, Ncirc = 0
  real(kind=DP) :: pi_computed = 0.0, pi_actual
  real(kind=DP) :: x = 0.0, y = 0.0, r = 1.0
  real(kind=DP) :: r_squared = 0.0

  pi_actual = 2.0_DP * acos(0.0_DP)
  
  r_squared = r*r

  num_trials = get_nr_iters()

  do i = 1, num_trials
    x = lcgrandom()
    y = lcgrandom()
    if ((x*x + y*y) <= r_squared) then
        Ncirc = Ncirc + 1
    end if
  end do

  pi_computed = 4.0*((1.0*Ncirc)/(1.0*num_trials))

  print '(A, I10, A, F25.15)', "After ", num_trials, " loops, Pi = ", pi_computed
  print '(A, F25.15)', "Actual value of Pi = ", pi_actual
  print '(A, F25.15)', "Absolute difference = ", abs(pi_computed - pi_actual)

end program compute_pi_serial