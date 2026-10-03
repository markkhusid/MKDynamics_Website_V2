module spectrum
    use, intrinsic :: iso_fortran_env, only: int32, real64
    implicit none
    private
    public :: spectrum_of, write_series, print_peaks

contains

    subroutine spectrum_of(samples, sample_rate, magnitude, frequency, phase)
        real(real64), intent(in) :: samples(:)
        real(real64), intent(in) :: sample_rate
        real(real64), allocatable, intent(out) :: magnitude(:)
        real(real64), allocatable, intent(out) :: frequency(:)
        real(real64), allocatable, intent(out) :: phase(:)
        complex(real64), allocatable :: bins(:)
        integer(int32) :: n, k, half
        real(real64) :: pi, scale

        n = size(samples, kind=int32)
        if (.not. is_power_of_two(n)) then
            error stop 'spectrum_of: length must be a power of two'
        end if

        allocate(bins(n))
        do k = 1, n
            bins(k) = cmplx(samples(k), 0.0_real64, real64)
        end do
        call fft_inplace(bins)

        half = n / 2
        allocate(magnitude(half + 1))
        allocate(frequency(half + 1))
        allocate(phase(half + 1))
        pi = acos(-1.0_real64)
        scale = real(n, real64)
        do k = 0, half
            frequency(k + 1) = real(k, real64) * sample_rate / scale
            if (k == 0 .or. k == half) then
                magnitude(k + 1) = abs(bins(k + 1)) / scale
            else
                magnitude(k + 1) = 2.0_real64 * abs(bins(k + 1)) / scale
            end if
            phase(k + 1) = atan2(aimag(bins(k + 1)), real(bins(k + 1))) * (180.0_real64 / pi)
        end do
    end subroutine spectrum_of

    subroutine write_series(time_path, spectrum_path, sample_rate, samples, &
            magnitude, frequency, phase)
        character(len=*), intent(in) :: time_path
        character(len=*), intent(in) :: spectrum_path
        real(real64), intent(in) :: sample_rate
        real(real64), intent(in) :: samples(:)
        real(real64), intent(in) :: magnitude(:)
        real(real64), intent(in) :: frequency(:)
        real(real64), intent(in) :: phase(:)
        integer(int32) :: unit, i

        open(newunit=unit, file=time_path, status='replace', action='write')
        do i = 1, size(samples, kind=int32)
            write(unit, '(es24.16, 1x, es24.16)') &
                real(i - 1, real64) / sample_rate, samples(i)
        end do
        close(unit)

        open(newunit=unit, file=spectrum_path, status='replace', action='write')
        do i = 1, size(magnitude, kind=int32)
            write(unit, '(es24.16, 1x, es24.16, 1x, es24.16)') &
                frequency(i), magnitude(i), phase(i)
        end do
        close(unit)
    end subroutine write_series

    subroutine print_peaks(frequency, magnitude, phase, threshold)
        real(real64), intent(in) :: frequency(:)
        real(real64), intent(in) :: magnitude(:)
        real(real64), intent(in) :: phase(:)
        real(real64), intent(in) :: threshold
        integer(int32) :: i, count

        count = size(magnitude, kind=int32)
        print '(a)', 'frequency_hz magnitude phase_deg'
        do i = 0, count - 1
            call print_one_peak(frequency(i + 1), magnitude(i + 1), phase(i + 1), threshold)
        end do
    end subroutine print_peaks

    ! A block-if on a real comparison is miscompiled by the LFortran kernel.
    ! The test is stored in a logical, and the branch uses that logical.
    subroutine print_one_peak(frequency, magnitude, phase, threshold)
        real(real64), intent(in) :: frequency
        real(real64), intent(in) :: magnitude
        real(real64), intent(in) :: phase
        real(real64), intent(in) :: threshold
        character(len=48) :: line
        logical :: keep

        keep = magnitude >= threshold
        write(line, '(f12.3, 1x, f12.6, 1x, f12.3)') frequency, magnitude, phase
        if (.not. keep) return
        print '(a)', trim(line)
    end subroutine print_one_peak

    subroutine fft_inplace(bins)
        complex(real64), intent(inout) :: bins(:)
        complex(real64) :: twiddle, twiddle_step, even, odd
        integer(int32) :: n, bits, i, reversed, length, half, start, k
        real(real64) :: angle

        n = size(bins, kind=int32)
        bits = 0
        length = 1
        do while (length < n)
            length = length * 2
            bits = bits + 1
        end do

        do i = 0, n - 1
            reversed = reverse_bits(i, bits)
            if (reversed > i) then
                even = bins(i + 1)
                bins(i + 1) = bins(reversed + 1)
                bins(reversed + 1) = even
            end if
        end do

        length = 2
        do while (length <= n)
            half = length / 2
            angle = -2.0_real64 * acos(-1.0_real64) / real(length, real64)
            twiddle_step = cmplx(cos(angle), sin(angle), real64)
            do start = 1, n, length
                twiddle = cmplx(1.0_real64, 0.0_real64, real64)
                do k = 0, half - 1
                    even = bins(start + k)
                    odd = twiddle * bins(start + k + half)
                    bins(start + k) = even + odd
                    bins(start + k + half) = even - odd
                    twiddle = twiddle * twiddle_step
                end do
            end do
            length = length * 2
        end do
    end subroutine fft_inplace

    pure integer(int32) function reverse_bits(value, bits) result(reversed)
        integer(int32), intent(in) :: value
        integer(int32), intent(in) :: bits
        integer(int32) :: bit, remaining

        reversed = 0
        remaining = value
        do bit = 1, bits
            reversed = reversed * 2_int32 + mod(remaining, 2_int32)
            remaining = remaining / 2_int32
        end do
    end function reverse_bits

    pure logical function is_power_of_two(n)
        integer(int32), intent(in) :: n
        is_power_of_two = n >= 2 .and. iand(n, n - 1_int32) == 0
    end function is_power_of_two

end module spectrum
