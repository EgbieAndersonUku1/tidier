# -*- coding: utf-8 -*-

###############################################################################
#  NAME          : Tidier
#  Author        : Egbie Uku
#
#  Description
#  The more we use our computers the messy our directories become.
#  What do I by mean this...
#
#  Well we are constantly downloading, creating and adding new files to our
#  directories in an unorder manner. Before we know it our directories has
#  become a cesspool of files where we can no longer make head or tails and less
#  not mention searching for files.

#  What this program does is tidies your directory or reclusive tidies your
#  directory if that option is selected by sorting your files into
#  folders based on the year, date and the file extenstion their were created.
#
#  For example if you have a file in your computer that was created on the
#  10th march 2014 and the file is a PDF file located on the Desktop.
#  Then the program would create the folder named 2014 the year the file was created
#   and within that folder it would created 10_march_2014 the date the file was created
#   and finally it would create another folder called pdf_files the extenstion used for the file.
#  Finally it would move the file to that folder and viola no more untidy files.
#
# Now you have files in sorted order based on the year and date their were created
#
# DOES NOT WORK IN WINDOWS BECAUSE WINDOWS USES CPICKLE AND LINUX USES DLL

###############################################################################

from os import listdir, chdir, getcwd, mkdir
from os.path import isdir, isfile, join, dirname, exists, join
from utils import get_time_stamp, get_file_usage, convert_month_to_str
from shutil import move
from pathos.multiprocessing import ProcessingPool as Pool
from operator import concat
from optparse import OptionParser

class Tidier(object):
    """Tidies files in a directory or sub-directory based on their creation date.

    params path        : The path containing the files
    params exclude_dirs: The path to directories to exclude.from tidying
    """
    def __init__(self, path, excluded_dirs=[]):

        if not exists(path):
            return '[-] Directory does not exists !!!'

        self.path  =  path[:-1] if (path.endswith('/') or path.endswith('//')) else path # remove back slash for the URL if exists
        self.exclude_dirs = {}
        for f in excluded_dirs: #
            if f:
                if f.endswith('/') or f.endswith('//'):
                    self.exclude_dirs[str(f[:-1])] = True
                else:
                    self.exclude_dirs[str(f)] = True

    def _make_directory(self, path, name):
        """_make_directory(str,) str) -> return(None)

        params path: The path for the directory to be created
        params name: The name for the given directory
        """
        mkdir(join(path, name))

    def set(self, path):
        """set a path to given path"""
        self.path = path

    def _get_dir_contents(self):
        """Returns the entire contents of a directory"""

        # Return the content of the file if its not in not included list
        if not self.exclude_dirs.get(self.path, False):
            return [join(self.path, f) for f in listdir(self.path) if not f.startswith('.')]
        return []

    def get_files(self, f):
        """get_files(str) -> return(list)

        Returns all files within a directory non reclusive mode.
        """
        files = []

        if isdir(f):
            chdir(f)
            self.set(getcwd())
            for f in self._get_dir_contents():
                if not isdir(f):
                    files.append(f)
        else:
            files.append(f)
        return files

    def get_files_rercursive_mode(self, f):
        """get_files_rercursive_mode(None) -> return(None)

        Given a given directory recursive searches that directory and sub-directory
        within that folder and extract all the contents.
        """
        files, stack   = [], None

        # For each file in the for loop it checks if whether its a directory.
        # If the file is a directory it changes into that directory and extract the contents
        # If it is a file it appends the content to a file list.
        f = str(f)
        if isdir(f):
            chdir(f)
            self.set(f)
            stack, next_depth = self._get_dir_contents(), [] # extract the content of that directory
        else:
            files.append(f)

        # recursive search through each sub-directory until there are no more files
        while stack:
            f = str(stack.pop())
            if isdir(f):
                chdir(f)
                self.set(f)
                next_depth.extend(self._get_dir_contents())
            else:
                files.append(f)
            if not stack:
                stack, next_deptph = next_depth, []   # empty the contents of next_depth into the stack
        return files

    def save_error_logs(self, events):
        pass

    def _process_file(self, current_path, f, dir_name_path):
        """process_file(str, str, str) -> return(None)

        params -> current_path : The current path
        params -> f: A file path
        params -> dir_name_path: creates a directory by the that name at path x

        Takes a file from the current directory and moves it to the new directory
        path.
        """
        current_path, f, dir_name_path = str(current_path), str(f), str(dir_name_path)
        if exists(dir_name_path):
            if not exists(f): move(f, current_path)
        else:
            try:
                mkdir(dir_name_path)
            except:
                print('[-] Insufficient permission to create directory in specific location')
            else:
                chdir(dir_name_path)
                move(f, getcwd())

    def categorise_files(self, f):
        """categorise_files(str) -> return(None)

        param f (file): A file that would be categorise.
        Sorts a file based on the date it was created.
        """
        year, month, day = get_time_stamp(f.strip())
        events, file_errors  = [], []

        if year != None:
            date = '{}_{}_{}'.format(day, month, year)
            dir_name_path = str(get_file_usage(f.split('.')[-1]))
            dir_path = str(dirname(f))
            chdir(dir_path)

            # check if the folder for year, month, date exists
            # if it does it moves the file over. If any of the folder
            # does not exist it creates the missing folders before moving the files over
            if exists(year):
                chdir(year)
                if exists(month):
                    chdir(month)
                    if exists(date):
                        chdir(date)
                        if exists(dir_name_path):
                            chdir(dir_name_path)
                            try:
                                move(f, getcwd())
                            except:
                                events.append(f)
                        else:
                            self._process_file(getcwd(), f, dir_name_path)
                    else:
                        date_dir = join(getcwd(), date)
                        mkdir(date_dir)
                        chdir(date_dir)
                        self._process_file(getcwd(), f, dir_name_path)
                else:
                    month_dir = join(getcwd(), month)
                    mkdir(month)
                    chdir(month_dir)
                    mkdir(date)
                    chdir(date)
                    self._process_file(getcwd(), f, dir_name_path)
            else:
                year_dir = join(dir_path, year)
                try:
                    mkdir(year_dir)
                    chdir(year_dir)
                    mkdir(month)
                    chdir(month)
                    mkdir(date)
                    chdir(date)
                except OSError:
                    print('[-] Sufficient permission to access file')
                else:
                    self._process_file(getcwd(), f, dir_name_path)
        else:
            file_errors.append(f)

        #self.save_error_logs(events, file_errors)

