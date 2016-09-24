NAME          : Tidier
Author        : Egbie Uku

Description
============

The more we use our computers the messy our directories become.

What do I mean this ?

Well we are constantly downloading, creating and adding new files to our
directories in an unorder manner. Before we know it our directories has
become a cesspool of files where we can no longer make head or tails and lets
not mention searching for files.

What this program does is tidies your directory or reclusive tidies your
directory if that option is selected by sorting the files into
folders based on the year, date and the file extenstion their were created.

For example if you have a file in your computer that was created on the
10th march 2014. The file in question is a PDF file located in the Desktop.

Then the program would perform several steps

1) Create the folder named 2014 the year the file was created.

2) Within that folder it would created the month folder the month the folder was created. In this caseis March.

3) Within the month( March in this case) folder it would create another folder the date the folder was
   created which in this case is the 10_march_2014.

4) Finally it would create another folder using the extenstion of the file as name
   of the folder e.g. pdf_files before moving the file to that folder and viola no more untidy files.

Now for each file it finds it would run the four steps above if the folder does not already exist. If it exists
the four steps above will be negeated and the file would be move to that folder instead.

Now you have the files in sort order based on the year and date their were created.


Program information

 The program takes a directory and tidies or reclusive tidies
 the file or the files in that sub-directories based on the creation
 date.

 Program usages

 -d directory path

 optional arguments

 -r reclusive tidies a directory and all sub-directories within it
 -e Takes a list of directories all separted with commas or a single directory
    and excludes from the cleanup list.
    e.g.
    dir/path1, dir/path2, dir/path3
