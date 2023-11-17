#!/usr/bin/env python3
import settings as s
import classes

def main():

    queue = classes.Queue(s.DIRECTORIES)


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
