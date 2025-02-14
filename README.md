# Joy-with-Sort-and-Scan

## Angular Sort
Run angular-sort.py by passing in the name of the timsort information file as a command line argument, but redirect both the standard input and output.
~~~
python3 angular-sort.py points-timsort-info.txt < input-points.txt > out
~~~
Since timsort is a deterministic sorting algorithm, the outputs of both files should match exactly.
Test the given input-output files using the diff Unix command.
~~~
diff sorted-points.txt out
~~~

## Closest Points
The file points.txt contatins a point set with 1 million points. Each point is described on a single line. It will produce a single line of output that indicates the distance of the closest pair.
Use the diff command to check if the output matches exactly with the one shown in file closest.out.
~~~
python3 closest.py < points.txt > out
diff out closest.out
~~~
In the above statement, note that the input file is acquired through standard input (using input redirection), and the output is sent to standard output.
