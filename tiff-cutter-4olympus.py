#!/usr/bin/env python3
import os


TIME_BEFORE = 10    # in sec.
TIME_AFTER  = 30    # in sec.

DIRECTORIES = [
    'F:\Lab Work Files\\2-photon',
]




def metadata_parser(file_path):

    starting_string = '""[Event 1]"	"""'

    with open(file_path, 'r') as file:

        line_number = 0
        for line in file:
            if starting_string in line:
                count += 1



def file_finder(directory):
    files = []  # To store the paths of .txt files

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt") and not file.startswith("!") :
                files.append(os.path.join(root, file[:-4]))

    return files


def file_lister(directories):
    files = []

    for directory in directories:

        if os.path.isdir(directory):
            
            files.extend(file_finder(directory))
            
            if files:
                print("Open path: ", directory)
            else:
                print("No .txt files found in the: ", directory)

        else:
            print("Invalid directory path: ", directory)
    
    return files


def main():

    files = file_lister(DIRECTORIES)

    for file in files:
        
        



if __name__ == "__main__":
    main()
