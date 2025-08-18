module get_nr_iters_mod
    implicit none
    private
    public :: get_nr_iters

contains

    function get_nr_iters() result(nr_iters)
        use, intrinsic :: iso_fortran_env, only : error_unit
        use, intrinsic :: iso_fortran_env, only : DP => REAL64, I8 => INT64
        implicit none
        integer(kind=I8) :: nr_iters
        integer(kind=I8), parameter :: default_nr_iters = 1000_I8
        character(len=1024) :: buffer, msg
        integer :: istat

        if (command_argument_count() >= 1) then
            call get_command_argument(1, buffer)
            read (buffer, fmt=*, iostat=istat, iomsg=msg) nr_iters
            if (istat /= 0) then
                write (unit=error_unit, fmt='(2A)') &
                    'error: ', msg
                stop 1
            end if
        else
            nr_iters = default_nr_iters
        end if
    end function get_nr_iters

end module get_nr_iters_mod
