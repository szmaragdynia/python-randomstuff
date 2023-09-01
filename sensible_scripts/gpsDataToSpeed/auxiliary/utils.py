
from auxiliary.constants import path_to_files_dir, log_filename
import csv
import atexit
log_file = open(path_to_files_dir + log_filename, 'w')                # this is executed at module import!

def logger(*args_list, **keyword_args_dict):                          # names for future-me
    if "stream" in keyword_args_dict:
        if keyword_args_dict["stream"] == "consoleOnly":
            del keyword_args_dict["stream"]                           # so it's not "used" (and crashed) by print
            print(*args_list, **keyword_args_dict)
        elif keyword_args_dict["stream"] == "fileOnly":
            del keyword_args_dict["stream"] 
            print(*args_list, file=log_file, **keyword_args_dict)
    else:
        print(*args_list, **keyword_args_dict)
        print(*args_list, file=log_file, **keyword_args_dict)


def saveDictListAsCsv(dictionaries_list, file_name):
  csv_headers = dictionaries_list[0].keys()
  with open(path_to_files_dir + file_name, 'w', newline='') as output_file:             #  '' is imporant, beacuse else I get empty rows in csv every entry
    dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
    dict_writer.writeheader()
    dict_writer.writerows(dictionaries_list)


def nDigitsToWriteDownIndex(list):
    return len(str(len(list)))

@atexit.register
def _closing():                      # " This convention is used for declaring private variables, functions, methods and classes in a module. Anything with this convention are ignored in from module import *. "
    log_file.close()
    # logger('Just closed log_file') # this cannot be done as file is closed - as it shoulb be. Leaving as comment for odd-cases-debugger