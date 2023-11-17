#!/usr/bin/env python3
import os
import re
import csv
import settings as s


class Queue:
    
    def __init__(self, dirs):

        self.out = []

        # walk thrue directories to add files to the queue 
        for dir in dirs:
            self.out.extend(self.file_lister(dir, r'^[^!].*\.txt$'))
        
        return self.out



    def metadata_parser(self, path, file):    

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
       

    def file_finder(self, path, pattern, nonrecursive=False):
        files_list = []  # To store the paths of .txt files

        # # Walk through the directory and its subdirectories
        for root, _, files in os.walk(path):
            for filename in files:
                if re.search(pattern, filename):
                    files_list.append([root if root[-1] == '/' else root + '/', filename[:-4]])
            
            if nonrecursive:
                break

        return files_list


    def file_lister(self, path, pattern, nonrecursive=False):
        files = []

        if os.path.isdir(path):        
            files.extend(
                self.file_finder(
                    path,
                    pattern,
                    nonrecursive
                )
            )                
        else:
            print("!!!    Fail: invalid path        ", path)
        
        return files


class CSV:

    def csv_write(self, csv_output, path, file, event_name, i):

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


    def find_time_index(self, content, time):
        content = (float(i)-time for i in list(zip(*content))[0])
        diffs = [abs(i) for i in content]
        index = diffs.index(min(diffs))

        return index


    def normalize(self, content, start, zero):
        content_normalized = []
        
        for column in content:
            baseline = column[start:zero]
            baseline_sum = sum((float(cell) for cell in baseline))
            baseline_len = len(baseline)
            mean = baseline_sum/baseline_len if baseline_len else 1
            
            column_normalized = [(float(cell)-mean)/mean for cell in column]    # dF/F0
            #column_normalized = [float(cell)/mean for cell in column]          # dF/F

            content_normalized.append(column_normalized)

        return content_normalized


    def csv_cutter(self, content, eventname, time):
        timeline_zero = (float(i)-time for i in list(zip(*content))[0])

        start = self.find_time_index(content, time - s.TIME_BEFORE_TRIG)
        zero = self.find_time_index(content, time)
        end = self.find_time_index(content, time + s.TIME_AFTER_TRIG)
        
        content = list(zip(*content))[1:]
        content[:0] = [timeline_zero]

        if s.RELATIVE_VALUES: 
            content[1:] = self.normalize(content[1:], start, zero)        

        csv_output = list(zip(*content))[start:end]

        return csv_output


    def csv_transform(self, content_raw, t_resolution):
        first_col = (str(i*t_resolution) for i in range(len(content_raw)))
        content = list(zip(*content_raw))[2::4]
        content[:0] = [first_col]
        content = list(zip(*content))[1:]

        return content


    def csv_read(self, patch, file):

        with open(patch + file + '.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            content_raw = tuple(reader)

        return content_raw


    def csv_process(self, path, file, metadata, t_resolution=1000):
        csv_list = []
        csv_list.extend(
            Queue.file_lister(
                path,
                r'^' + re.escape(file) + r'.*\.csv$',
                nonrecursive=True
            )
        )

        if csv_list:

            for csv_path, csv_file in csv_list:
                content_raw = self.csv_read(csv_path, csv_file)
                content = self.csv_transform(content_raw, t_resolution)     

                for i, event in enumerate(metadata):                
                    csv_output = self.csv_cutter(content, *event)
                    self.csv_write(csv_output, csv_path, csv_file ,event[0], i)

            result = '***    Done: csv files for        {}{}'.format(path, file)
        
        else:
            result = '!!!    Fail: no csv files for     {}{}'.format(path, file)
                    
        csv_list = None
        return result

