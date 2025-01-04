program sine
  use csv_module
  use nf, only: dense, input, network, sgd
  use iso_fortran_env, only: real32

  implicit none

  real, parameter :: pi = 4 * atan(1.)
  
  ! CSV file objects for the training, testing, and prediction data
  type(csv_file) :: sine_NN_data_file
  type(network) :: net

  ! Status of the CSV file operations
  logical :: status_ok
 
  ! Neural Network Training parameters
  integer, parameter :: num_iterations = 100000
  integer, parameter :: test_size = 50
  real(kind=real32), parameter :: learning_rate = 0.1
  
  ! Neural Network (Fully Connected) Parameters
  integer, parameter :: num_inputs = 1
  integer, parameter :: num_outputs = 1
  integer, parameter :: num_neurons_first_layer = 10
  integer, parameter :: num_neurons_second_layer = 10

  ! Training, Testing, and Prediction Data
  real(kind=real32), dimension(test_size) :: x_test, y_test, x_train, y_train, y_pred
  real, dimension(1) :: x_train_arr_temp
  real, dimension(1) :: y_train_arr_temp
  real, dimension(1) :: x_test_arr_temp
  real, dimension(1) :: y_pred_arr_temp
  
  ! Mean Squared Error
  real(kind=real32), dimension(num_iterations) :: mean_squared_error

  ! Loop variables
  integer :: i, j

  ! Temporary variables
  real(kind=real32) :: x_train_temp

  ! Initialize the CSV file
  call sine_NN_data_file%initialize(verbose=.true.)
  
  ! Open the CSV file
  print *, '[*] Opening the CSV file...'
  call sine_NN_data_file%open('sine_NN_data.csv', n_cols=7, status_ok=status_ok)
  if (.not. status_ok) then
    print *, '[!] Error opening the CSV file...'
    stop
  end if

  ! Add header to the CSV file
  print *, '[*] Adding header to the CSV file...'
  call sine_NN_data_file%add(['Iteration', 'x_test___', 'y_test___', 'x_train__', 'y_train__', 'y_pred___', 'MSE______'])
  call sine_NN_data_file%next_row()
  
  print '("[*] Creating Sine Wave Testing Data")'

  ! Create the Sine Wave Testing Data
  x_test = [((j - 1) * 2.0d0 * pi / test_size, j = 1, test_size)]
  y_test = (sin(x_test) + 1.0d0) / 2.0d0

  ! Create the Neural Network
  print *, '[*] Creating the Neural Network...'
  print '(60("="))'
  net = network([ &
    input(num_inputs), &
    dense(num_neurons_first_layer), &
    dense(num_neurons_second_layer), &
    dense(num_outputs) &
  ])

  ! Print the Neural Network information
  call net % print_info()
  print *

  ! Train the Neural Network
  print *, '[*] Training the Neural Network...'
  print '(60("="))'

  ! Loop over the number of iterations (epochs)
  do i = 1, num_iterations

    ! Train the Neural Network on the mini - batch of training data
    do j = 1, test_size
      ! Generate a random mini - batch of training data
      call random_number(x_train_temp)
      x_train(j) = x_train_temp * 2.0d0 * pi
      y_train(j) = (sin(x_train(j)) + 1.0d0) / 2.0d0

      ! Forward / backward pass and update the weights
      x_train_arr_temp = x_train(j)
      y_train_arr_temp = y_train(j)
      call net % forward(x_train_arr_temp)
      call net % backward(y_train_arr_temp)
      call net % update(optimizer=sgd(learning_rate=learning_rate))

      ! Evaluate the Neural Network on the testing data
      x_test_arr_temp = x_test(j)
      y_pred_arr_temp = net % predict(x_test_arr_temp)
      y_pred(j) = y_pred_arr_temp(1)
    end do
    
    ! Calculate the mean squared error
    mean_squared_error(i) = sum((y_pred - y_test)**2) / test_size

    do j = 1, test_size
      ! Save the iteration number, testing, training, prediction and mean squared error data to the CSV file
      ! For each interation there will be 30 rows of data of testing, training, prediction and mean squared error
      call sine_NN_data_file%add([i], int_fmt='(i6)')
      call sine_NN_data_file%add([ &
        x_test(j), & 
        y_test(j), &
        x_train(j), &
        y_train(j), &
        y_pred(j), &
        mean_squared_error(i)], &
        real_fmt='(f9.6)')
      call sine_NN_data_file%next_row()
    end do

    ! Print the MSE every (num_iterations/10) iterations
    if (mod(i, (num_iterations/10)) == 0) then
      print '("Iteration: ", I6, " | MSE: ", F9.6)', &
        i, mean_squared_error(i)
    end if
  
  end do

  print *, '[*] Training complete!'
  print *, '[*] Saving data to the CSV file...'

  ! Close the CSV file
  print *, '[*] Closing the CSV file...'
  call sine_NN_data_file%close(status_ok=status_ok)
  if (.not. status_ok) then
    print *, '[!] Error closing the CSV file...'
    stop
  end if
  
end program sine

