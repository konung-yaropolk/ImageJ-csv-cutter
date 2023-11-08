#!/usr/bin/env python3
import os
import re


TIME_BEFORE_TRIG = 10    # in sec.
TIME_AFTER_TRIG  = 30    # in sec.

DIRECTORIES = [
    # 'C:/Users/yarop/Coding/ImageJ-csv-cutter/',
     'F:/Lab Work Files/scripts/ImageJ-csv-cutter',
    # 'F:/Lab Work Files/2-photon',
    
]


def metadata_parser(path, file):    
    file_path = path + file
    events = []

    with open(file_path + '.txt', 'r') as file:

        trigger = '"[Event '
        strings = file.readlines()

        for i, line in enumerate(strings):
            if trigger in line:
                events.append([strings[i+1][18:-2], float(strings[i+2][15:-6])])

    return events
       

def file_finder(path, pattern):
    files_list = []  # To store the paths of .txt files

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(path):
        for filename in files:
            #if file.endswith('.txt') and not file.startswith('!'):
            if re.search(pattern, filename):
                files_list.append([root + '/', filename[:-4]])

    return files_list[0]


def file_lister(path, pattern):
    files = []

    if os.path.isdir(path):
        
        files.extend(file_finder(path, pattern))
        
        if files:
            print("Open path: ", path)
        else:
            print("No files found in the: ", path)

    else:
        print("Invalid directory path: ", path)
    
    return files


def main():

    metadatas = [file_lister(dir, r'^[^!].*\.txt$') for dir in DIRECTORIES]
    print(metadatas)
    for path, file in metadatas:
        metadata = metadata_parser(path, file)
        print(metadata)

        #if file_lister(file, r'^[^!].*\.txt$'):


    
        
        



if __name__ == "__main__":
    main()
