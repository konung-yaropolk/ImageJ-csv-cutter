#!/usr/bin/env python3
import os
import re


TIME_BEFORE_TRIG = 10    # in sec.
TIME_AFTER_TRIG  = 30    # in sec.

DIRECTORIES = [
    # 'C:/Users/yarop/Coding/ImageJ-csv-cutter/',
     'F:/Lab Work Files/scripts/ImageJ-csv-cutter/',
    # 'F:/Lab Work Files/2-photon/Pirt GCamp3 x Thy1 RGeco + DRS + Bicuculine/2022_12_09/',
    # 'F:/Lab Work Files/2-photon',
    
]


def parse(path, file):    
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
                files_list.append([root if root[-1] == '/' else root + '/', filename[:-4]])

    return files_list


def file_lister(path, pattern):
    files = []

    if os.path.isdir(path):        
        files.extend(file_finder(path, pattern))        
        # if not files:
        #     print("No files found in the: ", path)

    else:
        print("Invalid directory path: ", path)
    
    return files

#def csv_transforming(patch, file, metadata):


def process_csv(path, file, metadata):

    csv_list = []
    csv_list.extend(file_lister(path, r'^' + file + r'.*\.csv$'))

    if csv_list != []:
        for patch, file in csv_list:
            #csv_transforming(patch, file, metadata)
            print(patch+file)

    #print('\n',csv_list, '\n')    
    csv_list = None


def main():

    queue = []

    # walk thrue directories to add files to the queue 
    for dir in DIRECTORIES:
        queue.extend(file_lister(dir, r'^[^!].*\.txt$'))

    # append metadata to the queue
    for i, elem in enumerate(queue):
        metadata = parse(elem[0], elem[1])
        queue[i].append(metadata)

    print(queue)

    for path, file, metadata in queue:
        process_csv(path, file, metadata)

        



if __name__ == "__main__":
    main()
