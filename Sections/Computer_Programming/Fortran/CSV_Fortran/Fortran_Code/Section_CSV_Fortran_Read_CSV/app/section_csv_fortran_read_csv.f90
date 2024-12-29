program csv_read_test

  use csv_module
  use iso_fortran_env, only: wp => real64
  
  implicit none
  
  type(csv_file) :: f
  logical :: status_ok
  integer,dimension(:),allocatable :: itypes

  character(len=5),dimension(:),allocatable :: header
  real(wp),dimension(:),allocatable :: x,y,z
  logical,dimension(:),allocatable :: t

  character(len=30), dimension(:,:), allocatable :: table_data_strings
  real(wp), dimension(:,:), allocatable :: table_data_floats

  character(len=30) :: trimmed_string
    
  integer :: i, j, n_rows, n_cols
  integer, dimension(1) :: dim_header
  integer, dimension(2) :: dims_table
  
  ! read the file
  call f%read('test.csv',header_row=1,status_ok=status_ok)
  
  ! get the header and type info
  call f%get_header(header,status_ok)
  call f%variable_types(itypes,status_ok)
  
  ! get some data
  call f%get(1, x, status_ok)
  call f%get(2, y, status_ok)
  call f%get(3, z, status_ok)
  call f%get(4, t, status_ok)
  call f%get(table_data_strings, status_ok)

  ! print the size, shape and contents of the header
  print *, "Print out the size, shape and contents of the header"
  write (*, '(a, i3)') 'size = ', size(header)
  dim_header = shape(header)
  write (*, '(a, i3)') 'shape = ', dim_header(1)
  write (*, *) 'header = ', header

  print *

  ! print the types
  print *, "Print out the types"
  write (*, *) 'types = ', itypes

  print *
  
  ! print the data
  print *, "Print out the data that was read one at a time"
  print *, 'x = ',x
  print *, 'y = ',y
  print *, 'z = ',z
  print *, 't = ',t

  print *

  ! print the size, shape and contents of the table data
  print *, "Print out the size, dimensions and contents of the table data read all at once"
  write (*, '(a, i3)') 'table size = ', size(table_data_strings)

  dims_table = shape(table_data_strings)
  n_rows = dims_table(1)
  n_cols = dims_table(2)

  write (*, '(a, i3)') '# of rows = ', n_rows
  write (*, '(a, i3)') '# of columns = ', n_cols
  print *
  print *, "Printing out the table data directly from the variable..."
  write (*, *) 'table_data = ', table_data_strings

  ! use loop to print the table data
  print *, "Using loop to print the table data..."
  do i = 1, size(table_data_strings,1)
    write (*, *) table_data_strings(i,:)
  end do

  print *

  ! convert the table data to floats
  print *, "Converting the table data from strings to floats..."

  allocate(table_data_floats(n_rows,n_cols))
  do i = 1, n_rows
    do j = 1, (n_cols - 1) ! last column is a string i.e. T or F
      trimmed_string = adjustl(trim(table_data_strings(i,j)))
      read(trimmed_string, *) table_data_floats(i,j)
      !read(trimmed_string, '(f30.20)') table_data_floats(i,j)
      !print *, 'trimmed_string = ', trimmed_string
    end do
  end do

  print *

  ! print the table data as floats using a loop
  print *, "Printing out the table data as floats using a loop"
  do i = 1, n_rows
      write (*, *) table_data_floats(i,1:3)
  end do

  deallocate(table_data_floats)
  deallocate(table_data_strings)
  deallocate(header)
  deallocate(itypes)
  deallocate(x)
  deallocate(y)
  deallocate(z)
  deallocate(t)

  ! destroy the file
  call f%destroy()
  
  end program csv_read_test
  
