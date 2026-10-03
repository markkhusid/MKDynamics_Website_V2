module signals
    use, intrinsic :: iso_fortran_env, only: int32, real64
    implicit none
    private
    public :: sine_tone, square_wave, two_sines, switched_sine

contains

    function sine_tone(n, sample_rate, frequency, amplitude) result(samples)
        integer(int32), intent(in) :: n
        real(real64), intent(in) :: sample_rate
        real(real64), intent(in) :: frequency
        real(real64), intent(in) :: amplitude
        real(real64), allocatable :: samples(:)
        integer(int32) :: i
        real(real64) :: pi

        pi = acos(-1.0_real64)
        allocate(samples(n))
        do i = 1, n
            samples(i) = amplitude * sin(2.0_real64 * pi * frequency * time_at(i, sample_rate))
        end do
    end function sine_tone

    function square_wave(n, sample_rate, frequency, amplitude) result(samples)
        integer(int32), intent(in) :: n
        real(real64), intent(in) :: sample_rate
        real(real64), intent(in) :: frequency
        real(real64), intent(in) :: amplitude
        real(real64), allocatable :: samples(:)
        integer(int32) :: i
        real(real64) :: position

        allocate(samples(n))
        do i = 1, n
            position = modulo(time_at(i, sample_rate) * frequency, 1.0_real64)
            samples(i) = merge(amplitude, -amplitude, position < 0.5_real64)
        end do
    end function square_wave

    function two_sines(n, sample_rate, frequency_a, amplitude_a, &
            frequency_b, amplitude_b) result(samples)
        integer(int32), intent(in) :: n
        real(real64), intent(in) :: sample_rate
        real(real64), intent(in) :: frequency_a
        real(real64), intent(in) :: amplitude_a
        real(real64), intent(in) :: frequency_b
        real(real64), intent(in) :: amplitude_b
        real(real64), allocatable :: samples(:)
        integer(int32) :: i
        real(real64) :: pi, t

        pi = acos(-1.0_real64)
        allocate(samples(n))
        do i = 1, n
            t = time_at(i, sample_rate)
            samples(i) = amplitude_a * sin(2.0_real64 * pi * frequency_a * t) &
                + amplitude_b * sin(2.0_real64 * pi * frequency_b * t)
        end do
    end function two_sines

    function switched_sine(n, sample_rate, carrier, gate, amplitude) result(samples)
        integer(int32), intent(in) :: n
        real(real64), intent(in) :: sample_rate
        real(real64), intent(in) :: carrier
        real(real64), intent(in) :: gate
        real(real64), intent(in) :: amplitude
        real(real64), allocatable :: samples(:)
        integer(int32) :: i
        real(real64) :: pi, t, position

        pi = acos(-1.0_real64)
        allocate(samples(n))
        do i = 1, n
            t = time_at(i, sample_rate)
            position = modulo(t * gate, 1.0_real64)
            samples(i) = merge(amplitude * sin(2.0_real64 * pi * carrier * t), &
                0.0_real64, position < 0.5_real64)
        end do
    end function switched_sine

    pure real(real64) function time_at(index, sample_rate)
        integer(int32), intent(in) :: index
        real(real64), intent(in) :: sample_rate
        time_at = real(index - 1, real64) / sample_rate
    end function time_at

end module signals