def run(tidier_obj, recursive=False):
    """Tidies up the files either by using reclusive or non reclusive mode"""

    def tidy(command):
        p = Pool(processes=10)
        files = tidier_obj._get_dir_contents()
        files_num = len(files)

        try:
            results = p.map(command, files, chunksize=10)
        except OSError:
            exit('[+] You do not have permission to tidy that file')
        else:
            print('[+] Obtaining the files needed to tidy please wait....')

            try:
                t = reduce(concat, results) # concatenate all the lists together
            except TypeError:
                print('[-] No files found!!!')
            else:
                p.map(tidier_obj.categorise_files, t, chunksize=5)
                p.close()
                p.join()
                print('[+] Done the files have been tidied.')

    if not recursive:
        print('[+] Performing tidy in chosen directory please wait....')
        tidy(tidier_obj.get_files)
    else:
        print('[+] Performing reclusive tidy of files within that directory this could take a while please wait....')
        tidy(tidier_obj.get_files_rercursive_mode)

def main():
    parser = OptionParser('usage % -d <directory to tidy>, optional -r <when added reclusive tidies that directory>')
    parser.add_option('-e', '--exclude_dirs', dest='excluded_dirs', type=str, help='Takes a string of directories each separated with commas e.g./home/path_to_some_directory, /home/path_to_dir2. Exclude all files in this path')
    parser.add_option('-d', '--directory_path', dest='directory', help='The directory to tidy' )
    parser.add_option('-r', '--recursive', action='store_true', dest='recursive_tidy', default=False,
                           help='when use with -d command recursive tidies all directories and sub-directories in that folder' )

   
    (options, args) = parser.parse_args()
    if options.excluded_dirs:
        dirs_to_exclude = options.excluded_dirs.split(',')
	
    if options.directory:
        if options.directory == '.': # if the user enters '.' meaning current directory
          options.directory = getcwd()
        else:
          if not exists(options.directory):
             parser.usage
        if not options.recursive_tidy and not options.excluded_dirs:
             run(Tidier(options.directory))
        elif not options.recursive_tidy and options.excluded_dirs:
             print('[+] A total of {} will be excluded in the clean up'.format(len(dirs_to_exclude)))
             run(Tidier(options.directory, dirs_to_exclude))
        elif options.recursive_tidy and not options.excluded_dirs:
             run(Tidier(options.directory), True)
        elif options.recursive_tidy and options.excluded_dirs:
             run(Tidier(options.directory, dirs_to_exclude), True)
    else:
        parser.usage = '''

                 Program information
                 ===================

                 The program takes a directory and tidies or reclusive tidies
                 the file or the files in that sub-directories based on the creation
                 date.

                 Program usage
                 =============

                 -d <directory path>

                 optional arguments
                 ===================

                 -r reclusive tidies a directory and all sub-directories within it
                 -e Takes a string of directories all separted with commas or a single directory
                    and excludes them from the cleanup list. Enter either ' or " at the start of
                    the string and at the end of the string. Otherwise only the first directory would be
                    excluded.
		    
                    e.g.
                    'dir/path1, dir/path2, dir/path3' or "dir/path1, dir/path2, dir/path3"
              '''
        print(parser.usage)

if __name__ == '__main__':
    main()
