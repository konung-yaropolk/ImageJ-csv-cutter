#!/usr/bin/env python3
import os
import re


TIME_BEFORE_TRIG = 10    # in sec.
TIME_AFTER_TRIG  = 30    # in sec.

DIRECTORIES = [
    'C:/Users/yarop/Coding/ImageJ-cvs-cutter/'
    # 'F:/Lab Work Files/scripts/ImageJ-cvs-cutter',
    # 'F:/Lab Work Files/2-photon',
    
]


def metadata_parser(file_path):    
    events = []

    with open(file_path + '.txt', 'r') as file:

        trigger = '"[Event '
        strings = file.readlines()

        for i, line in enumerate(strings):
            if trigger in line:
                events.append([strings[i+1][18:-2], float(strings[i+2][15:-6])])

    return events
       

def file_finder(directory, pattern):
    files_list = []  # To store the paths of .txt files

    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for name in files:
            #if file.endswith('.txt') and not file.startswith('!'):
            if re.search(pattern, name):
                files_list.append(os.path.join(root, name[:-4]))

    return files_list


def file_lister(directory, pattern):
    files = []

    if os.path.isdir(directory):
        
        files.extend(file_finder(directory, pattern))
        
        if files:
            print("Open path: ", directory)
        else:
            print("No files found in the: ", directory)

    else:
        print("Invalid directory path: ", directory)
    
    return files


def main():

    metadatas = [file_lister(directory, r'^[^!].*\.txt$') for directory in DIRECTORIES][0]

    for file in metadatas:
        metadata = metadata_parser(file)
        print(metadata)

        #if file_lister(file, r'^[^!].*\.txt$'):


    
        
        



if __name__ == "__main__":
    main()
