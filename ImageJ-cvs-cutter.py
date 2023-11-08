#!/usr/bin/env python3
import os


TIME_BEFORE_TRIG = 10    # in sec.
TIME_AFTER_TRIG  = 30    # in sec.

DIRECTORIES = [
    'C:/Users/yarop/Coding/ImageJ-cvs-cutter/'
    # 'F:/Lab Work Files/scripts/ImageJ-cvs-cutter',
    # 'F:/Lab Work Files/2-photon',
    
]


#def is_csv_files_exist():



def metadata_parser(file_path):    
    events = []

    with open(file_path + '.txt', 'r') as file:

        trigger = '"[Event '
        strings = file.readlines()

        for i, line in enumerate(strings):
            if trigger in line:
                events.append([strings[i+1][18:-2], float(strings[i+2][15:-6])])

    return events
       

def file_finder(directory):
    files_list = []  # To store the paths of .txt files

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt') and not file.startswith('!'):
                files_list.append(os.path.join(root, file[:-4]))

    return files_list


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

    metadatas = file_lister(DIRECTORIES)

    for file in metadatas:
        print(metadata_parser(file))
      #  if is_csv_files_exist(file):

    
        
        



if __name__ == "__main__":
    main()
