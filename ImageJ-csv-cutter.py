#!/usr/bin/env python3
import os
import re
import csv
import settings as s


def metadata_parser(path, file):    

    with open('{}{}.txt'.format(path, file), 'r') as file:        

        trigger = '"[Event '
        strings = file.readlines()

        string = strings[12]
        if not string.startswith('"T Dimension"'):
            raise ValueError

        n_slides = int(re.findall(r'\	"([^[]*), ', string)[0])
        t_duration = float(re.findall(r'- ([^[]*)\ \[', string)[0])
        t_resolution = t_duration/n_slides
       
        events = (
            (strings[i+1][18:-2], float(strings[i+2][15:-6])/1000) for i, line in enumerate(strings) if trigger in line
        )

    return events, t_resolution
       

def file_finder(path, pattern):
    files_list = []  # To store the paths of .txt files

    # # Walk through the directory and its subdirectories
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
    else:
        print("!!!    Fail: invalid path        ", path)
    
    return files


def zero_point_adjuster(content, time):
    content = (float(i)-time for i in list(zip(*content))[0])
    diffs = [abs(i) for i in content]
    t_zero_index = diffs.index(min(diffs))

    return t_zero_index


def csv_write(csv_output, path, file, event_name, i):

    os.makedirs(path + file + '_events/', exist_ok=True)
    with open('{}{}_events/{}_{}_[-{}s ; +{}s].csv'.format(
            path, 
            file, str(i+1), 
            event_name, 
            str(s.TIME_BEFORE_TRIG), 
            str(s.TIME_AFTER_TRIG)
        ), 'w') as f:                

        writer = csv.writer(f, delimiter=',', lineterminator='\r',)
        for row in csv_output:
            writer.writerow(row)        


def csv_cutter(content, eventname, time):
    timeline_zero = (float(i)-time for i in list(zip(*content))[0])

    start = zero_point_adjuster(content, time - s.TIME_BEFORE_TRIG)
    end = zero_point_adjuster(content, time + s.TIME_AFTER_TRIG)
    
    content = list(zip(*content))[1:]
    content[:0] = [timeline_zero]
    csv_output = list(zip(*content))[start:end]

    return csv_output


def csv_transform(content_raw, t_resolution):
    first_col = (str(i*t_resolution) for i in range(len(content_raw)))
    content = list(zip(*content_raw))[2::4]
    content[:0] = [first_col]
    content = list(zip(*content))[1:]

    return content


def csv_read(patch, file):

    with open(patch + file + '.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        content_raw = tuple(reader)

    return content_raw


def csv_process(path, file, metadata, t_resolution=1000):
    csv_list = []
    csv_list.extend(file_lister(path, r'.*' + re.escape(file) + r'.*\.csv$'))

    if csv_list:

        for csv_path, csv_file in csv_list:
            content_raw = csv_read(csv_path, csv_file)
            content = csv_transform(content_raw, t_resolution)     

            for i, event in enumerate(metadata):                
                csv_output = csv_cutter(content, *event)
                csv_write(csv_output, csv_path, csv_file ,event[0], i)

        result = '***    Done: csv files for        {}{}'.format(path, file)
    
    else:
        result = '!!!    Fail: no csv files for     {}{}'.format(path, file)
                
    csv_list = None
    return result


def main():

    queue = []

    # walk thrue directories to add files to the queue 
    for dir in s.DIRECTORIES:
        queue.extend(file_lister(dir, r'^[^!].*\.txt$'))

    # append metadata to the queue
    for i, item in enumerate(queue):
        try: metadata, t_resolution = metadata_parser(item[0], item[1])
        except ValueError as _: 
            print('!!!    Fail: wrong metadata for   {}{}'.format(item[0], item[1]))
            continue
        queue[i].append(metadata)
        queue[i].append(t_resolution)

    for item in queue:

        if len(item)==4:
            path, file, metadata, t_resolution = item
            result = csv_process(path, file, metadata, t_resolution)
            print(result)

        else:
            # print('!!!    Fail: no csv data to process {}{}'.format(item[0], item[1]))
            continue


if __name__ == "__main__":
    main()
