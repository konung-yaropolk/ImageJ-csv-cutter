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
       

def file_finder(path, pattern, nonrecursive=False):
    files_list = []  # To store the paths of .txt files

    # # Walk through the directory and its subdirectories
    for root, _, files in os.walk(path):
        for filename in files:
            if re.search(pattern, filename):
                files_list.append([root if root[-1] == '/' else root + '/', filename[:-4]])
        
        if nonrecursive:
            break

    return files_list


def file_lister(path, pattern, nonrecursive=False):
    files = []

    if os.path.isdir(path):        
        files.extend(
            file_finder(
                path,
                pattern,
                nonrecursive
            )
        )                
    else:
        print("!!!    Fail: invalid path        ", path)
    
    return files


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


def find_time_index(content, time):
    content = (float(i)-time for i in list(zip(*content))[0])
    diffs = [abs(i) for i in content]
    index = diffs.index(min(diffs))

    return index


def normalize(content, start, zero):
    content_normalized = []
    
    for column in content:
        baseline = column[start:zero]
        baseline_sum = sum((float(cell) for cell in baseline))
        mean = baseline_sum/len(baseline)
        
        column_normalized = [(float(cell)-mean)/mean for cell in column]    # dF/F0
        #column_normalized = [float(cell)/mean for cell in column]          # dF/F

        content_normalized.append(column_normalized)

    return content_normalized


def csv_cutter(content, eventname, time):
    timeline_zero = (float(i)-time for i in list(zip(*content))[0])

    start = find_time_index(content, time - s.TIME_BEFORE_TRIG)
    zero = find_time_index(content, time)
    end = find_time_index(content, time + s.TIME_AFTER_TRIG)
    
    content = list(zip(*content))[1:]
    content[:0] = [timeline_zero]

    if s.RELATIVE_VALUES: 
        content[1:] = normalize(content[1:], start, zero)        

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
    csv_list.extend(
        file_lister(
            path,
            r'^' + re.escape(file) + r'.*\.csv$',
            nonrecursive=True
        )
    )

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
