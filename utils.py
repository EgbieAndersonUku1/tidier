
from os.path import getmtime
from datetime import datetime
from file_extenstions import extentions

VIDEO_EXT, DOCUMENTS_EXT, ALL_DOCUMENTS, PROGRAMMING_EXT = extentions()

def convert_month_to_str(month_num):
    """convert_month_to_str(int)> return(str)

    params: month_num, Takes a number and converts it to a string
    """
    months = {1: 'January',    2: 'February', 3 : 'March',    4 : 'April',
              5: 'May',        6: 'June',     7 : 'July',     8 : 'August',
              9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    return months.get(month_num, None)

def get_file_usage(ext):
    """get_file_usage(string) -> return(string)

    Returns the type of documents used for that extenstion
    e.g docx returns -> Microsoft word documents
        xls  returns  -> Excel document
    """
    ext = '.' + ext.lower()
    file_ext = DOCUMENTS_EXT.get(ext, None)     # check for file extenstion in small dictionary document
    if file_ext == None:
        file_ext = ALL_DOCUMENTS.get(ext, None) # check for file extenstion in larger dictionary document
        if file_ext == None:
            file_ext = PROGRAMMING_EXT.get(ext, None) # check in the programming extenstion dictionary
            if file_ext == None:
                file_ext = VIDEO_EXT.get(ext, None) # check for ext in video file dictionary
    return file_ext

def get_time_stamp(f):
    """get_time_stamp(str) -> return(tuple)
        Returns the time stamp of the date the file was created.

        Returns tuple in the format of (yyyy, mm, dd)
    """
    try:
         date_obj = datetime.fromtimestamp(getmtime(str(f)))
    except KeyError:
         return None, None, None
    return str(date_obj.year), convert_month_to_str(date_obj.month), str(date_obj.day)
