# hex_utils
Hex utilities that I made as a form of training

simple_hex_viewer: 
It prints the hex values of a file and it's ascii equivalents.
To run it you need to pass two arguments in a command line, the file (-f) and the size of lines in bytes (-s)

simple_hex_comparator: 
It compares the hex values changes between two files based on their relative addresses, has better use when it's the same file but altered
To run it you need to pass in a command line the original file (-ff) and the altered one (-sf), you can also specify the number of bytes per line (-n) and if you want
to print only the altered bytes (-e)
