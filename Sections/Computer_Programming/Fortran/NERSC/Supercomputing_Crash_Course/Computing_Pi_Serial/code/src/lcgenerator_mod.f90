module lcgenerator_mod
  use, intrinsic :: iso_fortran_env, only : DP => REAL64, I8 => INT64
  implicit none
  private
  public :: lcgrandom

  contains
    real function lcgrandom()
      integer(kind=I8), parameter :: MULTIPLIER = 1366
      integer(kind=I8), parameter :: ADDEND = 150889
      integer(kind=I8), parameter :: PMOD = 714025
      integer(kind=I8), save :: random_last = 0

      integer(kind=I8) :: random_next = 0
      random_next = mod((MULTIPLIER * random_last + ADDEND), PMOD)
      random_last = random_next
      lcgrandom = (1.0_DP * random_next) / PMOD
      return
    end function lcgrandom
end module lcgenerator_mod
