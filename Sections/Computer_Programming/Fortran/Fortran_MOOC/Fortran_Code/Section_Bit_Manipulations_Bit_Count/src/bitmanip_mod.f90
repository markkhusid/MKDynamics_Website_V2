module bitmanip_mod
    use, intrinsic :: iso_fortran_env, only : INT32, error_unit
    use csv_module

    implicit none

    private

    ! A 256-element lookup table stored in the module
    integer, public, parameter :: I4 = INT32
    integer, dimension(0:255), private :: lookup_table
    logical, private, save :: initialized = .false.

    ! Public procedures
    public :: naive_count_bits, early_stopping_count_bits, bit_repr, &
              lookup_table_count_bits, kernighan_count_bits

contains

    !----------------------------------------------------------------------
    !> Main routine that ensures the module lookup_table is initialized
    subroutine ensure_lookup_table_initialized()
        if (.not. initialized) then
            call initialize_lookup_table()
        end if
    end subroutine ensure_lookup_table_initialized

    !----------------------------------------------------------------------
    !> Initialize the module lookup_table by reading 256 integers from the CSV
    subroutine initialize_lookup_table()
        implicit none
        integer :: ios

        ! Clear the module array
        lookup_table = 0

        ! Call parse_csv_file to fill the local array
        call parse_csv_file("lookup_table.csv", lookup_table, ios)

        if (ios == 0) then
            initialized = .true.
        else
            write(error_unit, '(A,I0)') "Failed to read CSV lookup table, ios=", ios
            stop 1
        end if
    end subroutine initialize_lookup_table

    !----------------------------------------------------------------------
    !> Reads up to 256 integers from the CSV file using csv-fortran’s get_csv_data_as_str
    subroutine parse_csv_file(filename, table_data, ios)
        !! Reads a CSV file that has trailing ", &" on each line,
        !! removing them before calling csv-fortran's get_csv_data_as_str.
        use csv_module
        
        implicit none

        character(len=*), intent(in) :: filename
        integer, dimension(256), intent(out) :: table_data
        integer, intent(out) :: ios

        type(csv_file) :: c
        character(len=255), allocatable, dimension(:,:) :: string_table
        integer :: nrow, ncol
        integer :: i, j, idx, ios2, val

        !! For pre-processing:
        integer :: uin, uout, stat_in, stat_out
        character(len=1024) :: line, tmpfile
        logical :: done, status_ok

        ! Initialize outputs
        ios = 0
        table_data = 0

        ! Generate a temp file name
        tmpfile = 'tempfile.csv'

        !-------------------------------------------------
        !  STEP 1: Pre-process 'filename' => 'tempfile.csv'
        !-------------------------------------------------
        open(newunit=uin, file=filename, status='old', action='read', &
            form='formatted', iostat=stat_in)
        if (stat_in /= 0) then
            write(*,*) "Error opening input file:", filename
            ios = 101
            return
        end if

        open(newunit=uout, file=tmpfile, status='replace', action='write', &
            form='formatted', iostat=stat_out)
        if (stat_out /= 0) then
            write(*,*) "Error creating temp file:", tmpfile
            ios = 102
            close(uin)
            return
        end if

        do
            read(uin, '(A)', iostat=stat_in) line
            if (stat_in < 0) exit   ! EOF
            if (stat_in /= 0) then
                ios = 103
                exit
            end if

            call remove_trailing_comma_ampersand(line)
            write(uout, '(A)') trim(line)
        end do

        close(uin)
        close(uout)

        if (ios /= 0) return  ! Error occurred

        !----------------------------------
        ! STEP 2: Use csv-fortran on tmpfile
        !----------------------------------

        call c%initialize()
        call c%read(tmpfile, status_ok=status_ok)
        if (ios /= 0) then
            write(*,*) "Error reading temp CSV file:", tmpfile
            call c%close(status_ok)
            return
        end if

        call c%get(string_table, status_ok=status_ok)
        if (ios /= 0) then
            write(*,*) "Error extracting data as strings."
            call c%close(status_ok)
            return
        end if

        ! Parse up to 256 integers
        nrow = size(string_table,1)
        ncol = size(string_table,2)

        idx = 1
        do i = 1, nrow
            do j = 1, ncol
                if (len_trim(string_table(i,j)) > 0) then
                    read(string_table(i,j), *, iostat=ios2) val
                    if (ios2 == 0) then
                        if (idx <= 256) table_data(idx) = val
                        idx = idx + 1
                    else
                        write(*,*) "Error converting cell:", trim(string_table(i,j))
                        ios = 2
                        call c%close(status_ok)
                        return
                    end if
                end if
            end do
        end do

        if (idx - 1 < 256) then
            write(*,*) "Not enough integers. Found", idx - 1
            ios = 3
        end if

        ! Close CSV
        call c%close(status_ok)

    end subroutine parse_csv_file

    !------------------------------------------
    subroutine remove_trailing_comma_ampersand(line)
        implicit none
        character(len=*), intent(inout) :: line
        integer :: n

        n = len_trim(line)
        if (n < 3) return

        do while (n >= 3)
            if (line(n-2:n) == ", &") then
                line(n-2:n) = ""
                n = n - 3
            else
                exit
            end if
        end do
    end subroutine remove_trailing_comma_ampersand

    !----------------------------------------------------------------------
    !> Bit-counting routines that rely on the lookup_table
    function naive_count_bits(n) result(bit_count)
        implicit none
        integer(kind=I4), value :: n
        integer :: bit_count
        integer :: i

        call ensure_lookup_table_initialized()

        bit_count = 0
        do i = 1, 32
            bit_count = bit_count + and(n, 1_I4)
            n = ishft(n, -1)
        end do
    end function naive_count_bits

    function early_stopping_count_bits(n) result(bit_count)
        implicit none
        integer(kind=I4), value :: n
        integer :: bit_count
        integer :: i

        call ensure_lookup_table_initialized()

        bit_count = 0
        do i = 1, 32
            bit_count = bit_count + and(n, 1_I4)
            n = ishft(n, -1)
            if (n == 0) exit
        end do
    end function early_stopping_count_bits

    function lookup_table_count_bits(n) result(bit_count)
        implicit none
        integer(kind=I4), value :: n
        integer :: bit_count

        call ensure_lookup_table_initialized()

        ! The lookup table is now loaded
        bit_count = lookup_table(and(n, 255_I4)) + &
                    lookup_table(and(ishft(n, -8), 255_I4)) + &
                    lookup_table(and(ishft(n, -16), 255_I4)) + &
                    lookup_table(and(ishft(n, -24), 255_I4))
    end function lookup_table_count_bits

    function kernighan_count_bits(n) result(bit_count)
        implicit none
        integer(kind=I4), value :: n
        integer :: bit_count

        call ensure_lookup_table_initialized()

        bit_count = 0
        do while (n /= 0)
            n = and(n, n - 1_I4)
            bit_count = bit_count + 1
        end do
    end function kernighan_count_bits

    function bit_repr(val) result(repr)
        implicit none
        integer(kind=I4), value :: val
        character(len=32) :: repr
        integer :: i

        do i = 32, 1, -1
            if (and(val, 1_I4) == 1_I4) then
                repr(i:i) = '1'
            else
                repr(i:i) = '0'
            end if
            val = ishft(val, -1)
        end do
    end function bit_repr

end module bitmanip_mod
